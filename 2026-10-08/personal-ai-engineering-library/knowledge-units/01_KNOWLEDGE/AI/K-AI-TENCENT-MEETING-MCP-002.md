# K-AI-TENCENT-MEETING-MCP-002 — tencent-meeting-mcp: 场景7：提交反馈（Agent 意见箱）

- **Domain**: AI / AI | **Type**: Troubleshooting
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-006（Agent Skill: tencent-meeting-mcp）| **Extracted**: 2026-10-08

## 知识正文

**触发条件（强制触发 - 优先级最高）**
Agent 在执行腾讯会议相关任务过程中遇到以下任何情况时，**必须立即暂停当前任务**并主动询问用户是否调用 `submit_feedback` 上报反馈：
- **工具缺失**：用户请求的功能在当前工具集中完全不存在
- **工具报错**：任何工具调用返回非成功状态
- **能力不足**：工具存在但参数限制或功能范围无法满足用户需求
- **结果不符预期**：工具调用成功但返回结果与用户预期明显不一致
- **改进建议**：发现工具集有明显改进空间或新增功能需求

**强制触发机制**
- **立即暂停**：必须立即暂停当前任务流程
- **明确询问**：必须询问用户是否上报反馈
- **二次确认**：必须获得用户明确同意后才调用工具

**详细触发规则**：详见 `references/feedback_rules.md`

**输出规范**
上报成功后，向用户简要告知已记录该反馈（含 `feedback_id`）；用户拒绝或未确认时，告知用户"已取消反馈上报"。

---

## Provenance

- source_skill_id: `SKILL-AI-TENCENT-MEETING-MCP`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/skills/@wemeeting/tencent-meeting-skill/SKILL.md`
- source_name: `tencent-meeting-mcp`
- original_section: `场景7：提交反馈（Agent 意见箱）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
