# K-SOFTWARE-WEIXINPAY-PAY — 回复前检查清单

- **Domain**: Software / General | **Type**: Constraint
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-005（Agent Skill: weixinpay-pay）| **Extracted**: 2026-10-08

## 知识正文

1. 出现支付信号即调用工具：出现 `WeixinPay-Required` 时立即调用 `weixinpay_pay`，而非将内容复述给用户
2. token 逐字符原样传递：`WeixinPay-Required` 的值须逐字符复制到 `paymentCode`，禁止编码 / 解码 / 大小写转换 / 拼写修正 / 截断
3. 禁止编造状态、禁止主动轮询：不输出"支付成功"、"已扣款"等无依据状态；即时支付需用户在确认链接上自行确认（PC 扫码 / 微信内点击）
4. 区分链接类型：`https://...` 为绑定链接，不可与 `paymentCode` 混淆
5. 出现 `weixin://wxpay/bizpayurl?pr=...` 格式的支付 URL 时不调用 `weixinpay_pay`：本 host 不支持该模式
6. "轻触前往绑定"必须原样输出：工具返回含此文案时，按返回文本原样输出绑定链接给用户，不省略、不改写
7. 仅使用本轮新出现的支付信号，不复用历史凭证
8. 没收到"支付成功"的结果就不声称已支付：本 host 无支付结果查询工具，不得编造核实结果，也不得据此继续履约

## Provenance

- source_skill_id: `SKILL-GEN-WEIXINPAY-PAY`
- source_skill_path: `/home/ubuntu/.hermes/plugins/weixinpay/skills/weixinpay-pay/SKILL.md`
- source_name: `weixinpay-pay`
- original_section: `回复前检查清单`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
