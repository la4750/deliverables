# K-SOFTWARE-CODEBASE-MAPPING — 流程（按序执行）

- **Domain**: Software / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-020（Agent Skill: codebase-mapping）| **Extracted**: 2026-10-08

## 知识正文

1. **定界**：确认目标路径与只读要求。先用非 LLM 脚本清点文件（类型/体积/分类）。分类规则：当前代码按路径；备份区（隐藏目录、backup 命名）；运行产物（日志/导出）；生成物（缓存/元数据）。每类记录理由——不确定就标注，不擅自排除，源文件一律不动。
2. **确定性提取脚本**（stdlib+yaml、只读遍历）：解析入口配置；提取类声明与继承；静态可证的依赖边（preload/require/import）；事件/信号的声明方与发出方；消费方用 grep 补充。结果写 `STRUCTURE_RAW.yaml`——**raw 不整份进上下文**，只打印汇总数字。
3. **聚合成模块表**：每模块 文件数/行数、入度/出度 Top-N、事件 hub、符号消费方——全部从 raw 计算，不再读源文件。
4. **定向深读**：只读中央节点（入口、单例、hub）的文件头注释与关键 grep 行。消费方问题用**一条 `grep -rl` 扫全树**。
5. **产出地图**，结论严格分三层：**已验证**（能指到文件/行或交叉数据）、**推断**（写明依据）、**UNKNOWN / NEEDS_VERIFICATION**（动态接线、运行时挂载、字符串拼接引用——静态证明不了就标注，不按文件名猜）。
6. **落盘三件套**：raw、地图、进度标记（含“已分析/未分析范围”与断点提示），保证任何时刻停止可恢复。

## Provenance

- source_skill_id: `SKILL-GEN-CODEBASE-MAPPING`
- source_skill_path: `/home/ubuntu/.hermes/skills/codebase-mapping/SKILL.md`
- source_name: `codebase-mapping`
- original_section: `流程（按序执行）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
