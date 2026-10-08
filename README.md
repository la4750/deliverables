# Deliverables Archive

按 **产出时间 / 项目来源 / 交付物** 归档的工程交付文档。

```
<产出时间>/<项目来源>/<交付物文件>
```

## 目录

| 时间 | 来源 | 交付物 | 说明 |
|---|---|---|---|
| 2026-10-07 | personal-ai-engineering-library | SKILL_INTEGRATION_DESIGN.md | Skill Integration Design——Agent Skill 与 0–8 架构共存设计 + FCP-001 草案（待人工批准） |
| 2026-10-07 | personal-ai-engineering-library | SKILL_INVENTORY.yaml | 只读全量扫描：430 个 SKILL.md 文件级清单（6 个来源层） |
| 2026-10-07 | personal-ai-engineering-library | SKILL_CLASSIFICATION.yaml | 358 个逻辑技能的 10 类分类（规则打底 + 逐条人工复核） |
| 2026-10-07 | personal-ai-engineering-library | SKILL_REGISTRY.yaml | 正式注册表：358 条 REGISTERED（SSOT，技能正文留在原始路径） |
| 2026-10-07 | personal-ai-engineering-library | SKILL_INDEX.md | 人类可读索引（由 Registry 派生） |
| 2026-10-07 | personal-ai-engineering-library | SKILL_RULES.md | 登记与治理规则（DRAFT，FCP-001 待批） |
| 2026-10-07 | personal-ai-engineering-library | SKILL_OVERLAP_REPORT.md | 重复/重叠分析：72 精确簇、3 同名异容、9 组职责重叠 |
| 2026-10-07 | personal-ai-engineering-library | SKILL_OPTIMIZATION_REPORT.md | 质量检查、粒度分析、CURRENT/TARGET/MIGRATION STATE |
| 2026-10-07 | personal-ai-engineering-library | SKILL_MIGRATION_PROPOSALS.yaml | 358 条处置提案（KEEP/MERGE/CONVERT/REVIEW——仅提案，未执行） |

## 状态声明

- 审计基准：personal-ai-engineering-library @ ec5f983；本轮**零既有文件改动、零删除、零合并、零新建 Skill**。
- 所有迁移/合并/转换均为**提案**，等待人工批准。
- 文档中出现的运行时/模型名均为事实来源记录，非依赖声明（见 SKILL_RULES §6）。

## 2026-10-08/personal-ai-engineering-library/ — Skill Contract Audit（READ-ONLY）

| 文件 | 说明 |
|---|---|
| SKILL_CONTRACT_AUDIT.md | 全量审计报告：L1/L2/L3 契约、边界、依赖、披露、TOOL/KNOWLEDGE 深审、Merge 复核、风险、Foundation 触点、P0–P3、五问结论 |
| SKILL_CONTRACT_AUDIT.yaml | 逐技能 Contract 判定（358 条：required/current/gap/reason + 缺失字段 + 文件核对） |
| SKILL_CONTRACT_AUDIT_REPORT.md | 上半场：契约判定规则、一致性核对、分项达成度 |
| SKILL_CONTRACT_STATUS.yaml | 16 项机读状态汇总 |

### 本批新增（Skill → Knowledge Ingestion，BATCH2）

| 文件 | 说明 |
|---|---|
| SKILL_KNOWLEDGE_INGESTION_REPORT.md | 迁移报告：计数、分布、规则执行、Skill→Knowledge 映射、KGAP 提案 |
| SKILL_KNOWLEDGE_INGESTION.yaml | 358 行逐技能迁移追踪 + 10 项质检 + 映射 |
| KNOWLEDGE_REGISTRY.yaml / SOURCE_REGISTRY.yaml / INGESTION_QUEUE.yaml / KNOWLEDGE_INDEX.md | Phase 4 注册表入库后状态（57 units / 46 sources / BATCH2） |
| knowledge-units/ | 50 个新 Knowledge Unit 内容文件（镜像库内路径） |

## _intermediate/ — 各阶段中间输出（脚本与过程数据）

按产出时间归档，保证每个阶段可复现：

- `2026-10-07/personal-ai-engineering-library/_intermediate/` — Skill Inventory/Classification/Registry/Optimization 阶段：扫描清单、原始/逻辑分类数据、人工复核清单、生成与统计脚本
- `2026-10-08/personal-ai-engineering-library/_intermediate/audit/` — Contract 三级审计与边界/依赖/披露/风险深审计：审计脚本与聚合数据
- `2026-10-08/personal-ai-engineering-library/_intermediate/ingestion/` — Skill→Knowledge 吸收阶段：候选段提取、吸收结果与三段式脚本

### 本批新增（Final Classification & Learning，2026-10-08 第三步）

| 文件 | 说明 |
|---|---|
| SOURCE_50_UNIT_SET.yaml | 执行前 50 单元快照（index/id/source/path/hash，count=50 已验证） |
| SKILL_KNOWLEDGE_FINAL_CLASSIFICATION.yaml | 50 单元最终分类（含 HARD 裁决执行、markers、溯源） |
| SKILL_TO_KNOWLEDGE_MIGRATION_MAP.yaml | 38 个来源技能 → 单元 → 处置的迁移映射 |
| SKILL_KNOWLEDGE_FINAL_REVIEW.md | 评审：HARD 24/24 执行 + 26 项自主判断理由 |
| SKILL_KNOWLEDGE_LEARNING_PROPOSAL(.yaml → LEARNING_PROPOSALS.yaml) | 6 条学习提案（全部 PROPOSED） |
| SKILL_KNOWLEDGE_VALIDATION_REPORT.md | A–M 验证 + 验收（STATUS: PASS） |
| KNOWLEDGE_REGISTRY.yaml / KNOWLEDGE_INDEX.md | 终态（REJECTED 26、域修正 2、tool/project/security 块） |
