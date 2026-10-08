# K-SOFTWARE-NOVEL-REVIEW — 维度 5：写作风格执行度（对照 settings/writing-style.md）

- **Domain**: Software / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-013（Agent Skill: novel-review）| **Extracted**: 2026-10-08

## 知识正文

> 对照 writing-style.md 对应字段逐条检查。AI 味相关的硬性检测（疲劳词、句式癖好）见 anti-ai.md，本维度聚焦内容层面的风格执行。

| # | 细项 | 对照字段 | 检查要点 |
|---|------|---------|---------|
| 5.1 | 客观叙事原则 | `core_principles.global_rules[0-4]` | 有无道德化、合理化、回避负面？ |
| 5.2 | 让故事自己说话 | `core_principles.global_rules[2]` | 有无作者跳出来评论/总结/升华？摘出违规句 |
| 5.3 | 禁用诗词腔 | `core_principles.global_rules[7]` | 空洞文艺词、四字成语连用、排比古风句？ |
| 5.4 | 行文逻辑连续 | `core_principles.global_rules[8]` | 跳场景/跳时间/跳心理的断层？ |
| 5.5 | 线性叙事遵守 | `core_principles.global_rules[9]` | 插叙？突然切视角？ |
| 5.6 | 叙事顺序正确 | `core_principles.global_rules[10]` | "动作→神态→开口→内心"顺序是否遵守？ |
| 5.7 | 句式规则执行 | `natural_expression[4-7]` | 短句节奏切断？长复合句连续？单段超过 5 行？ |
| 5.8 | 句式开头多样性 | `natural_expression[6]` | 相邻 4 句相同代词/连词开头？ |
| 5.9 | 形容词副词控制 | `natural_expression[2]` | 公式化副词（不由得/不禁/忍不住/下意识地）？ |
| 5.10 | 环境描写占比 | `natural_expression[3]` | 单段是否超过 2 行？是否用作剧情转折点？ |
| 5.11 | Show Don't Tell | `description_vs_depiction` | 直接描述感受的句子（"她很伤心"）？摘出违规句 |
| 5.12 | 俗套比喻检查 | `description_vs_depiction[1]` | 俗套比喻（眼泪像珍珠/心像刀割）？ |
| 5.13 | 角色塑造原则 | `character_building` | 通过行动和选择塑造？角色弧光？多角色占比平衡？ |
| 5.14 | POV 一致性 | `pov_consistency` | 视角跳跃？"他注意到""他意识到"解释性过渡？ |
| 5.15 | possible_mistakes 扫描 | `possible_mistakes[]` | 逐条对照，触犯 → 摘原文 + 对应禁项 |
| 5.16 | 描写技法运用 | `depiction_techniques[]` | 5 种技法是否自然使用不刻意？ |
| 5.17 | 读者心理学遵守 | `reader_psychology` | 期待管理/信息不对称/情绪节奏/锚定/沉没成本？ |
| 5.18 | 欲望引擎驱动 | `desire_engine` | 压制→期待释放/信息缺口→期待揭晓/关系张力→期待突破？ |
| 5.19 | 代入感六支柱 | `immersion_pillars[]` | 标签化/熟悉感/共鸣/欲望/五感钩子/反差细节？ |
| 5.20 | 创作宪法执行 | `creative_constitution[]` | 逐条检查。智商在线？日常七成为伏笔？关系改变有事件驱动？ |
| 5.21 | 题材特定规则 | `genre` | pacing_rules？题材疲劳词？反套路规则？ |
| 5.22 | 六步人物心理 | `character_psychology_method.steps[]` | 处境→动机→信息边界→性格→选择→情绪外化是否可回溯？ |

## Provenance

- source_skill_id: `SKILL-GEN-NOVEL-REVIEW`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/review/SKILL.md`
- source_name: `novel-review`
- original_section: `维度 5：写作风格执行度（对照 settings/writing-style.md）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
