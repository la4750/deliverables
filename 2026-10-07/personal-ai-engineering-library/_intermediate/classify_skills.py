#!/usr/bin/env python3
# Skill Inventory 分析流水线：修正 loaded → 逻辑技能归并 → 10 类分类 → 质量检查
import json, re, collections, os, datetime

SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
items = json.load(open(SCRATCH + "/skill_inventory_raw.json"))

LOADED = {"codebase-mapping","hermes-agent","insight-registry","legacy-system-migration","studio-roles",
"architecture-diagram","humanizer","novel-writing","cn-market-data-failover",
"weixinpay:weixinpay-feedback","weixinpay:weixinpay-pay","weixinpay:weixinpay-register",
"maps","powerpoint","arxiv","ai-engineering-library","game-dev-lessons","game-studio","godot-kb",
"hermes-agent-skill-authoring","node-inspect-debugger","python-debugpy","requesting-code-review",
"rules-knowledge-base","spike","systematic-debugging","test-driven-development"}

TIER_ORDER = {"A_user_hermes":0, "D_legacy_openclaw":1, "C_plugin":2, "E_other":3, "B_bundled_hermes_agent":4}

for it in items:
    it["loaded_in_hermes"] = (it["tier"] in ("A_user_hermes","C_plugin")) and \
        (it["name"] in LOADED or os.path.basename(it["dir"]) in LOADED)

# ---------- 1. 逻辑技能归并（sha256 完全相同 = 同一技能的副本） ----------
clusters = collections.defaultdict(list)
for it in items:
    clusters[it["sha256"]].append(it)

logical = []
for h, group in clusters.items():
    group.sort(key=lambda x: TIER_ORDER[x["tier"]])
    canon = group[0]
    copies = [g["path"] for g in group[1:]]
    rec = dict(canon)
    rec["copy_paths"] = copies
    rec["copy_count"] = len(group)
    rec["loaded_in_hermes"] = any(g["loaded_in_hermes"] for g in group)
    rec["all_tiers"] = sorted({g["tier"] for g in group})
    logical.append(rec)
logical.sort(key=lambda x: (x["tier"], x["path"]))

# 同名不同内容（版本变体）标注
byname = collections.defaultdict(list)
for rec in logical:
    byname[rec["name"].lower()].append(rec)
for nm, grp in byname.items():
    if len(grp) > 1:
        for rec in grp:
            rec["name_variants"] = [g["path"] for g in grp if g is not rec]

# ---------- 2. 读取正文头部做分类与质检 ----------
def read_body(p):
    fp = os.path.expanduser(p)
    try:
        return open(fp, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""

for rec in logical:
    rec["body"] = read_body(rec["path"])

# ---------- 3. 10 类分类规则 ----------
CAT = {}
def C(pred, cat): CAT.setdefault(cat, []).append(pred)

workflow_markers = r"(##\s*(何时使用|使用时机|流程|步骤|工作流|Workflow|When to use|Process|Playbook|阶段)|\bstep[- ]by[- ]step\b|阶段\s*\d|第[一二三四五六七八九十]+步)"

RULES = [
 ("META_SKILL", r"(skill[-_ ]?(author|creat|review|optim|audit|write)|self[-_]improv|find[-_]skill|skillhub|技能(的)?(创建|审查|优化|元)|legacy[-_]system[-_]migration|meta[-_]skill)"),
 ("PROJECT_SPECIFIC", r"(深空殖民|deep[-_ ]?space|colony|项目专属|本项目|this project only|specific to (the )?project)"),
 ("AGENT_WORKFLOW", r"(multi[-_ ]?agent|多智能体|多\s*Agent|agent\s*(collabor|orchestr|team|swarm|dispatch|selection|协作|编排|协同)|delegate_task|子代理|角色卡|studio[-_ ]?roles?|novel[-_ ]?dispatch|orchestrat)"),
 ("TOOL_WRAPPER", r"(mcp\b|gh\s+cli|命令行调用|cli tool|调用(一个|某)?(脚本|工具|命令)|uses the `|scraping|web\s*search api|tavily|obsidian|notion api|tencent[-_]?(docs|cos|meeting)|weixinpay|browser\s*automation|selenium|playwright|curl\b)"),
 ("CAPABILITY_WRAPPER", r"^\s*(image[-_ ]?resize|pdf[-_ ]?(convert|merge)|code[-_ ]?(format|lint)|docx|xlsx|pptx|powerpoint|gif[-_ ]?search|maps?|arxiv|transcode|thumbnail|convert\b|resize\b|format\b|compress\b|extract[-_ ]?text|manim)"),
 ("KNOWLEDGE_WRAPPER", r"(knowledge[-_ ]?(base|base)?|知识库|参考手册|cheat[-_ ]?sheet|glossary|api[-_ ]?(reference|docs)|编码规范|coding[-_ ]?(standard|guide)|godot[-_ ]?kb|最佳实践(汇)?(编|总)|handbook|\bkb\b)"),
 ("OBSOLETE", r"(已废弃|不再维护|deprecated\s*skill|obsolete|openclaw\s*(cli|runtime)\s*要求|仅限\s*openclaw)"),
 ("WORKFLOW_SKILL", workflow_markers),
]

def classify(rec):
    if rec["copy_paths"]:
        pass  # 副本关系单独记录，分类看本体
    text = (rec["name"] + " " + rec["description"] + " " + rec["path"]).lower()
    body_head = rec["body"][:8000]
    for cat, pat in RULES:
        if re.search(pat, text, re.I) or re.search(pat, body_head, re.I):
            return cat
    # 正文启发：多步流程
    if len(re.findall(r"^\s*(\d+\.|[-*]\s*\[ \])", rec["body"], re.M)) >= 5 and re.search(workflow_markers, rec["body"], re.I):
        return "WORKFLOW_SKILL"
    return "UNKNOWN"

for rec in logical:
    rec["category"] = classify(rec)
    # 副本：非规范路径上的副本标 DUPLICATE_OR_OVERLAP
    if rec["copy_paths"]:
        rec["dup_copies"] = rec["copy_paths"]

# ---------- 4. 质量检查 ----------
def qchecks(rec):
    body = rec["body"]; q = {}
    q["has_description"] = bool(rec["description"])
    q["description_triggers"] = bool(re.search(r"(何时使用|when to use|use when|trigger|适用|用于|需要.*时)", rec["description"] + body[:1500], re.I))
    q["oversized"] = rec["body_bytes"] > 40000
    # 知识混入：代码围栏/API 表格多而流程少
    code_blocks = len(re.findall(r"```", body)) // 2
    q["knowledge_heavy"] = code_blocks >= 6 and not re.search(workflow_markers, body, re.I)
    q["broken_refs"] = []
    for m in set(re.findall(r"(?:~|\./|\.\./)[A-Za-z0-9_\-./一-鿿]+", body)):
        if m.startswith("~/") or m.startswith("./") or m.startswith("../"):
            base = rec["dir"]
            p2 = os.path.expanduser(m.replace("./", base + "/", 1)) if m.startswith("./") else (os.path.expanduser(m) if m.startswith("~/") else os.path.normpath(os.path.join(base, m)))
            if not os.path.exists(p2) and len(m) > 4:
                q["broken_refs"].append(m)
    q["broken_refs"] = q["broken_refs"][:5]
    q["scripts_present"] = bool(rec["scripts"])
    q["references_present"] = bool(rec["subdirs"]) or bool([f for f in rec["other_files"] if f.endswith(".md")])
    q["has_inputs"] = bool(re.search(r"(^##?\s*(输入|Inputs?|Prerequisites?)\b|inputs?:)", body, re.I | re.M))
    q["has_outputs"] = bool(re.search(r"(^##?\s*(输出|Outputs?|Result|Deliverable)\b|outputs?:)", body, re.I | re.M))
    q["has_completion"] = bool(re.search(r"(完成条件|验收|done when|success criteria|definition of done|完成标志)", body, re.I))
    q["has_validation"] = bool(re.search(r"(验证|validate|validation|测试|test it|check that|确认.*生效)", body, re.I))
    q["runtime_binding"] = sorted(set(re.findall(r"(openclaw|hermes|claude\s*code|cursor|windsurf|copilot)", body[:6000], re.I)))
    q["llm_binding"] = sorted(set(re.findall(r"(gpt-4|claude-[0-9a-z.]+|deepseek-[a-z0-9.]+|llama-[0-9]+|mimo-[a-z0-9.]+)", body, re.I)))
    q["deprecated_tool"] = sorted(set(re.findall(r"(bing\s*search|google\s*custom\s*search|gpt-3\.5|openclaw\s*cli\b)", body, re.I)))
    return q

for rec in logical:
    rec["quality"] = qchecks(rec)
    rec.pop("body", None)

json.dump(logical, open(SCRATCH + "/skill_logical_classified.json", "w"), ensure_ascii=False, indent=1)

# ---------- 5. 统计 ----------
print("文件总数:", len(items))
print("逻辑技能数(按内容去重):", len(logical))
print("副本文件数(冗余):", sum(r["copy_count"] - 1 for r in logical))
print("已加载(A/C且在skills_list):", sum(1 for r in logical if r["loaded_in_hermes"]))
print()
print("== 分类分布 ==")
for k, v in collections.Counter(r["category"] for r in logical).most_common():
    print(f"  {k}: {v}")
print()
print("== UNKNOWN 明细(待人工复核) ==")
for r in logical:
    if r["category"] == "UNKNOWN":
        print(f"  [{r['tier'][:1]}] {r['name']} :: {r['description'][:90]} :: {r['path']}")
