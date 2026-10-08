# Knowledge Index

> Status: ACTIVE — Phase 4（BATCH2 Skill→Knowledge Ingestion 完成）
> Knowledge Unit count: 57 | Source count: 46 | Queue count: 2
> Machine registry: `_REGISTRY/KNOWLEDGE_REGISTRY.yaml`
> Rules: `KNOWLEDGE_RULES.md` | Spec: `KNOWLEDGE_INGESTION_SPEC.md`

检索维度（Spec §19）：
Domain / Topic / Technology / Version / Confidence / Source / Capability / Project

---

## By Domain

| Domain | Count |
|---|---:|
| Engineering | 0 |
| Software | 38 |
| AI | 11 |
| Robotics | 0 |
| Mechanical | 0 |
| Manufacturing | 0 |
| Electronics | 2 |
| General | 6 |

## By Confidence

| Confidence | Count |
|---|---:|
| high | 7 |
| medium | 5 |
| low | 45 |

## By Status

| Status | Count |
|---|---:|
| Candidate | 50 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |

## Knowledge Units

| ID | Title | Subdomain | Confidence | Status | Source |
|---|---|---|---|---|---|
| K-SOFTWARE-GDSCRIPT-STATIC-TYPING-001 | GDScript 静态类型系统 |  | high | Reviewed | SRC-GODOT-001 |
| K-SOFTWARE-GODOT-REFCOUNTED-001 | RefCounted 引用计数对象生命周期 |  | high | Reviewed | SRC-GODOT-002 |
| K-SOFTWARE-GODOT-SIGNAL-001 | Signal 信号机制与 Callable 连接 |  | high | Reviewed | SRC-GODOT-003 |
| K-SOFTWARE-GODOT-RESOURCE-001 | Resource 自定义资源与序列化 |  | high | Reviewed | SRC-GODOT-004 |
| K-SOFTWARE-GODOT-DIRACCESS-001 | DirAccess 目录遍历模式 |  | high | Reviewed | SRC-GODOT-005 |
| K-SOFTWARE-GODOT-FILEACCESS-001 | FileAccess 文件读写与游标 |  | high | Reviewed | SRC-GODOT-006 |
| K-SOFTWARE-GODOT-EXPORT-ACCESS-001 | 导出项目的文件访问限制 |  | high | Reviewed | SRC-GODOT-005 |
| K-AI-PROMPT-AUDIT | 维度 H：规则去重（硬门禁） | AI | medium | Candidate | SRC-SKILL-001 |
| K-ELECTRON-NOVEL-PROOFREAD | novel-proofread: 6.5.1 语境词表（题材可配置） | General | low | Candidate | SRC-SKILL-002 |
| K-SOFTWARE-TENCENT-DOCS | tencent-docs: 核心规则 | General | medium | Candidate | SRC-SKILL-003 |
| K-SOFTWARE-WEIXINPAY-PAY | 回复前检查清单 | General | low | Candidate | SRC-SKILL-005 |
| K-AI-TENCENT-MEETING-MCP | tencent-meeting-mcp: 概述 | AI | low | Candidate | SRC-SKILL-006 |
| K-SOFTWARE-SHOPIFY | Storefront API (public read-only) | General | low | Candidate | SRC-SKILL-007 |
| K-GENERAL-ART-BIBLE | art-bible: 阶段 0：解析参数和上下文检查 | Game Design | low | Candidate | SRC-SKILL-008 |
| K-SOFTWARE-TENCENT-DOCS-002 | tencent-docs: 注意事项 | General | low | Candidate | SRC-SKILL-009 |
| K-SOFTWARE-TENCENT-DOCS-003 | 常见错误码及解决方案 | General | medium | Candidate | SRC-SKILL-009 |
| K-SOFTWARE-NOVEL-ARCHIVE | 发布前质检清单（Pre-Publish Checklist） | General | low | Candidate | SRC-SKILL-010 |
| K-GENERAL-NOVEL-CHAPTER | e. 验收（章纲完成后强制执行，全部通过才进提示词生成） | General | low | Candidate | SRC-SKILL-011 |
| K-AI-NOVEL-PROMPT | novel-prompt: Step 2: 按指南填充 9 层 | AI | low | Candidate | SRC-SKILL-012 |
| K-SOFTWARE-NOVEL-REVIEW | 维度 5：写作风格执行度（对照 settings/writing-style.md） | General | low | Candidate | SRC-SKILL-013 |
| K-AI-STYLE-DISTILL | 一、主卡蒸馏 | AI | low | Candidate | SRC-SKILL-014 |
| K-SOFTWARE-CN-MARKET-DATA-FAILOVER | 数据源层级（2026-07/08 实测） | General | low | Candidate | SRC-SKILL-015 |
| K-SOFTWARE-OSS-FORENSICS | API Rate Limiting | General | low | Candidate | SRC-SKILL-016 |
| K-AI-TENCENT-MEETING-MCP-002 | tencent-meeting-mcp: 场景7：提交反馈（Agent 意见箱） | AI | low | Candidate | SRC-SKILL-006 |
| K-AI-PROMPT-AUDIT-002 | 维度 F：去 AI 校验（新增核心维度） | AI | low | Candidate | SRC-SKILL-001 |
| K-SOFTWARE-SHORT-PLAN | short-plan: Phase planning：构思与排纲 | General | low | Candidate | SRC-SKILL-017 |
| K-SOFTWARE-XURL | Raw API Access | General | low | Candidate | SRC-SKILL-018 |
| K-AI-WEIXINPAY-FEEDBACK | weixinpay-feedback: 适用场景 | AI | low | Candidate | SRC-SKILL-019 |
| K-SOFTWARE-CODEBASE-MAPPING | 流程（按序执行） | General | low | Candidate | SRC-SKILL-020 |
| K-GENERAL-NOVEL-MIGRATE | novel-migrate: Step 执行失败 | Game Design | low | Candidate | SRC-SKILL-021 |
| K-AI-NOVEL-DISPATCH | 断点续跑语义 | AI | low | Candidate | SRC-SKILL-022 |
| K-ELECTRON-NOVEL-PROOFREAD-002 | novel-proofread: 11.2 跨章检测项 | General | low | Candidate | SRC-SKILL-002 |
| K-SOFTWARE-NOVEL-REVIEW-002 | 维度 4：角色一致性（对照 settings/character-setting/*.m | General | low | Candidate | SRC-SKILL-013 |
| K-SOFTWARE-GODOT-KB | godot-kb: 使用规则 | Game Design | low | Candidate | SRC-SKILL-023 |
| K-SOFTWARE-RULES-KNOWLEDGE-BASE | rules-knowledge-base: 1. 先立契约，再填内容 | General | low | Candidate | SRC-SKILL-024 |
| K-SOFTWARE-COMFYUI | What's in this skill | General | low | Candidate | SRC-SKILL-025 |
| K-SOFTWARE-WEIXINPAY-PAY-002 | 失败返回与处理 | General | low | Candidate | SRC-SKILL-005 |
| K-SOFTWARE-ANYSEARCH | Scenarios | General | low | Candidate | SRC-SKILL-026 |
| K-AI-SELF-IMPROVING-AGENT | Pattern-Key Taxonomy | AI | low | Candidate | SRC-SKILL-027 |
| K-SOFTWARE-TENCENT-CLOUD-COS | (prelude) | General | low | Candidate | SRC-SKILL-028 |
| K-SOFTWARE-TENCENT-CLOUD-COS-002 | 功能对照表 | General | low | Candidate | SRC-SKILL-028 |
| K-SOFTWARE-TENCENT-DOCS-004 | 📁 文件目录结构 | General | low | Candidate | SRC-SKILL-003 |
| K-SOFTWARE-STUDIO-ROLES | studio-roles: 角色表 | Game Design | low | Candidate | SRC-SKILL-029 |
| K-SOFTWARE-CODEBASE-MAPPING-002 | Pitfalls | General | medium | Candidate | SRC-SKILL-020 |
| K-GENERAL-NOVEL-CHAPTER-002 | 主 agent 汇总 + 仲裁 | General | low | Candidate | SRC-SKILL-011 |
| K-AI-NOVEL-DISPATCH-002 | 作者确认关卡（人铸灵魂，AI 行笔墨） | AI | low | Candidate | SRC-SKILL-022 |
| K-SOFTWARE-NOVEL-OUTLINE | novel-outline: 2.2 拆章节 + 填冲突载体 | General | low | Candidate | SRC-SKILL-030 |
| K-SOFTWARE-SHORT-AUDIT | 审计五项（每项附原文证据） | General | low | Candidate | SRC-SKILL-031 |
| K-GENERAL-SHORT-VERIFY | 十项核对清单 | General | low | Candidate | SRC-SKILL-032 |
| K-GENERAL-UPDATER-ARCHIVE | 二、归档前检查 | General | low | Candidate | SRC-SKILL-033 |
| K-SOFTWARE-VOLUME-WRITING | volume-writing: 9. AI 味自检与去除 | General | low | Candidate | SRC-SKILL-034 |
| K-SOFTWARE-RULES-KNOWLEDGE-BASE-002 | rules-knowledge-base: 2. 并行子代理扇出（学习阶段） | General | low | Candidate | SRC-SKILL-024 |
| K-SOFTWARE-ONE-THREE-ONE-RULE | one-three-one-rule: Example | General | low | Candidate | SRC-SKILL-035 |
| K-SOFTWARE-OSINT-INVESTIGATION | osint-investigation: 2. Acquire data | General | low | Candidate | SRC-SKILL-036 |
| K-SOFTWARE-BOX | Choose the right path | General | low | Candidate | SRC-SKILL-037 |
| K-AI-SELF-IMPROVING-AGENT-002 | Evolution Priority Matrix | AI | medium | Candidate | SRC-SKILL-038 |
| K-SOFTWARE-AWESOME-NOVEL | 各阶段文件读取指南 | General | low | Candidate | SRC-SKILL-040 |

内容文件：Godot/Unity/Unreal → `02_GAME_ENGINES/<Engine>/Knowledge/`（Engine Isolation §9）；其余 → `01_KNOWLEDGE/<Domain>/`

---

## AI Retrieval 要求（Spec §20）

AI 不应"读取整个 Knowledge Library"，而应走管线：

```
用户需求 → Task Classification → Knowledge Retrieval → Capability Retrieval
→ Dependency Retrieval → Implementation Retrieval → Execution
```

Knowledge Retrieval 必须支持：关键词、语义、Domain、Version、Source、Confidence、Related Capability。
