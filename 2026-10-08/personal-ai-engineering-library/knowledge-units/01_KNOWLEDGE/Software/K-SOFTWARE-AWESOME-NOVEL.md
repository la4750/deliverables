# K-SOFTWARE-AWESOME-NOVEL — 各阶段文件读取指南

- **Domain**: Software / General | **Type**: Procedure
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-040（Agent Skill: awesome-novel）| **Extracted**: 2026-10-08

## 知识正文

每个子步骤按"写什么文件 → 读什么参考 → 可选的参考阅读"来准备。读完一份，再看下一份。

| 子步骤 | 写什么文件 | 必读的参考 | 参考阅读 |
|--------|---------|--------------|---------|
| **1.1 新建项目** | 项目骨架 + `story.md` | `scripts/init.py`（创建骨架） | — |
| **1.2 题材选择+风格** | `settings/genre-setting.md`<br>`settings/writing-style.md`（预填） | `references/genre-style.md`（选题指南+验收） | `references/genre-example/` 对应类型（配置参考） |
| **1.3 世界观** | `settings/world-setting.md` | `references/world-setup-style.md`（引导讨论+自检） | — |
| **1.4 角色** | `settings/character-setting/<id>.md` | 已有角色文件（追加时不覆盖）<br>`references/character-setting-style.md`（认知6层+自检） | — |
| **2.0 主线拆纲** | `story.md#story_arc`（主线+分卷） | `references/story-arc-style.md`（从结局倒推法） | `settings/world-setting.md` core（冲突空间参考）<br>角色文件（按需看动机） |
| **2.1 卷纲** | `volumes/volume-{N}.md`（章节列表） | `references/volume-setting-style.md`（指南+自检） | — |
| **3.1 章纲** | `chapters/vol-{N}-ch-{M}.md` | `volumes/volume-{N}.md#chapters_summary`（卷纲给的本章方向）<br>`references/chapter-setting-style.md`（指南+自检） | — |
| **3.2 提示词** | `prompts/vol-{N}-ch-{M}-prompt.md` | `references/prompt-setting-style.md`（提示词指南+模板） | — |
| **3.2a 提示词验收**（主流程独立执行） | `prompts/vol-{N}-ch-{M}-prompt.md`（检查对象） | `references/prompt-setting-style.md` Section 三（验收标准） | — |
| **3.3 正文生成** | `archives/vol-{N}-ch-{M}-*.draft.md` | `prompts/vol-{N}-ch-{M}-prompt.md`（单一入口） | `skills/write/SKILL.md`（SOP） |
| **3.3a 正文验收**（主流程独立执行） | `archives/vol-{N}-ch-{M}-*.draft.md`（检查对象） | `references/chapter-quality-checklist.md`（验收标准） | — |
| **3.4 深度评审**（可选） | 诊断报告（内存） | `skills/review/SKILL.md` | — |
| **3.5 归档** | `archives/vol-{N}-ch-{M}-*.md`（去 draft）<br>`chapters/vol-{N}-ch-{M}.md`（status→archived）<br>角色状态追加 + `status.md` 更新 | 各角色文件（追加状态历史+情绪弧线） | 最近 3 章 `chapters/`（回顾最近章节）；`memory/`（记忆晋升兜底） |

## Provenance

- source_skill_id: `SKILL-GEN-AWESOME-NOVEL`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/Agent/scholar-series/skills/awesome-novel/SKILL.md`
- source_name: `awesome-novel`
- original_section: `各阶段文件读取指南`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
