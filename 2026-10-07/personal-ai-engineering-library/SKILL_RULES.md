# SKILL_RULES — Skill Registry 登记与治理规则（DRAFT）

> Status: DRAFT — 本文件与 `Skills/` 目录依**用户 2026-10-07 明确指令**建立（Skill Inventory & Registry Registration 任务）。
> 本轮**未修改任何既有文件**；对 `LIBRARY_RULES §2/§11`（实体行）、`AGENT_ORCHESTRATION_SPEC §三十二`（目录契约）、
> `EVOLUTION_RULES §三/五/六/八`（演化对象与提案类型）的追加修订仍走 **FCP-001** 人工批准（见
> `SKILL_INTEGRATION_DESIGN.md §14`），批准前本规则以此 DRAFT 形式生效于本目录内。
> 与 `SKILL_INTEGRATION_DESIGN.md`（Schema/Lifecycle/边界设计）配套阅读；冲突时以设计文档+FCP 结论为准。

## 1. 定位（Registry ≠ 内容）

- Registry 只回答：「我有哪些 Skill？这个 Skill 是什么、在哪、何时适用、需要什么？」
- **技能正文留在原始路径**（Hermes 技能目录 / 遗产库），Registry 以 `skill_id + source_path + canonical_path + copies[]` 建立关系。
- 禁止把 SKILL.md 正文复制进 Registry；`SKILL_INDEX.md` 是派生文件，可由 `SKILL_REGISTRY.yaml` 随时重建（SSOT）。

## 2. skill_id 规则

- 格式：`SKILL-<域码>-<NAME>`，域码 ∈ GAME / AI / AUTO / GEN；NAME 大写、非字母数字折叠为 `-`。
- 唯一、稳定：**与显示名解耦、不随目录移动改变、内容小改不变**；同名异容追加 `-2/-3` 序号。
- 不使用路径作为永久 ID。

## 3. 生命周期（本目录权威词表，独立于 Capability 生命周期）

```
DISCOVERED → REGISTERED → REVIEWED → VALIDATED → ACTIVE → DEPRECATED → SUPERSEDED / ARCHIVED
```

- `DISCOVERED`：扫描入清单（SKILL_INVENTORY.yaml）
- `REGISTERED`：已登记（本目录 Registry）——**「存在于目录」≠「已验证」**
- `VALIDATED`：需真实任务执行的 Validation Evidence（引用 Phase 6 证据）
- `ACTIVE`：验证通过且被实际使用
- Hermes 能加载 ≠ 任何验证状态
- 与 Capability 生命周期**不机械同步**：依赖能力状态由 Phase 5 选时检查

## 4. 登记要求

- 字段无数据就写 `not_assessed / not_recorded / unknown`，**禁止伪造**。
- 每次登记/变更留痕：`last_reviewed`、`provenance.discovered_at`。
- 来源分层（source）：hermes_user_installed / bundled_core / bundled_optional / plugin / legacy_openclaw / third_party / other_local。
- third_party（venv 自带）默认不纳入治理，`usage_status: excluded_dependency`，待裁定。

## 5. 去重与优化纪律

- 只标记（`related_skills` + SKILL_MIGRATION_PROPOSALS），**删除/合并/重写/转换一律需人工批准**。
- 不因名称或关键词相似判重；必须同输入、同输出、同职责才可提合并。
- 不因数量多强制压缩；归档必须有使用数据证据。

## 6. 非硬编码

- Registry 与技能不得把 Hermes/OpenClaw/任一 LLM/模型厂商写成必要条件；`compatible_runtime` 只声明
  `agent_runtime` 接口能力（RUNTIME_INTERFACE §二十四）。运行时名仅可作为来源层（source）事实记录。

## 7. 查询接口（供 Phase 5 / Phase 7）

- Q1（任务→技能）：按 domain + purpose/描述 + status ∈ REVIEWED+ 检索
- Q2（Agent→技能）：按 compatible_agents（待评估后填）+ required_capabilities 检索
- 当前两字段均为 `not_assessed`——**REVIEWED 阶段补齐，不提前伪造**。

## 8. 变更控制

- 修改本规则文件 = 修改登记协议 → 走 FCP-001/相应变更流程。
- Registry 条目数据更新（状态跃迁、关系补全）= Content 级，按本规则自动执行并留痕。
