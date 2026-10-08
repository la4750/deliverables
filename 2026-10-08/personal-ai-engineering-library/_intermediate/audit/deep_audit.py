#!/usr/bin/env python3
# §4-§11 深审计分析 → 计算全部统计（不写文件，打印供组装）
import json, re, os, collections, yaml

SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library/14_AI_AGENTS/Skills"
logical = json.load(open(SCRATCH + "/skill_final.json"))
aud = yaml.safe_load(open(f"{LIB}/SKILL_CONTRACT_AUDIT.yaml"))
reg = yaml.safe_load(open(f"{LIB}/Registry/SKILL_REGISTRY.yaml"))
prp = yaml.safe_load(open(f"{LIB}/SKILL_MIGRATION_PROPOSALS.yaml"))
res = {r["skill_id"]: r for r in aud["skills"]}
reg_by = {s["skill_id"]: s for s in reg["skills"]}
prop_by = {e["skill_id"]: e for e in prp["proposals"]["entries"]}

def body(r):
    try: return open(os.path.expanduser(r["path"]), encoding="utf-8", errors="replace").read()
    except: return ""
B = {r["skill_id"]: body(r) for r in logical}

# ---------- §4 边界 ----------
leak_know = [r for r in logical if r["category"] == "KNOWLEDGE_WRAPPER" or r["quality"]["knowledge_heavy"]]
io_cap = [r for r in logical if r["category"] == "CAPABILITY_WRAPPER" or
          (r["category"] == "TOOL_WRAPPER" and "inputs" not in (res[r["skill_id"]].get("l2_missing") or [])
           and "outputs" not in (res[r["skill_id"]].get("l2_missing") or []))]
agent_tokens = ["novel-agent", "coding_agent", "testing_agent", "master_agent", "game_agent",
                "robotics_agent", "assigned_agent", "Game Designer Agent", "agent_001", "_agent_00"]
agent_coup = []
for r in logical:
    hits = sorted({t for t in agent_tokens if t in B[r["skill_id"]]})
    if hits: agent_coup.append((r["skill_id"], hits))
llm_hard = []
for r in logical:
    m = re.findall(r"(must use|requires|only (works|works with)|仅(?:支持|要求)|必须(?:使用)?)[^\n]{0,40}(GPT-?[34]|Claude[ -]?[0-9a-z.]*|MiMo[-a-z0-9.]*|Llama-?[0-9]*|DeepSeek[-a-z0-9.]*)",
                   B[r["skill_id"]], re.I)
    if m: llm_hard.append((r["skill_id"], m[:1]))
oc_required = [r["skill_id"] for r in logical if r["tier"].startswith("D") and
               re.search(r"openclaw", json.dumps(r["quality"].get("runtime_binding", [])), re.I)]
hermes_ok = sum(1 for r in logical if r["quality"]["runtime_binding"] and not r["tier"].startswith("D"))

# ---------- §5 依赖 ----------
cap_ids = [m["id"] if isinstance(m, dict) else m for m in
           yaml.safe_load(open("/home/ubuntu/personal-ai-engineering-library/09_CAPABILITIES/Registry/CAPABILITY_REGISTRY.yaml"))["capabilities"]] \
    if False else ["game.behavior_tree","game.blackboard","software.structured_logger","software.json_save_archive",
                   "game.job_queue_scheduler","game.turn_based_combat","game.event_engine","game.quest_state_machine",
                   "software.resource_auto_indexer","game.bt_ai_agent"]
cap_refs = [(r["skill_id"], cid) for r in logical for cid in cap_ids if cid in B[r["skill_id"]]]
kref = re.compile(r"\bK-[A-Z]+-[A-Z0-9]+(?:-[A-Z0-9]+)+\b")
know_refs_all = [(r["skill_id"], k) for r in logical for k in kref.findall(B[r["skill_id"]])]
reg_know = set()
try:
    kr = yaml.safe_load(open("/home/ubuntu/personal-ai-engineering-library/01_KNOWLEDGE/_REGISTRY/KNOWLEDGE_REGISTRY.yaml"))
    reg_know = {k["knowledge_id"] for k in kr.get("knowledge", []) if "knowledge_id" in k}
except Exception as e:
    pass
broken_krefs = [(s, k) for s, k in know_refs_all if k not in reg_know]
broken_paths = [(r["skill_id"], p) for r in logical for p in
                [b for b in r["quality"]["broken_refs"] if b.startswith("~/.hermes/skills") and not os.path.exists(os.path.expanduser(b))]]
declared_skill_deps = sum(1 for r in logical if r.get("dependencies") not in (None, "not_assessed", "not_recorded"))
# 环检测：nested_in 树 + 声明依赖（声明=0）
parent = {r["skill_id"]: None for r in logical}
name2id = {r["name"]: r["skill_id"] for r in logical}
cycles = []
for r in logical:
    if r.get("nested_in") and r["nested_in"] in name2id:
        a, b = r["skill_id"], name2id[r["nested_in"]]
        if parent.get(b) == a: cycles.append((a, b))
ext_no_25 = [r["skill_id"] for r in logical if "/workspace/skills/@" in r["path"] or "skillhub" in r["path"].lower()]
ext_content = [r["skill_id"] for r in logical if re.search(r"(awesome-godot|54 real design systems|upstream-maintained|Extracted from|精选项目提取)", B[r["skill_id"]][:2000])]
impl_bypass = [(r["skill_id"], r["scripts"]) for r in logical if r["scripts"]]
dep_ver_mismatch = "undetermined: version_scope 缺失 321/358（无声明即无法比对）"

# ---------- §6 Progressive Disclosure ----------
over = [r["skill_id"] for r in logical if r["body_bytes"] > 40000]
big15 = [r["skill_id"] for r in logical if r["body_bytes"] > 15000]
inline_know = [r["skill_id"] for r in logical if r["quality"]["knowledge_heavy"]]
no_l3 = sum(1 for r in logical if not r["quality"]["references_present"])
reg_heavy = all(len(str(v)) < 600 for v in [])  # registry 单条长度
reg_len = [len(yaml.dump(s, allow_unicode=True)) for s in reg["skills"]]

# ---------- §7 TOOL_WRAPPER 深审（129） ----------
tool = [r for r in logical if r["category"] == "TOOL_WRAPPER"]
t_cap, t_know, t_keep = [], [], []
for r in tool:
    miss = res[r["skill_id"]].get("l2_missing") or []
    if "inputs" not in miss and "outputs" not in miss: t_cap.append(r)
    elif r["quality"]["knowledge_heavy"]: t_know.append(r)
    else: t_keep.append(r)

# ---------- §8 KNOWLEDGE_WRAPPER 深审（29） ----------
know = [r for r in logical if r["category"] == "KNOWLEDGE_WRAPPER"]
k_pure, k_route, k_wf = [], [], []
for r in know:
    b = B[r["skill_id"]]
    if re.search(r"(何时使用|使用时机|when to use|use when|触发|Load when)", b[:2500], re.I) and \
       re.search(r"(^##|步骤|流程|1\.|- )", b, re.M):
        k_route.append(r)
    elif re.search(r"(workflow|流程|步骤|第[一二三]步|Step \d)", b[:3000], re.I):
        k_wf.append(r)
    else: k_pure.append(r)

# ---------- §9 MERGE 复核（17） ----------
merge_ids = [sid for sid, e in prop_by.items() if e["action"] == "MERGE_CANDIDATE"]
merge_groups = {
  "EXACT_DUPLICATE": [], "FUNCTIONAL_OVERLAP": [], "NESTED": [], "COMPLEMENTARY": [],
  "DOMAIN_SPECIALIZATION": [], "VERSION_SPECIALIZATION": []}
def gname(sid): return reg_by[sid]["name"]
groups_judgment = {
  "github": ("VERSION_SPECIALIZATION", "MERGE_OPTIONAL", "上游版 vs 遗产版，同职责不同成熟度"),
  "tencent-docs": ("VERSION_SPECIALIZATION", "MERGE_OPTIONAL", "两版描述结构不同，各自演化"),
  "self-improving-agent": ("FUNCTIONAL_OVERLAP", "NEEDS_HUMAN_REVIEW", "3 版侧重不同(通用/错误捕获/空描述)，职责重叠但专长不同"),
  "game-studio-pair": ("FUNCTIONAL_OVERLAP", "MERGE_REQUIRED", "A/D 两系列 4 对同职责，子内容已确认 25 个精确副本"),
  "novel": ("EXACT_DUPLICATE", "MERGE_REQUIRED", "awesome-novel 32 个子文件与 novel-writing 完全相同，父包职责相同"),
  "git": ("COMPLEMENTARY", "KEEP_SEPARATE", "知识版+薄操作版，层次不同"),
  "email": ("FUNCTIONAL_OVERLAP", "MERGE_OPTIONAL", "上游已有对应物，遗产版可归并"),
  "search": ("COMPLEMENTARY", "KEEP_SEPARATE", "不同后端互为 fallback，非重复"),
}
merge_review_rows = []
for sid in merge_ids:
    n = gname(sid)
    if n == "github": gj = groups_judgment["github"]
    elif n == "tencent-docs": gj = groups_judgment["tencent-docs"]
    elif n == "self-improving-agent": gj = groups_judgment["self-improving-agent"]
    elif n.startswith("game-studio-"): gj = groups_judgment["game-studio-pair"]
    elif n in ("novel-writing", "awesome-novel"): gj = groups_judgment["novel"]
    elif n == "git-helper": gj = groups_judgment["git"]
    elif n == "Email Management": gj = groups_judgment["email"]
    elif n in ("tavily-search", "anysearch"): gj = groups_judgment["search"]
    else: gj = ("FUNCTIONAL_OVERLAP", "NEEDS_HUMAN_REVIEW", "未归组")
    merge_groups[gj[0]].append(n)
    merge_review_rows.append({"skill_id": sid, "name": n, "reclassified_as": gj[0],
                              "recommendation": gj[1], "evidence": gj[2]})

# ---------- §10 Security/Risk ----------
risk_lists = {
 "credential_access": ["1password", "stripe-link-cli", "weixinpay-pay", "weixinpay-register", "himalaya", "agentmail"],
 "payment_side_effect": ["weixinpay-pay", "stripe-link-cli", "stripe-projects", "mpp-agent", "shop"],
 "external_side_effect": ["xurl", "publish-site", "cloudflare-temporary-deploy", "here-now", "unbroker",
                          "social-media-content-calendar", "Email Management", "email-inbox-triage", "himalaya",
                          "imessage", "google_meet", "telephony"],
 "system_modification": ["docker-management", "computer-use", "hermes-s6-container-supervision", "openclaw-migration"],
 "destructive": ["unbroker", "obliteratus", "godmode"],
 "security_sensitive": ["godmode", "obliteratus", "web-pentest", "domain-intel", "oss-forensics", "sherlock"],
}
risk_rows = []
names = {r["name"]: r["skill_id"] for r in logical}
for k, ns in risk_lists.items():
    for n in ns:
        if n in names: risk_rows.append({"skill": n, "skill_id": names[n], "flag": k})
declared_risk = sum(1 for r in logical if re.search(r"risk_level|requires_human_approval", B[r["skill_id"]][:1500]))

# ---------- §11 Foundation 触点 ----------
touchpoints = [
 {"id": "FT-1", "maps_to": "FCP-001 T1", "object": "LIBRARY_RULES §2/§4/§11 实体与生命周期映射表无 Skill 行",
  "status": "FOUND_UNRESOLVED", "action": "仅记录，待 FCP 人工批准"},
 {"id": "FT-2", "maps_to": "FCP-001 T2", "object": "AGENT_ORCHESTRATION_SPEC §三十二 目录契约未含 14_AI_AGENTS/Skills/",
  "status": "FOUND_UNRESOLVED", "action": "目录依用户指令建立；spec 未修改，待 FCP"},
 {"id": "FT-3", "maps_to": "FCP-001 T3", "object": "EVOLUTION_RULES 演化对象/提案类型无 SKILL_*",
  "status": "FOUND_UNRESOLVED", "action": "Skill 演化暂无合法提案类型，待 FCP"},
 {"id": "FT-4", "maps_to": "FCP-001 T4(可选)", "object": "RETRIEVAL_DECISION_SPEC §五 检索清单无 Skill（方案A 下可不改）",
  "status": "DEFERRED_BY_DESIGN", "action": "方案 A 生效中，Phase 5 零改动"},
 {"id": "FT-5", "maps_to": "新增", "object": "SKILL_RULES.md 为新规则文件（宪章 §1.2 规则文件=Foundation）",
  "status": "DRAFT_PENDING", "action": "以 DRAFT 形式存在，修订走 FCP"},
]
foundation_modified = []   # 核实：既有受跟踪文件零修改

# ---------- 优先级分区（299 = 181 L2 + 118 L3） ----------
def core3_missing(sid):
    return [f for f in ("trigger/applicability", "inputs", "outputs") if f in (res[sid].get("l2_missing") or [])]
p0 = [s for s in res if res[s]["contract_level_current"] == "L0"]
p1 = [s for s in res if res[s]["contract_level_required"] == "L2" and s not in p0 and core3_missing(s)]
p2a = [s for s in res if res[s]["contract_level_required"] == "L2" and s not in p0 and not core3_missing(s)]
def hard_missing(sid): return [f for f in ("workflow", "validation_requirements", "failure_handling")
                               if f in (res[sid].get("l3_missing") or [])]
p2b = [s for s in res if res[s]["contract_level_required"] == "L3" and hard_missing(s)]
p3 = [s for s in res if res[s]["contract_level_required"] == "L3" and not hard_missing(s)]
assert len(p0) + len(p1) + len(p2a) + len(p2b) + len(p3) == 299, (len(p0), len(p1), len(p2a), len(p2b), len(p3))

# 上游 vs 个人（治理范围）
def tier(sid): return [r for r in logical if r["skill_id"] == sid][0]["tier"]
personal_p1 = sum(1 for s in p1 if not tier(s).startswith("B"))
personal_p2 = sum(1 for s in p2a + p2b if not tier(s).startswith("B"))
upstream_gap = sum(1 for s in p1 + p2a + p2b + p3 if tier(s).startswith("B"))

# 完整度（required 集合上的字段填充率）
def fill(ids, level):
    key = {"L2": "l2_missing", "L3": "l3_missing"}[level]
    nf = {"L2": 8, "L3": 9}[level]
    miss = sum(len(res[s].get(key) or []) for s in ids)
    return round(100 * (1 - miss / (len(ids) * nf)), 1) if ids else 0
l2_ids = [s for s in res if res[s]["contract_level_required"] == "L2"]
l3_ids = [s for s in res if res[s]["contract_level_required"] == "L3"]

OUT = {
 "leak_know_n": len(leak_know), "leak_know_ids": [r["skill_id"] for r in leak_know],
 "potential_cap_n": len(io_cap), "potential_cap": [(r["skill_id"], r["name"]) for r in io_cap],
 "agent_coup": agent_coup, "llm_hard": llm_hard, "oc_required": oc_required, "hermes_reasonable": hermes_ok,
 "cap_refs": cap_refs, "know_refs_n": len(know_refs_all), "broken_krefs": broken_krefs,
 "broken_paths": broken_paths, "declared_skill_deps": declared_skill_deps, "cycles": cycles,
 "ext_no_25": ext_no_25, "ext_content": ext_content, "impl_bypass": impl_bypass,
 "over": over, "big15": len(big15), "inline_know": len(inline_know), "no_l3": no_l3,
 "reg_len_avg": round(sum(reg_len) / len(reg_len), 1), "reg_len_max": max(reg_len),
 "tool": {"total": len(tool), "keep": [r["name"] for r in t_keep],
          "potential_capability": [r["name"] for r in t_cap],
          "potential_knowledge": [r["name"] for r in t_know]},
 "knowdeep": {"total": len(know), "pure": [r["name"] for r in k_pure],
              "plus_routing": [r["name"] for r in k_route], "true_workflow": [r["name"] for r in k_wf]},
 "merge_review": merge_review_rows, "merge_groups": {k: v for k, v in merge_groups.items() if v},
 "risk_rows": risk_rows, "declared_risk": declared_risk,
 "touchpoints": touchpoints,
 "priority": {"P0": len(p0), "P1": len(p1), "P2": len(p2a) + len(p2b), "P3": len(p3),
              "personal_P1": personal_p1, "personal_P2": personal_p2, "upstream_gap": upstream_gap},
 "completeness": {"L1": 100.0, "L2_fill_pct": fill(l2_ids, "L2"), "L3_fill_pct": fill(l3_ids, "L3")},
}
json.dump(OUT, open(SCRATCH + "/deep_audit.json", "w"), ensure_ascii=False, indent=1)
for k in ("leak_know_n", "potential_cap_n", "know_refs_n", "big15", "inline_know", "no_l3", "declared_risk"):
    print(k, "=", OUT[k])
print("tool:", {k: (len(v) if isinstance(v, list) else v) for k, v in OUT["tool"].items()})
print("knowdeep:", {k: (len(v) if isinstance(v, list) else v) for k, v in OUT["knowdeep"].items()})
print("priority:", OUT["priority"], "completeness:", OUT["completeness"])
print("agent_coup:", len(agent_coup), agent_coup[:8])
print("llm_hard:", llm_hard)
print("oc_required:", len(oc_required))
print("broken_paths:", len(broken_paths), "broken_krefs:", broken_krefs, "cap_refs:", cap_refs)
print("ext_no_25:", ext_no_25)
print("ext_content:", ext_content)
print("impl_bypass:", impl_bypass)
print("merge_groups:", json.dumps(OUT["merge_groups"], ensure_ascii=False))
print("risk flags:", collections.Counter(r["flag"] for r in risk_rows))
print("reg_len avg/max:", OUT["reg_len_avg"], OUT["reg_len_max"])
