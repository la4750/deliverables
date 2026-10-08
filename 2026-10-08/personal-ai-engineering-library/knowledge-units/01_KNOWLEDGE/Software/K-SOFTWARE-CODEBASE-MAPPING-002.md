# K-SOFTWARE-CODEBASE-MAPPING-002 — Pitfalls

- **Domain**: Software / General | **Type**: Troubleshooting
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: medium | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-020（Agent Skill: codebase-mapping）| **Extracted**: 2026-10-08

## 知识正文

- **一次 grep 一个问题，扫全树**；按文件清单循环调 terminal 会瞬间烧掉几十次调用预算。
- **raw 进文件、汇总进上下文**：把提取结果整份读回来等于变相全树入上下文。
- **配对正则先看样本行**：对分段式结构化文本（场景文件、ini、config）先打印 2-3 行原始格式再写匹配；猜格式会静默失配（配对结果全为 `?` 却不报错）。
- **规则与实践分开报**：文档声明的做法与结构提取的实况冲突时两边都报，冲突本身是发现（标 NEEDS_VERIFICATION）。
- **清单式验收**：交付前逐项对照用户/规范给的完成清单（字段数、计数、警告），中英文标题混排时用逐字段程序核对，别靠肉眼扫 MD。

## Provenance

- source_skill_id: `SKILL-GEN-CODEBASE-MAPPING`
- source_skill_path: `/home/ubuntu/.hermes/skills/codebase-mapping/SKILL.md`
- source_name: `codebase-mapping`
- original_section: `Pitfalls`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
