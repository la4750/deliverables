# K-GENERAL-ART-BIBLE — art-bible: 阶段 0：解析参数和上下文检查

- **Domain**: General / Game Design | **Type**: Troubleshooting
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-008（Agent Skill: art-bible）| **Extracted**: 2026-10-08

## 知识正文

读取 `design/gdd/game-concept.md`。如果不存在，报错返回：
> "未找到游戏概念文档。请先完成游戏概念设定——艺术圣经在游戏概念通过后进行。"

从 game-concept.md 提取：
- 游戏标题
- 核心幻想和电梯演讲
- 游戏支柱（全部）
- 视觉身份锚点（如有）
- 目标平台

**改造模式检测**：检查 `design/art/art-bible.md` 是否存在。如果存在：
- 完整读取
- 对每个章节检查是否有实际内容或仅为占位符
- 构建章节状态表展示给用户
- 只处理"空"或"占位符"的章节，不重写已完成内容

如果文件不存在，正常开始全新创作。

检查项目配置中的性能预算和引擎约束。

---

## Provenance

- source_skill_id: `SKILL-GAME-ART-BIBLE`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/Agent/art-series/skills/art-bible/SKILL.md`
- source_name: `art-bible`
- original_section: `阶段 0：解析参数和上下文检查`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
