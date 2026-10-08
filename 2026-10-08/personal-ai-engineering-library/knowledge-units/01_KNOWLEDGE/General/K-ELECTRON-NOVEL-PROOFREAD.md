# K-ELECTRON-NOVEL-PROOFREAD — novel-proofread: 6.5.1 语境词表（题材可配置）

- **Domain**: Electronics / General | **Type**: Pattern
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-002（Agent Skill: novel-proofread）| **Extracted**: 2026-10-08

## 知识正文

执行时读取 `settings/writing-style.md` 中的 `context_vocab` 字段（如有）。以下为修仙题材的默认词表（完整版见 `references/context-vocab/xianxia.md`）：

##### 🚫 禁用词（出现即标记）

| 类别 | 禁用词 | 替代词 |
|------|--------|--------|
| 工程类 | 工程/方案/项目/机制/模式/操作/参数/代码/程序/算法 | 阵理/法门/体系/运转/门路/规制/符量/阵诀/阵序/推演法 |
| 科学类 | 科学/公式/数据/分析/物理/实验/概率/结果（作名词） | 阵道/阵式/阵录/推演/天地之理/试阵/天机/阵效 |
| 现代硬件 | PCB/电路/芯片/电池/传感器/系统 | 阵基/阵纹/阵枢/灵源/感灵纹/阵络 |
| 现代抽象 | 反馈/逻辑/模式/版本/配置/更新 | 应和/阵理/法门/版次/定式/更替 |
| 现代身份 | 专家/工程师/技术人员 | 高手/阵师/灵械师/大匠 |
| 现代事务 | 接入/连接/传输/处理/验证 | 引灵/勾连/递送/炼化/校验 |

> **执行说明：** 对话中角色说出现代词不计入——古代语境的角色不会说"接入系统"。**出现必改，不用上报。** 但若禁用词出现在对话中且角色故意用现代词制造效果 → 标记上报。

##### ✅ 术语一致性

| 模式 | 错误 | 正确 |
|------|------|------|
| 核心术语混用 | "真脉"混"灵脉" | 按设定统一 |
| 同一物体/概念多个说法 | 同一章内同一对象3种以上称呼 | 统一为1-2种 |
| 修为/境界名称错位 | 主角修为层级与其他章不一致 | 全文对齐 |
| 专有名称大小写/格式不一致 | "天工坊"写"天工坊"又写"天工坊（残）" | 统一为设定标准格式 |

**做法：** 扫描全文 + 对照 `settings/world-setting.md` 中的核心术语表（如有）+ 读取跨章缓存中的术语快照。不一致 → 直接改。

---

## Provenance

- source_skill_id: `SKILL-GEN-NOVEL-PROOFREAD`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/proofread/SKILL.md`
- source_name: `novel-proofread`
- original_section: `6.5.1 语境词表（题材可配置）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
