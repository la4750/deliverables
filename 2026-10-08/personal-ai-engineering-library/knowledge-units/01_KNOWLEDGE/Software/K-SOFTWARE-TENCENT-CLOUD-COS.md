# K-SOFTWARE-TENCENT-CLOUD-COS — (prelude)

- **Domain**: Software / General | **Type**: Reference
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-028（Agent Skill: tencent-cloud-cos）| **Extracted**: 2026-10-08

## 知识正文

# 腾讯云 COS 技能

一站式管理腾讯云对象存储(COS)和数据万象(CI)，通过统一的 Node.js SDK 脚本提供以下能力：

- **文件存储**：上传、下载、列出、删除文件，获取签名下载链接，批量操作，复制
- **存储桶管理**：列出/创建存储桶，ACL、跨域、标签、版本控制、生命周期管理
- **图片处理**：缩放、裁剪、旋转、格式转换、文字水印、质量评估、超分辨率、智能裁剪、二维码识别
- **内容识别**：图片标签识别、OCR 文字识别
- **文档处理**：办公文档转 PDF、文档预览（图片/HTML）
- **媒体处理**：视频智能封面、转码、截帧、媒体信息
- **内容审核**：图片/视频/音频/文本/文档违规检测
- **智能语音**：语音识别、语音合成、音频降噪、人声分离
- **文件处理**：哈希计算、压缩、解压
- **智能检索 MetaInsight**：数据集管理、索引管理、以图搜图、文本搜图、人脸搜索、元数据检索、多模态文档检索
- **🚀 知识库**：一键创建知识库（自动创建桶+数据集+绑定），上传文档到知识库，语义检索知识库内容

所有操作通过 `scripts/cos_node.mjs` 单一脚本完成，输出 JSON 格式。

> **请注意**对象存储(COS)与数据万象(CI)均为腾讯云付费服务，使用前请知悉，**使用本 skill 默认视为已知悉并接受相关费用**。具体见官方文档：
> [COS 费用](https://cloud.tencent.com/document/product/436/16871) ｜ [CI 费用](https://cloud.tencent.com/document/product/460/6970)

## Provenance

- source_skill_id: `SKILL-GEN-TENCENT-CLOUD-COS`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/skills/@shawnminh/tencent-cos-skill/SKILL.md`
- source_name: `tencent-cloud-cos`
- original_section: `(prelude)`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
