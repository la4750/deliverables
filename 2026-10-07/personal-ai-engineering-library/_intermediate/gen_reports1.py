#!/usr/bin/env python3
# 生成 SKILL_INDEX.md / SKILL_RULES.md / SKILL_OVERLAP_REPORT.md / SKILL_OPTIMIZATION_REPORT.md
import json, re, collections, yaml, os
SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library/14_AI_AGENTS/Skills"
logical = json.load(open(SCRATCH + "/skill_final.json"))
stats = json.load(open(SCRATCH + "/report_stats.json"))
reg = yaml.safe_load(open(LIB + "/Registry/SKILL_REGISTRY.yaml"))
props = yaml.safe_load(open(LIB + "/SKILL_MIGRATION_PROPOSALS.yaml"))
cls = yaml.safe_load(open(LIB + "/SKILL_CLASSIFICATION.yaml"))
by_id = {s["skill_id"]: s for s in reg["skills"]}
act_by_id = {e["skill_id"]: e for e in props["proposals"]["entries"]}
TODAY = "2026-10-07"

# ---------- SKILL_INDEX.md ----------
rows = []
for s in sorted(reg["skills"], key=lambda x: (x["domain"], x["category"], x["name"])):
    a = act_by_id[s["skill_id"]]["action"]
    rows.append(f"| `{s['skill_id']}` | {s['name']} | {s['domain']} | {s['category']} | {s['source']} | {s['usage_status']} | {a} |")
src = reg["registry"]["totals"]
index_md = f"""# SKILL_INDEX — 个人技能总索引（人类可读）

> 派生索引，权威数据 = `Registry/SKILL_REGISTRY.yaml`（SSOT，可由其重建）。
> 生成日期：{TODAY}｜阶段：DISCOVERED → **REGISTERED**（注册 ≠ 验证；全部 `validation_status: not_validated`）

**总量**：扫描文件 {src['files_discovered']} → 逻辑技能 **{src['logical_skills']}**（合并跨源副本 {src['redundant_copies']} 个）｜
分类：{dict(cls['classification']['counts'])}｜
域：{dict(collections.Counter(s['domain'] for s in reg['skills']))}（Robotics/CAD/Manufacturing/Electronics 当前为 0）

**图例**：source = hermes_user_installed / bundled_core / bundled_optional / plugin / legacy_openclaw / third_party｜
usage = active_use / loaded_unused / on_disk_inactive / not_loaded / excluded_dependency｜
action = KEEP / KEEP+OPTIMIZE / MERGE_CANDIDATE / CONVERT_TO_KNOWLEDGE / CONVERT_TO_CAPABILITY / REVIEW_REQUIRED

| skill_id | name | domain | category | source | usage | proposal |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}
"""
open(LIB + "/SKILL_INDEX.md", "w").write(index_md)

# ---------- SKILL_OVERLAP_REPORT.md ----------
ex = stats["ex"]
ex_lines = "\n".join(f"- {n} — 2 份（规范: 同内容跨源副本）" for n, c, t, k in sorted(ex))
near = []
for k, v in json.load(open(SCRATCH + "/overlap_raw.json"))["same_name"].items():
    near.append((k, len(v), v))
near_lines = "\n".join(f"- **{k}** — {n} 份不同内容（各自演化版本）：\n" + "\n".join(f"    - `{p}`" for p in v) for k, n, v in near)

overlap_md = f"""# SKILL_OVERLAP_REPORT — 重复与重叠分析

> 只标记，不删除、不合并。判定纪律：**不因名称/关键词相似判重**——必须同输入、同输出、同工作流、同职责。
> 方法：内容 sha256 → 精确重复；同名异容 → 版本重叠；职责+输入输出比对 → 功能重叠；目录包含 → 嵌套。
> 生成：{TODAY}

## 1. Exact Duplicate（内容完全相同）：72 簇 / 144 文件 / 72 个冗余副本

- 形态高度一致：**全部为 2 份**，绝大多数是 `legacy_openclaw_workspace ↔ hermes_user_installed` 的迁移对
  （OpenClaw 原件 + 已迁入 Hermes 的副本，内容零差异）——即历史迁移已完成但原件未注销。
- Registry 处理：同一 `skill_id` 下 `canonical_path`（活跃层）+ `copies[]`（原件路径），**不删文件**。
- 簇清单（按规范名）：
{ex_lines}

## 2. Near Duplicate（同名、不同内容）：3 簇 / 7 个逻辑技能

{near_lines}
- 判定：**各自演化版本，非误复制**。github（上游版 vs 遗产版）、tencent-docs（两版描述结构不同）、
  self-improving-agent（3 个不同侧重版本：通用记忆/错误捕获/空描述版）。
- 处置：全部标 `MERGE_CANDIDATE`——需人工比对后择优/合并，**本轮不动作**。

## 3. Functional Overlap（职责相同、内容各自演化）：9 对/组

| 对/组 | 证据（同职责判定） | 处置 |
|---|---|---|
| game-studio-architecture-review ↔ architecture-review | 同一职责：GDD→ADR 追溯矩阵审查，A/D 两系列各一份 | D 侧 MERGE_CANDIDATE |
| game-studio-balance-check ↔ balance-check | 同：游戏平衡数据异常检查 | D 侧 MERGE_CANDIDATE |
| game-studio-design-review ↔ design-review | 同：设计文档完整性/一致性审查 | D 侧 MERGE_CANDIDATE |
| game-studio-qa-plan ↔ qa-plan | 同：Sprint QA 测试计划生成 | D 侧 MERGE_CANDIDATE |
| novel-writing ↔ awesome-novel | 同：小说创作主流程；**awesome-novel 的 32 个子文件与 novel-writing 子技能内容完全相同**（迁移对） | awesome-novel MERGE_CANDIDATE |
| git-essentials ↔ git-helper | 同：git 操作（知识版 + 薄操作版），互补但职责重叠 | git-helper MERGE_CANDIDATE |
| Email Management ↔ email-inbox-triage | 同：收件箱分诊+拟回复（上游 B1 已有对应物） | Email Management MERGE_CANDIDATE |
| tavily-search ↔ anysearch ↔ duckduckgo-search ↔ searxng-search | 同：网页搜索（不同后端） | 遗产侧 2 个 MERGE_CANDIDATE（合并为带 fallback 的单一搜索技能是候选方案，需裁定） |
| godot-kb / godot-knowledge / godot-coding-patterns / 10 个 godot-* 指南 | 同域知识碎片化：Godot 知识散布在 13 个技能中，且与 Phase 4 已入库 7 个 `K-SOFTWARE-GODOT-*` 知识单元重叠 | 全部 CONVERT_TO_KNOWLEDGE（知识归 Phase 4，技能留薄路由） |

## 4. Nested（嵌套结构，属正常父子，不算重复）

- `novel-writing`：32 个子技能（含 D 层副本合并入簇）
- `game-studio`：25 个子技能（D 层同名子技能为内容相同副本，已并入 exact 簇）
- 判定：父 = 索引/调度层，子 = 工作流单元——**Progressive Disclosure 的合理形态**，不建议拆散。

## 5. Complementary（互补，明确不合并）

- 委派外部编码 CLI 家族：claude-code / codex / opencode / openhands / grok / blackbox —— 后端不同，职责不同实例
- 财务工作簿家族：dcf / lbo / comps / merger / 3-statement —— 模型类型不同
- 调试家族：systematic-debugging（方法论）/ python-debugpy / node-inspect-debugger（具体运行时）—— 层次不同
- 文档能力家族：docx / xlsx / pdf / powerpoint —— 格式不同
- 会议家族：google_meet / teams-meeting-pipeline / tencent-meeting-mcp / meeting-action-items —— 平台不同

## 6. 名称相似但**不构成重复**（反例纪律）

difflib 报出 10 对高名称相似（如 test-driven-development ~ spec-driven-development 0.87、
game-studio-create-epics ~ create-stories 0.84）——逐对核对后均为**不同职责**，全部排除出合并建议。

## 7. 汇总判定

| 类型 | 数量 |
|---|---|
| Exact duplicate | 72 簇 / 144 文件（72 冗余） |
| Near duplicate（同名异容） | 3 簇 / 7 技能 |
| Functional overlap | 9 对/组，涉及约 30 技能 |
| Nested（父子） | 2 父包 / 57 子技能 |
| Complementary | ≥5 家族（明确保留） |
| **Independent（无任何关联）** | **267 / 358（74.6%）** |
| 名称相似误报（已排除） | 10 对 |
"""
open(LIB + "/SKILL_OVERLAP_REPORT.md", "w").write(overlap_md)
print("INDEX + OVERLAP written")
