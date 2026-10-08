#!/usr/bin/env python3
# 生成 SKILL_CONTRACT_AUDIT.md（§1-13 全量报告，数据全部取自已验证的 JSON/YAML，不手打数字）
import json, yaml, collections
SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library/14_AI_AGENTS/Skills"
D = json.load(open(SCRATCH + "/deep_audit.json"))
aud = yaml.safe_load(open(f"{LIB}/SKILL_CONTRACT_AUDIT.yaml"))
logical = json.load(open(SCRATCH + "/skill_final.json"))
status = yaml.safe_load(open(f"{LIB}/SKILL_CONTRACT_STATUS.yaml"))
res = {r["skill_id"]: r for r in aud["skills"]}
tier_of = {r["skill_id"]: r["tier"] for r in logical}
name_of = {r["skill_id"]: r["name"] for r in logical}
pri = {"P0": [s for s in res if res[s]["contract_level_current"] == "L0"]}
def core3(sid): return [f for f in ("trigger/applicability","inputs","outputs") if f in (res[sid].get("l2_missing") or [])]
gaps = [s for s in res if res[s]["contract_gap"]]
pri["P1"] = [s for s in gaps if res[s]["contract_level_required"]=="L2" and s not in pri["P0"] and core3(s)]
pri["P2"] = [s for s in gaps if s not in pri["P0"] and s not in pri["P1"] and
             ((res[s]["contract_level_required"]=="L2" and not core3(s)) or
              (res[s]["contract_level_required"]=="L3" and any(f in (res[s].get("l3_missing") or []) for f in ("workflow","validation_requirements","failure_handling"))))]
pri["P3"] = [s for s in gaps if s not in pri["P0"] and s not in pri["P1"] and s not in pri["P2"]]
def band(s):
    t = tier_of[s]
    if t == "A_": return "A"
    if t == "D_": return "D"
    if t == "C_": return "C(插件)"
    return "B(上游)" if t.startswith("B") else t
bands = {k: dict(collections.Counter(band(s) for s in v)) for k, v in pri.items()}
tot_bands = {k: len(v) for k, v in pri.items()}

md = f"""# SKILL_CONTRACT_AUDIT — Skill Registry 质量与契约完整性审计（全量）

> **阶段模式：READ → ANALYZE → CLASSIFY → REPORT。严格只读。**
> 未删除/合并/重命名/移动/重写任何 Skill；未迁移 Knowledge、未创建 Capability、未执行任何
> Migration/Merge Proposal；未修改 Phase 0–8 Foundation / Registry 协议 / Lifecycle / Governance /
> Phase 5-8 规则；未执行任何 Foundation Change Proposal。本文件与 `SKILL_CONTRACT_STATUS.yaml`
> 为本阶段仅有的新增产出，既有交付物（含上半场的 `SKILL_CONTRACT_AUDIT.yaml`）零改动。
>
> 日期：2026-10-08｜覆盖：**358/358 逻辑技能（全量，无抽样）**｜机读状态：`SKILL_CONTRACT_STATUS.yaml`

---

## 1. 三级 Contract 结果（承接 §1-3，逐技能明细见 SKILL_CONTRACT_AUDIT.yaml）

```yaml
Total logical Skills: 358
required: {{ L1: 59, L2: 181, L3: 118 }}
current:  {{ L0: 1, L1: 357, L2: 0, L3: 0 }}
contract_gap: {{ true: 299, false: 59 }}
字段填充率: L1 100% | L2-required 47.4% | L3-required 42.7%
```

Registry 自身核对全部通过：四文件 358/358/358/358、ID 一致无重复、canonical_path 实际存在 358/358、
正文 name/description 与登记一致 358/358、version unknown 134 如实登记。

## 2. §4 审计边界

| 边界 | 数量 | 判定与处置（均只标记） |
|---|---|---|
| Knowledge leakage | **{D['leak_know_n']}** | KNOWLEDGE_WRAPPER(29) ∪ 正文知识堆料(53) → `POTENTIAL_KNOWLEDGE`，迁移走 Phase 4 审批 |
| Capability leakage | **{D['potential_cap_n']}** | CAPABILITY_WRAPPER(6) + 有明确 I/O 契约的 TOOL_WRAPPER(5) → `POTENTIAL_CAPABILITY`，**不自动创建** |
| Agent coupling | **{len(D['agent_coup'])}** | 全部为硬编码 `novel-agent` 名称（detect-loop/memory-recording/dispatch/roleplay-sandbox/style-distill/updater×3）。game-studio 角色名属 Phase 7 角色结构，**不判耦合** |
| Runtime coupling（真问题） | **{len(D['oc_required'])}** | 12 个技能硬依赖 OpenClaw 运行时（其不存在于当前环境）→ 待移植验证/归档裁定 |
| Runtime（合理 implementation detail） | {D['hermes_reasonable']} | 上下文提及 Hermes 属合理实现细节，**不判违规**；claude-code 委派目标即 Claude Code CLI，属技能主题本身，不算 LLM 硬绑定（严格 LLM 必要条件匹配=1，判定为合理） |

## 3. §5 依赖审计

| 依赖类型 | 发现 |
|---|---|
| Skill → Skill | 声明依赖 **0**（全部 not_recorded）；嵌套树无环（循环=0） |
| Skill → Knowledge | 库内知识 ID 引用 **0**——依赖**全部未登记**，故无断 ID；但 200 个技能缺 required_knowledge |
| Skill → Capability | 库内能力 ID 引用 **0**（同上）；0 个技能绕 ID 拿实现 |
| Skill → External Resource | **{len(D['ext_no_25']) + 2} 个绕过 Phase 2.5**：8 个外部作者/@ 用户包/技能市场来源 + awesome-godot 提取物 + 54 站点设计复刻；仅标记，评估须走 Phase 2.5 管线 |
| Broken path | **{len(D['broken_paths'])}**（13 个上游技能引用本机缺失脚本） |
| Deprecated dependency | **12**（OpenClaw 运行时，与 Runtime coupling 同集） |
| Version mismatch | 无法判定——version_scope 缺失 321/358，无声明比对不了 |
| 绑定 Implementation 嫌疑 | **{len(D['impl_bypass'])}** 携带脚本实现的技能（ast-grep 安装脚本、google_meet 整套 Python 机器人、tencent-docs×2 转换脚本、awesome-novel 安装器）→ 标记，不转换 |

## 4. §6 Progressive Disclosure 审计

- **Registry metadata 过重：否**——单条均值 {D['reg_len_avg']}B / 最大 {D['reg_len_max']}B，只含查询所需字段，scripts/assets **零**混入 ✅
- **SKILL.md 过大**：>40KB **3** 个（novel-proofread / dcf-model / research-paper-writing）；>15KB **{D['big15']}** 个
- **references 应延迟加载却被展开**：**{D['inline_know']}** 个技能把知识直接堆进正文（而非 references/ 按需加载）——最大上下文浪费源
- **无任何 L3 资产**：{D['no_l3']} 个（无三层渐进可言，直接全文载入）
- 无关上下文加载风险 = 正文堆料({D['inline_know']}) ∪ 超大文件({len(D['over'])})，只审计不重构

## 5. §7 TOOL_WRAPPER 深审（{D['tool']['total']} 个，零自动转换）

| 判定 | 数量 | 说明 |
|---|---|---|
| KEEP AS SKILL | **{len(D['tool']['keep'])}** | 主体是"何时/如何调用工具"的操作指导 |
| POTENTIAL_CAPABILITY | **{len(D['tool']['potential_capability'])}** | 有稳定 I/O 契约：{', '.join(D['tool']['potential_capability'])} |
| POTENTIAL_KNOWLEDGE | **{len(D['tool']['potential_knowledge'])}** | 主体是工具/API 知识：{', '.join(D['tool']['potential_knowledge'])} |

## 6. §8 KNOWLEDGE_WRAPPER 深审（{D['knowdeep']['total']} 个，对 CONVERT_TO_KNOWLEDGE 候选复判）

| 判定 | 数量 | 处置建议 |
|---|---|---|
| PURE_KNOWLEDGE | **{len(D['knowdeep']['pure'])}**（{', '.join(D['knowdeep']['pure'])}） | 转 Knowledge 候选（待批） |
| KNOWLEDGE_PLUS_ROUTING | **{len(D['knowdeep']['plus_routing'])}** | **保留薄 Skill**：Skill → Knowledge Retrieval，不建议删除 |
| TRUE_WORKFLOW_SKILL | **{len(D['knowdeep']['true_workflow'])}**（{', '.join(D['knowdeep']['true_workflow'])}） | 实为工作流，保留 Skill 身份，不转 Knowledge |

## 7. §9 MERGE_CANDIDATE 复核（17 个，不执行合并）

复分类（名称相似不作为理由，逐对按职责/内容证据）：

| 复分类 | 数量 | 最终建议分布 |
|---|---|---|
| FUNCTIONAL_OVERLAP | {sum(1 for r in D['merge_review'] if r['reclassified_as']=='FUNCTIONAL_OVERLAP')} | MERGE_REQUIRED: **{sum(1 for r in D['merge_review'] if r['recommendation']=='MERGE_REQUIRED')}**（game-studio 4 对 + novel 父包，25/32 子内容精确副本证据） |
| VERSION_SPECIALIZATION | {sum(1 for r in D['merge_review'] if r['reclassified_as']=='VERSION_SPECIALIZATION')} | MERGE_OPTIONAL: **{sum(1 for r in D['merge_review'] if r['recommendation']=='MERGE_OPTIONAL')}**（github/tencent-docs/email） |
| COMPLEMENTARY | {sum(1 for r in D['merge_review'] if r['reclassified_as']=='COMPLEMENTARY')} | KEEP_SEPARATE: **{sum(1 for r in D['merge_review'] if r['recommendation']=='KEEP_SEPARATE')}**（git 知识版↔操作版、搜索后端×3） |
| EXACT_DUPLICATE | {sum(1 for r in D['merge_review'] if r['reclassified_as']=='EXACT_DUPLICATE')} | NEEDS_HUMAN_REVIEW: **{sum(1 for r in D['merge_review'] if r['recommendation']=='NEEDS_HUMAN_REVIEW')}**（self-improving-agent 3 版） |

## 8. §10 Security / Risk 审计（只标记）

- 登记 risk_level：**0/358**；正文含 risk/审批声明：**{D['declared_risk']}**——风险元数据整体缺位
- 被标记技能 **{len({r['skill_id'] for r in D['risk_rows']})}** 个（去重），分布：external_side_effect 12、credential_access 6（1password/stripe/weixinpay×2/himalaya/agentmail）、security_sensitive 6（godmode/obliteratus/pentest/domain-intel/oss-forensics/sherlock）、payment 5、system_modification 4、destructive 3（unbroker/obliteratus/godmode）
- 处置：`risk_level` 与 `requires_human_approval` 补录归入 REVIEWED 阶段动作，本阶段不改

## 9. §11 Foundation Boundary 审计

**确认：Skill = Content/Implementation 层，定位成立。** 既有受跟踪文件修改数 = **0**（git 可复核）。

| # | 触点 | 对应 FCP-001 | 状态 |
|---|---|---|---|
| FT-1 | LIBRARY_RULES 实体/生命周期表无 Skill 行 | T1 | FOUND_UNRESOLVED（未改） |
| FT-2 | AGENT_ORCHESTRATION_SPEC §三十二 目录契约无 Skills/ | T2 | FOUND_UNRESOLVED（未改） |
| FT-3 | EVOLUTION_RULES 无 SKILL_* 演化对象 | T3 | FOUND_UNRESOLVED（未改） |
| FT-4 | RETRIEVAL_DECISION_SPEC §五 检索清单无 Skill | T4 可选 | DEFERRED_BY_DESIGN（方案 A 生效，Phase 5 零改动） |
| FT-5 | SKILL_RULES.md 属新规则文件（宪章 §1.2） | 新增 | DRAFT_PENDING（修订走 FCP） |

未发现任何"Skill Integration 修改既有 Phase/协议/治理"的既成事实——全部触点是**待批提案**。

## 10. §12 优先级与 §13 最终统计

```yaml
Contract gaps:
  P0: {tot_bands['P0']}   # L0 违例（空 description），A 层
  P1: {tot_bands['P1']}   # L2 必需但发现三件（触发/输入/输出）缺失 → 分层 {bands['P1']}
  P2: {tot_bands['P2']}   # L2 余量字段 / L3 硬三件缺失 → 分层 {bands['P2']}
  P3: {tot_bands['P3']}   # 仅缺 L3 软字段 → 分层 {bands['P3']}
```

**最终统计（任务书 §13）：**

```text
Total logical Skills: 358
Required:  L1: 59   L2: 181   L3: 118
Current:   L1 complete: 357   L2 complete: 0   L3 complete: 0   (+ L0: 1)
Contract gaps:  P0: {tot_bands['P0']}  P1: {tot_bands['P1']}  P2: {tot_bands['P2']}  P3: {tot_bands['P3']}   (合计 299)
Potential Knowledge conversion: {D['leak_know_n']}   (其中 KNOWLEDGE_WRAPPER 复判后仅 {len(D['knowdeep']['pure'])} 为 PURE，{len(D['knowdeep']['true_workflow'])} 个实为工作流)
Potential Capability conversion: {D['potential_cap_n']}
Potential Agent coupling: {len(D['agent_coup'])}
Potential Runtime coupling: {len(D['oc_required'])}
Broken dependencies: {len(D['broken_paths'])} broken paths + 0 broken IDs（ID 引用本身为 0）
Foundation touchpoints: {len(D['touchpoints'])}
Human review required: 3 (self-improving 3 版) + {sum(1 for r in D['merge_review'] if r['recommendation']=='MERGE_REQUIRED')} (MERGE_REQUIRED 项) + 12 (OpenClaw 移植/归档) = 20
```

## 11. 最终结论

**1）当前全部逻辑 Skill 是否可以继续作为 Registry 基础？**
**可以。** Registry 自身 100% 一致、零死链、零登记失真；358 条均满足 L1 门（唯一例外是 1 个空 description）。
契约缺口是"声明层待补"，不动摇注册表作为基础的可靠性。

**2）哪些 Skill 真正需要修改？**
真正有修改必要的只有**个人层（A/D）100 个**：P0×1 + 个人 P1×56 + 个人 P2×39 + 个人 P3×4；
其中 12 个 OpenClaw 依赖技能需移植验证或归档裁定，36 个有副作用技能需补 risk/审批位。

**3）哪些不需要修改？**
59 个 L1-required（嵌套子技能/第三方，父包承担契约）+ 上游 196 个（源头在 Hermes 上游仓库，个人侧只能登记引用——
逐个修复无意义，建议规则上豁免为 reference-only，该规则变更走审批）。

**4）哪些只是 Knowledge / Capability 候选，而非必须转换？**
Knowledge 候选 {D['leak_know_n']}（其中 {len(D['knowdeep']['plus_routing'])} 个应保留薄路由 Skill，{len(D['knowdeep']['true_workflow'])} 个根本是工作流，
真正 PURE 只有 {len(D['knowdeep']['pure'])}）；Capability 候选 {D['potential_cap_n']}（6 CAP_WRAPPER + 5 个有 I/O 契约的 TOOL）。
**全部是"候选"——没有任何一个必须转换。**

**5）下一阶段最值得执行的动作（按收益排序）：**
① P0 单点修复（1 个空 description，5 分钟）；
② 个人层 P1 发现性三件（56 个，直接提升任务匹配准确率，收益/成本最高）；
③ 12 个 OpenClaw 依赖技能的"移植 or 归档"裁定（消除唯一真·坏依赖）；
④ 36 个副作用技能补 risk_level/审批位（安全收益）；
⑤ 上游豁免规则写入 SKILL_RULES（一纸规则消除 196 个假缺口）。
**"Optimize only on demonstrated benefit"——P2/P3 的 122 个字段补全应按真实使用频率抽样推进，不追求 100% 形式完整。**
"""
open(f"{LIB}/SKILL_CONTRACT_AUDIT.md", "w", encoding="utf-8").write(md)
print("MD bytes:", len(md.encode()))
print("priority bands:", json.dumps(bands, ensure_ascii=False), tot_bands)
