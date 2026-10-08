# K-AI-NOVEL-DISPATCH — 断点续跑语义

- **Domain**: AI / AI | **Type**: Concept
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-022（Agent Skill: novel-dispatch）| **Extracted**: 2026-10-08

## 知识正文

**状态记录是唯一断点源，重启动时直接读 status.md 的 `## 当前章节进度` 段，不做 Glob 全量扫描（省 token）。**

**`章节状态` = 最近已完成的阶段**（子 agent order DONE 后才推进，dispatch 前不改）。判断用**严格大于 `>`**：状态 > 某阶段 = 已完成可跳过；**等值 = 该阶段未完成，需重派**。

| 阶段 | 已完成信号 | 判断 |
|------|-----------|------|
| setup | `setting-update-order` DONE 且 outputs 非空 | 不推进 phase——展示设定摘要等作者确认 |
| volume-planning | `章节状态 > volume-planning`；等值且 `volume-plan-order` DONE | `>` 成立 → 跳过；等值 DONE → 卷纲已写完待作者确认——重新展示卷纲摘要等确认，不重派 |
| chapter-planning | `章节状态 > chapter-planning`；等值且 `chapter-plan-order` DONE | `>` 成立 → 跳过；等值 DONE → 章纲已写完待作者确认——重新展示章纲摘要等确认，不重派 |
| prompt-crafting | `章节状态 > prompt-crafting` | 成立 → 跳过 |
| writing | `章节状态 > writing` | 成立 → 跳过 |
| anti-ai | `章节状态 > anti-ai` | 成立 → 跳过 |
| reviewing | `章节状态 > reviewing` | 成立 → 跳过 |
| archiving | `章节状态 > archiving` 或 `.done` 存在 | 成立 → 跳过 |

**状态更新规则（机械指令）**：某阶段子 agent order 标 DONE 后，才把 `章节状态` 更新为该阶段（= 已完成）。dispatch 进行中不改（当前阶段由 current_step 表达）。新章节开始重置状态。

**校正兜底（仅状态与实际明显冲突时）**：状态滞后（如状态=writing 但 `.draft.md` 已存在 → 实际完成）→ Glob 校验单文件并推进状态；状态超前（等值但产出缺失 → 实际未完成）→ 重派该阶段。不常态扫描。

**writer 中断恢复（唯一长输出阶段）**：读 `writing-order.md` 的 `partial_path:` 字段——有值且 `.draft.md` 不存在 →
重派 writer，order 带 `resume_from: {partial 路径}`，从 partial 已写到的段落续写，不整章重写。

**归档幂等**：`.agent/archiving/{chapter}.done` 存在 → 归档已完成，直接推进章节状态=全部完成，不重派。

## Provenance

- source_skill_id: `SKILL-AI-NOVEL-DISPATCH`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/novel-dispatch/SKILL.md`
- source_name: `novel-dispatch`
- original_section: `断点续跑语义`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
