# K-SOFTWARE-NOVEL-OUTLINE — novel-outline: 2.2 拆章节 + 填冲突载体

- **Domain**: Software / General | **Type**: Concept
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-030（Agent Skill: novel-outline）| **Extracted**: 2026-10-08

## 知识正文

以上一步确认的模板各阶段（首卷）或角色发声推导的冲突路径（卷 N+1）为骨架，逐章填充。

| 字段 | 标准 | 不合格示例 |
|------|------|-----------|
| id | "卷号-章号"（如 1-1），连续不跳号 | 1-1, 1-3（跳了 1-2） |
| title | 有信息量，能猜到本章核心事件 | "第一章""新的开始""转折" |
| summary | **三要素：谁做什么 + 冲突事件 + 结束时什么变了** | "主角继续调查"（什么都没变） |

**4 种不合格章纲，必须检测并修正：**

| 类型 | 典型句式 | 修正方向 |
|------|---------|---------|
| **主题式** | "本章讲信任"（无事件） | 把概念变成具体事件：谁在什么事上信任了谁 |
| **功能式** | "建立人物关系"（功能=展示，不是推进 | 把功能折入冲突事件：通过某件事来建立 |
| **梗概式** | "主角经历了一天的冒险"（无具体冲突点） | 指认一天里最核心的一件事 |
| **结果式** | "主角赢了比赛"（只有结果无过程） | 写出阻碍和对抗：怎么赢的、过程中遇到什么 |

**章节间必须存在因果链：** 前一章的章末变化是后一章的起点或动机。各章独立不递进 = 故事没有在推进。

## Provenance

- source_skill_id: `SKILL-GEN-NOVEL-OUTLINE`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/outline/SKILL.md`
- source_name: `novel-outline`
- original_section: `2.2 拆章节 + 填冲突载体`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
