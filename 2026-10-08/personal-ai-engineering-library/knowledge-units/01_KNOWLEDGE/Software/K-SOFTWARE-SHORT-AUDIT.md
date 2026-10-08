# K-SOFTWARE-SHORT-AUDIT — 审计五项（每项附原文证据）

- **Domain**: Software / General | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-031（Agent Skill: short-audit）| **Extracted**: 2026-10-08

## 知识正文

1. **转化质量**：抽查契约中来自题材包的招式条目——是否锚定本篇主角（角色名）、信息差（谁瞒谁追）、情绪节奏；发现原文复制或套用痕迹 → FAIL
2. **优先级顺序**：不可违反规则列表是否按 红线 > 字数 > 禁用项 > 叙事规则 > 写作规范同级其他 降序；建议性技法是否混入硬规则区 → 任一颠倒 FAIL
3. **规则去重**：同一对象同一格式的数量线 / 禁止项是否只出现一次；措辞不同但各有侧重的等价约束不算重复 → 完全重复 FAIL
4. **约束间一致性**：情绪与结构约束是否互相矛盾（如「反转一节内完成」vs 反转段占比折算字数；字数下限 vs 压缩策略）→ 任一矛盾 FAIL
5. **条目可核对性**：逐条检视硬规则区——每条是否可被定稿正文核对（机械判定或明确判据）；出现「把握好节奏」类无法核对的表述 → FAIL

## Provenance

- source_skill_id: `SKILL-GEN-SHORT-AUDIT`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/short/short-audit/SKILL.md`
- source_name: `short-audit`
- original_section: `审计五项（每项附原文证据）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
