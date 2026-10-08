# K-GENERAL-NOVEL-CHAPTER — e. 验收（章纲完成后强制执行，全部通过才进提示词生成）

- **Domain**: General / General | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-011（Agent Skill: novel-chapter）| **Extracted**: 2026-10-08

## 知识正文

详见 `references/chapter-setting-style.md#做完之后验收流程`。以下为 SOP 摘要：

**第 1 步：给作者看 structured 反馈**

按以下格式展示，不要丢原文：

```
📋 第{N}章 章纲反馈

本章定位：{一句话}
主要内容：{2-3 句}

关键场景：
- {title}（角色：{人物列表}）
- ...

冲突进展：{推进了什么}
字数目标：{N} 字
```

作者必须明确说"对"才算合格。"差不多""你看着写"不算通过。

**第 2 步：检查清单自检**

24 项详见指南 checklist。以下为高频必检项：

- [ ] 字数目标已确认（4000+）
- [ ] 段落分布已确认（推进/过渡/埋伏笔各几段）
- [ ] 每条 key_point 对应一个可写场景，含冲突事件
- [ ] 旧钩子兑现/新钩子埋下已记录
- [ ] 硬约束（prohibitions）每条可验证
- [ ] 情绪走向至少三个节点（A→B→C）

**第 3 步：快速嗅探**

遮住章纲能不能说出：
- 分多少条、每条写什么场景
- 每个角色知道什么、不知道什么
- 兑现了哪些旧钩子、新埋了什么钩子

**第 4 步：AI 味自检**

| # | 检测项 | 扫描字段 | 命中模式 |
|---|--------|---------|---------|
| 1 | 上帝视角概述 | outline、memo.current_task | "本章讲述了""主角经历了""本章将展示" |
| 2 | 抽象心理总结 | memo.reader_expectation、memo.key_choices | "他感到""他意识到""他内心挣扎" |
| 3 | 分析性结论 | memo.reader_expectation、memo.required_changes | "这表明""这意味着""这标志着关系转折" |
| 4 | 文学评论腔 | outline、memo.current_task | "通过X展现了Y""完成角色弧光转折" |
| 5 | "不是而是"句式 | 所有字段 | "不是X，而是Y" |
| 6 | 抽象标签 | memo.current_task、memo.required_changes | "关系递进""冲突升级"——应写具体事件 |

**作者确认章纲后：**
- 写入 `chapters/vol-{N}-ch-{M}.md`，status → `outline`

## Provenance

- source_skill_id: `SKILL-GEN-NOVEL-CHAPTER`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/chapter/SKILL.md`
- source_name: `novel-chapter`
- original_section: `e. 验收（章纲完成后强制执行，全部通过才进提示词生成）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
