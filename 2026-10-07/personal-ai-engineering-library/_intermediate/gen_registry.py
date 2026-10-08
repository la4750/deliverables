#!/usr/bin/env python3
# 生成 Skill 资产治理 7 份交付物 + SKILL_RULES.md，注册到 14_AI_AGENTS/Skills/
import json, re, collections, os, datetime, yaml

SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library/14_AI_AGENTS/Skills"
logical = json.load(open(SCRATCH + "/skill_final.json"))
inv = json.load(open(SCRATCH + "/skill_inventory_raw.json"))
ov = json.load(open(SCRATCH + "/overlap_raw.json"))
TODAY = "2026-10-07"
os.makedirs(LIB + "/Registry", exist_ok=True)

TIER_SRC = {"A_user_hermes":"hermes_user_installed","B1_bundled_core":"hermes_bundled_core",
 "B2_bundled_optional":"hermes_bundled_optional","B3_third_party_dep":"third_party_dependency",
 "C_plugin":"hermes_plugin","D_legacy_openclaw":"legacy_openclaw_workspace","E_other":"other_local"}

def ydump(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(obj, f, allow_unicode=True, sort_keys=False, width=120, default_flow_style=False)

# ============ 关系图（重叠/家族） ============
related = collections.defaultdict(set)
def link(a, b):
    related[a].add(b); related[b].add(a)

same_name_groups = {}
for k, v in ov["same_name"].items():
    names = set()
    for r in logical:
        if r["name"].lower() == k: names.add(r["skill_id"])
    same_name_groups[k] = sorted(names)
    ids = sorted(names)
    for i in ids:
        for j in ids:
            if i != j: link(i, j)

# A/D game-studio 同职责对
pairs = [("game-studio-architecture-review","architecture-review"),("game-studio-balance-check","balance-check"),
         ("game-studio-design-review","design-review"),("game-studio-qa-plan","qa-plan")]
by_name_first = {}
for r in logical: by_name_first.setdefault(r["name"], []).append(r)
def sid(n, idx=0):
    xs = by_name_first.get(n); return xs[idx]["skill_id"] if xs else None
for a, b in pairs:
    ra, rb = by_name_first.get(a), by_name_first.get(b)
    if ra and rb: link(ra[0]["skill_id"], rb[0]["skill_id"])
# novel 家族 / git / email / search
for a, b in [("novel-writing","awesome-novel"),("git-essentials","git-helper"),
             ("Email Management","email-inbox-triage")]:
    ra, rb = by_name_first.get(a), by_name_first.get(b)
    if ra and rb: link(ra[0]["skill_id"], rb[0]["skill_id"])
search_grp = ["tavily-search","anysearch","duckduckgo-search","searxng-search"]
sg = [by_name_first[n][0]["skill_id"] for n in search_grp if n in by_name_first]
for i in sg:
    for j in sg:
        if i != j: link(i, j)
# godot 知识簇
godot_k = [r["skill_id"] for r in logical if re.match(r"godot-|godot-kb", r["name"]) and r["category"]=="KNOWLEDGE_WRAPPER"]
for i in godot_k:
    for j in godot_k:
        if i != j: link(i, j)
# 同内容副本（已合并，不再成对）+ 父子关系
children = collections.defaultdict(list)
for r in logical:
    if r.get("nested_in"): children[r["nested_in"]].append(r["skill_id"])
for parent, kids in children.items():
    prs = by_name_first.get(parent)
    if prs:
        for k in kids: link(prs[0]["skill_id"], k)

# ============ 优化动作分配 ============
SAFETY_REVIEW = {"godmode", "obliteratus"}
d_oc = {r["name"] for r in logical if r["tier"].startswith("D") and "openclaw" in json.dumps(r["quality"].get("runtime_binding", [])).lower()}
merge_members = set()
for grp in same_name_groups.values(): merge_members.update(grp)
for a, b in pairs + [("novel-writing","awesome-novel"),("git-essentials","git-helper"),("Email Management","email-inbox-triage")]:
    for n in (a, b):
        if n in by_name_first:
            # 只把 D/非活跃一侧标为合并候选（活跃 A 侧保留）
            for r in by_name_first[n]:
                if r["tier"].startswith("D"): merge_members.add(r["skill_id"])
for n in search_grp:
    if n in by_name_first:
        for r in by_name_first[n]:
            if r["tier"].startswith("D"): merge_members.add(r["skill_id"])

def usage_status(r):
    if r["tier"] == "B3_third_party_dep": return "excluded_dependency"
    if r["loaded_in_hermes"]:
        u = r.get("usage")
        if u and u.get("use_count", 0) > 0: return "active_use"
        return "loaded_unused"
    if r["tier"].startswith("A") or r["tier"] == "C_plugin":
        u = r.get("usage")
        if u and u.get("use_count", 0) > 0: return "active_use"
        return "on_disk_inactive"
    return "not_loaded"

def action(r):
    n, c, t = r["name"], r["category"], r["tier"]
    if t == "B3_third_party_dep": return ("REVIEW_REQUIRED", "第三方依赖自带技能，非个人资产——建议 EXCLUDE 出治理范围（待裁定）")
    if n in SAFETY_REVIEW: return ("REVIEW_REQUIRED", "安全敏感技能（越狱/移除拒绝）——需人工合规复核后决定去留")
    if r["skill_id"] in merge_members: return ("MERGE_CANDIDATE", "与关联技能职责高度重叠（见 SKILL_OVERLAP_REPORT）——仅标记，不合并")
    if c == "KNOWLEDGE_WRAPPER": return ("CONVERT_TO_KNOWLEDGE", "主体为知识/参考内容——知识应迁 Phase 4，Skill 保留薄路由层")
    if c == "CAPABILITY_WRAPPER": return ("CONVERT_TO_CAPABILITY", "单一稳定能力接口——适合映射 Capability Registry（提案，不自动创建）")
    if n in d_oc: return ("REVIEW_REQUIRED", "绑定 OpenClaw 运行时——需移植验证或归档裁定")
    if c == "PROJECT_SPECIFIC": return ("KEEP", "项目专属，不泛化")
    q = r["quality"]
    if t in ("A_user_hermes","C_plugin","D_legacy_openclaw"):
        if (c in ("WORKFLOW_SKILL","TOOL_WRAPPER","META_SKILL","AGENT_WORKFLOW")) and \
           (not q["has_validation"] or not q["has_outputs"] or q["knowledge_heavy"] or not q["description_triggers"]):
            return ("KEEP+OPTIMIZE", "个人资产，但缺验证/输出声明或触发描述弱或知识混入（见 SKILL_OPTIMIZATION_REPORT）")
    return ("KEEP", "当前定位清晰，直接注册")

# ============ Registry ============
registry = {"registry": {
    "schema_version": "0.1.0",
    "schema_ref": "14_AI_AGENTS/Skills/SKILL_CLASSIFICATION.yaml（字段契约见 SKILL_RULES.md）",
    "created_at": TODAY, "created_by": "skill-inventory-audit（用户 2026-10-07 指令）",
    "status": "REGISTERED",
    "stage_note": "DISCOVERED→REGISTERED 已完成；REVIEWED/VALIDATED 未开始——注册≠验证",
    "totals": {"files_discovered": len(inv), "logical_skills": len(logical),
               "redundant_copies": len(inv) - len(logical), "registered": len(logical)},
    "updated_at": TODAY},
    "skills": []}

for r in sorted(logical, key=lambda x: (x["domain"], x["name"])):
    u = r.get("usage")
    registry["skills"].append({
        "skill_id": r["skill_id"], "name": r["name"],
        "description": (r["description"] or "")[:300] or None,
        "category": r["category"], "domain": r["domain"],
        "status": "REGISTERED", "version": r.get("version") or "unknown",
        "source": TIER_SRC[r["tier"]],
        "source_path": r["path"],
        "canonical_path": r["path"],
        "copies": r.get("copy_paths") or [],
        "nested_in": r.get("nested_in"),
        "dependencies": "not_recorded",
        "required_capabilities": "not_assessed",
        "required_knowledge": "not_assessed",
        "compatible_agents": "not_assessed",
        "compatible_runtime": (r["quality"]["runtime_binding"] or ["unspecified"]),
        "validation_status": "not_validated",
        "usage_status": usage_status(r),
        "use_count": (u or {}).get("use_count"),
        "last_used_at": (u or {}).get("last_used_at"),
        "last_reviewed": TODAY,
        "provenance": {"origin": TIER_SRC[r["tier"]], "discovered_at": TODAY,
                       "discovery_method": "filesystem full-scan (find SKILL.md)",
                       "original_mtime": r["mtime"]},
        "related_skills": sorted(related.get(r["skill_id"], [])) or [],
        "supersedes": None, "superseded_by": None})

ydump(registry, LIB + "/Registry/SKILL_REGISTRY.yaml")

# ============ INVENTORY（430 文件级） ============
def itier(p):
    if p.startswith("~/.hermes/skills/"): return "hermes_user_installed"
    if p.startswith("~/.hermes/hermes-agent/"):
        if "optional-skills" in p: return "hermes_bundled_optional"
        if "/venv/" in p or "site-packages" in p: return "third_party_dependency"
        return "hermes_bundled_core"
    if p.startswith("~/.hermes/plugins/"): return "hermes_plugin"
    if p.startswith("~/ai-heritage-library/"): return "legacy_openclaw_workspace"
    return "other_local"

inventory = {"inventory": {
    "stage": "DISCOVERED（只读扫描，未修改任何 Skill）", "scanned_at": TODAY,
    "roots": ["~/.hermes/skills", "~/.hermes/hermes-agent", "~/.hermes/plugins",
              "~/ai-heritage-library", "其他本地目录(全 home 深扫)"],
    "total_files": len(inv),
    "by_source": dict(collections.Counter(itier(i["path"]) for i in inv)),
    "note": "同一逻辑技能可能有多个文件（跨层副本），去重后见 SKILL_REGISTRY（logical_skills）"},
    "entries": []}
for i in sorted(inv, key=lambda x: x["path"]):
    inventory["entries"].append({
        "name": i["name"], "path": i["path"], "source": itier(i["path"]),
        "has_skill_md": True, "version": i.get("version") or "unknown",
        "description": (i["description"] or "")[:200] or None,
        "scripts": i["scripts"] or [], "subdirs": i["subdirs"] or [],
        "other_files": i["other_files"] or [],
        "body_bytes": i["body_bytes"], "sha256_16": i["sha256"],
        "last_modified": i["mtime"], "loaded_in_hermes": i["loaded_in_hermes"],
        "author": "not_recorded"})
ydump(inventory, LIB + "/SKILL_INVENTORY.yaml")

# ============ CLASSIFICATION（358） ============
cls = {"classification": {
    "taxonomy": ["WORKFLOW_SKILL","CAPABILITY_WRAPPER","KNOWLEDGE_WRAPPER","TOOL_WRAPPER",
                 "AGENT_WORKFLOW","PROJECT_SPECIFIC","META_SKILL","DUPLICATE_OR_OVERLAP",
                 "OBSOLETE","UNKNOWN"],
    "method": "规则打底 + 358 条逐条人工复核定类；DUPLICATE_OR_OVERLAP/OBSOLETE/UNKNOWN 由重叠分析与证据单独标注",
    "counts": dict(collections.Counter(r["category"] for r in logical)),
    "dup_note": f"72 个完全重复簇/144 个文件的副本关系记录在 registry.copies；3 个同名异容簇单列",
    "obsolete_note": "本轮无确证 OBSOLETE（deprecated_tool 命中 1、OpenClaw 运行时绑定 13 项列为 REVIEW_REQUIRED 待移植验证）",
    "classified_at": TODAY},
    "skills": []}
dup_ids = set(merge_members)
for r in sorted(logical, key=lambda x: x["skill_id"]):
    cats = [r["category"]]
    if r["skill_id"] in dup_ids: cats.append("DUPLICATE_OR_OVERLAP(候选)")
    cls["skills"].append({"skill_id": r["skill_id"], "name": r["name"],
        "category": cats[0], "overlap_flag": len(cats) > 1,
        "domain": r["domain"], "tier": r["tier"],
        "nested_in": r.get("nested_in"), "copies": len(r.get("copy_paths") or []),
        "granularity_flags": r["granularity"] or [],
        "judged_by": "manual_review_2026-10-07"})
ydump(cls, LIB + "/SKILL_CLASSIFICATION.yaml")

# ============ MIGRATION PROPOSALS ============
acts = collections.Counter()
props = {"proposals": {
    "stage": "PROPOSAL ONLY——本轮禁止删除/合并/重写/转换，全部动作待人工批准",
    "created_at": TODAY,
    "action_enum": ["KEEP","KEEP+OPTIMIZE","MERGE_CANDIDATE","CONVERT_TO_CAPABILITY",
                    "CONVERT_TO_KNOWLEDGE","CONVERT_TO_TOOL","ARCHIVE_CANDIDATE","REVIEW_REQUIRED"],
    "summary": {}, "entries": []}}
for r in sorted(logical, key=lambda x: x["skill_id"]):
    a, reason = action(r)
    acts[a] += 1
    props["proposals"]["entries"].append({"skill_id": r["skill_id"], "name": r["name"],
        "action": a, "reason": reason, "category": r["category"], "source": TIER_SRC[r["tier"]],
        "related_skills": sorted(related.get(r["skill_id"], []))})
props["proposals"]["summary"] = dict(acts.most_common())
ydump(props, LIB + "/SKILL_MIGRATION_PROPOSALS.yaml")

print("== 动作分布 ==")
for k, v in acts.most_common(): print(f"  {k}: {v}")
print("registry:", len(registry["skills"]), "| inventory:", len(inventory["entries"]),
      "| classification:", len(cls["skills"]), "| proposals:", len(props["proposals"]["entries"]))
print("usage_status:", dict(collections.Counter(s["usage_status"] for s in registry["skills"])))
json.dump({k: sorted(v) for k, v in related.items()}, open(SCRATCH + "/related.json", "w"))
