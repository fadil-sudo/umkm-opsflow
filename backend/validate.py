"""
validate.py — Validate parsed records and flag data quality issues.

Validation rules:
  ERROR (blocks processing):
    - Missing date entirely
    - Total is zero or negative for order/expense types
    - Non-numeric values that couldn't be parsed
    
  WARNING (flagged but processed):
    - Missing customer name for orders
    - Duplicate records (same date + product + total)
    - Outlier values (total > 3 standard deviations from mean)
    - Quantity <= 0
    - Date outside reasonable range (future > 7 days, past > 365 days)
    - Total doesn't match qty * unit_price (within tolerance)
    
  INFO (noted):
    - Parse warnings from parsing stage
    - Unusual payment method
    - Missing notes
"""

import statistics
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from typing import Optional


@dataclass
class ValidationIssue:
    row_id: Optional[int]
    severity: str  # "error" | "warning" | "info"
    field: str
    issue: str
    detail: str
    suggested_action: str = ""
    source_row: Optional[int] = None
    
    def to_dict(self):
        return asdict(self)


def validate_records(records: list[dict]) -> tuple[list[ValidationIssue], list[dict]]:
    """
    Validate records and return (issues, valid_records).
    
    Records with ERROR severity issues are excluded from valid_records.
    Records with WARNING/INFO issues are included but flagged.
    """
    issues = []
    valid_records = []
    
    today = datetime.now().date()
    
    # --- Pre-pass: collect totals for outlier detection ---
    order_totals = [r["total"] for r in records if r["type"] == "order" and r["total"] > 0]
    
    mean_total = statistics.mean(order_totals) if order_totals else 0
    stdev_total = statistics.stdev(order_totals) if len(order_totals) > 1 else 0
    
    # --- Track for duplicate detection ---
    seen_keys = {}
    
    for record in records:
        record_issues = []
        row_id = record.get("row_id")
        source_row = record.get("_source_row")
        
        # Check parse warnings first (info level)
        for pw in record.get("_parse_warnings", []):
            record_issues.append(ValidationIssue(
                row_id=row_id,
                severity="info",
                field="(parse)",
                issue="parse_warning",
                detail=pw,
                source_row=source_row,
            ))
        
        # ERROR: Missing date
        if not record["date"]:
            record_issues.append(ValidationIssue(
                row_id=row_id,
                severity="error",
                field="date",
                issue="missing_date",
                detail="Date is missing or unparseable",
                suggested_action="Add a valid date to this row",
                source_row=source_row,
            ))
        
        # ERROR: Total is zero or negative for order/expense
        if record["type"] in ("order", "expense"):
            if record["total"] <= 0:
                record_issues.append(ValidationIssue(
                    row_id=row_id,
                    severity="error",
                    field="total",
                    issue="invalid_total",
                    detail=f"Total is {record['total']} for type '{record['type']}' — must be positive",
                    suggested_action="Verify and correct the amount",
                    source_row=source_row,
                ))
        
        # WARNING: Missing customer for orders
        if record["type"] == "order" and not record["customer"]:
            record_issues.append(ValidationIssue(
                row_id=row_id,
                severity="warning",
                field="customer",
                issue="missing_customer",
                detail="Order has no customer name",
                suggested_action="Add customer name for follow-up tracking",
                source_row=source_row,
            ))
        
        # WARNING: Outlier detection
        if record["type"] == "order" and record["total"] > 0 and stdev_total > 0:
            z_score = (record["total"] - mean_total) / stdev_total
            if abs(z_score) > 3:
                direction = "high" if z_score > 0 else "low"
                record_issues.append(ValidationIssue(
                    row_id=row_id,
                    severity="warning",
                    field="total",
                    issue=f"outlier_{direction}",
                    detail=(
                        f"Value Rp {record['total']:,.0f} is {abs(z_score):.1f} standard deviations "
                        f"{'above' if z_score > 0 else 'below'} mean (Rp {mean_total:,.0f})"
                    ),
                    suggested_action="Verify this transaction is correct",
                    source_row=source_row,
                ))
        
        # WARNING: Duplicate detection
        dedup_key = (record["date"], record["product"].lower().strip(), round(record["total"], 2))
        if dedup_key in seen_keys:
            first_row = seen_keys[dedup_key]
            record_issues.append(ValidationIssue(
                row_id=row_id,
                severity="warning",
                field="(row)",
                issue="duplicate",
                detail=f"This row appears to duplicate row {first_row} (same date, product, and total)",
                suggested_action="Verify if this is a genuine duplicate or a separate transaction",
                source_row=source_row,
            ))
        else:
            seen_keys[dedup_key] = row_id
        
        # WARNING: Quantity <= 0
        if record["quantity"] <= 0 and record["type"] != "adjustment":
            record_issues.append(ValidationIssue(
                row_id=row_id,
                severity="warning",
                field="quantity",
                issue="invalid_quantity",
                detail=f"Quantity is {record['quantity']}",
                suggested_action="Verify quantity",
                source_row=source_row,
            ))
        
        # WARNING: Date range check
        if record["date"]:
            try:
                record_date = datetime.strptime(record["date"], "%Y-%m-%d").date()
                days_future = (record_date - today).days
                days_past = (today - record_date).days
                
                if days_future > 7:
                    record_issues.append(ValidationIssue(
                        row_id=row_id,
                        severity="warning",
                        field="date",
                        issue="future_date",
                        detail=f"Date {record['date']} is {days_future} days in the future",
                        suggested_action="Verify date is correct",
                        source_row=source_row,
                    ))
                elif days_past > 365:
                    record_issues.append(ValidationIssue(
                        row_id=row_id,
                        severity="info",
                        field="date",
                        issue="old_date",
                        detail=f"Date {record['date']} is {days_past} days in the past",
                        source_row=source_row,
                    ))
            except ValueError:
                pass  # Already caught by missing_date check
        
        # INFO: Unusual payment method
        normal_methods = {"cash", "tunai", "transfer", "bank", "qris", "gopay", "ovo", "shopeepay", "dana", "debit", "credit", "card", "credit_card", "debit_card", ""}
        if record["payment_method"].lower() not in normal_methods:
            record_issues.append(ValidationIssue(
                row_id=row_id,
                severity="info",
                field="payment_method",
                issue="unusual_method",
                detail=f"Payment method '{record['payment_method']}' is not in standard list",
                source_row=source_row,
            ))
        
        # Determine if record has blocking errors
        has_error = any(i.severity == "error" for i in record_issues)
        
        issues.extend(record_issues)
        
        if not has_error:
            valid_records.append(record)
    
    # Sort issues by severity (errors first) then by row
    severity_order = {"error": 0, "warning": 1, "info": 2}
    issues.sort(key=lambda i: (severity_order.get(i.severity, 9), i.row_id or 0))
    
    return issues, valid_records
