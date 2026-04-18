---
name: datapack-builder
description: Build professional financial services data packs from various sources including CIMs, offering memorandums, SEC filings, web search, or MCP servers. Extract, normalize, and standardize financial data into investment committee-ready Excel workbooks with consistent structure, proper formatting, and documented assumptions. Use for M&A due diligence, private equity analysis, investment committee materials, and standardizing financial reporting across portfolio companies. Do not use for simple financial calculations or working with already-completed data packs.
---

<!-- Derived from anthropics/financial-services-plugins under Apache-2.0. Modified by AIGroup for OpenClaw compatibility and banker workflow packaging. Not an official Anthropic release. -->


# Financial Data Pack Builder

Build professional, standardized financial data packs for private equity, investment banking, and asset management. Transform financial data from CIMs, offering memorandums, SEC filings, web search, or MCP server access into polished Excel workbooks ready for investment committee review.

## Stable Smoke-Test Path

For OpenClaw smoke tests or any environment where tool routing is flaky, prefer the deterministic script path first:

```bash
python scripts/build_minimal_datapack.py \
  --company "AcmeField" \
  --revenue 45.0 \
  --ebitda-margin 0.22 \
  --vertical "Vertical SaaS" \
  --geography "United States" \
  --xlsx-out /tmp/datapack.xlsx \
  --summary-out /tmp/datapack.md
```

This path is intentionally minimal and is meant to prove the skill can reliably emit a workbook plus a written summary before using more open-ended data collection flows.

For direct OpenClaw use, treat the deterministic script output as the base artifact, not the finished narrative. After the workbook is created, upgrade the markdown deliverable into an internally usable banking coverage note. Do not stop at a two-line smoke summary if the user asked for a usable datapack or briefing.

Execution rules for OpenClaw:

- Use the bundled deterministic script before attempting any free-form Python generation.
- Call Python directly. Do not use `cd ... && python ...`.
- Do not prepend `mkdir`, `mkdir -p`, shell chaining, or any other setup command. The bundled script already creates parent output directories when needed.
- Do not create temporary Python files for the first pass.
- Preferred command shape:

```bash
python scripts/build_minimal_datapack.py \
  --company "TargetCo" \
  --revenue 45.0 \
  --ebitda-margin 0.22 \
  --vertical "Vertical SaaS" \
  --geography "United States" \
  --business-description "Short factual company description for internal banking review." \
  --source-note "State whether the numbers come from filings, management materials, or prompt-supplied assumptions." \
  --contact-rationale "Reason 1|Reason 2|Reason 3" \
  --key-risks "Risk 1|Risk 2|Risk 3" \
  --investment-highlights "Highlight 1|Highlight 2|Highlight 3" \
  --xlsx-out /tmp/datapack.xlsx \
  --summary-out /tmp/datapack.md
```

- Only move to custom scripting after the deterministic script path has failed or the user explicitly asks for a bespoke workbook structure.
- When the prompt already contains company research, banking angle, or risk notes, pass them into the deterministic script via the optional narrative flags instead of dropping them.

Markdown minimum standard after the deterministic script runs:

- Keep the markdown deliverable at the user-requested output path.
- Default to Chinese output unless the user explicitly asks for English.
- Rewrite it into a banker-readable note with these sections when facts are available:
  - Company identity
  - Business description
  - Banking relationship angle
  - Financial context
  - Key risks
  - Investment highlights
  - Preliminary assessment
  - Suggested next steps
- Clearly label assumptions as preliminary if they are not yet validated.
- Do not use phrases such as "fictional facts" or "smoke testing" in user-facing output unless the user explicitly asked for a test artifact.

**Important:** Use the xlsx skill for all Excel file creation and manipulation throughout this workflow.

## CRITICAL SUCCESS FACTORS

Every data pack must achieve these standards. Failure on any point makes the deliverable unusable.

### 1. Data Accuracy (Zero Tolerance for Errors)
- Trace every number to source document with page reference
- Use formula-based calculations exclusively (no hardcoded values)
- Cross-check subtotals and totals for internal consistency
- Verify balance sheet balances: Assets = Liabilities + Equity
- Confirm cash flow ties to balance sheet changes

### 2. ESSENTIAL RULES

**RULE 1: Financial data (measuring money) → Currency format with $**
Triggers: Revenue, Sales, Income, EBITDA, Profit, Loss, Cost, Expense, Cash, Debt, Assets, Liabilities, Equity, Capex
Format: $#,##0.0 for millions, $#,##0 for thousands
Negatives: $(123.0) NOT -$123

**RULE 2: Operational data (counting things) → Number format, NO $**
Triggers: Units, Stores, Locations, Employees, Customers, Square Feet, Properties, Headcount
Format: #,##0 with commas
Negatives: (123) consistent with rest of table

**RULE 3: Percentages (rates and ratios) → Percentage format**
Triggers: Margin, Growth, Rate, Percentage, Yield, Return, Utilization, Occupancy
Format: 0.0% for one decimal place
Display: 15.0% NOT 0.15

**RULE 4: Years → Text format to prevent comma insertion**
Format: Text or custom to prevent 2,024
Display: 2020, 2021, 2022, 2023A, 2024E

**RULE 5: When context is mixed, each metric gets its own appropriate format**
Example:
```
Segment Analysis, 2022, 2023, 2024
Retail Revenue, $50.0, $55.0, $60.0
  Stores, 100, 110, 120
  Revenue per Store, $0.5, $0.5, $0.5
```
Revenue and per-store metrics use $, Store count uses number format.

**RULE 6: Use formulas for all calculations → Never hardcode calculated values**
All subtotals, totals, ratios, and derived metrics must be formula-based, not hardcoded values. This ensures accuracy and allows for dynamic updates.

### 3. Professional Presentation Standards

**Formatting Standards:**

**Color Scheme - Two Layers:**

**Layer 1: Font Colors (MANDATORY from xlsx skill)**
- **Blue text (RGB: 0,0,255)**: ALL hardcoded inputs (historical data, assumptions), NOT normal text
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links to other sheets

**Layer 2: Fill Colors (Optional for enhanced presentation)**
- Fill colors are optional and should only be applied if requested by the user or if enhancing presentation
- If the user requests colors or professional formatting, use this standard scheme:
  - **Section headers**: Dark blue (RGB: 68,114,196) background with white text
  - **Sub-headers/column headers**: Light blue (RGB: 217,225,242) background with black text
  - **Input cells**: Light green/cream (RGB: 226,239,218) background with blue text
  - **Calculated cells**: White background with black text
- Users can override with custom brand colors if specified

**How the layers work together (if fill colors are used):**
- Input cell: Blue text + light green fill = "User-entered data"
- Formula cell: Black text + white background = "Calculated value"
- Sheet link: Green text + white background = "Reference from another tab"

**Font color tells you WHAT it is. Fill color tells you WHERE it is (if used).**

**IMPORTANT:** Font colors from xlsx skill are mandatory. Fill colors are optional - default is white/no fill unless the user requests enhanced formatting or colors.

**Always apply:**
- Bold headers, left-aligned
- Numbers right-aligned
- 2-space indentation for sub-items
- Single underline above subtotals
- Double underline below final totals
- Freeze panes on row/column headers
- Minimal borders (only where structurally needed)
- Consistent font (typically Calibri or Arial 11pt)

**Never include:**
- Borders around every cell
- Multiple fonts or font sizes
- Charts unless specifically requested
- Excessive formatting or decoration

## Structural Consistency
Use the standard 8-tab structure unless explicitly instructed otherwise:
1. Executive Summary
2. Historical Financials (Income Statement)
3. Balance Sheet
4. Cash Flow Statement
5. Operating Metrics
6. Property/Segment Performance (if applicable)
7. Market Analysis
8. Investment Highlights

### Tab 1: Executive Summary
Purpose: One-page overview for busy executives

Contents:
- Company overview (2-3 sentences on business model)
- Key investment highlights (3-5 bullet points)
- Financial snapshot table (Revenue, EBITDA, Growth for last 3 years + projections)
- Transaction overview if applicable
- Key metrics prominently displayed

Format: Clean, bold headers, minimal decoration, critical numbers emphasized

### Tab 2: Historical Financials (Income Statement)
Purpose: Complete profit and loss history

Contents:
- Revenue breakdown by segment/product line
- Cost of goods sold / Cost of revenue
- Gross profit and gross margin %
- Operating expenses detailed (S&M, R&D, G&A)
- EBITDA and Adjusted EBITDA
- Below-the-line items (D&A, interest, taxes)
- Net income

Format:
- Years as columns (text format: 2020, 2021, 2022)
- $ millions or $ thousands (specify units clearly at top)
- Accounting format for all financial data
- Single underline above subtotals, double underline below net income
- Right-align all numbers

### Tab 3: Balance Sheet
Purpose: Financial position at period end

Contents:
- Current assets (cash, AR, inventory, prepaid, other)
- Long-term assets (PP&E, intangibles, goodwill, other)
- Current liabilities (AP, accrued expenses, current portion of debt, other)
- Long-term liabilities (long-term debt, deferred taxes, other)
- Shareholders' equity (common stock, retained earnings, other)

Format:
- Verify formula: Assets = Liabilities + Equity
- Consistent date labeling
- Include working capital calculation
- Single underline above major subtotals, double underline for final totals

### Tab 4: Cash Flow Statement
Purpose: Cash generation and use analysis

Contents:
- Operating cash flow (indirect method preferred)
- Investing cash flow (capex, acquisitions, asset sales)
- Financing cash flow (debt issuance/repayment, equity, dividends)
- Net change in cash
- Beginning and ending cash balances

Format:
- Link to income statement and balance sheet where possible
- Show reconciliation of net income to operating cash flow
- Clear labeling of cash uses (outflows) vs sources (inflows)

### Tab 5: Operating Metrics
Purpose: Non-financial KPIs and operational data

Contents (industry-dependent):
- Unit volumes, customer counts, locations
- Productivity metrics (revenue per employee, per store, per unit)
- Capacity utilization
- Market share
- Customer retention/churn rates
- Industry-specific KPIs

**CRITICAL FORMAT NOTE:**
NO dollar signs on operational metrics. These are quantities, not currency.

Format:
- Clear units specified (customers, employees, stores, square feet, etc.)
- Whole numbers with commas: 1,250 NOT $1,250
- Percentages for rates: 95.0%
- Right-align numbers

### Tab 6: Property/Segment Performance (if applicable)
Purpose: Detailed breakdown by business unit, property, or segment

Contents:
- Revenue and profitability by segment
- Key metrics by location/product
- Segment-specific KPIs
- Comparative performance analysis

Format: Consistent with financial tabs for revenue/EBITDA, number format for operational metrics

### Tab 7: Market Analysis
Purpose: Industry context and competitive positioning

Contents:
- Market size and growth trends
- Competitive landscape overview
- Market share analysis
- Industry benchmarks and peer comparisons
- Regulatory environment if relevant

Format: Mix of narrative text and tables, cite sources for market data

### Tab 8: Investment Highlights
Purpose: Narrative summary of key investment thesis points

Contents:
- Detailed writeup of competitive strengths
- Growth opportunities and strategic initiatives
- Risk factors and mitigation strategies
- Management assessment and track record
- Investment thesis summary

Format: Clear headers, bullet points, concise paragraphs

## STEP-BY-STEP WORKFLOW

### Phase 0.5: CN target pre-flight check

**If the target is a China-market entity (A股 / 港股 / 科创板 / 创业板 / 北交所 / 中概股 or private-unicorn Chinese company), activate the [`cn-client-investigation`](../cn-client-investigation/SKILL.md) skill BEFORE starting Phase 1.**

CN targets have a different data-source hierarchy (T1 = 巨潮资讯 + Tushare > T2 = 交易所 + 天眼查 > T3 = FMP/Finnhub > T4 = 财经媒体) and a different financial disclosure pattern (Chinese GAAP, 归母净利 vs 扣非, 科创板差异化披露). The cn-client-investigation skill's Rules 4-6 reset the data-collection defaults to match.

Additionally, the deliverable's `data-provenance.md` (Rule 5) is **mandatory** for CN targets — every hard number in the datapack Excel tabs must have a corresponding provenance row, verified via `provenance_verify.py`. No CN-target datapack ships without this gate passing.

For non-CN targets, skip this pre-flight and continue with Phase 1 below.

### Phase 1: Document Processing and Data Extraction

**Step 1.1: Analyze source data**
- Access source materials: uploaded documents, web search for public filings, or MCP server data
- Review data structure and identify key sections
- Locate financial statements (typically 3-5 years historical)
- Identify management projections if included
- Note fiscal year end date
- Flag any data quality issues immediately

**Step 1.2: Extract financial statements**
- Locate historical income statement data
- Extract balance sheet snapshots (year-end or quarter-end)
- Find cash flow statement
- Extract management projections if available
- Note all page references for traceability

**Step 1.3: Extract operating metrics**
- Identify non-financial KPIs relevant to industry
- Capture unit economics data
- Extract customer/location/capacity data
- Document growth metrics and trends

**Step 1.4: Extract market and industry data**
- Competitive positioning information
- Market size and growth rates
- Industry benchmark data
- Peer comparison information

**Step 1.5: Note key context**
- Transaction structure and rationale
- Management team background
- Investment highlights from source materials
- Risk factors and considerations
- Any data gaps or inconsistencies

### Phase 2: Data Normalization and Standardization

**Step 2.1: Normalize accounting presentation**
- Ensure consistent line item names across all years
- Standardize revenue recognition treatment
- Identify and document one-time charges
- Create "Adjusted EBITDA" reconciliation if needed
- Note any accounting policy changes

**Step 2.2: Apply format detection logic**
For each data point, determine format based on full context:
- Read tab name, table title, column header, and row label
- Apply essential rules (see above)
- When uncertain, examine original source document
- Default to cleaner formatting (less is more)

**Step 2.3: Identify normalization adjustments**
Common adjustments to document:
- Restructuring charges (add back if truly non-recurring)
- Stock-based compensation (add back per industry standard)
- Acquisition-related costs (add back, specify amounts)
- Legal settlements or litigation costs (evaluate recurrence risk)
- Asset sales or impairments (exclude from operating results)
- Related party adjustments (normalize to market rates)
Note: Source citation format varies by data source (page numbers for documents, URLs for web sources, server references for MCP data)

**Step 2.4: Create adjustment schedule**
For every normalization:
- Document what was adjusted and why
- Cite source (document page number, URL, or data source reference)
- Quantify dollar impact by year
- Assess recurrence risk
- Show calculation from reported to adjusted figures

**Step 2.5: Verify data integrity**
- Confirm subtotals sum correctly using formulas
- Verify balance sheet balances
- Check cash flow ties to balance sheet changes
- Cross-check numbers across tabs for consistency
- Flag any discrepancies for investigation

**Step 2.6: Statistical Validation via aigroup-econ-mcp (Optional — requires `aigroup-financial-services-openclaw-lab`)**

> **Stable plugin note**: `aigroup-econ-mcp` is NOT bundled in the stable `aigroup-financial-services-openclaw` plugin (0.2.0+). If the tool is not visible in the agent's tool list, skip this step and Step 2.7 entirely and continue to Phase 3. To enable these econometric validations, install the experimental `aigroup-financial-services-openclaw-lab` bundle separately (contains `aigroup-econ-mcp` + `aigroup-mdtopptx-mcp`). See the lab repo README for install instructions.

After data extraction and normalization, use `aigroup-econ-mcp` tools to deepen data quality and surface insights before building the Excel workbook. All outputs should be documented in a "Data Validation" note within the Executive Summary tab.

**Multicollinearity Check (when 5+ financial metrics are included):**
- Tool: `model_diagnostic_tests` (VIF calculation + Jarque-Bera normality test)
  - Input: key financial metrics table (revenue, EBITDA, margins, growth rates, etc.)
  - Output: VIF scores per metric; JB normality test results
  - Action: flag metrics with VIF > 5 as redundant; note non-normal distributions in assumptions section

**Core Value Driver Identification (when 8+ metrics are available):**
- Tool: `regularized_regression` (LASSO, λ selected by cross-validation)
  - Y = EBITDA or Net Income; X = all other extracted metrics
  - Output: non-zero LASSO coefficients = stable value drivers
  - Action: highlight these drivers in the Executive Summary "Key Metrics" table; annotate weaker metrics as secondary

**Peer Performance Decomposition (when peer group data is available):**
- Tool: `decomposition_oaxaca_blinder`
  - Input: target company vs. peer group financial metrics
  - Output: endowment effect (structural advantage) vs. coefficient effect (operational advantage)
  - Action: add a "Peer Decomposition" note to Tab 7 (Market Analysis): "Target outperforms peers in X due to structural advantage; underperforms in Y due to operational gap"

**Revenue Trend Analysis (when 3+ years of history are available):**
- Tool: `decomposition_time_series`
  - Input: historical revenue series
  - Output: trend + seasonal + residual components
  - Action: use trend component to cross-check management's projected growth rate; flag if projection significantly exceeds historical trend

**Bootstrap Confidence on Key Metrics (for IC materials):**
- Tool: `inference_bootstrap`
  - Input: EBITDA margin or revenue growth time series
  - Output: 95% CI on the mean
  - Action: add CI ranges to the Executive Summary financial snapshot table for credibility

**Integration Rule:** Skip econ-mcp validation if:
- Source data covers fewer than 3 years
- Only 1-2 financial metrics are available
- User explicitly asks for a fast/minimal data pack
If econ-mcp is unavailable, continue to Phase 3 without interruption.

**Step 2.7: Expanded Validation (econ-mcp 2.0.10+)**

Starting with `aigroup-econ-mcp@2.0.10`, the server exposes 66 tools across 11 groups. Treat the following new capabilities as *diagnostic enhancements* — invoke them only when the underlying data shape supports the method, and always surface the p-value / goodness-of-fit before adopting results into the deliverable.

**Missing data (before any other stats run):**
- `missing_data_simple_imputation` / `missing_data_multiple_imputation` — run first if any metric has gaps ≥5%. Note imputation method and assumption in the Data Validation section; disclose imputed rows in cell comments.

**Robust inference when residuals misbehave:**
- `robust_errors_regression` — use instead of plain OLS when model_diagnostic_tests flags heteroskedasticity. Report HC3 standard errors in the Executive Summary footnote.
- `generalized_least_squares` / `weighted_least_squares` — for data with known variance structure (e.g., segments with heterogeneous sample sizes).

**Panel / multi-segment datapacks:**
- `panel_data_diagnostics` — Hausman test for fixed vs random effects when the target has ≥3 segments × ≥3 years.
- `panel_data_dynamic_model` — Arellano-Bond style estimation for persistence of key ratios (margin, working capital).
- `panel_var_model` — joint dynamics of revenue / EBITDA / capex across entities.

**Selection bias / endogeneity in unit economics:**
- `micro_heckman` — for customer / deal / cohort data where inclusion itself is endogenous (e.g., LTV only observed on retained customers).
- `micro_logit` / `micro_probit` / `micro_multinomial_logit` / `micro_negative_binomial` / `micro_poisson` / `micro_tobit` — for discrete or censored operational KPIs (churn, upsell count, truncated revenue buckets).
- `causal_instrumental_variables` / `causal_control_function` — when the driver and outcome share unobserved confounders (price and volume, marketing and revenue).

**Spatial / geographic businesses (retail, real estate, logistics, multi-region services):**
- `spatial_weights_matrix` + `spatial_morans_i_test` / `spatial_gearys_c_test` / `spatial_local_moran_lisa` — detect geographic clustering of revenue / margin before writing Market Analysis.
- `spatial_regression_model` / `spatial_gwr_model` — quantify spatial spillover vs pure location effect.

**Simultaneous / system estimation:**
- `simultaneous_equations_model` — when two endogenous metrics feed each other (e.g., price ↔ volume, R&D ↔ revenue growth).

**Variance decomposition and system diagnostics:**
- `decomposition_variance_anova` — partition metric variance into segment / year / interaction sources for investment committee narrative.

**Reporting discipline:** each new tool invocation must be recorded in the Executive Summary "Data Validation" note with (a) tool name + econ-mcp version, (b) key p-value or fit statistic, (c) business interpretation in one sentence, (d) whether the result was adopted or treated as advisory.

### Phase 3: Build Excel Workbook

**CRITICAL: Use xlsx skill for all Excel file manipulation. Read xlsx skill documentation before proceeding.**

**Step 3.1: Create standardized tab structure**
Create workbook with tabs:
- Executive Summary
- Historical Financials
- Balance Sheet
- Cash Flow
- Operating Metrics
- Property Performance (if applicable)
- Market Analysis
- Investment Highlights

**Step 3.2: Build each tab with proper formatting**
Apply formatting rules systematically:
- Headers: Bold, left-aligned, 11pt font
- Financial data: Currency format $#,##0.0 for millions
- Operational data: Number format #,##0 (no $)
- Percentages: 0.0% format
- Years: Text format to prevent comma insertion
- Negatives: Use accounting format with parentheses
- Underlines: Single above subtotals, double below totals

**Step 3.3: Insert formulas for calculations**
- All subtotals and totals must be formula-based
- Link balance sheet to income statement where appropriate
- Link cash flow to both income statement and balance sheet
- Create cross-tab references for validation
- Avoid hardcoding any calculated values

<correct_patterns>

### Row Reference Tracking - Copy This Pattern

**Store row numbers when writing data, then reference them in formulas:**

```python
# ✅ CORRECT - Track row numbers as you write
revenue_row = row
write_data_row(ws, row, "Revenue", revenue_values)
row += 1

ebitda_row = row
write_data_row(ws, row, "EBITDA", ebitda_values)
row += 1

# Use stored row numbers in formulas
margin_row = row
for col in year_columns:
    cell = ws.cell(row=margin_row, column=col)
    cell.value = f"={get_column_letter(col)}{ebitda_row}/{get_column_letter(col)}{revenue_row}"
```

**For complex models, use a dictionary:**

```python
row_refs = {
    'revenue': 5,
    'cogs': 6,
    'gross_profit': 7,
    'ebitda': 12
}

# Later in formulas
margin_formula = f"=B{row_refs['ebitda']}/B{row_refs['revenue']}"
```

</correct_patterns>

<common_mistakes>

### WRONG: Hardcoded Row Offsets

**Don't use relative offsets - they break when table structure changes:**

```python
# ❌ WRONG - Fragile offset-based references
formula = f"=B{row-15}/B{row-19}"  # What is row-15? What is row-19?

# ❌ WRONG - Magic numbers
formula = f"=B{current_row-10}*C{current_row-20}"
```

**Why this fails:**
- Breaks silently when you add/remove rows
- Impossible to verify correctness by reading code
- Creates debugging nightmares in the delivered Excel file

</common_mistakes>

**Step 3.4: Apply professional presentation**
- Freeze top row and first column on each data tab
- Set appropriate column widths (typically 12-15 characters)
- Right-align all numeric data
- Left-align all text and headers
- Add single/double underlines per accounting standards
- Ensure clean, minimal appearance

### Phase 4: Scenario Building (if projections included)

**Management Case:**
Present company's projections as provided in source materials:
- Extract all management assumptions
- Document growth rates, margin expansion, capital requirements
- Note key drivers and sensitivities
- Flag any "hockey stick" inflections that require skepticism
- Present as "Management Case" with clear labeling

**Base Case (Risk-Adjusted):**
Apply conservative adjustments to management projections based on company-specific risk factors:
- Apply revenue growth haircut reflecting execution risk and historical forecast accuracy
- Moderate margin expansion assumptions based on industry benchmarks and operating leverage
- Increase capex assumptions if growth-dependent
- Add working capital requirements if understated
- Delay synergy realization if applicable, based on integration complexity
- Document all adjustments with rationale and supporting analysis

**Downside Case (optional but recommended for LBO analysis):**
Stress test scenario based on industry cyclicality and company vulnerabilities:
- Model revenue decline reflecting recession risk or competitive pressure
- Assume margin compression under stress (volume deleverage, pricing pressure)
- Test covenant compliance and liquidity
- Assess downside protection
- Document key risks being stress-tested

**Documentation requirements for scenarios:**
Create assumptions schedule showing:
- Key assumptions by scenario (revenue growth, margins, capex %)
- Rationale for each adjustment
- Sensitivity analysis on key variables
- Historical forecast accuracy if available
- Comparison to industry benchmarks

### Phase 5: Quality Control and Validation

**Step 5.1: Data accuracy checks**
Validate:
- Every number traces to source (check spot samples, cite documents/URLs/servers)
- All calculations are formula-based (no hardcoded values)
- Subtotals and totals are mathematically correct
- Years display without commas (2024 NOT 2,024)
- No formula errors: #REF!, #VALUE!, #DIV/0!, #N/A

**Step 5.2: Format consistency checks**
Verify:
- Financial data has $ signs in format
- Operational data has NO $ signs
- Percentages display as % (15.0% not 0.15)
- Negative numbers use parentheses for financial data
- Headers are bold and left-aligned
- Numbers are right-aligned
- Years are text format

**Step 5.3: Structure and completeness checks**
Confirm:
- All required tabs present and properly sequenced
- Executive summary is concise (fits on one page)
- All key metrics captured comprehensively
- Logical flow from summary to detail
- Appropriate level of granularity in each tab
- No missing data or incomplete sections

**Step 5.4: Professional presentation checks**
Review:
- Minimal borders (only for structure)
- Consistent indentation (2 spaces for sub-items)
- Proper accounting underlines (single and double)
- Clean, professional appearance throughout
- Appropriate column widths (not too narrow or wide)

**Step 5.5: Documentation and assumptions checks**
Ensure:
- All normalization adjustments documented with rationale
- Source citations included (document page numbers, URLs, or data source references)
- Assumptions clearly stated and reasonable
- Executive summary accurate and impactful
- Filename includes company name and date

### Phase 6: Final Delivery

**Step 6.1: Create executive summary**
Write concise, impactful summary including:
- Company overview: business model, products/services, geography (2-3 sentences)
- Key financial metrics: Revenue, EBITDA, Growth rates (table format)
- Investment highlights: 3-5 key strengths or opportunities
- Notable risks or considerations (briefly)
- Transaction context if applicable

**Step 6.2: Final file preparation**
- Save workbook with proper naming: CompanyName_DataPack_YYYY-MM-DD.xlsx

## NORMALIZATION PATTERNS

### Common Adjustments to EBITDA

**1. Restructuring charges**
- Add back if truly non-recurring (facility closure, one-time severance)
- Do NOT add back if company restructures every year
- Document specific nature and rationale for non-recurrence
- Example: "2023 restructuring: $3.0M facility closure, documented in source materials, one-time event"

**2. Stock-based compensation**
- Industry standard: add back for private equity analysis
- Treat as non-cash operating expense
- Be consistent across all periods
- Note if unusually high or includes one-time grants

**3. Acquisition-related costs**
- Add back transaction fees, integration costs
- Document specific amounts by type
- Do not add back ongoing integration investments
- Cite source for each adjustment

**4. Legal settlements and litigation**
- Add back if truly isolated incident
- Assess recurrence risk (one settlement vs pattern of litigation)
- Document nature of settlement
- Consider if this is normal course of business

**5. Asset sales or impairments**
- Exclude gains/losses on asset sales from operating EBITDA
- Remove impairment charges if truly non-recurring
- Document what assets were sold/impaired and why
- Adjust revenue if assets generated operating income

**6. Related party adjustments**
- Normalize above-market related party expenses (rent, management fees)
- Adjust to market rates with supporting documentation
- Remove personal expenses run through business
- Document market rate comparison

### Conservative vs Aggressive Normalization

**Management Case:**
- Include all adjustments management proposes
- Accept company's definition of "non-recurring"
- More aggressive EBITDA adjustments
- Use for understanding management's view

**Base Case (Recommended for investment decisions):**
- Only clearly non-recurring items
- Apply higher scrutiny to recurring "one-time" charges
- Exclude speculative adjustments
- More conservative, defensible to investment committee

## INDUSTRY-SPECIFIC ADAPTATIONS

### Technology/SaaS
Key metrics to capture:
- ARR (Annual Recurring Revenue) and MRR
- Customer count by cohort
- CAC (Customer Acquisition Cost) and LTV (Lifetime Value)
- Churn rate (gross and net)
- Net revenue retention
- Rule of 40 (Growth % + EBITDA Margin %)
- Magic number (sales efficiency)

Format notes: ARR is currency ($), customer count is number (no $), rates are %

### Manufacturing/Industrial
Key metrics to capture:
- Production capacity and capacity utilization %
- Units produced by product line
- Inventory turns
- Gross margin by product line
- Order backlog

Format notes: Units, capacity are numbers (no $), utilization is %, revenue/costs are currency

### Real Estate/Hospitality
Key metrics to capture:
- Properties/rooms/square footage
- Occupancy rates %
- ADR (Average Daily Rate) - currency format
- RevPAR (Revenue per Available Room) - currency format
- NOI (Net Operating Income) - currency format
- Cap rates %
- FF&E reserve

Format notes: Rooms/sqft are numbers, occupancy is %, ADR/RevPAR are currency

### Healthcare/Services
Key metrics to capture:
- Locations/facilities
- Providers/employees
- Patients/visits (volume metrics)
- Revenue per visit - currency
- Payor mix %
- Same-store growth %

Format notes: Locations/visits are numbers, revenue per visit is currency, rates are %

## FINAL DELIVERY CHECKLIST

Complete this checklist before delivering the data pack:

**Structure:**
- All required tabs present and in logical sequence
- Each tab has clear header and title
- Executive summary is concise (fits on one page)

**Data Accuracy:**
- All numbers trace to source (documents, URLs, or data servers)
- Source references documented for key figures (page numbers, URLs, etc.)
- All calculations are formula-based (no hardcoded calculated values)
- Subtotals and totals verified
- Balance sheet balances (Assets = Liabilities + Equity)
- No #REF!, #VALUE!, or #DIV/0! errors

**Formatting - Years and Numbers:**
- Years display correctly: 2020, 2021, 2022 (no commas)
- Financial data has $ signs: $50.0, $125.5
- Operational metrics have NO $ signs: 100 stores, 250 employees
- Percentages formatted correctly: 15.0%, 25.5%
- Negatives in parentheses: $(15.0) not -$15.0

**Formatting - Professional Standards:**
- Headers bold and left-aligned
- Numbers right-aligned
- Consistent indentation (2 spaces for sub-items)
- Single underline above subtotals
- Double underline below final totals
- Frozen panes on headers
- Consistent font throughout
- Minimal borders (only for structure)
- Clean, professional appearance throughout

**Content Completeness:**
- Financial statements complete (IS, BS, CF)
- Operating metrics comprehensively captured
- Normalization adjustments documented
- Assumptions clearly stated
- Executive summary clear, concise, and impactful
- Investment highlights compelling
- Market analysis provides context

**Documentation:**
- All normalization adjustments explained
- Every data cell cited from source with comments and links (document page numbers, URLs, or data source references)
- Assumptions documented with rationale
- Any data limitations noted
- Filename follows convention: CompanyName_DataPack_YYYY-MM-DD.xlsx

**Final Output:**
- File saved to outputs with proper naming convention
- All quality control checks passed
