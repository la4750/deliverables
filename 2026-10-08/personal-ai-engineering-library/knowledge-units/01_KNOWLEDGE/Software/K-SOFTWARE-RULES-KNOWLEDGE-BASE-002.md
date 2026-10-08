# K-SOFTWARE-RULES-KNOWLEDGE-BASE-002 — rules-knowledge-base: 2. 并行子代理扇出（学习阶段）

- **Domain**: Software / General | **Type**: API / Specification
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-024（Agent Skill: rules-knowledge-base）| **Extracted**: 2026-10-08

## 知识正文

- 用 `delegate_task` 按领域分组（每子代理 1–3 域）并行抓官方资料。任务书必须自带：来源白名单（仅官方，禁博客/SO/AI 内容）、完整 YAML schema 与 id 前缀、条目数量预算（宁缺毋滥）、checkpoint 格式、禁编造 API/版本差异、产出后自验（safe_load + 计数）。
- 每子代理工作流：抓官方页 → 提炼 → 写领域 YAML → 写 checkpoint → 汇报文件清单+条目数。
- **子代理汇报是自述**：父会话必须用脚本重新解析磁盘文件核对计数与字段，不采信摘要数字。
完成标准：全部 checkpoint `status: complete` 且声明数与磁盘实际一致。

## Provenance

- source_skill_id: `SKILL-GEN-RULES-KNOWLEDGE-BASE`
- source_skill_path: `/home/ubuntu/.hermes/skills/software-development/rules-knowledge-base/SKILL.md`
- source_name: `rules-knowledge-base`
- original_section: `2. 并行子代理扇出（学习阶段）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
