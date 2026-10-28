"""
export.py — Export reports and drafts to files.

Generates:
  - daily_report.md     : Full Markdown report with all metrics, issues, and actions
  - action_items.csv    : Action items in spreadsheet format
  - draft_messages.md   : Draft follow-up messages (for human review before sending)
  - validation_issues.csv : Data quality issues
  - metrics.json        : Raw metrics for audit/debugging
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from compute import Metrics
from validate import ValidationIssue
from actions import ActionItem


@dataclass
class ReportData:
    metrics: Metrics
    issues: list  # list of ValidationIssue
    actions: list  # list of ActionItem
    records: list  # validated records (list of dicts)
    input_file: str
    parse_warnings: list
    total_input_rows: int
    rejected_count: int
    clarifications: list = field(default_factory=list)  # list of ClarificationQuestion


def _format_rp(amount: float) -> str:
    """Format amount as Indonesian Rupiah string."""
    return f"Rp {amount:,.0f}".replace(",", ".")


def generate_markdown_report(data: ReportData) -> str:
    """Generate the full Markdown daily report."""
    m = data.metrics
    lines = []
    
    # Header
    lines.append("# UMKM OpsFlow — Daily Operations Report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Source File:** `{data.input_file}`")
    lines.append(f"**Date Range:** {m.date_min or 'N/A'} to {m.date_max or 'N/A'}")
    lines.append(f"**Records Processed:** {m.total_transactions} valid / {data.total_input_rows} total ({data.rejected_count} rejected)")
    lines.append("")
    
    # Parse warnings
    if data.parse_warnings:
        lines.append("## Parse Warnings")
        lines.append("")
        for w in data.parse_warnings:
            lines.append(f"- ⚠️ {w}")
        lines.append("")
    
    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total Revenue | {_format_rp(m.total_revenue)} |")
    lines.append(f"| Total Expenses | {_format_rp(m.total_expenses)} |")
    lines.append(f"| **Net Profit** | **{_format_rp(m.net_profit)}** |")
    lines.append(f"| Total Transactions | {m.total_transactions} |")
    lines.append(f"| Orders | {m.order_count} |")
    lines.append(f"| Expenses | {m.expense_count} |")
    lines.append(f"| Avg Order Value | {_format_rp(m.avg_order_value)} |")
    lines.append(f"| Median Order Value | {_format_rp(m.median_order_value)} |")
    lines.append("")
    
    # Payment Status
    lines.append("## Payment Status Breakdown")
    lines.append("")
    lines.append(f"| Status | Count | Total Amount |")
    lines.append(f"|--------|-------|--------------|")
    lines.append(f"| Paid | {m.paid_count} | {_format_rp(m.paid_total)} |")
    lines.append(f"| Unpaid | {m.unpaid_count} | {_format_rp(m.unpaid_total)} |")
    lines.append(f"| Partial | {m.partial_count} | {_format_rp(m.partial_total)} |")
    lines.append("")
    
    # Top Products
    if m.top_products_by_qty:
        lines.append("## Top Products by Quantity Sold")
        lines.append("")
        lines.append("| # | Product | Quantity | Revenue | Transactions | Avg Price |")
        lines.append("|---|---------|----------|---------|--------------|-----------|")
        for i, p in enumerate(m.top_products_by_qty, 1):
            lines.append(
                f"| {i} | {p['product']} | {p['total_quantity']:.0f} | "
                f"{_format_rp(p['total_revenue'])} | {p['transaction_count']} | "
                f"{_format_rp(p['avg_price'])} |"
            )
        lines.append("")
    
    if m.top_products_by_revenue:
        lines.append("## Top Products by Revenue")
        lines.append("")
        lines.append("| # | Product | Revenue | Quantity | Transactions |")
        lines.append("|---|---------|---------|----------|--------------|")
        for i, p in enumerate(m.top_products_by_revenue, 1):
            lines.append(
                f"| {i} | {p['product']} | {_format_rp(p['total_revenue'])} | "
                f"{p['total_quantity']:.0f} | {p['transaction_count']} |"
            )
        lines.append("")
    
    # Expense Breakdown
    if m.expense_by_product:
        lines.append("## Expense Breakdown")
        lines.append("")
        lines.append("| # | Category | Amount | Transactions |")
        lines.append("|---|----------|--------|--------------|")
        for i, e in enumerate(m.expense_by_product, 1):
            lines.append(
                f"| {i} | {e['product']} | {_format_rp(e['total_amount'])} | "
                f"{e['transaction_count']} |"
            )
        lines.append("")
    
    # Data Quality Issues
    if data.issues:
        error_count = sum(1 for i in data.issues if i.severity == "error")
        warning_count = sum(1 for i in data.issues if i.severity == "warning")
        info_count = sum(1 for i in data.issues if i.severity == "info")
        
        lines.append("## Data Quality Issues")
        lines.append("")
        lines.append(
            f"Found {len(data.issues)} issue(s): "
            f"{error_count} error(s), {warning_count} warning(s), {info_count} info."
        )
        lines.append("")
        lines.append("| Severity | Source Row | Field | Issue | Detail | Suggested Action |")
        lines.append("|----------|------------|-------|-------|--------|-------------------|")
        for issue in data.issues:
            icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(issue.severity, "")
            lines.append(
                f"| {icon} {issue.severity} | {issue.source_row or '-'} | "
                f"{issue.field} | {issue.issue} | {issue.detail} | "
                f"{issue.suggested_action or '-'} |"
            )
        lines.append("")
    
    # Clarification Questions
    if data.clarifications:
        lines.append("## Clarification Questions")
        lines.append("")
        lines.append("Agent detected ambiguous situations that require your input:")
        lines.append("")
        for i, q in enumerate(data.clarifications, 1):
            icon = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(q.severity, "")
            lines.append(f"{i}. {icon} **[{q.severity.upper()}]** {q.question}")
            lines.append(f"   - Context: {q.context}")
            lines.append(f"   - Suggested resolution: {q.suggested_resolution}")
            lines.append("")
        lines.append("Agent will proceed with default assumptions. Please review and correct if needed.")
        lines.append("")
    
    # Action Items
    if data.actions:
        lines.append("## Action Items")
        lines.append("")
        lines.append("The following actions are **proposed** based on rules. No action has been taken.")
        lines.append("All actions require human review and approval.")
        lines.append("")
        for action in data.actions:
            priority_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(action.priority, "")
            lines.append(f"### {priority_icon} [{action.priority.upper()}] {action.title}")
            lines.append(f"**ID:** {action.id} | **Category:** {action.category}")
            lines.append("")
            lines.append(f"{action.description}")
            if action.suggested_action:
                lines.append(f"")
                lines.append(f"**Suggested action:** {action.suggested_action}")
            if action.draft_needed:
                lines.append(f"")
                lines.append(f"**Draft message prepared** — see `draft_messages.md`")
            lines.append("")
    
    # Audit Trail
    lines.append("## Audit Trail")
    lines.append("")
    lines.append("### Calculation Sources")
    lines.append("")
    lines.append(f"- Revenue: Sum of `total` field for records where `type = order`. "
                 f"Source rows: {m.source_rows}")
    lines.append(f"- Expenses: Sum of `total` field for records where `type = expense`.")
    lines.append(f"- Net Profit: Revenue - Expenses (deterministic subtraction).")
    lines.append(f"- Avg/Median Order Value: Python `statistics.mean/median` on order totals.")
    lines.append(f"- Unpaid Total: Sum of `total` for records where `payment_status = unpaid`.")
    lines.append("")
    lines.append("### Reproducibility")
    lines.append("")
    lines.append("All calculations are performed by `compute.py` (deterministic Python). "
                 "The LLM was NOT used for any numeric calculation. "
                 "Running this script on the same input file will always produce identical results.")
    lines.append("")
    lines.append("### Assumptions")
    lines.append("")
    lines.append("- Records with `type` not specified were defaulted to `order`.")
    lines.append("- Records with `payment_status` not specified were defaulted to `paid`.")
    lines.append("- Missing `quantity` was defaulted to 1.")
    lines.append("- If `total` was 0 but `quantity * unit_price > 0`, total was computed.")
    lines.append("- Stock estimates assume `stock_in` minus orders sold = remaining stock. "
                 "This may not reflect actual physical inventory.")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by UMKM OpsFlow — Tencent Cloud Hackathon Indonesia 2026*")
    
    return "\n".join(lines)


def generate_draft_messages(data: ReportData) -> str:
    """Generate draft follow-up messages for human review."""
    lines = []
    lines.append("# Draft Follow-Up Messages")
    lines.append("")
    lines.append("**IMPORTANT: These are DRAFTS only. No message has been sent.**")
    lines.append("**Review each message before sending. Copy and send manually via WhatsApp/SMS.**")
    lines.append("")
    
    draft_actions = [a for a in data.actions if a.draft_needed]
    
    if not draft_actions:
        lines.append("No follow-up messages needed at this time.")
        return "\n".join(lines)
    
    for action in draft_actions:
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## {action.id}: {action.title}")
        lines.append(f"**Priority:** {action.priority}")
        lines.append(f"**Recipient:** {action.draft_recipient}")
        lines.append(f"")
        
        ctx = action.draft_context
        category = action.category
        
        if category == "payment" and "orders" in ctx:
            # Multi-order follow-up
            lines.append(f"**Draft WhatsApp message:**")
            lines.append(f"")
            customer = ctx.get("customer", "(customer name)")
            total = ctx.get("total_unpaid", 0)
            count = ctx.get("order_count", 0)
            order_details = "; ".join(
                f"{o['product']} ({_format_rp(o['amount'])}) on {o['date']}" 
                for o in ctx.get("orders", [])[:3]
            )
            lines.append(f"> Halo {customer},")
            lines.append(f"> ")
            lines.append(f"> Semoga sehat selalu. Berikut pengingat untuk {count} pesanan")
            lines.append(f"> yang belum diselesaikan pembayarannya:")
            lines.append(f"> ")
            lines.append(f"> {order_details}")
            if count > 3:
                lines.append(f"> ...dan {count - 3} pesanan lainnya")
            lines.append(f"> ")
            lines.append(f"> Total: {_format_rp(total)}")
            lines.append(f"> ")
            lines.append(f"> Mohon konfirmasi pembayaran ya. Terima kasih! 🙏")
        
        elif category == "payment":
            # Single payment follow-up
            lines.append(f"**Draft WhatsApp message:**")
            lines.append(f"")
            customer = ctx.get("customer", "(customer name)")
            product = ctx.get("product", "(product)")
            amount = ctx.get("amount", 0)
            date = ctx.get("date", "")
            lines.append(f"> Halo {customer},")
            lines.append(f"> ")
            lines.append(f"> Mengingatkan pesanan {product} ({_format_rp(amount)})")
            lines.append(f"> tanggal {date} yang pembayarannya masih sebagian/parsial.")
            lines.append(f"> ")
            lines.append(f"> Mohon konfirmasi sisa pembayaran. Terima kasih! 🙏")
        
        elif category == "stock":
            lines.append(f"**Draft message to supplier:**")
            lines.append(f"")
            product = ctx.get("product", "(product)")
            stock = ctx.get("estimated_stock", 0)
            sold = ctx.get("sold_today", 0)
            threshold = ctx.get("threshold", 10)
            lines.append(f"> Halo,")
            lines.append(f"> ")
            lines.append(f"> Ingin melakukan pemesanan ulang untuk: {product}")
            lines.append(f"> ")
            lines.append(f"> Estimasi sisa stok: {stock:.0f} unit")
            lines.append(f"> Terjual hari ini: {sold:.0f} unit")
            lines.append(f"> ")
            lines.append(f"> Mohon info ketersediaan dan harga terbaru. Terima kasih!")
        
        lines.append(f"")
    
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"**End of draft messages. Please review and send manually.**")
    lines.append(f"")
    lines.append(f"*Generated by UMKM OpsFlow — all amounts verified from source data.*")
    
    return "\n".join(lines)


def export_all(data: ReportData, output_dir: Path) -> Path:
    """Export all report files to output directory."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Daily report (Markdown)
    report_md = generate_markdown_report(data)
    report_path = output_dir / "daily_report.md"
    report_path.write_text(report_md, encoding="utf-8")
    
    # Draft messages (Markdown)
    drafts_md = generate_draft_messages(data)
    drafts_path = output_dir / "draft_messages.md"
    drafts_path.write_text(drafts_md, encoding="utf-8")
    
    # Action items (CSV)
    actions_csv_path = output_dir / "action_items.csv"
    with open(actions_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Priority", "Category", "Title", "Description", 
                        "Suggested Action", "Draft Needed", "Recipient"])
        for action in data.actions:
            writer.writerow([
                action.id, action.priority, action.category, action.title,
                action.description, action.suggested_action,
                "Yes" if action.draft_needed else "No", action.draft_recipient
            ])
    
    # Validation issues (CSV)
    issues_csv_path = output_dir / "validation_issues.csv"
    with open(issues_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Row ID", "Source Row", "Severity", "Field", "Issue", "Detail", "Suggested Action"])
        for issue in data.issues:
            writer.writerow([
                issue.row_id, issue.source_row, issue.severity, issue.field,
                issue.issue, issue.detail, issue.suggested_action
            ])
    
    # Raw metrics (JSON for audit)
    metrics_json_path = output_dir / "metrics.json"
    metrics_json_path.write_text(
        json.dumps(data.metrics.to_dict(), indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    
    return report_path
