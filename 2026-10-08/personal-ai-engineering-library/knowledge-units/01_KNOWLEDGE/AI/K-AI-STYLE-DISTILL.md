# K-AI-STYLE-DISTILL — 一、主卡蒸馏

- **Domain**: AI / AI | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-014（Agent Skill: style-distill）| **Extracted**: 2026-10-08

## 知识正文

1. 收集样本：项目根 `novel-samples/` 目录下的作者文档（.md/.txt，作者放置）、`.agent/task/style-sample.md`（聊天粘贴）或已归档章节。**少于 6000 字（约 3 章的量）向 novel-agent 说明质量不足可挂起**——1500 字样本句长分布/五层占比统计噪声大、场景卡子样本不足（每类 ≥800 字会大量跳过）；6000-10000 字才能覆盖多场景类型并给出稳定统计。
2. 读 `knowledge/style-distill/prompt-templates/feature-extract.md`（方法论 = 13 模板定义）。
3. 阶段一 拆解（模板 1-4）：对样本逐段/逐句/逐情绪标注（LLM 内部推理，不写文件）。
4. 阶段二 量化（模板 5-8）：频次/五层占比/情绪通道/词汇 → 量化表。
5. 阶段三 建模（模板 9-13）：句式卡/行为树/对话模式/节奏模型/锚点 → 建模规则。
6. 收敛：
   - 量化表 → 卡量化维（案例 1 九维，schema 见 check-agents）
   - 建模规则 → 卡声音层（hard_constraints / soft_guidance / few_shot_examples）
7. 写 `settings/writing-style.md`（收敛卡）+ `settings/style-profiles/analysis/general.md`（量化表 + 建模规则全文）。
8. 备份旧卡到 `settings/.style-versions/v{N}_{YYYY-MM-DD}.md`（N=现有最大+1，卡与分析稿同版本）。
9. confidence：LLM 按样本质量/一致性给 **1-100（必须 >0）**——0 仅用于未蒸馏/手动卡（走定性注入分支，见 prompt-crafting Step 1.1）；蒸馏卡置 0 会静默退回定性注入、丢失量化渲染。`last_updated` 写当日。
10. **生成作者画像**（作者确认用，写入 `settings/style-profiles/analysis/general.md` 顶部「作者画像」节 + 交接报告）：
    - 开头说明定位：**「以下是你文风在 AI 眼里的理解——不是文学评价，AI 会照着这个写。哪里不对直接说。」**
    - **全文用作者语言，不得出现任何内部词**（卡/主卡/场景卡/confidence/维度/override/蒸馏/量化/特征 等）——作者看不懂的都不用：
      - 「你的写作特点」（= 叙事身份，用大白话转述，不抄节名）
      - 「你定的规矩」（= 硬约束，用大白话转述 2-4 条）
      - 「AI 学到的量化感觉 3-5 条」：「短句为主（大多 20 字内）」「对话占比约一半」「白描为主、修辞克制」「你爱用的词：……」
      - 「你的典型句子」2-3 条（few_shot_examples 原文）
    - 结尾确认问句：「读起来像你的写法吗？不像 → 直接说『不像』，我会再学一次。」

## Provenance

- source_skill_id: `SKILL-AI-STYLE-DISTILL`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/style-distill/SKILL.md`
- source_name: `style-distill`
- original_section: `一、主卡蒸馏`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
