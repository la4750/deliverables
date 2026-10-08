# K-SOFTWARE-TENCENT-DOCS — tencent-docs: 核心规则

- **Domain**: Software / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: medium | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-003（Agent Skill: tencent-docs）| **Extracted**: 2026-10-08

## 知识正文

- **🚨 所有 PPT / 幻灯片任务统一走 Slide 工作流**：用户提供 `https://docs.qq.com/slide/<id>` 链接、或提及 "PPT / 幻灯片 / 演示文稿 / slide / 投影片" 等任何与 PPT 相关的需求（包括 0-1 生成整份、续写、加页、改页、删页、检查），**必须**按 `slide/entry.md` 的工作流执行：先跑状态脚本 → 必要时写 DESIGN → 用 `slide-mcp` 服务的 `slide_*` 工具落地（API Schema 详见 `references/slideengine_references.md`）。**严禁**用 `doc_*`（docengine）或 `tencent-docs` 主服务的通用工具去改 PPT —— 它们不支持 slide 内部结构（shape_id / page_index / 母版等），返回的内容 / 行为均不正确。
- **文档编辑与新建**：使用`manage.query_file_info`或者`文档链接前缀`获取文档类型，根据文档类型优先使用对应的工具集，可参考**场景路由表**
- **优先批量写入，避免多次重复调用**：当对同一文档存在**连续 3 次及以上**的数据写入（如向智能表格写多行记录、向 sheet 写多个单元格/区域、向文档插入多段内容等）时，**必须**使用对应工具的**批量写入接口**一次性提交（如 `smartsheet.add_records` / `smartsheet.update_records`、`sheet.set_range_value`、批量插入类工具），**严禁**用单条写入接口循环多次调用。批量调用可减少往返次数、降低限流与积分消耗、保证写入原子性。具体批量接口以各品类参考文档（场景路由表中对应文档）的 Schema 为准。
- **用户需要保存/上传Markdown格式内容**：直接填入 `create_smartcanvas_by_mdx` 的 `mdx` 参数，MDX 已向下兼容全部 Markdown 语法，无需转换，也无需切换 `content_format`
- **用户有本地文件保存/沉淀/落盘**：一律使用 `import_file.sh` → `manage.async_import` → `manage.import_progress` 统一上传通路，保留原文件结构，不要用 `create_*` 工具重新生成内容；文件格式是否支持由后端判定，收到"不支持"错误时再降级到其他通路
- **保存/沉淀/落盘/转写类**：用户提出"整理/保存/归档/转写/沉淀/会议纪要"等把当前对话内容落到云端的诉求时，优先使用 `create_smartcanvas_by_mdx`（智能文档 mdx 格式，排版美观、组件丰富）
- **URL 链接**：单独使用 `scrape_url` → `scrape_progress` 网页剪藏通路
- **创建文档支持 `parent_id`**：`create_*_by_markdown` 和 `create_flowchart_by_mermaid` 工具均支持 `parent_id` 参数，可将文档创建到指定目录；不填则在根目录创建。注意：`create_smartcanvas_by_mdx` 不支持 `parent_id` 参数
- **`node_id` 即 `file_id`**：空间节点的 `node_id` 同时也是文档的 `file_id`
- **删除节点需谨慎**：`delete_space_node` 默认仅删除当前节点（`remove_type=current`），使用 `all` 时会递归删除所有子节点
- **Markdown 内容**：使用 UTF-8 格式，特殊字符无需转义
- **OCR 图片识别**：`image_url`（公网 URL）与 `image_base64` 严格二选一；本地图片必须使用 `node ocr.js` 脚本（禁止手动传 base64），详见 `references/ocr_references.md`
- **异步任务使用 spawn 子会话轮询**：`scrape_url`（网页剪藏）等异步任务，推荐使用 spawn 子会话专职轮询，主会话保持响应避免阻塞用户交互
- **不支持的能力必须先上报**：当用户请求的功能在工具列表中找不到对应支持时，静默调用 `report_unsupported_feature` 上报（无需告知用户已上报）。详见 `references/unsupported_feature_reporting.md`

## Provenance

- source_skill_id: `SKILL-GEN-TENCENT-DOCS-2`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/skills/tencent-docs/SKILL.md`
- source_name: `tencent-docs`
- original_section: `核心规则`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
