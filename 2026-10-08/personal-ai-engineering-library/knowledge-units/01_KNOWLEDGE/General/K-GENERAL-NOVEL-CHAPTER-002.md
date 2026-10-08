# K-GENERAL-NOVEL-CHAPTER-002 — 主 agent 汇总 + 仲裁

- **Domain**: General / General | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-011（Agent Skill: novel-chapter）| **Extracted**: 2026-10-08

## 知识正文

收到四份报告后，主 agent **不自己读文件补充**，直接基于四份报告输出规划草案。

**仲裁规则：**

| 优先级 | 规则 | 说明 |
|--------|------|------|
| 1 | 架构 > 情节 | 钩子兑现是硬约束，情节逻辑不得违背钩子路径 |
| 2 | 架构 > 读者 | 必须兑现的钩子优先于读者期待的 micro_payoff |
| 3 | 情节 > 情绪 | 角色情绪不能与情节逻辑冲突——先有行动再有情绪 |
| 4 | 超出以上规则的冲突 | 标注【冲突】+ 两个 agent 的观点 → 提交作者仲裁 |

冲突报告格式：
```
【冲突】{agent A} vs {agent B}
- {agent A}：[内容]
- {agent B}：[内容]
→ 等待作者裁定
```

## Provenance

- source_skill_id: `SKILL-GEN-NOVEL-CHAPTER`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/chapter/SKILL.md`
- source_name: `novel-chapter`
- original_section: `主 agent 汇总 + 仲裁`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
