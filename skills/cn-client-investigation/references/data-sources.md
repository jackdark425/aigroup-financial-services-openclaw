# CN Data Sources — 按 tier 的详细调用指南

## T1 — 交易所 / 监管披露（必查，文本权威）

### 巨潮资讯网 cninfo.com.cn

- **用途**：上市公司招股书、年报、季报、重大公告的 PDF 原文
- **Search URL pattern**：`http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=<关键词>`
- **调用方式**：先 `brave-web-search "<公司名> 招股书 cninfo"` 拿 URL，再 `web_fetch` 下载 PDF，用 `pdf` skill / `markitdown` 提文本
- **审计要点**：优先取最近 1-2 年披露版本；注意"草案"（draft）与"正式版"（final）差异

### Tushare Pro（通过 aigroup-market-mcp）

支持的常用 tool 及用途：

| Tool | Purpose | 注意 |
|------|---------|------|
| `aigroup-market-mcp__basic_info` | 公司基础信息（上市日期、行业、注册地、代码） | 部分字段为空，需二次核对 |
| `aigroup-market-mcp__company_performance` | 季度/年度利润表、资产负债表 | 日期格式 YYYYMMDD；注意单季 vs TTM |
| `aigroup-market-mcp__stock_data` | 日线行情（开盘/收盘/成交量/换手） | 大批量需分页 |
| `aigroup-market-mcp__macro_econ` | 宏观指标（CPI/GDP/利率/汇率） | 可用于行业分析背景 |

Token 权限坑：Tushare 对各 api 有 points 要求，某些 api 可能 402 无权限。

### 上交所 / 深交所 / 港交所 官网

- SSE: `www.sse.com.cn` — 科创板和主板披露，重大事项通报
- SZSE: `www.szse.cn` — 创业板和主板
- HKEX: `www.hkex.com.hk` — 港股招股书（IPO prospectus）、年报

## T2 — 工商 / 法律 / 商业 数据库

### 天眼查（tianyancha.com）/ 企查查（qcc.com）

- 股权结构、对外投资、诉讼、专利、招投标
- 如果 `aigroup-tianyancha-mcp` MCP 已装，优先走它；否则 `brave-web-search` + `web_fetch` 公开页
- 未上市公司 / 独角兽（如摩尔线程、壁仞）主要靠这个

### 国家企业信用信息公示系统 gsxt.gov.cn

- 官方工商登记底档
- 适合查实际控制人穿透 / 分支机构 / 行政处罚

## T3 — 第三方数据服务

### Wind / 同花顺 / 东方财富

- 付费服务，本栈不直接调；agent 若遇到数据可用性 gap，可建议用户线下 Wind 查，报告里标 "数据来源 Wind（未直接抓取）"

### FMP / Finnhub（via aigroup-fmp-mcp / aigroup-finnhub-mcp）

- 主要覆盖港股 H 股、中概股 ADR、和海外 peers（NVDA/AMD/INTC）
- 对 A 股覆盖有限，慎用

## T4 — 公开财经媒体

按权威程度排序（仅做补充，不作主数据源）：

| 媒体 | 特点 |
|------|------|
| 财新 caixin.com | 调查深度高，付费墙部分可跳过 |
| 21 世纪经济报道 21jingji.com | 产业观察 |
| 中国证券报 zgjrjw.com | 证监会官媒口径 |
| 上海证券报 cnstock.com | 同上 |
| 财联社 cls.cn | 实时快讯，准确率中等 |
| 澎湃 thepaper.cn | 长文深度 |
| 第一财经 yicai.com | 宏观 |

## 数据 provenance 记录模板

每个报告建一个 `data-provenance.md` 放在 deliverable 目录，格式：

```markdown
# <Company> 数据溯源表

| 指标 | 数值 | 单位 | 期间 | T | 源 | URL / 工具 | 取数时间 | 交叉验证 |
|------|-----|------|------|---|----|-----------|----------|---------|
| 2024Q3 营业收入 | 5.2 | 亿RMB | 2024-07 至 2024-09 | T1 | 巨潮资讯 2024Q3 业绩快报 | http://... | 2026-04-18 | Tushare company_performance OK ±0.5% |
| 最新市值 | 825 | 亿RMB | 2026-04-17 | T1 | Tushare stock_data | aigroup-market-mcp__stock_data | 2026-04-18 | 东方财富网页 OK |
| 2024 研发费用 | 8.3 | 亿RMB | 2024 全年（估算） | T3 | 研报推算 | 分析师电话会议 2024-12 | 2026-04-18 | 单源估算 |
| 实际控制人 | 陈天石、陈云霁 | — | 最新 | T1 | 招股书 2020 | http://... | 2026-04-18 | 天眼查 OK |
```

所有报告内出现的**硬数字** MUST 有一行 provenance 条目。估算/单源数据必须在报告页脚标注。
