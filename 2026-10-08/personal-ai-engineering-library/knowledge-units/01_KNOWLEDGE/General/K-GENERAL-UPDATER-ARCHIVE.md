# K-GENERAL-UPDATER-ARCHIVE — 二、归档前检查

- **Domain**: General / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-033（Agent Skill: updater-archive）| **Extracted**: 2026-10-08

## 知识正文

| 检查项 | 操作 |
|--------|------|
| 正文草稿存在？ | `archives/vol-{N}-ch-{M}-*.draft.md` 存在？缺失→**STOP**，正文尚未生成 |
| chapter.md 完整？ | memo + emotional_design 有值？缺失→返回补章纲 |
| chapter.md#status 为 outline？ | 归档成功后改为 archived（见 Step 1 末尾）；已是 archived → 说明重复归档，进幂等模式 |
| `.agent/archiving/{chapter}.done` 存在？ | **存在 → 本章已归档过，进入幂等模式：跳过已完成步骤，只补缺失项**（见下"幂等规则"） |

## Provenance

- source_skill_id: `SKILL-GEN-UPDATER-ARCHIVE`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/updater-archive/SKILL.md`
- source_name: `updater-archive`
- original_section: `二、归档前检查`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
