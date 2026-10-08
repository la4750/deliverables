# K-GENERAL-SHORT-VERIFY — 十项核对清单

- **Domain**: General / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-032（Agent Skill: short-verify）| **Extracted**: 2026-10-08

## 知识正文

| # | 项 | 判据 |
|---|----|------|
| 1 | 契约硬规则逐条 | 对照冻结契约不可违反规则区，逐条给出遵守/违反 + 原文证据 |
| 2 | 大纲子事件落地 | outline 每节每个子事件在正文有对应情节；缩水或缺失报出 |
| 3 | 情绪目标 | 对照 setting 四段情绪强度：实际成稿情绪位置是否达成 |
| 4 | 反转揭穿位置 | 实际揭穿节号 ÷ 总节数 = 契约承诺位置（±1 节内视为兑现） |
| 5 | 贯穿道具三次 | 出现三次且语义递进（无害→引注意→揭真相）完整 |
| 6 | 催化性失常 | 60-75% 位置存在矛盾体（题材标注不适用则跳过） |
| 7 | 人物前后一致 | 无与 setting 人设或动机矛盾的行动；前后行为逻辑自洽 |
| 8 | 对话逐句功能 | 每句标注功能（推动/性格/冲突/伏笔）；连续多句仅寒暄或衔接 → 不合格 |
| 9 | 字数与节数 | 总字数 ≥8000（机器复测）；每节达标；节数 = 大纲节数 |
| 10 | 标点禁令 | 禁用标点清零（机器扫描） |

## Provenance

- source_skill_id: `SKILL-GEN-SHORT-VERIFY`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/short/short-verify/SKILL.md`
- source_name: `short-verify`
- original_section: `十项核对清单`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
