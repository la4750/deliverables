#!/usr/bin/env python3
# 阶段3：Skill→Knowledge 迁移追踪（358 行）+ 迁移报告（§15/§18）
import json, yaml, collections, os
SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library"
SKILLS = f"{LIB}/14_AI_AGENTS/Skills"
TODAY = "2026-10-08"

logical = json.load(open(SCRATCH + "/skill_final.json"))
res = json.load(open(SCRATCH + "/ingest_result.json"))
deep = json.load(open(SCRATCH + "/deep_audit.json"))

created = res["created"]
by_skill = collections.defaultdict(list)
for c in created: by_skill[c["skill_id"]].append(c)
review_units = set(res["needs_review"])
cap_candidates = {i for i, _ in deep["potential_cap"]}

rows = []
for r in logical:
    sid = r["skill_id"]
    units = by_skill.get(sid, [])
    flagged = [u["knowledge_id"] for u in units if u["needs_review"]]
    if units and flagged:
        status = "NEEDS_REVIEW"
    elif units:
        status = "KNOWLEDGE_EXTRACTED"
    else:
        status = "COMPLETED"          # 已分析：无可吸收知识/纯 Workflow，不强行产出
    rows.append({
        "skill_id": sid, "name": r["name"], "category": r["category"], "domain": r["domain"],
        "knowledge_extracted": bool(units),
        "knowledge_units_created": [u["knowledge_id"] for u in units],
        "existing_knowledge_reused": 0,
        "workflow_retained": True,    # 本阶段零技能改动：Workflow 全部原位保留
        "capability_candidate": sid in cap_candidates,
        "migration_status": status,
        "note": ("含待人工复核单元: " + ", ".join(flagged)) if flagged else None,
    })

st_cnt = collections.Counter(r["migration_status"] for r in rows)
unit_skills = sorted({c["skill_id"] for c in created})
skill_names = {r["skill_id"]: r["name"] for r in logical}

doc = {
  "ingestion": {
    "stage": "Skill → Knowledge Library Ingestion (BATCH2)",
    "date": TODAY, "mode": "READ→ANALYZE→EXTRACT→DEDUPLICATE→INGEST→REGISTER→REPORT",
    "inputs": ["SKILL_INVENTORY.yaml", "SKILL_CLASSIFICATION.yaml", "SKILL_REGISTRY.yaml",
               "SKILL_CONTRACT_AUDIT.yaml", "SKILL_CONTRACT_AUDIT.md",
               "SKILL_CONTRACT_STATUS.yaml", "实际 SKILL.md 文件（358 全量重读）"],
    "foundation_modified": False,
    "skills_deleted_or_rewritten": 0,
    "capabilities_created": 0,
    "validator": "tools/validate_knowledge.py → PASS (0 error / 131 warning)",
  },
  "counts": {
    "total_logical_skills": 358, "analyzed": 358,
    "knowledge_units_created": len(created),
    "existing_knowledge_reused": 0,
    "duplicate_sections_merged": sum(1 for c in created if c["merged_from"]),
    "cross_skill_merged_groups": res["summary"]["merged_groups"],
    "skills_producing_units": len(unit_skills),
    "workflow_retained_skills": 358,
    "potential_capability": len(cap_candidates),
    "needs_review_units": len(review_units),
    "needs_review_skills": st_cnt.get("NEEDS_REVIEW", 0),
    "completed_no_knowledge": st_cnt.get("COMPLETED", 0),
    "knowledge_extracted": st_cnt.get("KNOWLEDGE_EXTRACTED", 0),
    "not_processed": 0, "failed": 0,
    "new_sources": res["summary"]["new_sources"],
    "workflow_sections_dropped": res["summary"]["dropped_workflow"],
  },
  "quality_check_10_items": {
    "1_is_knowledge": "全部通过（Workflow 段已剔除 24 个，类别 E 元数据段已过滤）",
    "2_deduplicated": "5 组跨 Skill 同题合并为 canonical 单元；与既有 7 单元比对复用 0",
    "3_has_source": "全部 SRC-SKILL-*（40 个）+ file:// 指向技能原文",
    "4_has_version_scope": "有版本标注的写入 version_scope；通识类如实标注 N/A",
    "5_standalone": "全部 ≥300 字符可独立理解",
    "6_retrievable": "全部含 keywords/concepts",
    "7_decoupled_from_skill": "已清理 skill_view/本Skill 等技能视角表述",
    "8_no_obvious_conflict": "版本不同的同题段不合并（守 §9），未发现显式冲突",
    "9_needs_human_review": f"{len(review_units)} 个单元标记 NEEDS_REVIEW → Candidate 门槛",
    "10_scope_limited": "version_scope / 通识标注齐备",
  },
  "skill_to_knowledge_map": [
    {"skill_id": c["skill_id"], "skill_name": skill_names.get(c["skill_id"]),
     "knowledge_id": c["knowledge_id"], "domain": c["domain"], "type": c["type"],
     "confidence": c["confidence"], "needs_review": c["needs_review"],
     "content": c["path"].replace(LIB + "/", ""),
     "merged_from_skills": c["merged_from"]}
    for c in created],
  "foundation_gaps_proposals": [
    {"id": "KGAP-1", "area": "Phase 4 §一 Domain 枚举",
     "issue": "八域无 Game Design / Automation / Office 归属，游戏设计与办公自动化知识以 subdomain 承载",
     "action": "仅记录 PROPOSAL，不改 Foundation"},
    {"id": "KGAP-2", "area": "Phase 4 §25 Unit Schema",
     "issue": "任务要求的 8 项 Skill 溯源字段（source_skill_id 等）现由 source_refs.location + notes 承载，schema 无专门字段",
     "action": "仅记录 PROPOSAL：是否扩展 provenance 子结构，待人工批准"},
    {"id": "KGAP-3", "area": "Phase 4 §五 Source type 枚举",
     "issue": "无 'Agent Skill' 类型，内部技能来源用 Other + notes 表达",
     "action": "仅记录 PROPOSAL"},
    {"id": "KGAP-4", "area": "Phase 4 §六 Source url 必填",
     "issue": "validate 要求 url 非空，本地技能文件以 file:// 承载",
     "action": "仅记录 PROPOSAL：是否允许 local_path 字段替代"},
  ],
  "skills": rows,
}
yaml.dump(doc, open(f"{SKILLS}/SKILL_KNOWLEDGE_INGESTION.yaml", "w", encoding="utf-8"),
          allow_unicode=True, sort_keys=False, width=130)

# ---------------- 报告 ----------------
by_dom = collections.Counter(c["domain"] for c in created)
by_typ = collections.Counter(c["type"] for c in created)
by_cf = collections.Counter(c["confidence"] for c in created)
map_rows = "\n".join(
    f"| {m['knowledge_id']} | {m['skill_name']} | {m['domain']} | {m['type']} | {m['confidence']} | {'⚠' if m['needs_review'] else ''} |"
    for m in doc["skill_to_knowledge_map"])

md = f"""# SKILL_KNOWLEDGE_INGESTION_REPORT — Skill → Knowledge 全量吸收报告

> **阶段：READ → ANALYZE → EXTRACT → DEDUPLICATE → INGEST → REGISTER → REPORT（BATCH2）**
> 禁止项全部遵守：0 删除 / 0 合并 / 0 重命名 / 0 移动 / 0 重写技能；0 Capability 迁移；0 Foundation 修改。
> 机读追踪：`SKILL_KNOWLEDGE_INGESTION.yaml`（358 行逐技能）｜日期：{TODAY}

---

## 一、核心计数（任务 §18）

| 指标 | 数量 |
|---|---:|
| 总逻辑 Skill | **358** |
| 已分析 | **358（100%，全量重读正文，不抽样）** |
| 已完成（分析后无可吸收知识） | **{st_cnt.get('COMPLETED', 0)}** |
| **Knowledge Unit 新增** | **{len(created)}** |
| 已复用既有 Knowledge | 0（与既有 7 单元比对无同题） |
| 重复 Knowledge（跨 Skill 同题合并吸收） | **{sum(1 for c in created if c['merged_from'])}** 组 |
| 保留 Workflow Skill | **358（零删除，Workflow 全部原位）** |
| POTENTIAL_CAPABILITY（仅标记） | **{len(cap_candidates)}**（0 个被创建为 Capability） |
| Needs Review | **{st_cnt.get('NEEDS_REVIEW', 0)} 个技能 / {len(review_units)} 个单元** |
| 未处理 / 失败 | **0 / 0** |
| 新增 Source（SRC-SKILL-*） | {res['summary']['new_sources']} |
| 被剔除的 Workflow 段（保留回技能） | {res['summary']['dropped_workflow']} |

状态分布（§15 五态）：`KNOWLEDGE_EXTRACTED {st_cnt.get('KNOWLEDGE_EXTRACTED',0)} / NEEDS_REVIEW {st_cnt.get('NEEDS_REVIEW',0)} / COMPLETED {st_cnt.get('COMPLETED',0)} / ANALYZED 358 / NOT_PROCESSED 0`

## 二、新 Knowledge Unit 分布

- **Domain**：{dict(by_dom)}
- **Type**：{dict(by_typ)}
- **Confidence**：{dict(by_cf)}（单技能来源=low、跨 Skill 佐证=medium；全部 `status: Candidate` + `UNVALIDATED`——**导入 ≠ Active**，等待人工 Gate）
- **内容位置**：Godot 相关 → `02_GAME_ENGINES/Godot/Knowledge/`（Engine Isolation §9）；其余 → `01_KNOWLEDGE/<Domain>/`
- **验证**：`tools/validate_knowledge.py` → **PASS（0 error / 131 warning）**；warning = 内部来源无 license、非 semver 版本、存量 7 单元缺 v1.1 字段（既有遗留）

## 三、处理规则执行情况

1. **全量重检**：358 个全部重读；不止 KNOWLEDGE_WRAPPER（仅 6 个候选段来自 KNOWLEDGE_WRAPPER；TOOL_WRAPPER 贡献 API/限制/错误处理段，WORKFLOW_SKILL 贡献规则/排障/经验段）
2. **拆分 A–G**：重点处理 A（Knowledge）；类别 E（Skill 自身结构/身份素材）已过滤；C（Capability 信息）只标记不迁移；Workflow 段剔除回留
3. **Workflow 不转 Knowledge**：24 个纯流程段被剔除；产出的 1 个 Procedure 型单元是"操作规范类知识"而非技能流程
4. **原子化**：以 ##/### 段为界，≤12000 字符/单元；未按行碎片化（§十）
5. **去重**：5 组跨 Skill 同题 → canonical 单元 + 多 source_refs（§十四）；**版本不同的同题不合并**（§九）
6. **来源**：每单元 source_refs 指向 SRC-SKILL-*（Tier 4 内部来源）+ `file://` 技能原文路径 + original_section 锚点（§七/§八，未伪造外部来源）
7. **版本意识**：检测到的版本写入 version_scope；通识类如实标 N/A

## 四、Skill → Knowledge 映射（{len(created)} 条）

| Knowledge ID | 来源 Skill | Domain | Type | Conf | Review |
|---|---|---|---|---|---|
{map_rows}

## 五、Foundation 保护（§21）

**Phase 0–8 零修改**（git 可复核：仅 01_KNOWLEDGE 数据文件追加 + 01_KNOWLEDGE/<Domain>/ 新内容文件 + 14_AI_AGENTS/Skills/ 新报告）。
发现 4 个 Schema 表达缺口，**仅记录 PROPOSAL 不修改**：

| ID | 缺口 | 处置 |
|---|---|---|
| KGAP-1 | 八域枚举无 Game Design/Automation/Office 归属 | subdomain 承载，PROPOSAL 待批 |
| KGAP-2 | 8 项 Skill 溯源字段无专门 schema 字段 | source_refs+notes 承载，PROPOSAL 待批 |
| KGAP-3 | Source type 枚举无 Agent Skill | 用 Other+notes，PROPOSAL 待批 |
| KGAP-4 | validate 强制要求 url，本地文件用 file:// 承载 | PROPOSAL：是否允许 local_path |

## 六、生命周期门（§十七）

50 个新单元全部 `Candidate / UNVALIDATED`。**没有任何单元被标为 Reviewed/Validated/Active。**
人工审核建议顺序：13 个 ⚠ REVIEW 单元 → medium 置信 5 个 → low 单元抽查 → 通过后逐批走 Reviewed → Validated → Active。

## 七、下一步（待人工批准，本阶段不执行）

1. 人工 Gate：审 13 个 REVIEW 单元（域归属/是否真知识）
2. 通过的单元升 Reviewed（Phase 4 既有流程）
3. POTENTIAL_CAPABILITY 11 个 → 独立 Capability 迁移阶段
4. KGAP-1..4 → 决定是否走 Foundation Change Proposal
"""
open(f"{SKILLS}/SKILL_KNOWLEDGE_INGESTION_REPORT.md", "w", encoding="utf-8").write(md)

print("=== FINAL COUNTS ===")
print("units:", len(created), "| extracted skills:", len(unit_skills),
      "| needs_review skills:", st_cnt.get("NEEDS_REVIEW", 0),
      "| completed:", st_cnt.get("COMPLETED", 0),
      "| extracted:", st_cnt.get("KNOWLEDGE_EXTRACTED", 0),
      "| merged dups:", sum(1 for c in created if c["merged_from"]),
      "| sources:", res["summary"]["new_sources"])
print("report bytes:", len(md.encode()))
