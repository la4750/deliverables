# K-SOFTWARE-NOVEL-ARCHIVE — 发布前质检清单（Pre-Publish Checklist）

- **Domain**: Software / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-010（Agent Skill: novel-archive）| **Extracted**: 2026-10-08

## 知识正文

> 以下为发布前**建议检验项**。不通过不阻断归档（可标注"已知问题"后继续），但发布前必须清零。

| # | 检查项 | 验证方法 | 通过条件 |
|---|--------|---------|---------|
| 1 | proofread 版本号 | 读取 `publish/proofread-history/vol-{N}.md` 中本章记录 | ≥ v3（含） |
| 2 | body-verify 签名 | 检查 chapter.md memo 中是否有 `body_verify: passed` 标记 | 必须有 |
| 3 | 段落合规率 | 读取归档草稿，统计 50-90 字段落占比 | ≥ 95% |
| 4 | 段落合规：首尾段特殊处理 | 首段和尾段允许 30-110 字（宽容区间） | 全部合规或仅首尾超出 |
| 5 | 元数据完整性 | 检查 chapter.md 中 title/date/location/characters 字段 | 非空 |
| 6 | Expression Debt 热点检查 | 如果有 §15 expression-debt 历史，检查是否有 hot 标记未处理 | hot < 3 项或已标注"已知" |
| 7 | PEV 通过 | hit §12 PEV 的章应有 PEV 报告 | 0 处二次缺陷或已修复 |
| 8 | 跨卷锚定未违反 | 检查 canonical-facts.json 中本章是否引入矛盾 | 无新增矛盾 |
| 9 | 卷审校版本号（仅卷完成时） | 检查 review 中该卷完成标志 | 若有则通过 |

**结果处理：**
- 全部通过 → 标记 `pre-publish: ready`
- 部分不通过但已标注"已知问题" → 标记 `pre-publish: aware-issues`，仍可归档
- 关键项（#1/#2）不通过 → **STOP，返回对应流程**

## Provenance

- source_skill_id: `SKILL-GEN-NOVEL-ARCHIVE`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/archive/SKILL.md`
- source_name: `novel-archive`
- original_section: `发布前质检清单（Pre-Publish Checklist）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
