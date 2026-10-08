# Skill Integration Design — Personal AI Engineering Library
## Agent Skill 与现有 0–8 架构共存的设计与架构审查结果

**状态：DRAFT — 待人工批准。本文件是设计交付物，未修改 Library 内任何文件。**
审查基准：本地克隆 `~/personal-ai-engineering-library`，HEAD = `ec5f983`（Phase 8 落盘提交，即已推送 11 个分阶段 commit 的末笔），工作区干净。
（注：审查时 `git pull` 因非交互环境凭据提示失败，未能确认远端是否有更新提交；如远端有新推送，落地前需重新核对。）

约束遵守声明：
- 未修改 Phase 0–8 基础架构，未新增 Phase，未动 Foundation Constitution、Registry 协议、生命周期模型、治理规则。
- 本文档全部产出为**设计 + 审查 + Foundation Change Proposal 草案**；所有库内写入动作（目录、Schema、Registry、FCP 登记）均列在 §20 决策点，等人工批准后执行。

---

## 0. 检查清单（任务项 1–2）

### 0.1 已检查的 0–8 架构文件

| 文件 | 检查要点 |
|---|---|
| `00_CORE/PHASE_0_FOUNDATION_CHARTER.md` | Foundation/Content 边界、变更流程（§2）、AI 权限（§3）、治理（§4） |
| `LIBRARY_RULES.md` | §2 实体模型（10 类）、§4 不混淆表、§9 安全、§11 生命周期标准化 + 类型映射表 |
| `VERSION_POLICY.md` | 语义化版本、状态跃迁版本影响、§6 依赖版本记录 |
| `CAPABILITY_SPEC.md` | §4 Capability 状态机、§5 Interface 七要素、§6 Capability↔Implementation 可替换规则 |
| `PHASE_ROADMAP.md` | 八阶段总纲 + 执行红线 |
| `05_DECISION/RETRIEVAL_DECISION_SPEC.md` | §五 检索资源清单、§七 基于 Interface 检索、§二十七～三十 边界、§三十七 禁止事项 |
| `12_TESTING_VALIDATION/EXECUTION_VALIDATION_SPEC.md` | §二十一～二十三 与其他阶段连接、§二十六 状态机、§二十九 禁止事项 |
| `14_AI_AGENTS/AGENT_ORCHESTRATION_SPEC.md` | §五 Agent Capability、§八 Agent Selection、§二十九～三十一 边界、§三十二 目录契约、§三十四 接口、§三十七 禁止事项 |
| `00_CORE/Evolution/EVOLUTION_RULES.md` | §一 Foundation/Content 表、§三 演化来源 14 类、§五 检测对象 12 类、§六 各对象演化规则、§八 20 种提案类型、§九 FCP 流程、§十六 边界 |
| `00_CORE/Evolution/FOUNDATION_CHANGE_PROPOSALS.yaml` | FCP schema（§30）与审批状态机（§31）——本次草案按此格式撰写 |
| `15_EXTERNAL_RESOURCES/EXTERNAL_RESOURCE_SPEC.md` | 资源类目含 `Agent Skill`（唯二处 "Skill" 字样之一） |
| `09_CAPABILITIES/Registry/*`、`01_KNOWLEDGE/_REGISTRY/*` | Registry 惯例、真实 capability/knowledge ID |
| `14_AI_AGENTS/{Registry,orchestration,policies,runtime,tools}` | 9 角色、11 Schema、RUNTIME_INTERFACE 10 方法、validate_agent.py |

**全库 `Skill` 检索结果：仅 1 处**——`EXTERNAL_RESOURCE_SPEC.md:29` 把 `Agent Skill` 列为外部资源类目。即：**Skill 概念在库内尚不存在**，本次是全新引入，无历史包袱，但也意味着没有现成承载结构。

### 0.2 14_AI_AGENTS 现状

```
14_AI_AGENTS/
├── AGENT_ORCHESTRATION_SPEC.md   (§1–37, Foundation)
├── Registry/    AGENT_REGISTRY(空) + AGENT_ROLES(9 角色) + AGENT_PERMISSIONS + AGENT_LIFECYCLE
├── orchestration/  11 Schema（无任何 Skill Schema）
├── policies/  runtime/  tools/  PHASE_7_AUDIT.md
└── Master_/Knowledge_/Coding_/Robotics_/CAD_/Manufacturing_/Game_/Testing_/Asset_Agent/  (README 角色指针)
```

结论：**没有适合 Skill 的现成位置**。候选只有三种：(甲) 14_AI_AGENTS 下新建 `Skills/`；(乙) 顶层新建编号目录；(丙) 塞进 05_DECISION / 09_CAPABILITIES（语义不符，排除）。详见 §15。

---

## 1. 四概念区分（任务项 3 的前提）

| 概念 | 回答 | 权威位置 | 实体形态 |
|---|---|---|---|
| **Knowledge** | 我知道什么？ | `01_KNOWLEDGE/`（Phase 4 管理） | 理解、原理、约束 |
| **Capability** | 我能做什么？ | `09_CAPABILITIES/`（Phase 2 Registry + Interface） | 命名的、可复用的能力接口 |
| **Skill** | 面对这个任务，我应该怎么做？ | **待建** `SKILL_REGISTRY`（本次设计） | 任务工作方法/流程/策略/操作规范 |
| **Agent** | 谁来做？ | `14_AI_AGENTS/`（Phase 7 管理） | 运行主体（Role + Instance） |

**Skill 的定位：Content / Implementation 层的可复用工作流资源**，不是 Foundation，不是新 Phase，不是第五种"能力"，不是运行主体。

一句话判据：
- 把方法**写进** Skill → 合法（这是 Skill 的本体）。
- 把**知识**写进 Skill 当唯一来源 → 违规（那是 Knowledge 的家）。
- 把**能力实现**抄进 Skill → 违规（那是 Implementation 的家，且绕过 Capability Registry）。
- 把**选择/委派/通信**写进 Skill → 违规（那是 Phase 7 的家）。

---

## 2. Skill Integration Architecture（任务项 4）

### 2.1 总体闭环

```
User Task
   ↓
Agent（Phase 7 选定的运行主体）
   │  ① 查 SKILL_REGISTRY："当前任务 / 当前 Agent 有哪些 Skill 可用？"（§2.2 接口 Q1/Q2）
   ↓
Skill（选定的工作方法；只带"何时需要什么"的声明，不带知识本体与能力实现）
   ↓
Phase 5 Retrieval & Decision（照常执行，不被取代）
   │  按 Skill 的 required_knowledge / required_capabilities / inputs / constraints
   │  → Candidate Retrieval → Filtering → Ranking → Decision → Execution Plan
   ↓
Knowledge（Phase 4）/ Capability Interface → Implementation（Phase 2）/ Asset / Template
   ↓
Phase 6 Execution & Validation（照常执行，不被取代）
   │  Execution → Validation → Evidence → Capability Status Feedback
   ↓
Phase 7 Agent Orchestration（复杂任务：Skill 产出的子任务结构 → Selection/Delegation/
   │  Parallel/Communication/Aggregation/Conflict/Recovery——Skill 不替代编排）
   ↓
Phase 8 Evolution（Skill 运行记录 + 失败 + 性能 + 人工介入 → Observation → Evidence →
      Evolution Proposal → Evaluation → Approval → Skill v(n+1)——Content Evolution，不动 Phase 0–8）
```

### 2.2 接口设计（最小 5 个，全部由既有阶段提供或以查询方式复用）

| # | 接口 | 归属 | 说明 |
|---|---|---|---|
| Q1 | `Task → Skill Registry Query → Skill Candidate` | 复用 Registry 查询（Phase 5 侧接口，见 §5 方案 A） | "针对当前任务有哪些 Skill 可用？" |
| Q2 | `Agent → Skill Registry Query → Skill Candidate` | Phase 7 新增查询（数据在 Skill Registry，协议不变） | "当前 Agent 可执行哪些 Skill？" |
| I1 | `Skill.required_* → Phase 5 Retrieval Query` | Phase 5 既有接口 2（Requirements → Retrieval Query） | Skill 只提供需求，检索仍归 Phase 5 |
| I2 | `Skill.workflow step(type=execute/validate) → Phase 6 Execution/Validation Interface` | Phase 6 既有接口 1–4 | Skill 不自带执行/验证状态机 |
| I3 | `Skill Run Record → Phase 8 Evolution Source` | Phase 8 既有 Evolution Source 机制 | 需 FCP 触点 T3 增补来源类型（§17） |

### 2.3 Skill 的"允许 / 禁止"清单（落地为校验规则）

**允许**：调用 Knowledge（经 Phase 5 检索）｜经 Capability Interface 调用 Capability｜选用 Implementation（Phase 5 决策产物）｜引用 Asset / Template｜声明 Validation Requirements（Phase 6 执行）｜查询 Failure Database（`13_FAILURE_DATABASE/`，前向引用，落地时按既有约定）｜使用 Project Experience｜请求 External Resource（经 Phase 2.5）｜经 `dependencies` 调用其他 Skill（须无环）｜被多 Agent 复用。

**禁止**：直接修改 Foundation｜绕过 Capability Registry（内嵌能力实现）｜绕过 Validation（自封"已验证"）｜把 Knowledge 复制进 Skill 作为唯一来源｜把某个 LLM 写为必要条件｜把 Hermes/OpenClaw 写为运行时要求｜绕过 Phase 2.5 引入外部 Skill｜把 Skill 状态与 Capability 状态机械同步。

---

## 3. Skill 与现有 Phase 的关系与边界（任务项 8）

### 3.1 Skill ↔ Phase 4（Knowledge）

- Knowledge 的存储、版本、冲突、状态（Candidate→Reviewed→Approved）**全部仍归 Phase 4**。
- Skill 只声明"什么时候需要什么知识"：`required_knowledge[] = {query: {domain, knowledge_type, keywords, concepts, version}, pinned_ids?: [K-…]}`。
- `pinned_ids` 是**引用不是拷贝**（SSOT §3）；知识缺口 → 复用 `05_DECISION/gaps/KNOWLEDGE_GAPS.yaml`，Skill 不自建第二套知识登记。
- **反例（违规）**：Godot Debug Skill 内部保存大量 Godot API 知识 → 违反 SSOT 与 §4 不混淆。
- **正例**：Skill 步骤"分析错误 → 判断需要什么知识 → 检索 `K-SOFTWARE-GODOT-*` → 检索相关 Capability → 制定策略 → 执行 → 验证"。

### 3.2 Skill ↔ Phase 5（Retrieval & Decision）

**Skill 不取代 Phase 5。** Skill 的 `workflow` 描述"任务级工作流"；具体 Knowledge/Capability/Implementation/Asset 的**检索、过滤、排序、选择**仍走 Phase 5 五段管线（§五）与 Interface 匹配（§七）。

Skill 接入 Phase 5 有两种方案（决策点 D3，见 §20）：

| | 方案 A（推荐首期） | 方案 B（随 FCP 可选） |
|---|---|---|
| 机制 | Agent 先经 Q1/Q2 查 SKILL_REGISTRY 选定 Skill；Skill 的 required_* 作为需求输入 Phase 5 | Skill 成为 Phase 5 Candidate 的一种 `resource_type`，参与 Ranking |
| Phase 5 spec 改动 | **零改动**（§五检索清单不动） | 需改 §五检索资源清单（§五现列举：Knowledge、Capability、Implementation、Asset、Template、Project Experience、Validation Evidence，**无 Skill**）→ Foundation 触点 T4 |
| 优点 | 完全不动 Foundation | Skill 选择可解释、进统一 Decision Evidence |
| 缺点 | Skill 选择的证据在 Phase 5 之外，需自律记录 | 多一个 Foundation 触点 |

两者不互斥：先 A 落地，B 作为 FCP-001 的可选触点由用户勾选。

### 3.3 Skill ↔ Phase 6（Execution & Validation）

**Skill 不取代 Phase 6。** Skill 可以（也应该）在 `validation_requirements` 里规定验证步骤，但：
- 执行状态、Validation Evidence、Validation Result、Capability 状态转换（§十七 Evidence-driven Transition）**全部由 Phase 6 管理**。
- Skill 的 workflow step 一旦进入 execute/validate，必须落到 Phase 6 Execution/Validation Interface（I2），不得自带状态机。
- Skill 自身的验证分两层（见 §9）：**静态校验**（结构/引用检查，不需执行）与**运行证据**（执行记录）。
- Skill 运行数据（execution result / failures / performance / resource usage / human intervention / 成功与不成功案例）记为 Skill Run Record → Phase 8 素材（I3）。

### 3.4 Skill ↔ Phase 7（Agent Orchestration）

**Skill 不取代 Phase 7。** 分工：

| 关注点 | 归属 |
|---|---|
| 哪个 Agent 执行、委派、通信、并行、共享状态、聚合、冲突、恢复、Handoff | Phase 7 |
| 面对任务的工作方法、步骤顺序、何时检索/执行/验证 | Skill |
| Skill 产出的子任务结构（如 Vision/Kinematics/Gripper/Control/Testing） | Skill 生成**候选拆分**，Phase 7 执行 Selection → Delegation → Parallel → Communication → Aggregation → Conflict Resolution |
| `compatible_agents` | Skill 侧声明（约束"谁能用我"），供 Phase 7 查询 Q2；不改 §八 Selection 判据本身 |

场景（任务项 8 原例）：用户"帮我做一个机器人抓取系统" → Robotics Agent → 调 `skill.robotics.assembly` → 需求分析 → 经 Phase 5 检索机器人知识 + 抓取/机械臂 Capability → Phase 5 选 Implementation → Phase 6 执行验证；任务复杂时 Skill 拆出 5 个子任务交 Phase 7 编排。**Skill 全程不做 Agent 选择与委派。**

### 3.5 Skill ↔ Phase 8（Evolution）

- Skill 进化属于 **Content Evolution**：`Observation → Evidence → Evolution Proposal → Evaluation → Approval → Skill v2`，绝不因此修改 Phase 0–8。
- 前提：EVOLUTION_RULES 需承认 Skill 为演化对象——**Foundation 触点 T3**（§17）。
- 既有规则直接复用：12 问、Confidence、No Silent Mutation、Dedup、Priority、Rollback、Sandbox。
- 泛化阶梯（§18 反过度泛化）同样适用：单次项目成功的 skill 修改不得直接升为通用 Skill 更新。

---

## 4. Skill Schema（任务项 5）

设计原则：字段必答"有没有实际用途"；按组划分；**演化/废弃/替换/依赖/与 Capability 解耦/与 Agent 解耦**六个硬需求各由明确字段承担。

### 4.1 字段表（`SKILL_SCHEMA.yaml` 契约）

**A. 身份与分类**

| 字段 | 类型 | 必填 | 用途 |
|---|---|---|---|
| `skill_id` | string（`skill.<domain>.<name>`，仿 capability_id 惯例） | ✅ | SSOT 主键 |
| `name` | string | ✅ | 展示名 |
| `description` | string | ✅ | 一句话说明 |
| `domain` | enum（Game/Robotics/CAD/Manufacturing/Electronics/AI/Automation/…） | ✅ | Q1 按域检索 |
| `purpose` | string | ✅ | "解决哪类任务"——Q1 匹配任务的主依据（≠ description 的自我描述） |
| `version` | semver | ✅ | 版本演化（VERSION_POLICY：初始 0.1.0，状态跃迁按 §4 递增） |
| `status` | enum（见 §7 生命周期） | ✅ | 废弃/替换的载体之一 |

**B. 任务契约**

| 字段 | 类型 | 必填 | 用途 |
|---|---|---|---|
| `inputs` | array[{name, type, description, required}] | ✅ | 与 Phase 5 Requirements 对接；I/O 匹配校验 |
| `outputs` | array[{name, type, description}] | ✅ | 同上 |

**C. 依赖（解耦的核心）**

| 字段 | 类型 | 必填 | 用途 |
|---|---|---|---|
| `required_knowledge` | array[{query, pinned_ids?, version?}] | ✅（可为空数组） | **引用+查询**，不存知识本体（§3.1） |
| `required_capabilities` | array[{capability_id, interface_requirements?, version_range?}] | ✅（可为空数组） | 只引 ID + 接口需求，**不带实现**（§5）；version_range 承担 VERSION_POLICY §6 依赖版本 |
| `optional_capabilities` | array[同上] | ➖ | 增强项，缺失不阻断 |
| `dependencies.skills` | array[{skill_id, version_range}] | ➖ | Skill→Skill 复用；校验无环（§9） |
| `dependencies.external` | array[{resource_ref, via: Phase 2.5}] | ➖ | 外部依赖必须走 2.5 网关 |
| `compatible_agents` | array[role_id]（引 AGENT_ROLES，不引实例） | ✅ | **与 Agent 解耦**：多对多，Role 级声明 |
| `compatible_runtimes` | array[{interface: agent_runtime, requires: [method/feature]}] | ✅ | **与 Runtime 解耦**：只声明所需接口能力（如 `execute_task`、`checkpoint`），不出现任何平台名 |

**D. 工作流与约束**

| 字段 | 类型 | 必填 | 用途 |
|---|---|---|---|
| `workflow` | array[{step_id, title, action_type, target, description}] | ✅ | `action_type ∈ {analyze, retrieve_knowledge, retrieve_capability, decide, execute_capability, validate, delegate, record}`；`target` 只能是引用（capability_id / "Phase 5" / "Phase 6" / "Phase 7" / skill_id）——**结构上禁止内嵌实现**，这是"Skill→Capability Interface→Implementation"（§5）的 schema 级强制 |
| `constraints` | array[string]（含 hard/soft 标注） | ➖ | 供 Phase 5 约束过滤 |
| `risk_level` | enum low/medium/high/critical | 条件必填（涉现实世界则 ✅） | LIBRARY_RULES §9 安全规则延伸到工作流层 |
| `requires_human_approval` | bool | 条件必填（high/critical ✅） | 同上 |

**E. 验证与失败**

| 字段 | 类型 | 必填 | 用途 |
|---|---|---|---|
| `validation_requirements` | array[{criterion, evidence_type, phase6_ref?}] | ✅ | 规定验证步骤；**证据产出归 Phase 6** |
| `failure_handling` | {on_step_failure: abort/retry/fallback/escalate, fallback_skill?, escalate_to: human/agent, max_retries} | ✅ | 禁无限 Retry（与 Phase 7 §十九一致） |

**F. 治理与演化**

| 字段 | 类型 | 必填 | 用途 |
|---|---|---|---|
| `source` | enum internal/project_extracted/external/derived | ✅ | 溯源入口；external → 必须有 Phase 2.5 结论 |
| `provenance` | 按 `00_CORE/Metadata/PROVENANCE_SPEC.md` | ✅ | original_source/version/commit/modifications… |
| `version_scope` | string/obj（适用环境范围，如 `Godot 4.6.x; library schema ≥1.0`） | ✅ | 版本适用性；过期依赖检测（§9） |
| `superseded_by` / `deprecated_reason` | skill_id / string | 终态必填 | 废弃/替换；与 §11 规则一致，记录不删除 |
| `evolution_history` | array[{version, date, change, reason, evidence, proposal_id}] | ✅（初始 1 条） | 演化史；不覆盖旧版（VERSION_POLICY §6） |
| `known_limitations` | array[string] | ✅ | 已知缺陷 + 依赖状态提示（如"依赖能力仍 Experimental"） |
| `examples` | array[{scenario, io_sample}] | ➖ | 使用示例，非冗余：是任务匹配与测试用例素材 |
| `created_at` / `updated_at` | ISO 8601 | ✅ | 惯例字段 |

**明确砍掉的候选项**（用户清单中考虑后不单列）：`author`/`license` 并入 `provenance`（PROVENANCE_SPEC 已覆盖，不重复）；`metrics` 不设字段——按 Phase 8 §十二"指标数据首现时落位"先例，真实使用数据出现时再建 `SKILL_USAGE.yaml`，不造空系统。

### 4.2 六个硬需求 → 字段映射

| 需求 | 承担字段（+机制） |
|---|---|
| 版本演化 | `version` + `evolution_history` + VERSION_POLICY 语义化规则 |
| 废弃 | `status: Deprecated` + `deprecated_reason`（+推荐替代） |
| 替换 | `status: Superseded` + `superseded_by`（旧记录保留，可检索） |
| 依赖 | `dependencies.skills/external` + `required_*` 的 version_range |
| 与 Capability 解耦 | `required_capabilities` 只引 ID+接口需求；workflow `target` 引用制（§5） |
| 与 Agent 解耦 | `compatible_agents`（Role 级）、`compatible_runtimes`（接口级），多对多 |

---

## 5. Skill ↔ Capability 边界（任务项 5 的最重要部分）

### 5.1 正反结构

```
✅  Skill → Capability Interface → Implementation          （经 Registry、经 Phase 5 选择）
❌  Skill → 一大段硬编码实现                                （绕过 Registry、无法替换、无法验证）
```

例：
- Capability `pathfinding` = 系统具备"路径规划能力"（Interface：输入起点/终点/栅格，输出路径…，可能有 A*/JPS 多个 Implementation）。
- Skill `robot_navigation` = "如何完成一个机器人导航任务"（流程：感知→定位→规划→执行→验证）。
- Skill 通过 `required_capabilities: [pathfinding, obstacle_detection, localization, trajectory_generation]` 声明需求；具体选哪个 Implementation、走哪条验证线，**Phase 5 决定，Phase 6 验证**。

### 5.2 schema 级强制（不是口头约定）

1. `workflow[].action_type` 枚举中没有"写实现"这个动作——执行类动作只有 `execute_capability`，其 `target` 必须是 `capability_id`。
2. `required_capabilities[]` 的元素结构是 `{capability_id, interface_requirements, version_range}`——**不含** code、路径、脚本正文。
3. 静态校验（§9）检查：`required_capabilities` 里的 ID 是否存在于 `CAPABILITY_REGISTRY.yaml`；不存在 → 报 **Capability Gap**，走 `05_DECISION/gaps/CAPABILITY_GAPS.yaml`，不许 Skill 私自造一个"实现"顶替。
4. Skill 实现代码若确有需要（如一段编排脚本），属 `12_TESTING_VALIDATION`/工具层 Content，**不是 Skill 记录的一部分**，且不得承载能力逻辑。

---

## 6. Skill Registry（任务项 13）

### 6.1 文件与 SSOT

```
SKILL_REGISTRY.yaml   ← 权威（Content 条目）
SKILL_INDEX.md        ← 派生索引，可由 yaml 重建（SSOT §3；同 CAPABILITY_INDEX 惯例）
SKILL_RULES.md        ← Foundation（登记/跃迁/查询规则；随 FCP 批准建立）
```

### 6.2 `SKILL_REGISTRY.yaml` 条目 schema

```yaml
registry:
  schema_ref: "SKILL_SCHEMA.yaml"
  updated_at: "YYYY-MM-DD"
  status: EMPTY            # 首个 Skill 经批准后登记
skills:
  - skill_id: "skill.game.godot_development"
    name: "..."
    domain: Game
    version: "0.1.0"
    status: Candidate
    purpose: "..."
    required_capabilities: []      # 仅 ID+版本范围
    required_knowledge: []         # 查询+可选 pinned ID
    dependencies: {skills: [], external: []}
    compatible_agents: [GAME, CODING]
    validation_status: {static: not_run, runtime_evidence: []}
    risk_level: low
    provenance: {source: internal, ...}
    updated_at: "..."
```

（完整字段见 §4；Registry 为检索投影，可只保留高频查询字段 + 指向 skill 条目正文的 `entry_ref`——首个 Skill 落位时定，避免一次造全。）

### 6.3 两个法定查询

**Q1 — Phase 5 侧："针对当前任务，有哪些 Skill 可用？"**
输入：`{domain, task_purpose/keywords, inputs available, constraints, min_status}` → 过滤 `status ∈ {Tested, Verified, Reusable}`（可配置，Candidate/Experimental 仅在显式允许时入选）→ 按 purpose 匹配 + version_scope + required_capabilities 可满足性（交 Phase 5 §七 复核）排序 → 产出 Skill Candidate 列表（复用 Phase 5 Candidate 概念，不改其 schema——方案 A 下仅作为 Agent 决策上下文）。

**Q2 — Phase 7 侧："当前 Agent 可以执行哪些 Skill？"**
输入：`agent.role_id + agent.required_capabilities + 环境` → 过滤 `role_id ∈ compatible_agents` ∧ `required_capabilities ⊆ agent 声明能力`（接口层面）∧ status 过滤。返回附带 `known_limitations` 与依赖状态提示，供 Selection（§八）参考——**查询提供信息，不替代 §八 判据**。

---

## 7. Skill Lifecycle（任务项 7）

### 7.1 状态机

```
Candidate → Experimental → Tested → Verified → Reusable
                                              ↓
                              Deprecated（记 reason + 推荐替代）
                              Superseded（记 superseded_by，旧版保留）
```

跃迁规则（仿 CAPABILITY_SPEC §4，不发明新模型）：
- 不得跳级（Candidate 不能直通 Verified）。
- `Tested` = 通过**静态校验** + 至少一次受控试用（workflow 完整、引用成立、I/O 匹配）。
- `Verified` = 有**真实任务执行**的 Validation Evidence（经 Phase 6 产出的证据引用）。
- `Reusable` = Verified + 至少一个成功项目使用 + 被 ≥1 个其他 Agent 角色使用过。
- 终态必填 `deprecated_reason` / `superseded_by`；记录永不删除。
- 版本影响按 VERSION_POLICY §4：跃迁 PATCH/MINOR 对应表照搬。

### 7.2 与 Capability 生命周期解耦（关键设计）

**Skill 状态只反映 Skill 自身工作流的验证证据，不反映依赖对象的状态。**

- 允许：Skill = `Verified`，而其 `required_capabilities` 中某 Capability = `Experimental`。
- 机制：**选时检查（selection-time check）**——Phase 5 在每次为任务选 Capability 时按 §七/§八 处理依赖状态（Experimental 可选但须记录原因），**不回写 Skill 状态**。
- Skill 侧只做两件事：`known_limitations` 记录该情况；静态校验在依赖状态跌破阈值时**发警示（不改状态）**。
- 禁止：把 Skill 生命周期与 Capability 生命周期机械同步（那会制造跨 Registry 的一致性耦合，违反两者的独立演化）。

### 7.3 与 LIBRARY_RULES §11 标准化的衔接

映射行：Skill 的 Active-path = `Candidate → Experimental → Tested → Verified → Reusable`，终态 `Deprecated / Superseded`，完全落在 §11 canonical 视图（Candidate → Active/Validated → Deprecated → Superseded）内。**类型映射表需要新增一行 Skill——这是 Foundation 触点 T1（§17），不是生命周期模型本身的修改。**

---

## 8. Skill 验证机制（任务项 10）

### 8.1 静态校验（`tools/validate_skill.py`，参照 validate_agent.py 惯例）

1. Workflow 完整性：每步有 step_id/action_type/target；无孤儿步骤。
2. `required_capabilities` ID 均存在于 `CAPABILITY_REGISTRY.yaml`（否则 Capability Gap）。
3. `required_knowledge` 查询/pinned ID 可解析（否则 Knowledge Gap）。
4. `inputs/outputs` 与 workflow 首尾、与声明的依赖接口匹配。
5. 依赖无环（`dependencies.skills` + workflow 内 `invoke_skill` 深度，建议 ≤2）。
6. `prerequisites` 可满足（引用的对象存在、状态不低于阈值）。
7. 权限合规：risk_level/触发的 Capability 权限与 AGENT_PERMISSIONS 不冲突；high/critical 必须 `requires_human_approval: true`。
8. `validation_requirements` 每条都能指出 Phase 6 证据类型（不可验证的声明 = dead requirement）。
9. Dead step 检测：步骤的 target/输出从未被后续消费 → 警告。
10. 依赖有效性：version_scope 与依赖 version_range 无过期/冲突。
11. 非硬编码检查：字段/正文出现具体平台名作为**必要条件**（Hermes/OpenClaw/具体 LLM 作为 `compatible_runtimes` 之外的硬性词）→ 违规。

### 8.2 运行记录（进入 Phase 8 素材）

Skill 实际执行后记录（载体：`SKILL_USAGE.yaml`，**首个真实数据出现时落位**，不造空文件）：
`execution result / validation result(ref Phase 6 evidence) / failures / performance / resource usage / human intervention / successful cases / unsuccessful cases`。
→ 经 I3 进入 Evolution：连续问题 → `Common Pattern Detected` → Skill Evolution Proposal。

**核心立场：Skill 是"流程"不等于"天然正确"——流程同样可证伪、可验证、可进化。**

---

## 9. Skill Evolution（任务项 11）

```
使用观察（SKILL_USAGE / Failure / 用户反馈 / 依赖变化）
   ↓ Observation
证据固化（Evolution Event — 记录不修改）
   ↓ Evidence
Evolution Proposal（type: SKILL_UPDATE / SKILL_DEPRECATION / SKILL_REPLACEMENT）
   ↓ Evaluation（含静态校验 + 回归：v1 成功过的场景 v2 仍须通过）
   ↓ Approval（Content 级低风险按 §43 自动；Deprecated/Superseded 与高风险按规则人工）
   Skill v(n+1)（不覆盖旧版；evolution_history 追加）
```

例：Skill v1 手动 10 步 → 实际项目发现 Step3/4 可合并 → 证据 → Proposal → Evaluation → 批准 → v1.1。
**边界：这是 Content Evolution；禁止借 Skill 进化修改 Phase 0–8 Foundation。**（前提：T3 触点获批，见 §17。）

---

## 10. 最小目录结构（任务项 9）

**检查结论：14_AI_AGENTS 无现成 Skill 位置；优先复用的原则应用为"复用既有惯例"而非"塞进语义不符的目录"。**

### 方案甲（推荐）——`14_AI_AGENTS/Skills/`

与用户 §12 草图一致，且复用 14_AI_AGENTS 的 Registry/orchestration/tools 惯例：

```
14_AI_AGENTS/
└── Skills/
    ├── SKILL_SCHEMA.yaml          # §4 字段契约（批准后落位）
    ├── Registry/
    │   ├── SKILL_RULES.md         # Foundation（随 FCP 建立）
    │   ├── SKILL_REGISTRY.yaml    # Content 条目（SSOT，初始 status: EMPTY）
    │   └── SKILL_INDEX.md         # 派生索引（可重建）
    ├── tools/validate_skill.py    # §8 静态校验
    └── <domain>/…                 # Game/ Robotics/ Debugging/ …
                                    # ← 首个 Skill 实体落位时才建（05_DECISION §三十一
                                    #    "不为形式造空目录"先例）；每个 Skill 一个目录，
                                    #    workflow 正文 SKILL.md 放目录内，Registry 存投影
```

代价：Phase 7 spec §三十二 目录契约需加一行 → **FCP 触点 T2**。
备选说明：甲方案把"怎么做"（Skill）放进"谁来做"（Agent）目录，语义上并非完美；但比顶层新编号目录（动 00-15 骨架语义，Foundation 更重）代价小，且查询方主要就是 Phase 7/Agent。

### 方案乙（备选）——顶层 `16_SKILLS/`（或复用未定语义编号位 03/04/06/07/10 之一）
语义最干净，但骨架语义变更面更大；未定编号位的真实用途无据可查（库内无骨架语义表），**不建议猜测占用**。

**两方案都须 FCP 批准后才创建目录与文件（Phase 0 §2/§3：边界存疑默认按 Foundation 处理）。本次不创建任何目录。**

---

## 11. 三个示例 Skill（任务项 10）

> 全部为**设计示例**（Candidate / 0.1.0，未落盘）。真实 ID 已核对库内 Registry；库内不存在的需求一律标 GAP，不臆造 ID（AGENT_ROLES 同款自律）。

### 11.1 `skill.game.godot_development` — Godot Development Skill

```yaml
skill_id: skill.game.godot_development
name: Godot Development
domain: Game
version: "0.1.0"
status: Candidate
purpose: "在 Godot 4.6.x 项目中按库规范实现新游戏功能：复用优先、引擎隔离、证据验证"
inputs:
  - {name: feature_requirement, type: text, required: true}
  - {name: project_ref, type: ref, required: true}      # 11_PROJECTS 下的项目
  - {name: godot_version, type: string, required: true}
outputs:
  - {name: implementation_plan, type: ref}               # Phase 5 Execution Plan 引用
  - {name: code_artifacts, type: ref}
  - {name: validation_evidence_ref, type: ref}           # Phase 6 证据引用
prerequisites:
  - "project_ref 存在且可写（深空殖民除外——原项目只读）"
  - "godot_version ∈ version_scope"
required_knowledge:
  - {query: {domain: Godot, keywords: [API, 节点, 信号, 资源]}, pinned_ids:
      [K-SOFTWARE-GDSCRIPT-STATIC-TYPING-001, K-SOFTWARE-GODOT-SIGNAL-001,
       K-SOFTWARE-GODOT-RESOURCE-001, K-SOFTWARE-GODOT-REFCOUNTED-001]}
required_capabilities: []          # 任务相关的能力由 Phase 5 检索（如 game.behavior_tree）
workflow:
  - {step_id: S1, action_type: analyze, target: inputs, description: 解析功能需求与引擎版本约束}
  - {step_id: S2, action_type: retrieve_knowledge, target: Phase 5, description: 按 required_knowledge 检索}
  - {step_id: S3, action_type: retrieve_capability, target: Phase 5, description: 复用优先：搜 CAPABILITY_REGISTRY，有则复用/扩展}
  - {step_id: S4, action_type: decide, target: Phase 5, description: 选 Implementation，记录选择原因}
  - {step_id: S5, action_type: execute_capability, target: capability_id, description: 经接口实现}
  - {step_id: S6, action_type: validate, target: Phase 6, description: 构建/测试证据}
  - {step_id: S7, action_type: record, target: SKILL_USAGE, description: 记录结果与偏差}
constraints: ["引擎隔离（LIBRARY_RULES §5）", "复用优先（§6）", "hard: 不修改 Godot 之外引擎目录"]
validation_requirements:
  - {criterion: 构建通过且测试证据可追溯, evidence_type: phase6_evidence}
failure_handling: {on_step_failure: escalate, escalate_to: human, max_retries: 1}
compatible_agents: [GAME, CODING]
compatible_runtimes: [{interface: agent_runtime, requires: [execute_task, checkpoint]}]
risk_level: low
source: internal
version_scope: "Godot 4.6.x; library schema ≥1.0"
known_limitations: ["仅覆盖流程；引擎 API 知识归 Phase 4", "依赖能力缺位时产出 Gap 而非替代实现"]
evolution_history: [{version: "0.1.0", date: 2026-10-07, change: 初稿, reason: 设计评审, proposal_id: —}]
```

### 11.2 `skill.robotics.grasp_assembly` — Robotics Engineering Skill（抓取系统）

```yaml
skill_id: skill.robotics.grasp_assembly
name: Robotics Grasp Assembly
domain: Robotics
version: "0.1.0"
status: Candidate
purpose: "完成机器人抓取系统从需求到验证的工作流（视觉-运动学-夹爪-控制-测试）"
inputs: [{name: task_spec, type: text, required: true}, {name: robot_platform, type: string, required: true}]
outputs: [{name: subsystem_plan, type: ref}, {name: simulation_evidence, type: ref}, {name: deployment_readiness, type: bool}]
prerequisites: ["仿真环境可用；实机操作前必须 Human Approval"]
required_knowledge:
  - {query: {domain: Robotics, keywords: [抓取, 运动学, 夹爪, 控制]}}   # 库内暂无 → Knowledge Gap（05_DECISION/gaps）
required_capabilities:                                 # 均为接口需求；库内 10 个 Capability 无一覆盖
  - {capability_id: robotics.localization,     status: GAP}   # → CAPABILITY_GAPS.yaml，禁私造实现
  - {capability_id: robotics.trajectory_generation, status: GAP}
  - {capability_id: robotics.grasp_planning,   status: GAP}
  - {capability_id: robotics.arm_control,      status: GAP}
workflow:
  - {step_id: S1, action_type: analyze, target: inputs, description: 需求分析与风险分级}
  - {step_id: S2, action_type: retrieve_knowledge, target: Phase 5, description: 检索机器人/抓取知识}
  - {step_id: S3, action_type: retrieve_capability, target: Phase 5, description: 检索抓取与机械臂 Capability（缺位记 Gap）}
  - {step_id: S4, action_type: decide, target: Phase 5, description: 选择 Implementation（优先 Verified）}
  - {step_id: S5, action_type: delegate, target: Phase 7, description: 复杂任务拆分候选：
       [Vision, Kinematics, Gripper, Control, Testing] → 交编排（选择/委派/并行/聚合归 Phase 7）}
  - {step_id: S6, action_type: execute_capability, target: capability_id, description: 经接口执行}
  - {step_id: S7, action_type: validate, target: Phase 6, description: 仿真→实机分级验证（Phase 6 §十六）}
  - {step_id: S8, action_type: record, target: SKILL_USAGE, description: 记录证据/失败/人工介入}
constraints:
  - "hard: 未经 Human Approval 不得实机动作（risk critical）"
  - "hard: 不得把实现代码写进本 Skill"
validation_requirements:
  - {criterion: 仿真抓取成功率达标, evidence_type: phase6_evidence}
  - {criterion: 实机前安全检查清单全过, evidence_type: human_approval_record}
failure_handling: {on_step_failure: abort, escalate_to: human, max_retries: 0}   # 实机失败即停
compatible_agents: [ROBOTICS, TESTING, CAD]
compatible_runtimes: [{interface: agent_runtime, requires: [execute_task, send_message, checkpoint, recover]}]
risk_level: critical
requires_human_approval: true
source: internal
version_scope: "library schema ≥1.0; 仿真栈待定（不写死）"
known_limitations: ["4 个 required_capability 均未登记——本 Skill 在能力补齐前只能走到 Gap 阶段"]
evolution_history: [{version: "0.1.0", date: 2026-10-07, change: 初稿, reason: 设计评审, proposal_id: —}]
```

### 11.3 `skill.debugging.root_cause` — Debugging Skill（横切域）

```yaml
skill_id: skill.debugging.root_cause
name: Root Cause Debugging
domain: Automation            # 横切域；domain 按任务上下文解释
version: "0.1.0"
status: Candidate
purpose: "对任意工程错误执行系统化根因定位与修复验证（四阶段：理解→定位→修复→回归）"
inputs: [{name: error_signal, type: text, required: true}, {name: context_ref, type: ref, required: false}]
outputs: [{name: root_cause, type: text}, {name: fix_ref, type: ref}, {name: regression_evidence, type: ref}]
prerequisites: ["error_signal 可复现或有日志/证据"]
required_knowledge:
  - {query: {keywords: [<错误关键字>], domain: <按错误判定>}}   # 关键：不内嵌任何引擎/API 知识
required_capabilities: []                                     # 修复所需能力由 Phase 5 按错误类型检索
workflow:
  - {step_id: S1, action_type: analyze, target: inputs, description: 分析错误，区分现象与根因}
  - {step_id: S2, action_type: decide, target: Phase 5, description: 判断需要什么知识（产出检索需求）}
  - {step_id: S3, action_type: retrieve_knowledge, target: Phase 5, description: 检索相关 Knowledge（如 K-SOFTWARE-GODOT-*）}
  - {step_id: S4, action_type: retrieve_capability, target: Phase 5, description: 检索相关 Capability}
  - {step_id: S5, action_type: retrieve_knowledge, target: 13_FAILURE_DATABASE, description: 查同类失败记录（前向引用，落地时接入）}
  - {step_id: S6, action_type: decide, target: Phase 5, description: 制定修复策略（多方案排序）}
  - {step_id: S7, action_type: execute_capability, target: capability_id, description: 执行修复}
  - {step_id: S8, action_type: validate, target: Phase 6, description: 回归验证——修复不能只凭"看起来好了"}
  - {step_id: S9, action_type: record, target: SKILL_USAGE, description: 失败模式入库候选 → Phase 8}
constraints: ["禁止编造知识（检索不到就记 Gap）", "禁止把最终表现当根因（须拆解链路）"]
validation_requirements:
  - {criterion: 回归用例通过, evidence_type: phase6_evidence}
  - {criterion: 根因与证据链一致, evidence_type: decision_evidence}
failure_handling: {on_step_failure: retry, fallback_skill: null, escalate_to: agent, max_retries: 2}
compatible_agents: [CODING, TESTING, GAME, KNOWLEDGE, ROBOTICS]     # 横切：多 Agent 复用的典型
compatible_runtimes: [{interface: agent_runtime, requires: [execute_task]}]
risk_level: low
source: internal
version_scope: "通用（按 required_knowledge 动态解析）"
known_limitations: ["不替代 Failure Database 的 RCA 记录规范", "修复执行依赖库内 Capability 覆盖度"]
evolution_history: [{version: "0.1.0", date: 2026-10-07, change: 初稿, reason: 设计评审, proposal_id: —}]
```

---

## 12. Foundation 冲突检查（任务项 11）

| # | 触点 | 涉及 Foundation 对象 | 冲突性质 | 能否 Content 层解决 | 处理 |
|---|---|---|---|---|---|
| T1 | **实体模型无 Skill** | `LIBRARY_RULES.md` §2 实体表 + §4 不混淆表 + §11 类型映射表（根级六件套 = Foundation） | 不加行 → Skill 成为"无 trackable status 的资源"，违反 §11"no resource may exist in an untracked state" | ❌ 不能——规则文件本身是 Foundation；藏在别的实体下会违反 §4（Skill≠Capability≠Agent） | **FCP-001 必选项**（只加行，不改既有行） |
| T2 | **目录契约无 Skills** | `AGENT_ORCHESTRATION_SPEC.md` §三十二（Spec = Foundation；14_AI_AGENTS 归属存疑 → 按宪章 §1.2 默认按 Foundation 处理） | 新目录不在契约内 | ❌ 不能（同上："规则文件是 Foundation"） | **FCP-001 必选项**（加 1 行；若选方案乙则换成骨架语义变更） |
| T3 | **演化对象/提案类型无 Skill** | `EVOLUTION_RULES.md` §三来源 14 类、§五检测 12 类、§六对象规则、§八提案类型 20 种 | Skill 进化无合法 type → 只能硬塞 AGENT_UPDATE（错位）或绕过流程（违规） | ❌ 不能（EVOLUTION_RULES 自我声明受 §30-31 保护） | **FCP-001 必选项**（各加 Skill 一项，不动既有项） |
| T4 | **Phase 5 检索清单无 Skill** | `RETRIEVAL_DECISION_SPEC.md` §五 | 仅当采纳方案 B（Skill 进 Candidate Ranking）才冲突 | 方案 A 下 ✅ 能——Skill 选择放 Agent 层，Phase 5 零改动 | **FCP-001 可选项**（用户勾选） |
| — | 生命周期模型本身 | — | **不冲突**：Skill 复用 5+2 状态词表与跃迁纪律 | — | 无修改 |
| — | Registry 协议本身 | — | **不冲突**：SKILL_REGISTRY 复用 registry 惯例（schema_ref/updated_at/status/条目） | — | 无修改 |
| — | Phase 0 宪法、AI 权限、治理规则 | — | **不冲突**：Skill 设计完全在"提案→人工批准"框架内运作 | — | 无修改 |
| — | CAPABILITY_SPEC §5/§6 Interface 可替换性 | — | **不冲突**：Skill→Interface→Implementation 恰好是该规则的延伸 | — | 无修改 |
| — | 非硬编码红线 | — | **不冲突**：compatible_runtimes 只声明 agent_runtime 接口能力 | — | 无修改 |
| — | 安全分级 | LIBRARY_RULES §9 只要求 Capability 声明 risk | 弱覆盖：工作流层风险无人声明 | 部分——Skill 自带 risk_level 字段属自加约束，不改 §9 | 记入观察，不改 Foundation |

**结论：Phase 1–6 核心边界、Registry 协议、生命周期模型、治理规则均无需修改；冲突集中在 4 个"清单/枚举/契约行"级别的触点，全部可由一个 FCP-001 承载，且均为纯追加（不改既有条目），兼容风险低。**

---

## 13. 重复功能检查（任务项 12）

| 疑似重复 | 实为 | 判定 |
|---|---|---|
| Composite Capability（Phase 5 §十七） | 数据层的"能力组合"定义 | **不重复**：Composite 是"组合哪些能力"，Skill 是"按什么方法完成任务"；Skill 可引用 Composite Capability 作为 required_capabilities |
| Execution Plan（Phase 5 §十六） | 单个任务的一次性执行计划 | **不重复**：Plan 是产物（每次任务生成），Skill 是可复用模板（跨任务、有版本）；Skill 指导 Plan 的生成 |
| AGENT_ROLES / Agent Capability（Phase 7 §五） | 职责结构与可调用能力声明 | **不重复**：Role 回答"谁的职责"，Skill 回答"怎么做"；两者经 compatible_agents 关联，多对多 |
| External Resource 类目 `Agent Skill` | 外部技能的**入口通道** | **不重复且互补**：外部 Skill 经 Phase 2.5 评估 → 采纳后登记进 SKILL_REGISTRY（provenance: external）——这正是 2.5 网关的用途 |
| Hermes / OpenClaw 的 SKILL.md 技能 | 当前 Runtime 的**打包格式** | **不重复但须防双 SSOT**：库内 SKILL_REGISTRY 为权威；Runtime 技能文件属派生打包物，必须声明来源可重建（LIBRARY_RULES §3）——列为落地时的实现注意项 |
| Phase 6 验证策略 | 执行级验证 | **不重复**：Skill 只声明 validation_requirements，证据与状态归 Phase 6 |
| 失败记录（13_FAILURE_DATABASE） | 失败事件库 | **不重复**：Skill 的 failure_handling 是事前策略，失败事件归 Failure DB |

---

## 14. 是否需要修改 Phase 0–8（任务项 13）

**结论：不新增 Phase；Phase 1–6 的核心边界、Registry 协议、生命周期模型、治理规则零修改；需要一个 Foundation Change Proposal（FCP-001）覆盖 3 个必选 + 1 个可选触点，人工批准前不动任何库文件。**

### FCP-001 草案（按 `FOUNDATION_CHANGE_PROPOSALS.yaml` §30 schema）

```yaml
foundation_change:
  proposal_id: "FCP-001-SKILL-INTEGRATION"
  affected_phase: "1, 5(可选), 7, 8"
  affected_rule: "LIBRARY_RULES §2/§4/§11；AGENT_ORCHESTRATION_SPEC §三十二；
                  EVOLUTION_RULES §三/§五/§六/§八；（可选）RETRIEVAL_DECISION_SPEC §五"
  problem: |
    Skill（任务工作方法层）在库内无实体地位、无目录契约、无演化类型：
    无法登记状态（违 §11 无未跟踪资源）、无处安放（违 §三十二 契约）、
    进化无合法提案类型（违 §八 枚举）。Skill 是 Content 层新资源，
    但其"规则文件"按宪章 §1.2 属 Foundation，必须走本流程。
  evidence:
    - "全库 Skill 检索仅 1 处（EXTERNAL_RESOURCE_SPEC.md:29 Agent Skill 类目）"
    - "LIBRARY_RULES.md §2 实体表 10 类无 Skill；§11 类型映射表无 Skill 行"
    - "AGENT_ORCHESTRATION_SPEC §三十二 目录契约无 Skills/"
    - "EVOLUTION_RULES §八 20 种提案类型无 SKILL_*"
    - "设计全文：见本次交付 SKILL_INTEGRATION_DESIGN.md"
  proposed_change:
    T1(必选): LIBRARY_RULES §2 加 "Skill" 实体行（任务工作方法/流程/策略）；
             §4 加 "Skill ≠ Capability"、"Skill ≠ Agent" 两行；
             §11 类型映射表加 Skill 行（Candidate→Experimental→Tested→Verified→Reusable + 终态）
    T2(必选): AGENT_ORCHESTRATION_SPEC §三十二 目录契约加一行 14_AI_AGENTS/Skills/（方案甲）
             ——若目录选方案乙，则改为骨架语义变更并单独影响分析
    T3(必选): EVOLUTION_RULES §三 加 Skill Updates 来源；§五 加 Skill 检测对象；
             §六 加 Skill 演化规则（版本/废弃/替换/泛化阶梯复用）；
             §八 提案类型加 SKILL_UPDATE / SKILL_DEPRECATION / SKILL_REPLACEMENT
    T4(可选): RETRIEVAL_DECISION_SPEC §五 检索资源清单加 Skill（方案 B；不勾选则 Phase 5 零改动）
    明确不改：Phase 0 宪法、Registry 协议结构、生命周期模型本体、治理规则、PHASE_ROADMAP（Skill 非 Phase）
  compatibility_impact:
    纯追加、不改动任何既有条目与状态机；既有 Agent/Capability/Knowledge 记录零迁移；
    唯一读者变化：新增 SKILL_REGISTRY 的查询方（Phase 5/7 可选接入）；
    不勾选 T4 时 Phase 5 行为完全不变。
  migration_plan:
    before: "库内无 Skill 概念（全库 Skill 检索仅 1 处外部资源类目）"
    after:  "LIBRARY_RULES/§三十二/§八 各增 Skill 条目；14_AI_AGENTS/Skills/ 落位
             （SKILL_SCHEMA + Registry 三件 + validate_skill.py；domain 目录首现实体再建）"
    affected_objects: ["LIBRARY_RULES.md", "AGENT_ORCHESTRATION_SPEC.md", "EVOLUTION_RULES.md",
                       "（可选）RETRIEVAL_DECISION_SPEC.md", "14_AI_AGENTS/Skills/**（新建）"]
    steps:
      1. 人工批准本 FCP（勾选是否含 T4）
      2. 按 §30/§32 顺序修改 4 份 spec/规则文件（保留原文，diff 报告）
      3. 落位 SKILL_SCHEMA.yaml + SKILL_REGISTRY.yaml(EMPTY) + SKILL_RULES.md + validate_skill.py
      4. 运行 validate_skill.py 空态自检 + 既有 validate_*.py 回归（不破坏旧校验）
      5. 递增受影响文件版本/状态行，登记 MIGRATION_REGISTRY / ROLLBACK_REGISTRY
    validation: "四文件 diff 仅追加；全库引用无断裂；既有工具全部通过；git status 仅含预期文件"
    rollback: "git revert 对应 commit 即恢复（纯追加、无数据迁移，单 commit 可整体回滚）"
  rollback_plan: "单 commit revert 恢复；Skills/ 目录整目录删除即回到 before 状态（初始为空态，无数据损失）"
  validation_plan: "静态：引用完整性 + 既有 validator 回归；行为：不勾选 T4 时 Phase 5 流程零变化"
  approval_status: PROPOSED      # 禁止 PROPOSED → AI 自动执行（§31）
```

---

## 15. 审查结果汇总（任务项 1–13 对照）

| # | 任务项 | 结论 |
|---|---|---|
| 1 | 检查 0–8 架构 | ✅ §0.1（13 份核心文件；HEAD=ec5f983；远端同步未能确认，见文首注） |
| 2 | 检查 14_AI_AGENTS | ✅ §0.2：无现成 Skill 位置；契约/Schema/Registry 三者皆无 Skill |
| 3 | Skill 与架构关系 | ✅ §1–3：Content 层工作流资源；四概念严格分离 |
| 4 | Integration Architecture | ✅ §2：闭环图 + 3 接口 + 允许/禁止清单 |
| 5 | Skill Schema | ✅ §4：26 字段分 6 组；6 个硬需求逐一映射 |
| 6 | Skill Registry Schema | ✅ §6：SSOT/派生分离 + Q1/Q2 两个法定查询 |
| 7 | Skill Lifecycle | ✅ §7：5+2 状态机 + 选时检查实现与 Capability 解耦 |
| 8 | 与 Phase 4/5/6/7/8 边界 | ✅ §3：每阶段"谁管什么 + Skill 禁止什么"；Phase 5 双方案 A/B |
| 9 | 最小目录结构 | ✅ §10：方案甲（14_AI_AGENTS/Skills/，复用惯例、不建空目录）/方案乙备选 |
| 10 | 3 个示例 Skill | ✅ §11：Godot Development / Robotics Grasp Assembly / Root Cause Debugging；真实 ID 已核对，缺位标 GAP |
| 11 | Foundation 冲突检查 | ✅ §12：4 触点（T1–T4），全为纯追加；生命周期/Registry/治理零冲突 |
| 12 | 重复功能检查 | ✅ §13：7 组疑似重复逐一裁定，无功能重复；1 个双 SSOT 风险点（Runtime 技能打包） |
| 13 | 是否需改 Phase 0–8 | ✅ §14：不新增 Phase、1–6 零修改；FCP-001 草案（3 必选 + 1 可选触点），status: PROPOSED，未登记入库 |

**与最高原则的一致性**：本设计没有"给 Library 加一个 Skill 文件夹"就完事——Skill 的每个落点（检索、执行、验证、编排、进化）都挂在既有 Phase 的既有接口上；Skill 换掉任何一段 workflow 不影响 Phase 0–8 承重墙。

---

## 16. 决策点（等待人工批准，批准前不执行任何库内写入）

- **D1（必答）**：是否批准 FCP-001 的 3 个必选触点（T1 实体模型行 / T2 目录契约 / T3 演化类型）？
- **D2（必答）**：目录方案 —— 甲 `14_AI_AGENTS/Skills/`（推荐，与你 §12 草图一致）还是 乙顶层新目录？
- **D3**：Phase 5 接入 —— 方案 A（零改 Phase 5，推荐首期）还是勾选 T4 走方案 B？
- **D4**：批准后的落地范围 —— 仅登记 FCP 条目？还是连同 SKILL_SCHEMA/Registry(EMPTY)/SKILL_RULES/validator 一并落位？（无论哪种，均不在本任务创建任何具体 Skill——那是后续批次，另行批准。）
- **D5**：遗产 Skill 语料（`ai-heritage-library` 134 项，§17）是否启动分批评估迁移？——分几批、入哪些域、非工程域如何处置，均需你裁定；本任务未执行任何导入。

批准 D1–D3 后执行顺序：FCP 入库登记 → spec/规则追加修改（diff 报告）→ Registry/Schema 落位 → validator 自检 → git 提交（推送需现场提供一次性 token，按既定凭据模式）。

---

## 17. 补充审查：遗产 Skill 语料（`ai-heritage-library` 134 项）与本设计的关系

> 起因：用户指出曾在 github.com/la4750/ai-heritage-library 看到一百多项 skill。本节为追问后的补充审查，纳入设计视野；**本任务未导入任何一项**。

### 17.1 事实盘点（本地克隆 `~/ai-heritage-library` 实测）

- **134 个 SKILL.md，130 个唯一名称**（重复：`self-improving-agent`×3、`tencent-docs`×2、`github`×2）。
- 分布：`workspace/Agent/coding-series` 38｜`scholar-series` 36｜`game-series` 29｜`workspace/skills`（技能市场/个人包）22｜`art-series` 6｜`office-agent` 3。
- 格式：OpenClaw/Hermes 打包格式（frontmatter 仅 `name` + `description`，正文 Markdown，含"何时使用/流程"等段）。
- **116/134 完全不含** `inputs/outputs/required_knowledge/required_capabilities` 等 schema 关键字段——即：**它们是 Runtime 技能，不是库内 Skill 实体**，直搬无法满足 §4 schema。
- 内容形态差异大：有"流程型"（novel 章纲、game-studio 各工作流——与本设计的 Skill 概念同构），也有"知识型"（`godot-knowledge` 等内嵌大量 API 知识——恰是 §3.1 定义的违规形态），还有"工具型"（`github`/`tencent-docs`——依赖具体 CLI/SaaS）。

### 17.2 定位判定

- 这批语料**不在 Personal AI Engineering Library 内**，相对库是**来源素材**：`source: internal-legacy`（自产、库外），provenance 标 OpenClaw workspace 原始路径与归档 commit。
- 虽是自产，非第三方，可不走 Phase 2.5 的 license 网关；但**复用同一套评估纪律**（Inventory → 域归属 → 映射 → 分批登记），不搞"见熟就直接入库"。
- 与 §13 双 SSOT 风险点直接呼应：已迁入 Hermes 的技能（godot-kb、game-studio、novel-writing 等源自这批）与未来库内登记必须定主从——**库为权威（SSOT），Runtime 技能为派生投影，声明来源可重建**。

### 17.3 转换规则（评估批次要做的事，逐项都需人工 Gate）

1. **去重**：134 → 130 唯一名；跨系列同名/同义（self-improving、design-review、architecture-review 多处出现）合并为单一条目。
2. **域归属裁定**：工程域（Godot 系 ~15、coding、game-studio）→ 对应 Library domain；**非工程域**（awesome-novel 网文、tencent-docs/office、meeting）超出"AI Engineering Library"定位 → 默认**不入**，留原处或标 out_of_scope，等你裁定。
3. **Schema 映射**：`name/description → 同名字段`；正文"何时使用"→ `purpose`；流程段 → `workflow` 逐步抽取为 action_type+target；**必填字段补不齐的（尤其是 `validation_requirements`、`failure_handling`）不登记**——补齐工作即评估工作本身，不允许"先入库再补"。
4. **知识剥离**：知识型技能（godot-knowledge 等）的 API 正文 → 提交 Phase 4 入库批次（走知识入库红线），Skill 本体只留 `required_knowledge` 查询——**这正是你 §6 举的 Godot Debug Skill 违规例的现实版本，迁移时必须现场纠正**。
5. **去平台硬编码**：清除 Hermes/OpenClaw 作为前提的表述；触发词降级为 `examples`；工具依赖（如 `gh` CLI）改写为 `compatible_runtimes.requires` 的能力声明或示例，不作运行必要条件（§14 禁止硬编码）。
6. **风险标注**：触及现实世界的（office/云端操作类）补 `risk_level` 与审批位。

### 17.4 批次建议（红线：禁止一次性 134 项导入，Ingestion 分批人工批准）

| 批次 | 范围 | 规模 | 目的 |
|---|---|---|---|
| 试点 | Godot 工程技能（结构最规整） | ~15 | 验证 §4→SKILL.md 映射与 validator，跑通全流程 |
| 第二批 | coding-series + game-studio | ~60 | 主体工程技能 |
| 第三批 | scholar/art/office 等余量 | ~40 | 含域归属裁定 |
| 裁定项 | 非工程域（novel、腾讯系） | ~30 | **先等你决定入不入**，不预设 |

**结论：134 项语料是 SKILL_REGISTRY 落成后最现成的 Content 消化来源，但它改变不了本设计的结论顺序——必须先有 FCP-001（D1）与目录/schema（D2/D4），才有合法的登记去处；语料迁移本身是独立的分批任务（D5），不随本设计自动启动。**
