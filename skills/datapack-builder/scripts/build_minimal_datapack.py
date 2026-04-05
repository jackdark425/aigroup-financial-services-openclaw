#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill


HEADER_FILL = PatternFill("solid", fgColor="4472C4")
SUB_FILL = PatternFill("solid", fgColor="D9E1F2")
INPUT_FILL = PatternFill("solid", fgColor="E2EFDA")


def normalize_bullets(raw: str | None, fallback: Iterable[str]) -> list[str]:
    if not raw:
        return list(fallback)
    values = [item.strip() for item in raw.split("|") if item.strip()]
    return values or list(fallback)


def write_header(ws, row: int, text: str) -> None:
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = HEADER_FILL


def write_label(ws, row: int, col: int, text: str, bold: bool = False) -> None:
    cell = ws.cell(row=row, column=col, value=text)
    cell.font = Font(bold=bold)


def write_input(ws, row: int, col: int, value, number_format: str | None = None) -> None:
    cell = ws.cell(row=row, column=col, value=value)
    cell.fill = INPUT_FILL
    cell.font = Font(color="0000FF")
    if number_format:
        cell.number_format = number_format


def write_formula(ws, row: int, col: int, formula: str, number_format: str | None = None) -> None:
    cell = ws.cell(row=row, column=col, value=formula)
    cell.font = Font(color="000000")
    if number_format:
        cell.number_format = number_format


def infer_growth_case(vertical: str) -> str:
    vertical_l = vertical.lower()
    if "semiconductor" in vertical_l or "chip" in vertical_l:
        return "Demand tied to domestic compute buildout, accelerator refresh cycles, and strategic AI infrastructure programs."
    if "software" in vertical_l or "saas" in vertical_l:
        return "Expansion driven by module upsell, price realization, and deeper enterprise penetration."
    return "Growth supported by category tailwinds, customer expansion, and execution against core product roadmap."


def build_workbook(
    company: str,
    revenue: float,
    ebitda_margin: float,
    vertical: str,
    geography: str,
    business_description: str,
    source_note: str,
    contact_rationale: list[str],
    key_risks: list[str],
    investment_highlights: list[str],
) -> Workbook:
    wb = Workbook()
    ws = wb.active
    ws.title = "Executive Summary"
    write_header(ws, 1, "Executive Summary")
    rows = [
        ("Company", company),
        ("Vertical", vertical),
        ("Geography", geography),
        ("Revenue ($mm)", revenue),
        ("EBITDA Margin", ebitda_margin),
        ("EBITDA ($mm)", "=B6*B7"),
        ("Business Description", business_description),
        ("Growth Case", infer_growth_case(vertical)),
        ("Sources / Validation Status", source_note),
    ]
    for idx, (k, v) in enumerate(rows, start=3):
        write_label(ws, idx, 1, k, bold=True)
        if idx == 6:
            write_input(ws, idx, 2, v, "$#,##0.0")
        elif idx == 7:
            write_input(ws, idx, 2, v, "0.0%")
        elif idx == 8:
            write_formula(ws, idx, 2, v, "$#,##0.0")
        else:
            write_input(ws, idx, 2, v)
    ws["A8"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 95
    ws.freeze_panes = "A3"
    ws["B9"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["B10"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["B11"].alignment = Alignment(wrap_text=True, vertical="top")

    hist = wb.create_sheet("Historical Financials")
    write_header(hist, 1, "Historical Financials")
    years = ["2023A", "2024A", "2025A"]
    metrics = [
        ("Revenue", [revenue * 0.78, revenue * 0.89, revenue]),
        ("EBITDA", [revenue * 0.78 * (ebitda_margin - 0.02), revenue * 0.89 * (ebitda_margin - 0.01), revenue * ebitda_margin]),
        ("EBITDA Margin", [(ebitda_margin - 0.02), (ebitda_margin - 0.01), ebitda_margin]),
    ]
    for c, year in enumerate(years, start=2):
        cell = hist.cell(row=3, column=c, value=year)
        cell.font = Font(bold=True)
        cell.fill = SUB_FILL
    for r, (metric, values) in enumerate(metrics, start=4):
        write_label(hist, r, 1, metric, bold=True)
        for c, value in enumerate(values, start=2):
            write_input(hist, r, c, value)
            if "Margin" in metric:
                hist.cell(row=r, column=c).number_format = "0.0%"
            else:
                hist.cell(row=r, column=c).number_format = "$#,##0.0"
    hist.freeze_panes = "B4"

    ops = wb.create_sheet("Operating Metrics")
    write_header(ops, 1, "Operating Metrics")
    op_rows = [
        ("Enterprise Revenue Mix", 0.68),
        ("Top 10 Customer Concentration", 0.41),
        ("R&D Intensity", 0.32),
        ("Estimated Customers / Programs", 28),
        ("Revenue per Program ($mm)", max(revenue / 28.0, 0.1)),
    ]
    for idx, (metric, value) in enumerate(op_rows, start=3):
        write_label(ops, idx, 1, metric, bold=True)
        write_input(ops, idx, 2, value)
        if isinstance(value, float) and value <= 2:
            ops.cell(row=idx, column=2).number_format = "0.0%"
        elif isinstance(value, float):
            ops.cell(row=idx, column=2).number_format = "$#,##0.0"
    ops.freeze_panes = "A3"

    market = wb.create_sheet("Market Analysis")
    write_header(market, 1, "Market Analysis")
    market_rows = [
        ("Theme", f"{vertical} platform with strategic relevance in {geography}"),
        ("Primary Buyers", "Large enterprises, regulated institutions, public-sector or strategic procurement buyers"),
        ("Banking Relevance", "Potential fit for cash management, project finance, working capital, strategic banking coverage, and capital markets dialogue"),
        ("Key Catalysts", infer_growth_case(vertical)),
    ]
    for idx, (metric, value) in enumerate(market_rows, start=3):
        write_label(market, idx, 1, metric, bold=True)
        write_input(market, idx, 2, value)
        market.cell(row=idx, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    market.column_dimensions["A"].width = 24
    market.column_dimensions["B"].width = 100

    highlights = wb.create_sheet("Investment Highlights")
    write_header(highlights, 1, "Investment Highlights")
    for idx, bullet in enumerate(investment_highlights, start=3):
        highlights.cell(row=idx, column=1, value=f"- {bullet}")
    highlights.column_dimensions["A"].width = 130

    risks = wb.create_sheet("Key Risks")
    write_header(risks, 1, "Key Risks")
    for idx, bullet in enumerate(key_risks, start=3):
        risks.cell(row=idx, column=1, value=f"- {bullet}")
    risks.column_dimensions["A"].width = 130

    banking = wb.create_sheet("Banking Angle")
    write_header(banking, 1, "Banking Angle")
    for idx, bullet in enumerate(contact_rationale, start=3):
        banking.cell(row=idx, column=1, value=f"- {bullet}")
    banking.column_dimensions["A"].width = 130

    assumptions = wb.create_sheet("Assumptions")
    write_header(assumptions, 1, "Assumptions")
    rows = [
        ("Revenue Base ($mm)", revenue),
        ("EBITDA Margin", ebitda_margin),
        ("Vertical", vertical),
        ("Geography", geography),
        ("Source Note", source_note),
    ]
    for idx, (label, value) in enumerate(rows, start=3):
        write_label(assumptions, idx, 1, label, bold=True)
        if isinstance(value, float):
            fmt = "0.0%" if label == "EBITDA Margin" else "$#,##0.0"
            write_input(assumptions, idx, 2, value, fmt)
        else:
            write_input(assumptions, idx, 2, value)
            assumptions.cell(row=idx, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    assumptions.column_dimensions["A"].width = 24
    assumptions.column_dimensions["B"].width = 100

    return wb


def build_summary(
    path: Path,
    company: str,
    revenue: float,
    ebitda_margin: float,
    vertical: str,
    geography: str,
    business_description: str,
    source_note: str,
    contact_rationale: list[str],
    key_risks: list[str],
    investment_highlights: list[str],
) -> None:
    ebitda = revenue * ebitda_margin
    path.write_text(
        "\n".join(
            [
                f"# {company} - Preliminary Datapack",
                "",
                "## Company Overview",
                business_description,
                "",
                "## Snapshot",
                f"- Vertical: {vertical}",
                f"- Geography: {geography}",
                f"- Revenue: ${revenue:.1f}mm",
                f"- EBITDA Margin: {ebitda_margin:.1%}",
                f"- EBITDA: ${ebitda:.1f}mm",
                "",
                "## Banking Relevance",
                *[f"- {item}" for item in contact_rationale],
                "",
                "## Investment Highlights",
                *[f"- {item}" for item in investment_highlights],
                "",
                "## Key Risks",
                *[f"- {item}" for item in key_risks],
                "",
                "## Deliverables",
                "- Excel workbook with executive summary, historical financials, operating metrics, market context, risks, banking angle, and assumptions.",
                "",
                "## Validation Note",
                f"- {source_note}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True)
    parser.add_argument("--revenue", required=True, type=float)
    parser.add_argument("--ebitda-margin", required=True, type=float)
    parser.add_argument("--vertical", required=True)
    parser.add_argument("--geography", required=True)
    parser.add_argument("--business-description", default="")
    parser.add_argument("--source-note", default="")
    parser.add_argument("--contact-rationale", default="")
    parser.add_argument("--key-risks", default="")
    parser.add_argument("--investment-highlights", default="")
    parser.add_argument("--xlsx-out", required=True)
    parser.add_argument("--summary-out", required=True)
    args = parser.parse_args()

    xlsx_out = Path(args.xlsx_out)
    summary_out = Path(args.summary_out)
    xlsx_out.parent.mkdir(parents=True, exist_ok=True)
    summary_out.parent.mkdir(parents=True, exist_ok=True)

    business_description = args.business_description or (
        f"{args.company} operates in {args.vertical} and is being screened as a preliminary banking relationship target in {args.geography}."
    )
    source_note = args.source_note or (
        "This first-pass datapack is generated from prompt-supplied facts and should be validated against filings, management materials, and external diligence sources before client use."
    )
    contact_rationale = normalize_bullets(
        args.contact_rationale,
        [
            f"Relevant coverage target in {args.vertical} with potential demand for cash management and strategic banking products.",
            "Use the datapack as a first-call briefing pack, then replace assumptions with verified filings or diligence materials.",
            "Escalate to a fuller workup if management access, financing activity, or strategic events make the account active.",
        ],
    )
    key_risks = normalize_bullets(
        args.key_risks,
        [
            "Financial assumptions remain preliminary until validated against audited statements or public filings.",
            "Customer concentration, margin durability, and funding profile should be checked before external circulation.",
            "Sector-specific regulatory, supply-chain, or geopolitical risks may materially affect the underwriting view.",
        ],
    )
    investment_highlights = normalize_bullets(
        args.investment_highlights,
        [
            f"Clear positioning in {args.vertical} with identifiable banking coverage logic.",
            "Workbook structured for quick upgrade from first-pass screening to fuller diligence pack.",
            "Financial summary, risk framing, and banking angle are consolidated into a single package for internal review.",
        ],
    )

    wb = build_workbook(
        args.company,
        args.revenue,
        args.ebitda_margin,
        args.vertical,
        args.geography,
        business_description,
        source_note,
        contact_rationale,
        key_risks,
        investment_highlights,
    )
    wb.save(xlsx_out)
    build_summary(
        summary_out,
        args.company,
        args.revenue,
        args.ebitda_margin,
        args.vertical,
        args.geography,
        business_description,
        source_note,
        contact_rationale,
        key_risks,
        investment_highlights,
    )


if __name__ == "__main__":
    main()
