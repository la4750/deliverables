# K-AI-NOVEL-PROMPT — novel-prompt: Step 2: 按指南填充 9 层

- **Domain**: AI / AI | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-012（Agent Skill: novel-prompt）| **Extracted**: 2026-10-08

## 知识正文

Read `references/prompt-setting-style.md`，按以下顺序填充：

1. **L1 元信息** — 从 writing-style.md + chapter.md 提取：题材/风格/字数/本章角色/模型
2. **L2 来龙** — 从 volume.md 前章摘要提取：结尾画面/情绪残留/缺口。**只读摘要，不读全文**
3. **L3 去脉** — 从 chapter.md memo 提取：核心悬念/悬念状态/读者感受
4. **L4 角色弧光** — 从 chapter.md 人物状态 + 角色文件提取：每角色起点→转折→落点 + 微习惯
5. **L5 场景序列** — 从 chapter.md outline 提取：
   - 按边界信号（换地点/跳时间/情绪转折）切分场景（2-4 个）
   - 每场景填种子三字段（入口画面/核心事件/出口画面）+ 情绪拐点
6. **L6 约束** — 从 chapter.md memo 提取：情节红线（2-4 条）+ 边界禁止 + 角色禁区
7. **L7 爽点设计** — 从 chapter.md memo 提取：类型/铺垫位置/释放位置/释放方式 + 克制点
8. **L8 文字规则** — 组装以下内容写入 L8 各字段：
   - 视角：从 genre-example `prompt_segment` 提取视角字段（如"第三人称限制"）
   - 描写要求：从 genre-example `prompt_segment` 提取描写手法/节奏/禁止项
   - 疲劳词阈值：从 anti-ai/common-rules.md 表一复制（如"突然≤3/章"）
   - 句式规则：从 anti-ai/common-rules.md 表二复制（如"连续4句主语不得相同"）
   - 元叙事禁止：从 anti-ai/common-rules.md 表三复制（如"禁止'读者'"）
   - 题材正反例：从 anti-ai/{genre}.md 复制（如存在）
   - **必须填入具体内容，不只是标注来源**
9. **L9 质感** — 从 chapter.md memo + 作者补充提取：无用细节/对话节奏/真人痕迹

**冲突检测：** 填完后检查 L2 情绪残留 = L4 第一角色起点、L7 释放位置在 L5 场景中存在。

全部填完后全局通读一次——掩住字段名，看每个种子读起来是叙事画面还是写作指令。

**[Checkpoint]** 展示完整提示词给作者确认，确认后保存。

## Provenance

- source_skill_id: `SKILL-AI-NOVEL-PROMPT`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/prompt/SKILL.md`
- source_name: `novel-prompt`
- original_section: `Step 2: 按指南填充 9 层`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
