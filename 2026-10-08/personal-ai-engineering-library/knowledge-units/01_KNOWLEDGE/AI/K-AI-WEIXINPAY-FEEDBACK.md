# K-AI-WEIXINPAY-FEEDBACK — weixinpay-feedback: 适用场景

- **Domain**: AI / AI | **Type**: Troubleshooting
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-019（Agent Skill: weixinpay-feedback）| **Extracted**: 2026-10-08

## 知识正文

用户在使用微信AI支付/AI专属卡过程中遇到无法通过重试或常规引导解决的问题、并希望反馈时使用。按问题类型选择反馈方式：

- **开通 / 绑定过程的问题**（如开通失败、绑定不上）直接展示反馈收集表链接引导手动提交，**不调用工具**（见「开通/绑定问题的反馈方式」）
- **支付 / 管理问题**（如支付失败、扣款异常、余额或 AI专属卡管理问题）调用工具 `weixinpay_feedback` 反馈（见执行流程）
- **用户直接要给微信支付反馈问题**（未明确属于上面哪类）默认走工具反馈

典型情况：

- 绑定、开通流程反复失败或卡住
- 支付点击后无反应、扣款失败或返回未知错误
- 支付技能返回未知错误码或异常输出
- 用户主动要求反馈上述绑定、开通或支付问题

> 连续报错主动引导：当同一环节（开通 / 绑定 / 支付 / 查询）出现连续或反复报错、重试后仍失败时，即使用户没有明确说"反馈"，也应主动提示可通过本技能将问题上报给微信支付团队，并询问用户是否愿意反馈。

## Provenance

- source_skill_id: `SKILL-AI-WEIXINPAY-FEEDBACK`
- source_skill_path: `/home/ubuntu/.hermes/plugins/weixinpay/skills/weixinpay-feedback/SKILL.md`
- source_name: `weixinpay-feedback`
- original_section: `适用场景`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
