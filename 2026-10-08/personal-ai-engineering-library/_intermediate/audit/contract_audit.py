#!/usr/bin/env python3
# Skill Registry Quality & Contract Completeness Audit — STRICTLY READ-ONLY 对既有技能/文件；
# 仅新增两份审计产出（SKILL_CONTRACT_AUDIT.yaml / SKILL_CONTRACT_AUDIT_REPORT.md）
import json, re, os, collections, yaml, datetime

SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library/14_AI_AGENTS/Skills"
TODAY = "2026-10-07"

# ---------- 0. 载入 8 份输入 ----------
reg = yaml.safe_load(open(f"{LIB}/Registry/SKILL_REGISTRY.yaml"))
cls = yaml.safe_load(open(f"{LIB}/SKILL_CLASSIFICATION.yaml"))
prp = yaml.safe_load(open(f"{LIB}/SKILL_MIGRATION_PROPOSALS.yaml"))
inv = yaml.safe_load(open(f"{LIB}/SKILL_INVENTORY.yaml"))
rules_txt = open(f"{LIB}/Registry/../SKILL_RULES.md").read()
idx_lines = [l for l in open(f"{LIB}/SKILL_INDEX.md") if l.startswith("| `SKILL-")]
overlap_txt = open(f"{LIB}/SKILL_OVERLAP_REPORT.md").read()
optim_txt = open(f"{LIB}/SKILL_OPTIMIZATION_REPORT.md").read()

skills = reg["skills"]
cls_by = {s["skill_id"]: s for s in cls["skills"]}
prp_by = {e["skill_id"]: e for e in prp["proposals"]["entries"]}

# ---------- 1. 跨文件完整性（integrity） ----------
integ = {}
integ["registry_count"] = len(skills)
integ["classification_count"] = len(cls["skills"])
integ["proposals_count"] = len(prp["proposals"]["entries"])
integ["index_rows"] = len(idx_lines)
integ["inventory_files"] = len(inv["entries"])
ids_reg = {s["skill_id"] for s in skills}
integ["id_set_equal_cls"] = ids_reg == {s["skill_id"] for s in cls["skills"]}
integ["id_set_equal_prp"] = ids_reg == {e["skill_id"] for e in prp["proposals"]["entries"]}
integ["index_ids_match"] = {l.split("`")[1] for l in idx_lines} == ids_reg
integ["duplicate_ids"] = len(skills) - len(ids_reg)

# ---------- 2. 实际文件核对（canonical_path / name / description） ----------
def readf(p):
    try:
        return open(os.path.expanduser(p), encoding="utf-8", errors="replace").read()
    except Exception:
        return None

def frontmatter(txt):
    m = re.match(r"^---\s*\n(.*?)\n---", txt or "", re.S)
    meta = {}
    if m:
        for line in m.group(1).split("\n"):
            mm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
            if mm: meta[mm.group(1).lower()] = mm.group(2).strip().strip('"\'')
    return meta

wf_pat = r"(##\s*(何时使用|使用时机|流程|步骤|工作流|Workflow|When to use|Process|Playbook|阶段)|step[- ]by[- ]?step|第[一二三四五六七八九十]+步|阶段\s*\d)"
step_pat = r"^\s*(\d+\.|[-*] \[ \]|###? Step)"

results = []
for s in skills:
    sid = s["skill_id"]
    c = cls_by[sid]
    body = readf(s["canonical_path"]) or ""
    meta = frontmatter(body)
    q_missing = []

    # ----- L1: Registry / Discovery -----
    l1_fields = {
        "skill_id": bool(s.get("skill_id")),
        "name": bool(s.get("name")),
        "description": bool(s.get("description")),          # null = 缺
        "category": bool(s.get("category")),
        "domain": bool(s.get("domain")),
        "source": bool(s.get("source")),
        "canonical_path": bool(s.get("canonical_path")) and os.path.exists(os.path.expanduser(s.get("canonical_path") or "")),
        "status": bool(s.get("status")),
        "version": ("version" in s),                        # 值可为 unknown（如实）
    }
    l1_missing = [k for k, v in l1_fields.items() if not v]
    l1_ok = not l1_missing
    version_unknown = s.get("version") in (None, "unknown")
    name_mismatch = bool(meta.get("name")) and meta.get("name") != s["name"]
    desc_mismatch = bool(meta.get("description")) and bool(s["description"]) and \
        not (meta["description"].startswith(s["description"][:80]) or s["description"].startswith(meta["description"][:80]))

    # ----- L2: Operational / Discoverability -----
    # 信号来自实际 SKILL.md 正文 + registry 登记值
    trigger = bool(re.search(r"(何时使用|使用时机|when to use|use when|when the user|触发|适用场景|Use when|Load when)", body[:3000], re.I))
    inputs = bool(re.search(r"(^##?\s*(输入|Inputs?|Prerequisites?|前置)\b|^Inputs?:)", body, re.I | re.M))
    outputs = bool(re.search(r"(^##?\s*(输出|Outputs?|Result|Deliverable|产出)\b|^Outputs?:)", body, re.I | re.M))
    cat = s["category"]
    dep_free = cat in ("TOOL_WRAPPER", "KNOWLEDGE_WRAPPER")   # 这两类 required_* 允许 N/A
    reg_declared = lambda f: s.get(f) not in (None, "not_assessed", "not_recorded", "unknown", "")
    rk_ok = dep_free or reg_declared("required_knowledge")
    rc_ok = dep_free or reg_declared("required_capabilities")
    ca_ok = reg_declared("compatible_agents")
    deps_ok = dep_free or reg_declared("dependencies")
    constraints = bool(re.search(r"(约束|Constraints?|禁止|必须(?!是)|hard:|soft:)", body[:5000], re.I))
    l2_missing = []
    if not trigger: l2_missing.append("trigger/applicability")
    if not inputs:  l2_missing.append("inputs")
    if not outputs: l2_missing.append("outputs")
    if not rk_ok:   l2_missing.append("required_knowledge")
    if not rc_ok:   l2_missing.append("required_capabilities")
    if not ca_ok:   l2_missing.append("compatible_agents")
    if not deps_ok: l2_missing.append("dependencies")
    if not constraints: l2_missing.append("constraints")
    l2_ok = l1_ok and not l2_missing

    # ----- L3: Engineering / Execution（仅判定，不强制升级） -----
    workflow_ok = bool(re.search(wf_pat, body, re.I)) and len(re.findall(step_pat, body, re.M)) >= 3
    validation_ok = bool(re.search(r"(验证|validate|validation|验收|测试|check that|确认.*生效|Definition of Done)", body, re.I))
    failure_ok = bool(re.search(r"(失败|错误处理|on error|fallback|retry|重试|escalate|回滚|rollback|失败处理)", body, re.I))
    risk_ok = bool(re.search(r"(risk_level|风险等级|risk level|high[- ]risk|critical|requires_human_approval)", body, re.I))
    vscope_ok = bool(re.search(r"(version_scope|适用版本|兼容.{0,6}版本|Godot \d|Python \d|requires .{0,10}\d+\.\d+)", body, re.I))
    limits_ok = bool(re.search(r"(known_limitations|已知(问题|限制|缺陷)|Limitations?|不适用|不支持)", body, re.I))
    examples_ok = bool(re.search(r"(示例|Examples?|例：|e\.g\.|for example)", body, re.I))
    runtime_ok = bool(re.search(r"(compatible_runtime|agent_runtime|requires.{0,20}(CLI|API|MCP)|运行时要求)", body, re.I))
    hard3 = [workflow_ok, validation_ok, failure_ok]
    soft = {"risk_level": risk_ok, "version_scope": vscope_ok, "known_limitations": limits_ok,
            "examples": examples_ok, "runtime/interface": runtime_ok}
    l3_missing = [k for k, v in [("workflow", workflow_ok), ("validation_requirements", validation_ok),
                                 ("failure_handling", failure_ok)] + list(soft.items()) if not v]
    l3_ok = all(hard3)

    # ----- contract level required（本阶段判定规则，见报告 §2） -----
    if c["tier"] == "B3_third_party_dep" or c.get("nested_in"):
        required = "L1"           # 父技能承担路由；第三方依赖不治理
        req_reason = "嵌套子技能由父包路由" if c.get("nested_in") else "第三方依赖，排除治理范围"
    elif cat in ("WORKFLOW_SKILL", "AGENT_WORKFLOW") and len(body) >= 2500:
        required = "L3"; req_reason = "复杂工程工作流（非嵌套、正文≥2.5KB）"
    else:
        required = "L2"; req_reason = "需任务匹配的独立技能（工具/知识/元/小型流程）" \
            if cat != "PROJECT_SPECIFIC" else "项目专属技能，需触发匹配"
        if not l1_ok: req_reason += "；L1 未达标需先补齐"

    current = "L3" if (l1_ok and l2_ok and l3_ok) else ("L2" if l2_ok else ("L1" if l1_ok else "L0"))
    rank = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}
    gap = rank[current] < rank[required]

    # reason（人读，含缺什么）
    if gap:
        miss = []
        if current in ("L0",): miss.append(f"L1缺:{','.join(l1_missing)}")
        if required == "L3" and current in ("L1", "L2"):
            if not l2_ok: miss.append(f"L2缺:{','.join(l2_missing[:4])}")
            if current == "L2": miss.append(f"L3缺:{','.join(l3_missing)}")
        reason = f"需{required}/现{current}——" + ("；".join(miss) if miss else "等级不足")
    else:
        reason = f"需{required}/现{current}——达标" + \
            (f"（L3 全字段仍有缺：{','.join(l3_missing[:3])}，不构成本级缺口）" if required != "L3" and l3_missing else "")

    results.append({
        "skill_id": sid, "name": s["name"], "category": cat, "domain": s["domain"],
        "contract_level_required": required, "contract_level_current": current,
        "contract_gap": gap, "reason": reason,
        "l1_missing": l1_missing or None, "l2_missing": l2_missing or None,
        "l3_missing": l3_missing or None,
        "file_checks": {"canonical_exists": l1_fields["canonical_path"],
                        "name_mismatch": name_mismatch or None,
                        "description_mismatch": desc_mismatch or None,
                        "version_unknown": version_unknown or None},
        "requirement_reason": req_reason})

# ---------- 3. 汇总 ----------
S = collections.Counter
sumry = {
    "total": len(results),
    "required": dict(S(r["contract_level_required"] for r in results)),
    "current": dict(S(r["contract_level_current"] for r in results)),
    "gap": dict(S(r["contract_gap"] for r in results)),
    "gap_by_required": {lv: S(r["contract_gap"] for r in results if r["contract_level_required"] == lv)
                        for lv in ("L1", "L2", "L3")},
    "gap_by_category": {k: {"n": v, "gap": sum(1 for r in results if r["category"] == k and r["contract_gap"])}
                        for k, v in S(r["category"] for r in results).items()},
    "l1_failures": [r["skill_id"] for r in results if r["l1_missing"]],
    "name_mismatch": [r["skill_id"] for r in results if r["file_checks"]["name_mismatch"]],
    "desc_mismatch": [r["skill_id"] for r in results if r["file_checks"]["description_mismatch"]],
    "missing_canonical": [r["skill_id"] for r in results if not r["file_checks"]["canonical_exists"]],
    "version_unknown_n": sum(1 for r in results if r["file_checks"]["version_unknown"]),
}
miss_counter = S()
for r in results:
    for f in (r["l2_missing"] or []) + (r["l3_missing"] or []) + (r["l1_missing"] or []):
        miss_counter[f] += 1
sumry["top_missing_fields"] = miss_counter.most_common()

def plain(o):
    if isinstance(o, dict): return {str(k): plain(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [plain(v) for v in o]
    if isinstance(o, (str, int, float, bool)) or o is None: return o
    return str(o)
sumry = plain(sumry)
out = {"contract_audit": {
    "stage": "Skill Registry Quality & Contract Completeness Audit（READ-ONLY，2026-10-07）",
    "inputs": ["SKILL_INVENTORY.yaml", "SKILL_CLASSIFICATION.yaml", "Registry/SKILL_REGISTRY.yaml",
               "SKILL_INDEX.md", "Registry/SKILL_RULES.md", "SKILL_OVERLAP_REPORT.md",
               "SKILL_OPTIMIZATION_REPORT.md", "SKILL_MIGRATION_PROPOSALS.yaml", "实际 SKILL.md 文件"],
    "coverage": f"{len(results)}/{len(skills)} 逻辑技能全量，无抽样",
    "level_rules": {
        "L1_required": "全部技能",
        "L2_required": "非嵌套、非第三方依赖、需任务匹配的独立技能",
        "L3_required": "非嵌套 WORKFLOW/AGENT_WORKFLOW 且正文≥2.5KB（复杂工程工作流）",
        "N/A_policy": "TOOL_WRAPPER/KNOWLEDGE_WRAPPER 的 required_knowledge/capabilities 允许 N/A；不为完整度虚构"},
    "summary": sumry, "integrity": integ},
    "skills": results}
yaml.dump(out, open(f"{LIB}/SKILL_CONTRACT_AUDIT.yaml", "w", encoding="utf-8"),
          allow_unicode=True, sort_keys=False, width=140)
json.dump(sumry, open(SCRATCH + "/contract_summary.json", "w"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in sumry.items() if k not in ("top_missing_fields",)}, ensure_ascii=False, indent=1, default=str))
print("top_missing:", sumry["top_missing_fields"][:15])
print("integrity:", json.dumps(integ, ensure_ascii=False))
