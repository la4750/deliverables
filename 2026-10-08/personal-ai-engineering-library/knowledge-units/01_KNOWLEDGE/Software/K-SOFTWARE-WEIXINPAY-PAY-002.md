# K-SOFTWARE-WEIXINPAY-PAY-002 — 失败返回与处理

- **Domain**: Software / General | **Type**: Engineering Rule
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-005（Agent Skill: weixinpay-pay）| **Extracted**: 2026-10-08

## 知识正文

失败时工具返回一段可直接展示的错误文本，统一形如 `支付请求失败：<原因>`（`isError=true`）。

处理规则：

1. 原样输出错误文本，不编造原因、不自行重试
2. 用户再次请求支付时，必须使用本轮新出现的支付信号重新调用 `weixinpay_pay`，严禁复用上下文里的旧 `paymentCode`
3. 若用户多次重试仍失败，或用户希望寻求帮助，引导用户用 `weixinpay-feedback` 技能反馈

特殊情况：当返回文本包含"轻触前往绑定"时，表示用户尚未绑定微信支付AI专属卡、系统已自动生成专属绑定链接（此为成功返回，`isError=false`；用户绑定后将自动继续完成本次支付，无需再次发起）。应按返回文本原样输出绑定链接给用户，逐字符不变、保持超链接格式。

## Provenance

- source_skill_id: `SKILL-GEN-WEIXINPAY-PAY`
- source_skill_path: `/home/ubuntu/.hermes/plugins/weixinpay/skills/weixinpay-pay/SKILL.md`
- source_name: `weixinpay-pay`
- original_section: `失败返回与处理`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
