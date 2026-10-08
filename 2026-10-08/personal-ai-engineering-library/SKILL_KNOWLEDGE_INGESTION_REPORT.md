# SKILL_KNOWLEDGE_INGESTION_REPORT — Skill → Knowledge 全量吸收报告

> **阶段：READ → ANALYZE → EXTRACT → DEDUPLICATE → INGEST → REGISTER → REPORT（BATCH2）**
> 禁止项全部遵守：0 删除 / 0 合并 / 0 重命名 / 0 移动 / 0 重写技能；0 Capability 迁移；0 Foundation 修改。
> 机读追踪：`SKILL_KNOWLEDGE_INGESTION.yaml`（358 行逐技能）｜日期：2026-10-08

---

## 一、核心计数（任务 §18）

| 指标 | 数量 |
|---|---:|
| 总逻辑 Skill | **358** |
| 已分析 | **358（100%，全量重读正文，不抽样）** |
| 已完成（分析后无可吸收知识） | **320** |
| **Knowledge Unit 新增** | **50** |
| 已复用既有 Knowledge | 0（与既有 7 单元比对无同题） |
| 重复 Knowledge（跨 Skill 同题合并吸收） | **5** 组 |
| 保留 Workflow Skill | **358（零删除，Workflow 全部原位）** |
| POTENTIAL_CAPABILITY（仅标记） | **11**（0 个被创建为 Capability） |
| Needs Review | **13 个技能 / 13 个单元** |
| 未处理 / 失败 | **0 / 0** |
| 新增 Source（SRC-SKILL-*） | 40 |
| 被剔除的 Workflow 段（保留回技能） | 24 |

状态分布（§15 五态）：`KNOWLEDGE_EXTRACTED 25 / NEEDS_REVIEW 13 / COMPLETED 320 / ANALYZED 358 / NOT_PROCESSED 0`

## 二、新 Knowledge Unit 分布

- **Domain**：{'AI': 11, 'Electronics': 2, 'Software': 31, 'General': 6}
- **Type**：{'Constraint': 9, 'Pattern': 5, 'Engineering Rule': 11, 'Troubleshooting': 9, 'API / Specification': 7, 'Principle': 1, 'Concept': 5, 'Reference': 2, 'Procedure': 1}
- **Confidence**：{'medium': 5, 'low': 45}（单技能来源=low、跨 Skill 佐证=medium；全部 `status: Candidate` + `UNVALIDATED`——**导入 ≠ Active**，等待人工 Gate）
- **内容位置**：Godot 相关 → `02_GAME_ENGINES/Godot/Knowledge/`（Engine Isolation §9）；其余 → `01_KNOWLEDGE/<Domain>/`
- **验证**：`tools/validate_knowledge.py` → **PASS（0 error / 131 warning）**；warning = 内部来源无 license、非 semver 版本、存量 7 单元缺 v1.1 字段（既有遗留）

## 三、处理规则执行情况

1. **全量重检**：358 个全部重读；不止 KNOWLEDGE_WRAPPER（仅 6 个候选段来自 KNOWLEDGE_WRAPPER；TOOL_WRAPPER 贡献 API/限制/错误处理段，WORKFLOW_SKILL 贡献规则/排障/经验段）
2. **拆分 A–G**：重点处理 A（Knowledge）；类别 E（Skill 自身结构/身份素材）已过滤；C（Capability 信息）只标记不迁移；Workflow 段剔除回留
3. **Workflow 不转 Knowledge**：24 个纯流程段被剔除；产出的 1 个 Procedure 型单元是"操作规范类知识"而非技能流程
4. **原子化**：以 ##/### 段为界，≤12000 字符/单元；未按行碎片化（§十）
5. **去重**：5 组跨 Skill 同题 → canonical 单元 + 多 source_refs（§十四）；**版本不同的同题不合并**（§九）
6. **来源**：每单元 source_refs 指向 SRC-SKILL-*（Tier 4 内部来源）+ `file://` 技能原文路径 + original_section 锚点（§七/§八，未伪造外部来源）
7. **版本意识**：检测到的版本写入 version_scope；通识类如实标 N/A

## 四、Skill → Knowledge 映射（50 条）

| Knowledge ID | 来源 Skill | Domain | Type | Conf | Review |
|---|---|---|---|---|---|
| K-AI-PROMPT-AUDIT | prompt-audit | AI | Constraint | medium |  |
| K-ELECTRON-NOVEL-PROOFREAD | novel-proofread | Electronics | Pattern | low |  |
| K-SOFTWARE-TENCENT-DOCS | tencent-docs | Software | Engineering Rule | medium |  |
| K-SOFTWARE-WEIXINPAY-PAY | weixinpay-pay | Software | Constraint | low |  |
| K-AI-TENCENT-MEETING-MCP | tencent-meeting-mcp | AI | Troubleshooting | low |  |
| K-SOFTWARE-SHOPIFY | shopify | Software | API / Specification | low |  |
| K-GENERAL-ART-BIBLE | art-bible | General | Troubleshooting | low |  |
| K-SOFTWARE-TENCENT-DOCS-002 | tencent-docs | Software | API / Specification | low |  |
| K-SOFTWARE-TENCENT-DOCS-003 | tencent-docs | Software | Troubleshooting | medium |  |
| K-SOFTWARE-NOVEL-ARCHIVE | novel-archive | Software | Engineering Rule | low |  |
| K-GENERAL-NOVEL-CHAPTER | novel-chapter | General | Constraint | low |  |
| K-AI-NOVEL-PROMPT | novel-prompt | AI | Constraint | low |  |
| K-SOFTWARE-NOVEL-REVIEW | novel-review | Software | Engineering Rule | low |  |
| K-AI-STYLE-DISTILL | style-distill | AI | Engineering Rule | low |  |
| K-SOFTWARE-CN-MARKET-DATA-FAILOVER | cn-market-data-failover | Software | Troubleshooting | low |  |
| K-SOFTWARE-OSS-FORENSICS | oss-forensics | Software | API / Specification | low |  |
| K-AI-TENCENT-MEETING-MCP-002 | tencent-meeting-mcp | AI | Troubleshooting | low |  |
| K-AI-PROMPT-AUDIT-002 | prompt-audit | AI | Constraint | low |  |
| K-SOFTWARE-SHORT-PLAN | short-plan | Software | Principle | low |  |
| K-SOFTWARE-XURL | xurl | Software | API / Specification | low |  |
| K-AI-WEIXINPAY-FEEDBACK | weixinpay-feedback | AI | Troubleshooting | low |  |
| K-SOFTWARE-CODEBASE-MAPPING | codebase-mapping | Software | Engineering Rule | low |  |
| K-GENERAL-NOVEL-MIGRATE | novel-migrate | General | Troubleshooting | low |  |
| K-AI-NOVEL-DISPATCH | novel-dispatch | AI | Concept | low |  |
| K-ELECTRON-NOVEL-PROOFREAD-002 | novel-proofread | Electronics | Pattern | low |  |
| K-SOFTWARE-NOVEL-REVIEW-002 | novel-review | Software | Concept | low |  |
| K-SOFTWARE-GODOT-KB | godot-kb | Software | Engineering Rule | low |  |
| K-SOFTWARE-RULES-KNOWLEDGE-BASE | rules-knowledge-base | Software | Engineering Rule | low |  |
| K-SOFTWARE-COMFYUI | comfyui | Software | API / Specification | low |  |
| K-SOFTWARE-WEIXINPAY-PAY-002 | weixinpay-pay | Software | Engineering Rule | low |  |
| K-SOFTWARE-ANYSEARCH | anysearch | Software | API / Specification | low |  |
| K-AI-SELF-IMPROVING-AGENT | self-improving-agent | AI | Pattern | low |  |
| K-SOFTWARE-TENCENT-CLOUD-COS | tencent-cloud-cos | Software | Reference | low |  |
| K-SOFTWARE-TENCENT-CLOUD-COS-002 | tencent-cloud-cos | Software | Concept | low |  |
| K-SOFTWARE-TENCENT-DOCS-004 | tencent-docs | Software | Engineering Rule | low |  |
| K-SOFTWARE-STUDIO-ROLES | studio-roles | Software | Pattern | low | ⚠ |
| K-SOFTWARE-CODEBASE-MAPPING-002 | codebase-mapping | Software | Troubleshooting | medium |  |
| K-GENERAL-NOVEL-CHAPTER-002 | novel-chapter | General | Constraint | low | ⚠ |
| K-AI-NOVEL-DISPATCH-002 | novel-dispatch | AI | Constraint | low | ⚠ |
| K-SOFTWARE-NOVEL-OUTLINE | novel-outline | Software | Concept | low | ⚠ |
| K-SOFTWARE-SHORT-AUDIT | short-audit | Software | Constraint | low | ⚠ |
| K-GENERAL-SHORT-VERIFY | short-verify | General | Engineering Rule | low | ⚠ |
| K-GENERAL-UPDATER-ARCHIVE | updater-archive | General | Engineering Rule | low | ⚠ |
| K-SOFTWARE-VOLUME-WRITING | volume-writing | Software | Constraint | low | ⚠ |
| K-SOFTWARE-RULES-KNOWLEDGE-BASE-002 | rules-knowledge-base | Software | API / Specification | low | ⚠ |
| K-SOFTWARE-ONE-THREE-ONE-RULE | one-three-one-rule | Software | Pattern | low | ⚠ |
| K-SOFTWARE-OSINT-INVESTIGATION | osint-investigation | Software | Concept | low | ⚠ |
| K-SOFTWARE-BOX | box | Software | Reference | low | ⚠ |
| K-AI-SELF-IMPROVING-AGENT-002 | self-improving-agent | AI | Troubleshooting | medium |  |
| K-SOFTWARE-AWESOME-NOVEL | awesome-novel | Software | Procedure | low | ⚠ |

## 五、Foundation 保护（§21）

**Phase 0–8 零修改**（git 可复核：仅 01_KNOWLEDGE 数据文件追加 + 01_KNOWLEDGE/<Domain>/ 新内容文件 + 14_AI_AGENTS/Skills/ 新报告）。
发现 4 个 Schema 表达缺口，**仅记录 PROPOSAL 不修改**：

| ID | 缺口 | 处置 |
|---|---|---|
| KGAP-1 | 八域枚举无 Game Design/Automation/Office 归属 | subdomain 承载，PROPOSAL 待批 |
| KGAP-2 | 8 项 Skill 溯源字段无专门 schema 字段 | source_refs+notes 承载，PROPOSAL 待批 |
| KGAP-3 | Source type 枚举无 Agent Skill | 用 Other+notes，PROPOSAL 待批 |
| KGAP-4 | validate 强制要求 url，本地文件用 file:// 承载 | PROPOSAL：是否允许 local_path |

## 六、生命周期门（§十七）

50 个新单元全部 `Candidate / UNVALIDATED`。**没有任何单元被标为 Reviewed/Validated/Active。**
人工审核建议顺序：13 个 ⚠ REVIEW 单元 → medium 置信 5 个 → low 单元抽查 → 通过后逐批走 Reviewed → Validated → Active。

## 七、下一步（待人工批准，本阶段不执行）

1. 人工 Gate：审 13 个 REVIEW 单元（域归属/是否真知识）
2. 通过的单元升 Reviewed（Phase 4 既有流程）
3. POTENTIAL_CAPABILITY 11 个 → 独立 Capability 迁移阶段
4. KGAP-1..4 → 决定是否走 Foundation Change Proposal
