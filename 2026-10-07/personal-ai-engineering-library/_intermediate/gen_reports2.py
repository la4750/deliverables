#!/usr/bin/env python3
# 生成 SKILL_OPTIMIZATION_REPORT.md + SKILL_RULES.md
import json, collections, yaml, re
SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library/14_AI_AGENTS/Skills"
logical = json.load(open(SCRATCH + "/skill_final.json"))
stats = json.load(open(SCRATCH + "/report_stats.json"))
reg = yaml.safe_load(open(LIB + "/Registry/SKILL_REGISTRY.yaml"))
props = yaml.safe_load(open(LIB + "/SKILL_MIGRATION_PROPOSALS.yaml"))
TODAY = "2026-10-07"
N = len(logical)

# 质量统计
q = collections.Counter()
for r in logical:
    x = r["quality"]
    if not x["has_description"]: q["缺 description"] += 1
    if not x["description_triggers"]: q["触发条件表述弱（L1 发现性不足）"] += 1
    if x["oversized"]: q["SKILL.md 过大(>40KB)"] += 1
    if x["knowledge_heavy"]: q["知识混入（代码/文档堆料、无流程）"] += 1
    if not x["has_inputs"]: q["无明确输入声明"] += 1
    if not x["has_outputs"]: q["无明确输出声明"] += 1
    if not x["has_completion"]: q["无完成条件"] += 1
    if not x["has_validation"]: q["无验证步骤"] += 1
    if not x["references_present"]: q["无 references/scripts/附属文件(L3)"] += 1
    if x["runtime_binding"]: q["正文提及运行时名（hermes/openclaw 等）"] += 1
    if x["llm_binding"]: q["正文提及具体模型名"] += 1
    if x["broken_refs"]: q["含本地路径引用且目标缺失（含示例路径，需人工核实）"] += 1
    if x["deprecated_tool"]: q["提及疑似废弃工具"] += 1
scripts_n = sum(1 for r in logical if r["scripts"])
tf = [(r["name"], r["body_bytes"], r["category"]) for r in logical if "TOO_FINE_CANDIDATE" in r["granularity"] and not r.get("nested_in")]
ovs = [r["name"] for r in logical if "OVERSIZED" in r["granularity"]]
mac = ["apple-notes", "apple-reminders", "findmy", "imessage", "harness-anything-mac"]
acts = props["proposals"]["summary"]

opt_md = f"""# SKILL_OPTIMIZATION_REPORT — 质量检查与优化建议

> 全部为建议，不执行。基准：{N} 个逻辑技能。启发式自动检查 + 抽样人工核实（断链项已核实精度）。
> 生成：{TODAY}

## 1. 质量检查汇总（20 项中可自动化的部分）

| 检查项 | 命中 | 占比 | 解读 |
|---|---|---|---|
""" + "\n".join(f"| {k} | {v} | {v*100//N}% |" for k, v in q.most_common()) + f"""

**要点**：
- **输入/输出/完成条件大面积缺失**（75%/86%/86%）：历史技能为「描述+正文」两段式，无契约化字段——这正是本次
  Registry 以 `not_assessed` 如实登记、不伪造字段的原因；补契约只对个人层（A/D）117 个 KEEP+OPTIMIZE 项逐步做。
- **运行时名提及 232**：绝大多数（B1/B2 195 个）是上游内置技能正文里的合理第一人称（"Hermes does X"），
  不构成硬绑定；**真正需要移植的是 D 层 13 个假定 OpenClaw 运行时的遗产技能**（列 REVIEW_REQUIRED）。
- **具体模型名提及 36**：抽样为示例/对比语境（如 grok/openhands 技能描述自身后端），**未发现"必须用某 LLM"的硬依赖**。
- **断链**：自动命中 102，人工抽样确认多数是示例输出路径（`./out/deck.pdf` 类）；
  **严格口径（指向 ~/.hermes/skills 内部且文件不存在）= 17 处真实缺失**，见 §5。
- **带 scripts 的技能仅 5 个 / 358**——历史技能几乎全是纯文档型，可执行资产极少。

## 2. Progressive Disclosure 三级评估

| 级别 | 要求 | 现状 | 差距 |
|---|---|---|---|
| L1 name+description | 发现即知何时用 | 缺描述 1；触发表述弱 {q['触发条件表述弱（L1 发现性不足）']} | 41% 需重写触发条件（个人层优先） |
| L2 SKILL.md | 只放流程/约束/路由/完成/验证 | 过大 {len(ovs)}（{', '.join(ovs)}）；知识混入 {q['知识混入（代码/文档堆料、无流程）']} | 知识拆出到 references 或 Phase 4 |
| L3 references/scripts/assets | 按需加载 | 无任何附属文件 {q['无 references/scripts/附属文件(L3)']} | 不强制补——薄 TOOL_WRAPPER 属合理形态 |

## 3. 粒度分析

- **过细（独立、非嵌套）**：{len(tf)} 个 —— {', '.join(n for n,_,_ in tf)}
  - `git-helper`（760B，纯命令清单）→ MERGE_CANDIDATE（并入 git-essentials）
  - `godot-*` 知识碎片（~1.5KB 单主题指南）→ 实为**知识过细碎片**，走 CONVERT_TO_KNOWLEDGE 归并
  - 其余（github/tavily-search/impeccable 等）为薄工具/知识卡——**符合 L2 理想形态，不算问题**
  - `game-studio-*` 子工作流虽小但都是父包组件（嵌套），**不算过细**
- **合理粒度**：绝大多数 WORKFLOW_SKILL（如 systematic-debugging 的 输入→分析→检索→修复→验证）
- **过粗**：2 个父包 —— `novel-writing`（32 子）、`game-studio`（25 子）。
  二者是**索引/调度型父技能**（Progressive Disclosure 正当形态），非"Godot Everything"式巨型技能——**不建议拆**；
  `awesome-novel` 是 novel-writing 的重叠父包 → MERGE_CANDIDATE。

## 4. 依赖与绑定健康

- 真实缺失的内部引用（严格口径）：**17 处**，涉及 12 个技能，全部为 B1/B2 上游技能引用本机不存在的脚本/数据：
{chr(10).join(f"  - `{n}` → `{p}`" for n, p in stats['real_missing'])}
- 平台绑定（macOS-only，当前 Linux 环境不可用）：{', '.join(mac)} —— 上游资产，登记时已如实标记，不建议动
- 疑似废弃工具提及：1 处（deprecated_tool 命中）
- OpenClaw 运行时绑定（D 层）：13 个 → REVIEW_REQUIRED（移植验证或归档裁定）

## 5. 高风险技能（question 15）

| 技能 | 风险 | 建议 |
|---|---|---|
| godmode | 越狱类提示技术，安全敏感 | REVIEW_REQUIRED，人工裁定 |
| obliteratus | 移除模型拒绝机制 | REVIEW_REQUIRED，人工裁定 |
| web-pentest / domain-intel / oss-forensics | 攻防类（描述声明 authorized） | KEEP，使用时人工授权门禁 |
| weixinpay-*（3，官方插件） | 真实支付 | KEEP——已有官方 guardrails，风险由插件层控制 |
| 现实世界控制类（机器人/制造） | **0 个** | 当前技能集不含现实世界执行风险 |

## 6. 与 Library Foundation 的职责冲突检查（question 17）

| 冲突点 | 状态 | 处理 |
|---|---|---|
| 29 个 KNOWLEDGE_WRAPPER 与 Phase 4 Knowledge 职责重叠 | 有实质重叠（Godot 知识与已入库 K-SOFTWARE-GODOT-* 直接撞车） | CONVERT_TO_KNOWLEDGE 提案，知识迁移走 Phase 4 分批审批 |
| 16 个 AGENT_WORKFLOW 与 Phase 7 编排职责部分重叠 | 有重叠但层级不同（技能=单任务协作模板，Phase 7=系统级编排） | 保留，登记时标注，Phase 7 采纳前需比对 |
| 6 个 CAPABILITY_WRAPPER 在 Capability Registry 中无对应能力 | 缺口 | CONVERT_TO_CAPABILITY 提案（不自动创建） |
| `ai-engineering-library` 技能 vs LIBRARY_RULES 双重治理 | 潜在 | KEEP，但注明：库治理权威 = 库内规则文件，技能只是门禁速查 |
| 本目录（14_AI_AGENTS/Skills/）未列入 Phase 7 §三十二 契约 | **Foundation 触点（FCP-001 T2）待批** | 目录依用户指令建立；spec 追加修改仍走 FCP，本轮未改任何既有文件 |

## 7. 优化动作汇总（= SKILL_MIGRATION_PROPOSALS.yaml）

| 动作 | 数量 | 含义 |
|---|---|---|
| KEEP | {acts.get('KEEP',0)} | 定位清晰，直接注册 |
| KEEP+OPTIMIZE | {acts.get('KEEP+OPTIMIZE',0)} | 保留，需补触发/输出/验证声明或剥离知识 |
| MERGE_CANDIDATE | {acts.get('MERGE_CANDIDATE',0)} | 与关联技能职责重叠——仅标记 |
| CONVERT_TO_KNOWLEDGE | {acts.get('CONVERT_TO_KNOWLEDGE',0)} | 知识归 Phase 4，技能留薄路由 |
| CONVERT_TO_CAPABILITY | {acts.get('CONVERT_TO_CAPABILITY',0)} | 映射 Capability Registry（提案） |
| REVIEW_REQUIRED | {acts.get('REVIEW_REQUIRED',0)} | 安全敏感/第三方/OpenClaw 绑定，人工裁定 |
| ARCHIVE_CANDIDATE | {acts.get('ARCHIVE_CANDIDATE',0)} | **0——无使用数据支撑归档**（D/B 层无 usage 记录，30 天后再评） |

## 8. CURRENT / TARGET / MIGRATION STATE

**CURRENT STATE**（本轮实测）
- 430 个 SKILL.md 文件 / **358 个逻辑技能**（72 个跨源副本）；来源 6 层；Hermes 顶层加载 27（含 3 插件）
- 注册前库内登记：**0**；本轮后：**358 REGISTERED、0 VALIDATED**
- 真实使用证据仅存在于 Hermes usage：active_use 7、loaded_unused 17、on_disk_inactive 60、not_loaded 272
- 质量：L1 触发弱 41%；无验证声明 58%；知识混入 53；真断链 17；脚本资产 5

**TARGET STATE**（分析导出，非人为压缩）
- 合并获批后逻辑技能 ≈ **346**（−12，全部来自职责重合对；**零删除建议**）
- 26 个知识技能 → Phase 4 候选批次（技能降为薄路由）；6 个能力包装 → Capability 提案
- 117 个个人技能完成 L1/L2 补强；17 处断链修复；13 个 OpenClaw 绑定完成移植裁定
- 数量结论由分析给出：**保留 358→约 346（96.6%），不压缩、不凑整**；若 30 天使用数据显示长期零使用，再以证据提归档

**MIGRATION PLAN**（全部待人工批准，本轮未执行任何一步）
| 阶段 | 内容 | 门禁 |
|---|---|---|
| 0 ✅ | 只读扫描 + 分类 + 注册（本轮回合，纯新增文件） | 已完成 |
| 1 | FCP-001 触点修订（LIBRARY_RULES 实体行 / §32 契约 / 演化类型） | 人工批准 D1 |
| 2 | 17 个 MERGE_CANDIDATE 逐对比对（每对附证据包）→ 择优合并 | 逐对人工批准 |
| 3 | 26 个知识迁移 → Phase 4 入库批次 | 分批人工 Gate |
| 4 | 6 个能力包装 → Capability Registry 评估 | 逐个批准，不自动创建 |
| 5 | 117 个 KEEP+OPTIMIZE 补强 + 17 断链修复 | 批量低风险，按规则执行 |
| 6 | 30 天使用数据复审 → 以证据提归档候选 | 数据支撑 |
"""
open(LIB + "/SKILL_OPTIMIZATION_REPORT.md", "w").write(opt_md)

rules_md = f"""# SKILL_RULES — Skill Registry 登记与治理规则（DRAFT）

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
"""
open(LIB + "/SKILL_RULES.md", "w").write(rules_md)
print("OPTIMIZATION + RULES written")
print("quality table:")
for k, v in q.most_common(): print(f"  {k}: {v}")
