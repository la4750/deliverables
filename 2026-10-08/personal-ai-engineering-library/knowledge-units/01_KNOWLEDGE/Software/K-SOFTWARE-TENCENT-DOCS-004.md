# K-SOFTWARE-TENCENT-DOCS-004 — 📁 文件目录结构

- **Domain**: Software / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-003（Agent Skill: tencent-docs）| **Extracted**: 2026-10-08

## 知识正文

```
tencent-docs/
├── SKILL.md                        # 入口文件（本文件），全局导航与核心规则
├── setup.sh                        # 本地安装脚本
├── import_file.sh                  # 文件导入辅助脚本（预导入+上传COS）
├── aipage_pack.js                  # 本地 HTML 打包成 .aipage
├── ocr.js                    # 本地图片 OCR 辅助脚本（本地图片→base64→调用 ocr.* 工具，跨平台）
├── references/                     # 参考文档（按品类/功能划分）
│   ├── auth.md                     # 鉴权与授权流程
│   ├── workflows.md                # 公共接口（get_content）+ 常见工作流
│   ├── aipage_references.md        # 本地 HTML → .aipage 打包 + 导入完整工作流
│   ├── smartsheet_references.md    # 智能表格（smartsheet）操作
│   ├── slideengine_references.md   # 幻灯片 `slide_*` 系列工具完整 API Schema（必须通过独立的 slide-mcp 服务调用，禁止用 doc_ 或 tencent-docs 通用工具改 PPT）
│   ├── diagram_references.md       # 思维导图 + 流程图创建
│   ├── docengine_references.md     # Word 文档精细编辑（doc.* 系列工具，必须通过独立的 doc-mcp 服务调用）
│   ├── space_references.md         # 知识库空间管理（空间/节点/文件夹）
│   ├── manage_references.md        # 文件管理（重命名/移动/删除/复制/导入导出/权限）
│   ├── ocr_references.md           # OCR 图片识别（ocr.extract / ocr.toword / ocr.toexcel）
│   └── unsupported_feature_reporting.md # 不支持能力上报规则（report_unsupported_feature）
├── smartcanvas/                    # 智能文档（smartcanvas）品类模块
│   ├── entry.md                    # 智能文档（smartcanvas）品类入口，创建与编辑。MDX 格式，兼容全部 Markdown 语法
│   └── mdx_references.md           # MDX 格式规范（smartcanvas 内容格式）
├── doc/                            # Word 文档（doc）品类模块
│   ├── entry.md                    # Word 品类入口，工作流指引
│   └── doc_format/                 # Word 格式定义与模板
├── slide/                          # 幻灯片（slide / PPT）品类模块
│   └── entry.md                    # Slide 品类入口（生成 / 续写 / 改页 / 检查 等全工作流，统一走 JSX + slide-mcp）
├── sidebar-pptx-generator/         # Slide 品类工作流的组件规范与脚本
│   ├── references/                 # JSX 组件语法（component-*.md）+ DESIGN.md 编写规范
│   └── scripts/                    # 状态脚本 get_slide_info.sh、slidep 安装脚本 setup.js 等
└── sheet/                          # Excel 文档（sheet）品类模块
    ├── entry.md                    # Sheet 品类入口（sheet.* 工具列表与工作流指引；必须通过独立的 sheet-mcp 服务调用）
    └── api/                        # Sheet 专用 API 定义
```

## Provenance

- source_skill_id: `SKILL-GEN-TENCENT-DOCS-2`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/skills/tencent-docs/SKILL.md`
- source_name: `tencent-docs`
- original_section: `📁 文件目录结构`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
