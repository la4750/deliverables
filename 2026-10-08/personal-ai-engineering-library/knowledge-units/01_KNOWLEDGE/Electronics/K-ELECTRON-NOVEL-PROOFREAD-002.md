# K-ELECTRON-NOVEL-PROOFREAD-002 — novel-proofread: 11.2 跨章检测项

- **Domain**: Electronics / General | **Type**: Pattern
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-002（Agent Skill: novel-proofread）| **Extracted**: 2026-10-08

## 知识正文

##### 11.2.1 时间线一致性

| 检测模式 | 说明 |
|---------|------|
| 前章 say "三天后"，本章开头说"第二天" | 时间间隔矛盾 |
| 前章是"清晨"，本章开头是"夜深"但无天数跳跃 | 时间跨度过短 |
| 季节/气候突变，与上章结尾无过渡 | 环境断层 |

##### 11.2.2 角色状态连续性

| 检测模式 | 说明 |
|---------|------|
| 前章结尾角色重伤，本章开头活蹦乱跳 | 状态跳跃 |
| 前章角色在某地，本章开头出现在另一地无过渡 | 空间跳跃（瞬移） |
| 前章已消耗/丢失的道具本章又出现 | 物品状态矛盾 |
| 前章已死亡的角色本章又出场 | 角色状态矛盾 |

##### 11.2.3 术语一致性（跨章对比）

- 比对本章的语境词表命中结果与缓存中的 `terms_taken` → 同一条术语在不同章写法不同则标记
- 例：前章用"灵脉"，本章用"真脉" → 标记术语混用

##### 11.2.4 设定信息连续性

- 对照缓存中的 `established_facts` → 本章与之矛盾处逐条标记
- 例：前章确立"主角没有灵识"，本章写"主角用灵识感知" → 标记设定矛盾

##### 11.2.5 道具/物品追踪

- 对照 `items_state` → 上章已被破坏/消耗/遗失的物品本章无故重现 → 标记

##### 11.2.6 角色隐身/瞬移（单章内亦可检测）

- 同一场景中：角色A上场之后未再提及，后续又突然说话/行动
- 正则穷举后确定无法自动检测，需人工精读：注意场景中角色进出是否都有交代

## Provenance

- source_skill_id: `SKILL-GEN-NOVEL-PROOFREAD`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/proofread/SKILL.md`
- source_name: `novel-proofread`
- original_section: `11.2 跨章检测项`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
