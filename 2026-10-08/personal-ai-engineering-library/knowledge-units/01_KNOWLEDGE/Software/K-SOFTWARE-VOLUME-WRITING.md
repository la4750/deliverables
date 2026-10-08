# K-SOFTWARE-VOLUME-WRITING — volume-writing: 9. AI 味自检与去除

- **Domain**: Software / General | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-034（Agent Skill: volume-writing）| **Extracted**: 2026-10-08

## 知识正文

扫描卷纲全文，命中任一条 → 修改后重新检查，确认全部清除才算通过。

**模式一：空洞的冲突描述**
核心冲突或 chapter summary 用了形容词表态但没写具体事件。
- ❌ "展开精彩对决" → ✅ "陆征在废弃工厂与灰短袖男人对峙，对方掏出旧案卷宗要挟"
- ❌ "冲突激烈升级" → ✅ "方岩被上级停职，陆征失去警队内部信息源"
- 速查：全文搜"精彩""激烈""惊心动魄"——有 → 命中

**模式二："万能推进句式"**
不推进具体情节、只填充位置的万能句。
- ❌ "随着调查的深入，真相逐渐浮出水面"
- ❌ "在这个过程中，主角遇到了新的挑战"
- ❌ "故事开始朝着不可预测的方向发展"
- 速查：全文搜"随着""在这个过程中""与此同时"——有 → 命中

**模式三：预告片式语言**
像预告片一样勾勒气氛但不给事件。
- ❌ "更大的阴谋正在酝酿" → 谁在酝酿？酝酿什么？有行动吗？
- ❌ "命运的齿轮开始转动" → 哪件事触发了什么？
- 速查：全文搜"酝酿""拉开帷幕""命运的齿轮"——有 → 命中

**模式四：空洞的节奏填充词**
用来撑篇幅的节奏词，后文没有对应事件。
- ❌ "暗流涌动"（卷纲出现但不写涌动的内容）→ 必须写明谁和谁在对抗
- ❌ "波谲云诡"（同上）
- 速查：全文搜"暗流""波谲""扑朔迷离"——有 → 命中

**模式五：AI 自指 meta**
- ❌ "经过一系列的冒险"
- ❌ "故事的核心冲突在于"
- ❌ "我们接下来要讲述的是"
- 速查：全文搜"经过一系列""核心冲突在于""我们要讲述"——有 → 命中

## Provenance

- source_skill_id: `SKILL-GEN-VOLUME-WRITING`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/volume-writing/SKILL.md`
- source_name: `volume-writing`
- original_section: `9. AI 味自检与去除`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
