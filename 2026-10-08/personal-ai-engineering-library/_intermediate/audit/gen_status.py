#!/usr/bin/env python3
# 组装 §12 输出：SKILL_CONTRACT_STATUS.yaml（16 项）+ SKILL_CONTRACT_AUDIT.md（§1-13 报告）
import json, yaml, collections, os
SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library/14_AI_AGENTS/Skills"
D = json.load(open(SCRATCH + "/deep_audit.json"))
aud = yaml.safe_load(open(f"{LIB}/SKILL_CONTRACT_AUDIT.yaml"))
logical = json.load(open(SCRATCH + "/skill_final.json"))
res = {r["skill_id"]: r for r in aud["skills"]}
tier_of = {r["skill_id"]: r["tier"] for r in logical}
name_of = {r["skill_id"]: r["name"] for r in logical}

# 修正优先级分层（按来源精确重算）
def is_up(sid): return tier_of[sid].startswith("B")
gaps = [s for s in res if res[s]["contract_gap"]]
pri = {"P0": [s for s in res if res[s]["contract_level_current"] == "L0"]}
def core3(sid): return [f for f in ("trigger/applicability","inputs","outputs") if f in (res[sid].get("l2_missing") or [])]
pri["P1"] = [s for s in gaps if res[s]["contract_level_required"]=="L2" and s not in pri["P0"] and core3(s)]
pri["P2"] = [s for s in gaps if s not in pri["P0"] and s not in pri["P1"] and
             ((res[s]["contract_level_required"]=="L2" and not core3(s)) or
              (res[s]["contract_level_required"]=="L3" and any(f in (res[s].get("l3_missing") or []) for f in ("workflow","validation_requirements","failure_handling"))))]
pri["P3"] = [s for s in gaps if s not in pri["P0"] and s not in pri["P1"] and s not in pri["P2"]]
assert sum(len(v) for v in pri.values()) == len(gaps), (len(gaps), {k: len(v) for k, v in pri.items()})
tier_split = {k: {"total": len(v), "personal": sum(1 for s in v if not is_up(s)),
                  "upstream_reference_only": sum(1 for s in v if is_up(s))} for k, v in pri.items()}

# merge 复核分组修正
bare_reviews = {"architecture-review","balance-check","qa-plan","design-review"}
for row in D["merge_review"]:
    if row["name"] in bare_reviews:
        row.update(reclassified_as="FUNCTIONAL_OVERLAP", recommendation="MERGE_REQUIRED",
                   evidence="与 game-studio-* 同职责对；game-studio 侧 25 个子内容已确认精确副本")
    elif row["name"] == "git-essentials":
        row.update(reclassified_as="COMPLEMENTARY", recommendation="KEEP_SEPARATE",
                   evidence="知识版+薄操作版，层次不同")
grp_count = collections.Counter(r["reclassified_as"] for r in D["merge_review"])
rec_count = collections.Counter(r["recommendation"] for r in D["merge_review"])

# 风险去重
risk_unique = sorted({r["skill_id"] for r in D["risk_rows"]})

# 潜在能力候选（11 = CAP_WRAPPER 6 + 有 I/O 契约的 TOOL 5）
pot_cap_names = [n for _, n in D["potential_cap"]]

# ---------- STATUS YAML（16 项） ----------
status = {
 "status": {
   "stage": "Skill Registry Quality & Contract Completeness Audit（READ→ANALYZE→CLASSIFY→REPORT）",
   "date": "2026-10-08", "mode": "READ-ONLY",
   "note": "仅新增本文件与 SKILL_CONTRACT_AUDIT.md；既有交付物零修改"},
 "1_total_logical_skills": 358,
 "2_level_required_distribution": {"L1": 59, "L2": 181, "L3": 118},
 "3_contract_completeness": {
   "level_current": {"L0": 1, "L1": 357, "L2": 0, "L3": 0},
   "gap": {"true": len(gaps), "false": 59},
   "field_fill_pct": {"L1_required": 100.0, "L2_required": D["completeness"]["L2_fill_pct"],
                      "L3_required": D["completeness"]["L3_fill_pct"]}},
 "4_knowledge_leakage": {"count": D["leak_know_n"],
   "definition": "KNOWLEDGE_WRAPPER 或正文知识堆料(knowledge_heavy)",
   "disposition": "仅标记 CONVERT_TO_KNOWLEDGE 候选；知识迁移须走 Phase 4 分批审批",
   "ids_sample": D["leak_know_ids"][:12]},
 "5_capability_leakage": {"count": D["potential_cap_n"], "flag": "POTENTIAL_CAPABILITY",
   "items": pot_cap_names, "disposition": "不得自动创建 Capability"},
 "6_agent_coupling": {"count": len(D["agent_coup"]),
   "items": [{"skill": name_of[s], "tokens": t} for s, t in D["agent_coup"]],
   "note": "全部为硬编码 novel-agent 名称；角色名引用（game-studio team roles）属 Phase 7 角色结构，不算实例耦合"},
 "7_runtime_coupling": {
   "real_issues_openclaw_required": {"count": len(D["oc_required"]), "ids": D["oc_required"]},
   "llm_hard_requirement": {"count": len(D["llm_hard"]), "items": D["llm_hard"],
                            "verdict": "claude-code 委派目标即该 CLI，属技能主题本身，不算违规"},
   "reasonable_implementation_context": {"count": D["hermes_reasonable"],
     "verdict": "上游/用户技能正文提及 Hermes 属合理 implementation detail，不判违规"}},
 "8_broken_dependencies": {
   "skill_to_skill": {"declared": 0, "cycles": 0, "note": "依赖均未声明（not_recorded），嵌套树无环"},
   "broken_path": {"count": len(D["broken_paths"]), "scope": "13 个上游技能引用本机缺失脚本"},
   "broken_id": {"capability_refs_found": 0, "knowledge_refs_found": D["know_refs_n"],
                 "broken": 0, "note": "技能从未引用库内 Capability/Knowledge ID——依赖全部未登记，故无 ID 可断"},
   "deprecated_dependency": {"count": 12, "note": "OpenClaw 运行时依赖（与 runtime_coupling 同集）"},
   "version_mismatch": {"count": "undetermined", "note": "version_scope 缺失 321/358，无声明无法比对"},
   "bypass_phase_2_5_external": {"count": len(D["ext_no_25"]) + 2,
     "items": D["ext_no_25"] + ["SKILL-GAME-GODOT-CODING-PATTERNS(awesome-godot 提取)",
                                "SKILL-GEN-POPULAR-WEB-DESIGNS(54 站点设计复刻)"],
     "disposition": "仅标记，外部资源评估走 Phase 2.5 管线"},
   "bypass_capability_interface": {"count": len(D["impl_bypass"]),
     "items": [f"{s} {sc}" for s, sc in D["impl_bypass"]],
     "disposition": "标记绑定 Implementation 嫌疑，不转换"}},
 "9_tool_wrapper_audit": {"total": D["tool"]["total"], "KEEP_AS_SKILL": len(D["tool"]["keep"]),
   "POTENTIAL_CAPABILITY": D["tool"]["potential_capability"],
   "POTENTIAL_KNOWLEDGE": len(D["tool"]["potential_knowledge"]),
   "potential_knowledge_items": D["tool"]["potential_knowledge"], "auto_conversion": "NONE"},
 "10_knowledge_wrapper_audit": {"total": D["knowdeep"]["total"],
   "PURE_KNOWLEDGE": D["knowdeep"]["pure"], "KNOWLEDGE_PLUS_ROUTING": len(D["knowdeep"]["plus_routing"]),
   "TRUE_WORKFLOW_SKILL": D["knowdeep"]["true_workflow"],
   "true_workflow_items": D["knowdeep"]["true_workflow"],
   "disposition": "PLUS_ROUTING 保留薄 Skill（Skill→Knowledge Retrieval）；不建议删除任何 Skill"},
 "11_merge_candidate_review": {"total": len(D["merge_review"]),
   "by_type": dict(grp_count), "by_recommendation": dict(rec_count),
   "name_similarity_as_reason": "FORBIDDEN——逐对以职责/内容证据判定，详见 SKILL_CONTRACT_AUDIT.md §9"},
 "12_progressive_disclosure_issues": {
   "registry_metadata_overweight": False, "registry_entry_avg_bytes": D["reg_len_avg"],
   "registry_entry_max_bytes": D["reg_len_max"], "verdict": "Registry 元数据轻量（均值~1KB），合格",
   "skill_md_oversized_gt40k": D["over"], "skill_md_gt15k": D["big15"],
   "references_inline_not_lazy": {"count": D["inline_know"], "note": "知识堆进正文而非 references/ 按需加载"},
   "scripts_assets_in_metadata": 0, "no_l3_assets_at_all": D["no_l3"]},
 "13_security_risk": {"risk_level_declared_in_registry": 0,
   "risk_keywords_in_bodies": D["declared_risk"], "flagged_skills": len(risk_unique),
   "flags": dict(collections.Counter(r["flag"] for r in D["risk_rows"])),
   "credential_access": ["1password","stripe-link-cli","weixinpay-pay","weixinpay-register","himalaya","agentmail"],
   "disposition": "只标记；risk_level/requires_human_approval 补录属 REVIEWED 阶段动作"},
 "14_foundation_touchpoints": {"count": len(D["touchpoints"]), "items": D["touchpoints"],
   "foundation_files_modified": 0, "verdict": "Skill=Content 层定位成立；5 个触点全部为待 FCP 的追加项，无一处已修改"},
 "15_priorities": {k: {"skills": len(v), **tier_split[k]} for k, v in pri.items()},
 "16_recommended_next_actions": [
   "P0：补 1 个空 description（SKILL-AI-SELF-IMPROVING-AGENT）——最小修复",
   "个人层 P1（56）：补触发/输入/输出三件（A/D 层，发现性直接受益）",
   "个人层 P2（39）：L2 余量字段 + L3 硬三件，按真实使用频率排序执行",
   "12 个 OpenClaw 运行时依赖技能：移植验证或归档裁定（REVIEW）",
   "风险补录：36 个有副作用技能在 REVIEWED 阶段登记 risk_level/审批位",
   "上游 199 个缺口：建议 SKILL_RULES 修订为 reference-only 考核豁免（协议变更→走审批），不逐个修",
   "以上全部为提案；本阶段不执行任何动作"],
}
yaml.dump(status, open(f"{LIB}/SKILL_CONTRACT_STATUS.yaml", "w", encoding="utf-8"),
          allow_unicode=True, sort_keys=False, width=130)
json.dump({"pri": {k: len(v) for k, v in pri.items()}, "tier_split": tier_split,
           "grp": dict(grp_count), "rec": dict(rec_count), "risk_unique": len(risk_unique)},
          open(SCRATCH + "/status_extra.json", "w"), ensure_ascii=False, indent=1)
print("STATUS written. priorities:", {k: len(v) for k, v in pri.items()})
print("tier_split:", json.dumps(tier_split, ensure_ascii=False))
print("merge by rec:", dict(rec_count), "| risk unique:", len(risk_unique))
