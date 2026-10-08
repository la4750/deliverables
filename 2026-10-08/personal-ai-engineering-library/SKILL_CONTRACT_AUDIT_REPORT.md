# SKILL_CONTRACT_AUDIT_REPORT — 三级 Contract 完整性审计报告

> **本阶段严格 READ-ONLY。** 未删除/合并/重命名/移动/重写任何 Skill；未迁移 Knowledge、未创建 Capability、
> 未执行任何 Migration/Merge Proposal；未修改 Phase 0–8 Foundation、Protocol/Schema/Lifecycle/Governance、
> 未执行任何 Foundation Change Proposal。本轮仅新增两份审计产出（本报告 + `SKILL_CONTRACT_AUDIT.yaml`）。
>
> 日期：2026-10-08｜覆盖：**358/358 逻辑技能，全量无抽样**｜机读结果：`SKILL_CONTRACT_AUDIT.yaml`

---

## 1. 审计输入与方法

输入 9 项：SKILL_INVENTORY.yaml、SKILL_CLASSIFICATION.yaml、Registry/SKILL_REGISTRY.yaml、SKILL_INDEX.md、
SKILL_RULES.md、SKILL_OVERLAP_REPORT.md、SKILL_OPTIMIZATION_REPORT.md、SKILL_MIGRATION_PROPOSALS.yaml、
**实际 SKILL.md 文件**（每个技能重新读取正文做字段级判定，不依赖上一阶段的自评结论）。

## 2. 跨文件一致性与文件核对（先审 Registry 自身）

| 检查 | 结果 |
|---|---|
| Registry / Classification / Proposals / Index 条目数 | 358 / 358 / 358 / 358 ✅ |
| 四者 skill_id 集合一致、无重复 | ✅ |
| Inventory 文件数 | 430（与 358 逻辑技能 = 72 副本关系吻合）✅ |
| `canonical_path` 实际存在 | **358/358 ✅**（注册表无死链） |
| 正文 frontmatter `name` 与登记名一致 | **358/358 ✅** |
| 正文 `description` 与登记描述一致 | **358/358 ✅** |
| `version` 元数据 | **134 个 unknown**（历史文件本无版本字段，如实登记不伪造）⚠️ |

**结论：Registry 本身结构健康，无 ID 漂移、无路径失效、无登记失真。**

## 3. Contract Level 判定规则

**required（本阶段裁定）：**

| Level | 适用 | 数量 |
|---|---|---|
| L1 | 全部技能的底线；嵌套子技能（父包路由承担匹配）与第三方依赖技能到此为止 | 59 |
| L2 | 非嵌套、需任务匹配的独立技能（工具/知识/元/小型流程/项目专属） | 181 |
| L3 | 非嵌套 `WORKFLOW_SKILL`/`AGENT_WORKFLOW` 且正文 ≥2.5KB（复杂工程工作流） | 118 |

**N/A 政策**：TOOL_WRAPPER / KNOWLEDGE_WRAPPER 的 `required_knowledge`、`required_capabilities` 允许 N/A；
不为完整度虚构字段——**缺就记缺，有才记有**。

**current 判定**：L3 = workflow 结构 + validation + failure_handling（硬三件）齐；L2 = L1 齐 + 触发/输入/输出 +
（知识与能力声明，或该类允许 N/A）+ compatible_agents/dependencies/constraints 齐；L1 = 注册字段齐。

## 4. 总体结果

```yaml
contract_level_required: { L1: 59,  L2: 181,  L3: 118 }
contract_level_current:  { L0: 1,   L1: 357,  L2: 0, L3: 0 }
contract_gap:            { true: 299, false: 59 }
```

- **299/358（83.5%）存在 Contract Gap**；59 个无缺口 = 全部是 required L1 的嵌套子技能(57)与第三方依赖(2)。
- **没有任何技能达到 L2 现状水平**——L2 是合取判定，`compatible_agents` 一项即 358/358 全缺。
- 分布核对：按域 Game 61/87、AI 75/81、Automation 22/22、General 141/168；按来源 user_installed 24/81、
  bundled_core 46/46、bundled_optional 150/150、plugin 3/3、legacy 76/76、third_party 0/2（合计 299 ✅）。

## 5. 分项达成度（部分分——修复排序依据，不改变等级判定）

| 分项 | 达成 |
|---|---|
| 触发/适用（L2 核心①） | 230/358（64%） |
| inputs（L2 核心②） | 87/358（24%） |
| outputs（L2 核心③） | 48/358（13%） |
| **触发+输入+输出三全** | **8/358（2%）** |
| workflow 结构（L3 硬①） | 177/358；在 118 个 L3-required 内 70 |
| validation 表述（L3 硬②） | 157/358；L3-required 内 59 |
| failure_handling 表述（L3 硬③） | 132/358；L3-required 内 54 |
| **硬三件全** | **34/358（9.5%）** |

## 6. 最缺字段排行（全量）

| 字段 | 缺 | 层级 |
|---|---|---|
| compatible_agents | 358 | L2 |
| runtime/interface requirements | 351 | L3 |
| known_limitations | 326 | L3 |
| version_scope | 321 | L3 |
| outputs | 310 | L2 |
| risk_level | 286 | L3 |
| constraints | 279 | L2 |
| inputs | 271 | L2 |
| failure_handling | 226 | L3 |
| validation_requirements | 201 | L3 |
| required_knowledge / required_capabilities / dependencies | 各 200 | L2 |
| workflow 结构 | 181 | L3 |
| trigger/applicability | 128 | L2 |

## 7. 例外与异常清单

- **L1 未达标 1 个**：`SKILL-AI-SELF-IMPROVING-AGENT`——description 为空（三个同名版本中的空描述版）。
  → L0，本阶段只记录，不修改。
- **name/description 与正文不一致：0**；**canonical_path 死链：0**。
- **version unknown 134**：集中在历史遗产与部分上游技能（文件本无版本字段）——按"不伪造"如实登记。
- 三个同名异容簇（github / tencent-docs / self-improving-agent）在 Contract 视角下**各自独立判级**，
  与重叠报告的 MERGE_CANDIDATE 建议互不干扰（合并与否是后续提案的事）。

## 8. 关键发现

1. **注册层健康，契约层空心**：Registry 自身 100% 通过一致性与文件核对；但操作契约（L2）与工程契约（L3）
   在历史语料中基本不存在——`SKILL_RULES §7` 早已预言：compatible_agents/required_* 等字段在 REVIEWED
   阶段才补齐，当前 `not_assessed` 是**分阶段的既定状态**，不是登记失误。
2. **L2 缺口的 84% 由 4 个字段解释**（compatible_agents / inputs / outputs / constraints）——补齐它们，
   L2 达成率即可从 0% 大幅抬升；TOOL/KNOWLEDGE 类按 N/A 政策更可快速达标。
3. **L3 只应覆盖 118 个复杂工作流**（167 个 WORKFLOW 中 49 个正文过小或为嵌套组件，被正确排除）——
   不对 TOOL_WRAPPER、简单 META、KNOWLEDGE_WRAPPER 强制升级，符合任务书要求。
4. **上游捆绑技能（B1/B2 196 个）缺口全量存在但不可治理**：其源在 Hermes 上游仓库，个人侧只能登记引用
   ——建议在 REVIEWED 阶段将其 required 级别实际按 L1/N-A 处理（本阶段不改动判定，仅提出）。
5. 结构性优势：`workflow` 结构已有 177/358——历史技能"有流程没契约"，补声明比从零写流程便宜得多。

## 9. 后续修复建议（均为提案，本阶段不执行）

| 优先级 | 范围 | 动作 |
|---|---|---|
| P0 | 1 个 L0 | 补 description（最小 L1 修复） |
| P1 | 350 个缺触发/输入/输出 | L2 核心三件补声明（个人层 A/D 优先，上游层只记录） |
| P2 | compatible_agents 358 | REVIEWED 阶段结合真实使用评估填 Role 映射 |
| P3 | 118 个 L3-required | 硬三件（workflow/validation/failure）补齐 → 再补 risk/version_scope/limitations |
| — | 上游 196 | 标记为 reference-only，不参与个人契约考核（需 SKILL_RULES 修订 → 属协议变更，走审批） |

## 10. READ-ONLY 声明

本轮产出仅两件：`SKILL_CONTRACT_AUDIT.yaml`（机读，358 条逐技能 `contract_level_required / current / gap / reason`）
与本报告。**既有 8 份交付物、358 个技能文件、Phase 0–8 全部未被触碰**（可由 `git status --short` 复核：
`Skills/` 下仅新增这两个文件）。
