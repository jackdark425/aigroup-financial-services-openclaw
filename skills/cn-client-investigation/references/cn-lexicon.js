// cn-lexicon.js
// 中国大陆客户调查分析的预缓存汉字词典。
// Purpose: avoid MiniMax / small-context models token-level typos in `\uXXXX`
// escape sequences when pptxgenjs slide code is generated.
// Usage (from slide-NN.js):
//   const L = require('../../skills/cn-client-investigation/references/cn-lexicon.js');
//   slide.addText(L.company.cambricon.cn_full, { fontSize: 26, fontFace: "Microsoft YaHei" });
//
// Rule: when you need a Chinese term in slide code, PREFER `require` this file
// and reference its constants. Do NOT inline-type long Chinese strings or
// encode as `\uXXXX` — both routes are typo-prone on MiniMax-M2.7.
//
// Add new entries by editing this file (UTF-8, no BOM) and committing. Do not
// emit entries via agent tool-call JSON; write them via `edit` or `write` on
// this file directly.

'use strict';

const LEXICON = {
  // ---- 业务常用 section headers ----
  sections: {
    executive_summary: '执行摘要',
    company_overview: '公司概览',
    company_positioning: '公司定位',
    management: '管理层',
    shareholder_structure: '股权结构',
    product_matrix: '产品矩阵',
    tech_architecture: '技术架构',
    timeline: '发展时间线',
    market: '市场分析',
    tam_sam_som: '市场规模与国产替代',
    competition: '竞争格局',
    financial: '财务分析',
    financials_history: '财务历史',
    valuation: '估值分析',
    comps: '可比估值',
    risk: '风险分析',
    risk_matrix: '风险矩阵',
    catalysts: '催化剂清单',
    investment_thesis: '投资逻辑',
    investment_highlights: '投资亮点',
    investment_conclusion: '投资结论',
    appendix: '附录',
    disclaimer: '免责声明',
    data_sources: '数据来源',
  },

  // ---- 财务 line items（尤其易错字）----
  finance: {
    revenue: '营业收入',
    gross_profit: '毛利',
    gross_margin: '毛利率',
    operating_profit: '营业利润',
    operating_margin: '营业利润率',
    net_income_attributable: '归属于母公司股东的净利润',
    net_income_nonrecurring_adj: '扣除非经常性损益的净利润',
    net_margin: '净利率',
    ebitda: 'EBITDA',
    rd_expense: '研发费用',
    rd_intensity: '研发费用率',
    selling_expense: '销售费用',
    admin_expense: '管理费用',
    operating_cashflow: '经营活动现金流净额',
    free_cashflow: '自由现金流',
    capex: '资本开支',
    cash_and_equivalents: '货币资金',
    total_assets: '总资产',
    total_liabilities: '总负债',
    equity: '所有者权益',
    debt: '有息负债',
    net_debt: '净有息负债',
    market_cap: '总市值',
    ev: '企业价值',
    ps_ratio: '市销率',
    pe_ratio: '市盈率',
    pb_ratio: '市净率',
    ev_revenue: 'EV/Revenue',
    ev_ebitda: 'EV/EBITDA',
    loss: '亏损',
    deficit: '赤字',
    impairment: '减值',
    amortization: '摊销',
    depreciation: '折旧',
  },

  // ---- 投资建议 & 评级 ----
  rating: {
    overweight: '增持',
    neutral: '中性',
    underweight: '减持',
    buy: '买入',
    sell: '卖出',
    hold: '持有',
    aggressive_coverage: '积极关注',
    initiate_coverage: '首次覆盖',
    maintain_coverage: '维持评级',
    target_price: '目标价',
    target_price_range: '目标价区间',
  },

  // ---- 中国市场 / 监管常用术语 ----
  cn_market: {
    a_share: 'A股',
    star_market: '科创板',
    chinext: '创业板',
    bj_exchange: '北交所',
    main_board: '主板',
    hk_main: '港股主板',
    hk_h_share: 'H股',
    zhongcai_gai: '中概股',
    ipo_cninfo: '招股书',
    annual_report: '年报',
    quarterly_report: '季报',
    prospectus: '招股说明书',
    sse: '上海证券交易所',
    szse: '深圳证券交易所',
    hkex: '香港交易所',
    csrc: '中国证监会',
    entity_list: '美国实体清单',
    export_control: '美国出口管制',
    controlling_shareholder: '实际控制人',
    strategic_investor: '战略投资人',
    state_capital: '国资背景',
    esop: '员工持股计划',
    lock_up_period: '解禁期',
    guochan_tihuan: '国产替代',
    shibazhanlue: '"十四五"规划',
    xinjijianshe: '新基建',
    zhuanjing_tixin: '专精特新',
    smart_compute_center: '智算中心',
    ai_accelerator: 'AI加速卡',
    cuda_compat: 'CUDA兼容',
    self_research: '自研',
  },

  // ---- 目标公司 / 典型 peer（中英 ticker 对齐）----
  // 添加新公司时填齐 cn_full / cn_short / en_full / en_short / ticker / exchange
  company: {
    cambricon: {
      cn_full: '中科寒武纪科技股份有限公司',
      cn_short: '寒武纪',
      en_full: 'Cambricon Technologies Corporation Limited',
      en_short: 'Cambricon',
      ticker: '688256.SH',
      exchange: '上海证券交易所科创板',
    },
    hygon: {
      cn_full: '海光信息技术股份有限公司',
      cn_short: '海光信息',
      en_full: 'Hygon Information Technology',
      en_short: 'Hygon',
      ticker: '688041.SH',
      exchange: '上海证券交易所科创板',
    },
    moore_threads: {
      cn_full: '摩尔线程智能科技（北京）有限责任公司',
      cn_short: '摩尔线程',
      en_full: 'Moore Threads Intelligent Technology',
      en_short: 'Moore Threads',
      ticker: 'N/A',
      exchange: '港交所递表中（2024-11）',
    },
    huawei_hisilicon: {
      cn_full: '华为海思半导体有限公司',
      cn_short: '海思',
      en_full: 'HiSilicon (Huawei)',
      en_short: 'HiSilicon',
      ticker: 'N/A（华为未上市）',
      exchange: '未上市',
    },
    biren: {
      cn_full: '壁仞科技（上海）有限公司',
      cn_short: '壁仞科技',
      en_full: 'Biren Technology',
      en_short: 'Biren',
      ticker: 'N/A',
      exchange: '未上市',
    },
    enflame: {
      cn_full: '上海燧原科技有限公司',
      cn_short: '燧原科技',
      en_full: 'Enflame Technology',
      en_short: 'Enflame',
      ticker: 'N/A',
      exchange: '未上市',
    },
    // —— 加新公司请在这里往下追加 ——
  },

  // ---- 数据源 ----
  data_sources: {
    tushare: 'Tushare Pro',
    cninfo: '巨潮资讯网 cninfo.com.cn',
    sse_official: '上交所官网 sse.com.cn',
    szse_official: '深交所官网 szse.cn',
    hkex_official: '港交所官网 hkex.com.hk',
    tianyancha: '天眼查',
    qichacha: '企查查',
    wind: 'Wind 资讯',
    ths: '同花顺',
    eastmoney: '东方财富',
    caixin: '财新网',
    cls: '财联社',
  },
};

module.exports = LEXICON;
