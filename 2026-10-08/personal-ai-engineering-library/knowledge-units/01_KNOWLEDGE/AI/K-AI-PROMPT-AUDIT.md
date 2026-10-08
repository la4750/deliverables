# K-AI-PROMPT-AUDIT — 维度 H：规则去重（硬门禁）

- **Domain**: AI / AI | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: medium | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-001（Agent Skill: prompt-audit）| **Extracted**: 2026-10-08

## 知识正文

**目的：** 确保 prompt 里同一语义只出现一次，没有从多源（writing-style / anti-ai / scene-craft / genre-example）带进来的重复规则。这是"组装后去重检查"（prompt-crafting.md Step 2）的核验——组装流程要求了，但需要独立视角确认做到了没有。

**步骤：**
1. 通读 prompt 全文，提取所有带约束性质的规则（数量线、禁止项、阈值、硬性要求）
2. 对每条规则，追问：这个语义在 prompt 其他位置是否已经出现过？
3. 按类别归并：跨源重复 / 数量线重复

**检查表：**

| 检查项 | PASS 标准 | FAIL 信号 |
|--------|-----------|----------|
| 跨源重复 | 同一约束（对话密度/破折号/字数等）全 prompt 只出现一次 | 同一规则在写作规范、场景指引、质感要求里各出现一次 |
| 数量线重复 | 同一对象只有一处定义（如"对话≤8句"只在反 AI 注入处出现一次） | 同一数量线在反 AI 注入和场景方法论里各写一遍 |

**判定标准：**
- 任一重复 → **FAIL**（打回时指出哪两条是同一件事，建议合并哪条）
- 全部唯一 → **PASS**

**操作判据（硬门禁必须可判定）：**

判为重复（FAIL）的两种情形——
1. **同一格式重复**：同一对象被同一格式定义了两次（数量线/阈值/禁止项完全重复，如"对话≤8句"出现两次）
2. **完全重复**：两条规则措辞几乎一致，指同一件事，无信息增量

不判为重复（有效冗余，不算 FAIL）的情形——
- **措辞不同的等价约束**："对话要短"+"纯台词不超8句"+"少让角色长篇"指向同一件事但各有侧重（一个给原则、一个给数量、一个给反例）→ 是有效冗余，保留。审计只要求**同一格式的完全重复**被合并，不要求所有语义等价约束合并成一条。

## Provenance

- source_skill_id: `SKILL-AI-PROMPT-AUDIT`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/prompt-audit/SKILL.md`
- source_name: `prompt-audit`
- original_section: `维度 H：规则去重（硬门禁）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
