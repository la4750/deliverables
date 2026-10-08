# K-AI-PROMPT-AUDIT-002 — 维度 F：去 AI 校验（新增核心维度）

- **Domain**: AI / AI | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-001（Agent Skill: prompt-audit）| **Extracted**: 2026-10-08

## 知识正文

**目的：** 确保 prompt 从根源上抑制 AI 均匀工整的写作惯性。

**检查表：**

| 检查项 | PASS 标准 | FAIL 信号 |
|--------|-----------|----------|
| 技法稀疏使用 | 每个场景类型只注入 1-2 条技法，未要求全覆盖 | 要求每个场景类型使用 ≥ 3 条技法或"全部技法" |
| 主次区分 | 输出·写作规范明确要求主次笔墨区分（高权重复、低权重简） | 无任何主次区分规则，暗示"均匀描写" |
| 四步执行逻辑 | 输出·写作规范包含焦点锁定/感官分层/节奏交替/信息控制四条 | 缺失其中 2 条及以上 |
| 不完美约束 | 质感要求包含半截话/生活化细节/段落精度分层 | 无任何"不完美"约束 |
| 禁止均匀堆砌 | 有明确指令禁止全维度感官堆砌、等长段落、成套修辞 | 无相关禁止项 |
| 温感平衡 | prompt 不要求极端碎片化（无"独句段占比不低于X%"类硬性指标） | prompt 要求独句段≥25%或"强制硬切" |

**判定标准：**
- 6 项全部 PASS → **PASS（去 AI 设计完整）**
- 4-5 项 PASS → **WARN（建议补充缺失项）**
- ≤ 3 项 PASS → **FAIL（严重去 AI 缺陷）**

## Provenance

- source_skill_id: `SKILL-AI-PROMPT-AUDIT`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/prompt-audit/SKILL.md`
- source_name: `prompt-audit`
- original_section: `维度 F：去 AI 校验（新增核心维度）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
