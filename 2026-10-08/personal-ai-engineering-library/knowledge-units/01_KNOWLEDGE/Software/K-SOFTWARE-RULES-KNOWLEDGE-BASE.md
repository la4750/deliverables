# K-SOFTWARE-RULES-KNOWLEDGE-BASE — rules-knowledge-base: 1. 先立契约，再填内容

- **Domain**: Software / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-024（Agent Skill: rules-knowledge-base）| **Extracted**: 2026-10-08

## 知识正文

- 目录：每领域 `<DOMAIN>/{RULES,API,ANTI_PATTERNS}.yaml + NOTES.md`；`CHECKPOINTS/CHECKPOINT_<DOMAIN>.md`；顶层四库（BEST_PRACTICES / ANTI_PATTERNS / API_INDEX / VERSION_RULES）+ `_stats.json`；`tools/`；`tools/domains_registry.yaml`。
- 规则 schema 必填：`id / rule / level(MUST|SHOULD|MAY|SHOULD_NOT|MUST_NOT) / category / why / version_scope / confidence / source`；可选 `preferred / note / canonical_id`。
- **version_scope 用闭集枚举**，版本备注放独立 `note` 字段——下游按值精确匹配，备注混入主字段必漏检。
- confidence：high=≥2 独立来源、medium=1、low=仅第三方（禁用）。独立性归一化：同主版本同页快照（stable/latest/4.N）折叠为一个来源；跨主版本快照（3.x vs 4.x 同页）对版本差异主张算不同证据。
完成标准：契约（README 或注册表）落盘，schema 可被 `yaml.safe_load` 解析。

## Provenance

- source_skill_id: `SKILL-GEN-RULES-KNOWLEDGE-BASE`
- source_skill_path: `/home/ubuntu/.hermes/skills/software-development/rules-knowledge-base/SKILL.md`
- source_name: `rules-knowledge-base`
- original_section: `1. 先立契约，再填内容`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
