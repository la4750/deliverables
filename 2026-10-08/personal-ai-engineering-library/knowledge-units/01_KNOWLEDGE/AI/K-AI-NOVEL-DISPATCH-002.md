# K-AI-NOVEL-DISPATCH-002 — 作者确认关卡（人铸灵魂，AI 行笔墨）

- **Domain**: AI / AI | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-022（Agent Skill: novel-dispatch）| **Extracted**: 2026-10-08

## 知识正文

设定、卷纲、章纲是故事的灵魂，AI 只负责笔墨。以下产出 order DONE 后**必须停下等作者确认**，未确认前不写下一步 order、不推进 step（与 setup 的确认语义同构）：

| 产出 | 确认动作 | 作者确认后 |
|------|---------|-----------|
| 设定（`setting-update-order.md` DONE） | 展示设定摘要（文件清单 + 世界观/题材/角色/文风要点） | phase→outline, step→volume-planning |
| 卷纲（`volume-plan-order.md` DONE） | 展示卷纲摘要（四幕结构/情绪走向/章数，日常语言） | step→chapter-planning |
| 章纲（`chapter-plan-order.md` DONE） | 展示章纲摘要（本章核心剧情/情绪节奏/钩子，日常语言） | phase→draft, step→prompt-crafting |

确认语义：

- 作者明确确认（"可以/没问题/就这样"）→ 推进；作者要改 → 重派对应 agent（order 内嵌修改意见）→ 改完再次展示确认（受重试/断路器约束）
- 作者回复模糊（"差不多""你看着办"）→ 一律视为未确认，追问具体哪项不确定
- 作者说"你全权写/别等确认"（全自动模式）→ 展示摘要后视为已确认直接推进；**单次有效**，下一关卡仍停（作者再说一次即再放行）
- **作者说"继续/推进"= 推进到下一个作者确认关卡即停**，不是推到底；正文流水线（提示词→正文→去AI味→验收→归档）属 AI 笔墨，确认章纲后可连续推进到归档后的重写/下一章询问

## Provenance

- source_skill_id: `SKILL-AI-NOVEL-DISPATCH`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/novel-dispatch/SKILL.md`
- source_name: `novel-dispatch`
- original_section: `作者确认关卡（人铸灵魂，AI 行笔墨）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
