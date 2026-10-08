# SKILL_KNOWLEDGE_FINAL_REVIEW — 2026-10-08 BATCH2 最终整理评审

> 机制：**执行时服从裁决 · 发现新问题走 LEARNING_PROPOSAL · 未经验证不改长期知识与架构。**
> 输入：SOURCE_50_UNIT_SET（50，逐文件读取+hash）、HARD CONSTRAINT 24 项、SKILL_CONTRACT_AUDIT.md。

## 一、SOURCE_50_UNIT_SET

count = **50/50**（Registry ingestion_date=2026-10-08 ∩ SKILL_KNOWLEDGE_INGESTION map 交叉核对一致；
每单元记录 sha256_16、source_skill、source_path、current_classification）。HARD 24 项全部命中，0 缺失。

## 二、HARD CONSTRAINT 执行（24/24，未推翻）

| Unit | 裁决分类 | 结果 |
|---|---|---|
| K-SOFTWARE-CODEBASE-MAPPING | RETURN_TO_SKILL | ✅ |
| K-GENERAL-NOVEL-CHAPTER | RETURN_TO_SKILL | ✅ |
| K-AI-NOVEL-PROMPT | RETURN_TO_SKILL | ✅ |
| K-AI-NOVEL-DISPATCH | RETURN_TO_SKILL | ✅ |
| K-GENERAL-ART-BIBLE | RETURN_TO_SKILL | ✅ |
| K-SOFTWARE-AWESOME-NOVEL | RETURN_TO_SKILL | ✅ |
| K-SOFTWARE-BOX | RETURN_TO_SKILL | ✅ |
| K-SOFTWARE-COMFYUI | RETURN_TO_SKILL | ✅ |
| K-SOFTWARE-CODEBASE-MAPPING-002 | KEEP_KNOWLEDGE | ✅ |
| K-AI-PROMPT-AUDIT | KEEP_KNOWLEDGE | ✅ |
| K-AI-PROMPT-AUDIT-002 | KEEP_KNOWLEDGE | ✅ |
| K-AI-SELF-IMPROVING-AGENT | KEEP_KNOWLEDGE | ✅ |
| K-AI-SELF-IMPROVING-AGENT-002 | KEEP_KNOWLEDGE | ✅ |
| K-SOFTWARE-SHOPIFY | KEEP_TOOL_KNOWLEDGE | ✅ |
| K-SOFTWARE-XURL | KEEP_TOOL_KNOWLEDGE | ✅ |
| K-SOFTWARE-TENCENT-CLOUD-COS | KEEP_TOOL_KNOWLEDGE | ✅ |
| K-SOFTWARE-TENCENT-DOCS | KEEP_TOOL_KNOWLEDGE | ✅ |
| K-SOFTWARE-TENCENT-DOCS-002 | KEEP_TOOL_KNOWLEDGE | ✅ |
| K-SOFTWARE-TENCENT-DOCS-003 | KEEP_TOOL_KNOWLEDGE | ✅ |
| K-SOFTWARE-WEIXINPAY-PAY | NEEDS_REVIEW | ✅ |
| K-SOFTWARE-WEIXINPAY-PAY-002 | NEEDS_REVIEW | ✅ |
| K-SOFTWARE-CN-MARKET-DATA-FAILOVER | PROJECT_EXPERIENCE | ✅ || K-ELECTRON-NOVEL-PROOFREAD | KEEP_KNOWLEDGE（主分类）+ DOMAIN_MISCLASSIFIED 标记 | ✅ |
| K-ELECTRON-NOVEL-PROOFREAD-002 | KEEP_KNOWLEDGE（主分类）+ DOMAIN_MISCLASSIFIED 标记 | ✅ |

- RETURN_TO_SKILL 8 个 → Registry `status: REJECTED`（不再作为普通长期知识）+ 溯源链保留：
  `Knowledge Unit → originating Skill → RETURN_TO_SKILL → reason`；**Skill 文件零删除**。
- SELF-IMPROVING-AGENT-002 已按裁决抽象：具体 Skill 名（prd-planner/architecting-solutions/debugger/code-reviewer 等）
  移出知识正文，改为 `Evolution Trigger → Target Skill/Capability → Priority → Proposed Action → Validation` 五列抽象矩阵；
  原始具体映射由 provenance 指回来源技能。
- CN-MARKET-DATA-FAILOVER 落 `project_experience`：observation_date/context/revalidation_required=true/permanent_fact=false。
- 6 个 Tool 单元落 `tool_reference`（tool/platform/version_scope/observed_date/volatility/validation_status），
  validation 一律 UNVALIDATED（未验证不升级为事实）。
- 2 个 WEIXINPAY 单元 → **NEEDS_REVIEW + SECURITY_SENSITIVE**（无安全分类可用 → LP-002）；全批凭据扫描 **0 命中**。
- 2 个 NOVEL-PROOFREAD 单元：**DOMAIN_MISCLASSIFIED** → domain Electronics→General、subdomain→Creative Writing、
  文件迁至 `01_KNOWLEDGE/General/`（误判根因：修仙题材禁用词表里恰有 'PCB/电路/芯片'）→ LP-001。

## 三、其余 26 项自主判断（读取实际内容后裁决）

| Unit | 分类 | 理由 |
|---|---|---|
| K-AI-NOVEL-DISPATCH-002 | RETURN_TO_SKILL | 作者确认关卡是 novel-agent 派发流水线的调度语义（order/phase/step），属 Skill routing |
| K-AI-STYLE-DISTILL | RETURN_TO_SKILL | 蒸馏流水线逐步操作（模板1-13/文件路径），属 Workflow；样本量阈值另作 LP-004 证据 |
| K-AI-TENCENT-MEETING-MCP | RETURN_TO_SKILL | 技能自述概述与反馈路由，Skill 元数据/路由 |
| K-AI-TENCENT-MEETING-MCP-002 | RETURN_TO_SKILL | submit_feedback 的调用时机与流程 = 工具使用流程，非 API 事实 |
| K-AI-WEIXINPAY-FEEDBACK | RETURN_TO_SKILL | 支付反馈路由流程（已扫描无凭据），按支付敏感同源原则回技能 |
| K-GENERAL-NOVEL-CHAPTER-002 | RETURN_TO_SKILL | 主 agent 汇总仲裁规则表，属项目内多 agent 编排 |
| K-GENERAL-NOVEL-MIGRATE | RETURN_TO_SKILL | 迁移步骤失败恢复表，步骤绑定的故障处理流程 |
| K-GENERAL-SHORT-VERIFY | RETURN_TO_SKILL | 绑定冻结契约/outline 管线字段的核对清单 |
| K-GENERAL-UPDATER-ARCHIVE | RETURN_TO_SKILL | 归档幂等规程（.done 标记）项目绑定；幂等模式作 LP-004 证据 |
| K-SOFTWARE-ANYSEARCH | KEEP_TOOL_KNOWLEDGE | anysearch API 场景行为表（匿名/带 key/配额耗尽）为 API 事实 |
| K-SOFTWARE-GODOT-KB | RETURN_TO_SKILL | 技能自身使用规则与查库路由 |
| K-SOFTWARE-NOVEL-ARCHIVE | RETURN_TO_SKILL | 发布前质检清单绑定本管线字段（proofread 版本/body-verify） |
| K-SOFTWARE-NOVEL-OUTLINE | KEEP_KNOWLEDGE | 章纲质量标准（三要素/四类不合格章纲/章节因果链）可脱离管线复用 |
| K-SOFTWARE-NOVEL-REVIEW | RETURN_TO_SKILL | 对照 settings/writing-style 字段的执行度检查流程 |
| K-SOFTWARE-NOVEL-REVIEW-002 | RETURN_TO_SKILL | 对照 character-setting 文件的角色一致性检查流程 |
| K-SOFTWARE-ONE-THREE-ONE-RULE | KEEP_KNOWLEDGE | 1-3-1 决策沟通 Pattern（问题/三选项带利弊/建议）为通用表达模式 |
| K-SOFTWARE-OSINT-INVESTIGATION | RETURN_TO_SKILL | 调用技能自带 fetch 脚本的命令流程（操作步骤非 API 知识） |
| K-SOFTWARE-OSS-FORENSICS | KEEP_TOOL_KNOWLEDGE | GitHub/BigQuery rate limit 数值与条件请求头为 API 参考事实（占位符无真实凭据） |
| K-SOFTWARE-RULES-KNOWLEDGE-BASE | KEEP_KNOWLEDGE | 规则库构建方法论（schema 必填、version_scope 闭集、confidence 按独立来源数）通用 |
| K-SOFTWARE-RULES-KNOWLEDGE-BASE-002 | RETURN_TO_SKILL | 子代理扇出执行规程；其自述复核原则作 LP-004 证据 |
| K-SOFTWARE-SHORT-AUDIT | KEEP_KNOWLEDGE | 规则集审计五项（优先级/去重/一致性/可核对性）= 约束集 QA 方法论（适用范围：规则/契约审计） |
| K-SOFTWARE-SHORT-PLAN | RETURN_TO_SKILL | 短篇构思与排纲的有序步骤流程 |
| K-SOFTWARE-STUDIO-ROLES | RETURN_TO_SKILL | 技能自身角色表（类别 E 元数据） |
| K-SOFTWARE-TENCENT-CLOUD-COS-002 | KEEP_TOOL_KNOWLEDGE | COS action 功能对照表为工具 API 参考 |
| K-SOFTWARE-TENCENT-DOCS-004 | RETURN_TO_SKILL | 技能自身文件目录结构（类别 E 元数据） |
| K-SOFTWARE-VOLUME-WRITING | KEEP_KNOWLEDGE | AI 味空洞表达五模式与速查关键词，通用 AI 写作编辑知识 |

判断顺序按任务 §四执行（内容本质 → 独立复用 → 长期价值 → Workflow/Tool/Project/重复/版本 → 终分类）。
边界执行：绑定 order/step/文件路径/对照字段的流程 → RETURN_TO_SKILL；可脱离管线独立检索复用的规则、
模式、API 事实 → 保留 Knowledge；Tool 操作命令流不伪装成通用知识（OSINT-INVESTIGATION → RETURN_TO_SKILL）。

## 四、最终计数

```yaml
KEEP_KNOWLEDGE: 12   # 5 HARD + 5 AI + 2 DOMAIN修正
KEEP_TOOL_KNOWLEDGE: 9   # 6 HARD + 3 AI
RETURN_TO_SKILL: 26   # 8 HARD + 18 AI
PROJECT_EXPERIENCE: 1
REJECT: 0
NEEDS_REVIEW: 2
POTENTIAL_CAPABILITY: 0   # 本轮未发现新的可执行能力候选；未创建任何 Capability
```

## 五、学习机制

6 条 **LEARNING_PROPOSAL（全部 PROPOSED，0 ADOPTED）**：域分类启发式误判（LP-001）、安全分类缺失（LP-002）、
Project Experience 类型缺失（LP-003）、从 Workflow 抽象通用原则的通道（LP-004）、tool_reference 字段结构（LP-005）、
抽取前置边界门（LP-006，证据：50 中 26 个返工）。详见 `SKILL_KNOWLEDGE_LEARNING_PROPOSALS.yaml`。

## 六、结论

执行稳定（幂等重跑 50 SKIP）、发现开放（6 提案待审）、学习可追踪（每单元 curation.decided_by/reason）、
长期知识未越权（0 升级 Active/Validated）、Foundation 受保护（git 复核 0 触碰）。
**STATUS: PASS**
