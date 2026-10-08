# K-SOFTWARE-CN-MARKET-DATA-FAILOVER — 数据源层级（2026-07/08 实测）

- **Domain**: Software / General | **Type**: Troubleshooting
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-015（Agent Skill: cn-market-data-failover）| **Extracted**: 2026-10-08

## 知识正文

| 层级 | 源 | 能力 | 限制 |
|---|---|---|---|
| 主 | `push2.eastmoney.com`、`push2his`、数字前缀子域 | 实时行情 + 历史K线 | 风控时全部 http 000 |
| 备1 | `push2delay.eastmoney.com` | **仅实时**行情（clist/get） | kline/get 返回空 `klines:[]`，不可用于历史K线 |
| 备2 | 新浪K线 `quotes.sina.cn/cn/api/jsonp_v2.php/var/CN_MarketDataService.getKLineData?symbol=sz000651&scale=240&ma=no&datalen=120` | 历史K线兜底 | 盘中滞后到上一交易日 |
| 备3 | 新浪行业板块 `vip.stock.finance.sina.com.cn/q/view/newSinaHy.php` | 收盘后仍可用；含领涨股字段 | GBK 编码、JSONP；仅 49 个行业（东财约 100），粒度不一致 |

腾讯板块接口不稳定（参数报错），未纳入层级。板块「上涨/下跌家数、领涨股」是实时快照，**历史无法回溯**，需当前成分股反推。K线直测 curl 可用、urllib 偶发断连（反爬），需带 User-Agent + Referer。

## Provenance

- source_skill_id: `SKILL-GEN-CN-MARKET-DATA-FAILOVER`
- source_skill_path: `/home/ubuntu/.hermes/skills/finance/cn-market-data-failover/SKILL.md`
- source_name: `cn-market-data-failover`
- original_section: `数据源层级（2026-07/08 实测）`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
