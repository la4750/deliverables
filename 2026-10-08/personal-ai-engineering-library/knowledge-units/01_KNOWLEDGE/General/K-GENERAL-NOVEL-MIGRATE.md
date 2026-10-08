# K-GENERAL-NOVEL-MIGRATE — novel-migrate: Step 执行失败

- **Domain**: General / Game Design | **Type**: Troubleshooting
- **Version scope**: 未标注（通识） | **Technology**: Python
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-021（Agent Skill: novel-migrate）| **Extracted**: 2026-10-08

## 知识正文

| 步骤 | 失败场景 | 恢复策略 |
|------|---------|---------|
| Step 0（检测） | story.yaml 格式异常/不可解析 | 手动确认目录状态后问作者"检测到疑似旧版项目，但 story.yaml 无法解析。是否继续迁移？" |
| Step 2（挪入 old/） | 文件移动中断（权限/磁盘） | 已移的保留，未移的报具体文件名，提示用 `sudo` 或手动 mv |
| Step 3（init.py） | Python 不可用或脚本报错 | 回退：手动创建目录结构 + `scripts/templates/*.template` → 对应路径去掉 .template |
| Step 4（subagent） | subagent 超时或结果不完整 | 标记失败文件为"待迁移"，继续其他 subagent。最终汇报列出失败清单 |
| Step 4（subagent） | subagent 数量受限 | 按优先级降序：4e > 4g > 4b > 4d > 4a > 4c > 4f。不够并行时串行 |
| Step 5（拷贝正文） | 无 archives/ 目录 | 跳过，标记"无正文" |
| Step 6（验收） | 部分字段为空（旧版无此数据） | 在汇报"待补充字段"中列出，不影响 migrated=true |

## Provenance

- source_skill_id: `SKILL-GAME-NOVEL-MIGRATE`
- source_skill_path: `/home/ubuntu/.hermes/skills/creative/novel-writing/references/skills/migrate/SKILL.md`
- source_name: `novel-migrate`
- original_section: `Step 执行失败`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
