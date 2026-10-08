# K-SOFTWARE-TENCENT-CLOUD-COS-002 — 功能对照表

- **Domain**: Software / General | **Type**: Concept
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-028（Agent Skill: tencent-cloud-cos）| **Extracted**: 2026-10-08

## 知识正文

| 分类 | action | 说明 |
|------|--------|------|
| **存储** | `upload` | 上传文件 |
| | `put-string` | 上传字符串 |
| | `download` | 下载文件 |
| | `list` | 列出文件 |
| | `sign-url` | 获取签名链接 |
| | `delete` | 删除文件 |
| | `delete-multiple` | 批量删除 |
| | `head` | 文件元信息 |
| | `copy-object` | 复制对象 |
| **存储桶管理** | `list-buckets` | 列出所有存储桶 |
| | `create-bucket` | 创建存储桶 |
| | `head-bucket` | 检查存储桶是否存在 |
| | `get-bucket-acl` / `put-bucket-acl` | ACL 权限管理 |
| | `get-bucket-cors` / `put-bucket-cors` | 跨域配置 |
| | `get-bucket-tagging` / `put-bucket-tagging` | 标签管理 |
| | `get-bucket-versioning` | 查询版本控制 |
| | `get-bucket-lifecycle` | 查询生命周期 |
| | `get-bucket-location` | 查询存储桶地域 |
| **图片基础** | `image-info` | 图片元信息 |
| | `image-thumbnail` | 缩放 |
| | `image-crop` | 裁剪 |
| | `image-rotate` | 旋转 |
| | `image-format` | 格式转换 |
| | `watermark-font` | 文字水印 |
| **AI图片** | `assess-quality` | 质量评估 |
| | `ai-super-resolution` | 超分辨率 |
| | `ai-pic-matting` | 智能裁剪 |
| | `ai-qrcode` | 二维码识别 |
| **内容识别** | `recognize-image` | 图片标签识别 |
| | `ocr-general` | OCR 文字识别 |
| **文档处理** | `create-doc-to-pdf-job` | 文档转 PDF |
| | `describe-doc-job` | 查询文档任务 |
| | `doc-preview` | 文档预览（转图片） |
| | `doc-preview-html-url` | 文档在线预览链接 |
| **媒体处理** | `create-media-smart-cover-job` | 智能封面 |
| | `describe-media-job` | 查询媒体任务 |
| | `media-transcode-job` | 视频转码 |
| | `media-snapshot` | 视频截帧 |
| | `media-info` | 媒体文件信息 |
| **内容审核** | `audit-image` | 图片同步审核 |
| | `audit-image-job` | 图片异步审核 |
| | `audit-video-job` | 视频审核 |
| | `audit-audio-job` | 音频审核 |
| | `audit-text-job` | 文本审核 |
| | `audit-document-job` | 文档审核 |
| | `describe-audit-job` | 查询审核结果 |
| **智能语音** | `speech-recognition-job` | 语音识别 |
| | `tts-job` | 语音合成 |
| | `noise-reduction-job` | 音频降噪 |
| | `voice-separate-job` | 人声分离 |
| **文件处理** | `file-hash` | 哈希计算 |
| | `file-compress-job` | 文件压缩 |
| | `file-uncompress-job` | 文件解压 |
| | `describe-file-job` | 查询文件任务 |
| **MetaInsight 管理** | `list-datasets` | 列出数据集 |
| | `create-dataset` | 创建数据集 |
| | `describe-dataset` | 查询数据集详情 |
| | `create-dataset-binding` | 绑定存储桶 |
| | `describe-dataset-bindings` | 查询绑定关系 |
| **MetaInsight 索引** | `create-file-meta-index` | 创建文件索引 |
| | `describe-file-meta-index` | 查询文件索引 |
| | `delete-file-meta-index` | 删除文件索引 |
| **MetaInsight 检索** | `image-search-pic` | 以图搜图 |
| | `image-search-text` | 文本搜图 |
| | `face-search` | 人脸搜索 |
| | `dataset-simple-query` | 元数据检索 |
| | `hybrid-search` | 多模态检索（文档检索） |
| **通用** | `ci-request` | 调用任意 CI API |
| **🚀 知识库** | `create-knowledge-base` | "创建知识库" → 一键创建桶+数据集+绑定 |
| | `upload` → 指向知识库桶 | "上传到知识库" → 上传文档 |
| | `hybrid-search` → 指向知识库数据集 | "查询知识库" → 语义检索文档内容 |
| **🚫 禁止** | ~~deleteBucket~~ | **不允许删除/清空存储桶** |
| **🔐 凭证管理** | `encrypt-env` | 加密 .env → .env.enc 并删除明文 |
| | `decrypt-env` | 解密 .env.enc → .env 还原明文 |

## Provenance

- source_skill_id: `SKILL-GEN-TENCENT-CLOUD-COS`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/skills/@shawnminh/tencent-cos-skill/SKILL.md`
- source_name: `tencent-cloud-cos`
- original_section: `功能对照表`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
