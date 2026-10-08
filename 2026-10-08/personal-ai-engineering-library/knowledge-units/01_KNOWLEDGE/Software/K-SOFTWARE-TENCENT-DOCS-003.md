# K-SOFTWARE-TENCENT-DOCS-003 — 常见错误码及解决方案

- **Domain**: Software / General | **Type**: Troubleshooting
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: medium | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-009（Agent Skill: tencent-docs）| **Extracted**: 2026-10-08

## 知识正文

| 错误码 | 错误类型 | 解决方案 |
|--------|----------|----------|
| **400006** | **Token 鉴权失败** | 🔑 **检查 Token 配置**：确认 Header 的 key **必须**使用 `Authorization`；同时确认 Token 值正确，可访问 [https://docs.qq.com/open/auth/mcp.html](https://docs.qq.com/open/auth/mcp.html) 重新获取 |
| **400007** | **VIP权限不足** | ⭐ **立即升级VIP**：访问 [https://docs.qq.com/vip?immediate_buy=1?part_aid=persnlspace_mcp](https://docs.qq.com/vip?immediate_buy=1?part_aid=persnlspace_mcp) 购买VIP服务 |
| **-32601** | **请求接口错误** | 🔍 **检查请求工具** 确认调用的工具是否在工具列表中存在 |
｜ **-32603** | **请求参数错误** | 🔍 **检查请求参数**：确认请求参数是否正确，例如`file_id`、`content` 等 |

## Provenance

- source_skill_id: `SKILL-GEN-TENCENT-DOCS`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/Agent/office-agent/skills/tencent-docs/SKILL.md`
- source_name: `tencent-docs`
- original_section: `常见错误码及解决方案`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
