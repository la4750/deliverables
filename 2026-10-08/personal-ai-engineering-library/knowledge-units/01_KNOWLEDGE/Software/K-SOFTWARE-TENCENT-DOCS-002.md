# K-SOFTWARE-TENCENT-DOCS-002 — tencent-docs: 注意事项

- **Domain**: Software / General | **Type**: API / Specification
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-009（Agent Skill: tencent-docs）| **Extracted**: 2026-10-08

## 知识正文

- **默认使用 smartcanvas**：除非用户明确指定其他格式，否则**新增文档**时优先使用 `create_smartcanvas_by_markdown`；**编辑已有智能文档**时使用 `smartcanvas.*` 系列工具
- **创建文档时支持 `parent_id`**：所有 `create_*_by_markdown` 和 `create_flowchart_by_mermaid` 工具均支持 `parent_id` 参数，可将文档直接创建到指定目录；不填则在根目录创建
- **删除节点**：`delete_space_node` 默认仅删除当前节点（`remove_type=current`），使用 `all` 时会递归删除所有子节点，需谨慎
- Markdown 内容使用 UTF-8 格式，特殊字符无需转义
- 幻灯片必须遵循层级结构，每页包含 2-4 个段落标题
- 分页查询每页返回 20-40 条记录，使用 `has_next` 判断是否有更多
- `node_id` 同时也是文档的 `file_id`
- `create_flowchart_by_mermaid` 的 mermaid 内容必须全部使用英文
- **智能文档元素操作**：`Text`、`Heading`、`Task` 必须挂载在 `Page` 下，`parent_id` 必须为 Page 类型元素 ID；操作前先调用 `smartcanvas.get_top_level_pages` 获取页面结构
- **智能文档分页查询**：`smartcanvas.get_page_info` 使用 `cursor` 分页，`is_over=true` 表示已获取全部内容
- **智能文档删除注意**：删除 Page 元素时，其下所有子元素也会被一并删除
- **智能表格操作**：所有 smartsheet.* 工具都需要 `file_id` 和 `sheet_id`，操作前先调用 `smartsheet.list_tables` 获取 sheet_id
- **字段类型不可更新**：`update_fields` 时 field_type 不能修改，但必须传入原值
- **记录字段值格式**：不同字段类型的值格式不同，详见 `references/smartsheet_references.md` - 字段值格式参考

## Provenance

- source_skill_id: `SKILL-GEN-TENCENT-DOCS`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/Agent/office-agent/skills/tencent-docs/SKILL.md`
- source_name: `tencent-docs`
- original_section: `注意事项`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
