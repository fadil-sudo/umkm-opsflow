"""
compute.py — Deterministic computation of business metrics.

ALL numeric calculations happen here, in Python, never in the LLM.
This module produces a Metrics dataclass that the LLM can format into text.
"""

from dataclasses import dataclass, field, asdict
from collections import defaultdict
from typing import Optional
import statistics


@dataclass
class ProductSummary:
    product: str
    total_quantity: float
    total_revenue: float
    transaction_count: int
    avg_price: float
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Metrics:
    # Core financials
    total_revenue: float = 0
    total_expenses: float = 0
    net_profit: float = 0
    
    # Transaction counts
    order_count: int = 0
    expense_count: int = 0
    stock_in_count: int = 0
    adjustment_count: int = 0
    total_transactions: int = 0
    
    # Payment status
    paid_count: int = 0
    unpaid_count: int = 0
    partial_count: int = 0
    paid_total: float = 0
    unpaid_total: float = 0
    partial_total: float = 0
    
    # Product breakdown
    top_products_by_qty: list = field(default_factory=list)
    top_products_by_revenue: list = field(default_factory=list)
    
    # Expense breakdown
    expense_by_product: list = field(default_factory=list)
    
    # Averages
    avg_order_value: float = 0
    median_order_value: float = 0
    
    # Date range
    date_min: str = ""
    date_max: str = ""
    
    # Source tracking (audit trail)
    source_rows: list = field(default_factory=list)
    
    def to_dict(self):
        d = asdict(self)
        # Convert ProductSummary objects to dicts
        d["top_products_by_qty"] = [p if isinstance(p, dict) else p for p in self.top_products_by_qty]
        d["top_products_by_revenue"] = [p if isinstance(p, dict) else p for p in self.top_products_by_revenue]
        d["expense_by_product"] = [p if isinstance(p, dict) else p for p in self.expense_by_product]
        return d


def compute_metrics(records: list[dict]) -> Metrics:
    """
    Compute all metrics from validated records.
    
    This function is 100% deterministic — same input always produces same output.
    No LLM, no randomness, no external calls.
    """
    metrics = Metrics()
    
    if not records:
        return metrics
    
    # Track source rows for audit
    metrics.source_rows = [r["_source_row"] for r in records if r.get("_source_row")]
    metrics.total_transactions = len(records)
    
    # Date range
    dates = [r["date"] for r in records if r["date"]]
    if dates:
        metrics.date_min = min(dates)
        metrics.date_max = max(dates)
    
    # Product aggregation
    product_data = defaultdict(lambda: {"quantity": 0, "revenue": 0, "count": 0, "prices": []})
    expense_data = defaultdict(lambda: {"quantity": 0, "total": 0, "count": 0})
    
    for r in records:
        rtype = r["type"]
        total = r["total"]
        qty = r["quantity"]
        product = r["product"]
        uprice = r["unit_price"]
        
        if rtype == "order":
            metrics.order_count += 1
            metrics.total_revenue += total
            
            product_data[product]["quantity"] += qty
            product_data[product]["revenue"] += total
            product_data[product]["count"] += 1
            if uprice > 0:
                product_data[product]["prices"].append(uprice)
            
            # Payment status
            ps = r["payment_status"]
            if ps == "paid":
                metrics.paid_count += 1
                metrics.paid_total += total
            elif ps == "unpaid":
                metrics.unpaid_count += 1
                metrics.unpaid_total += total
            elif ps == "partial":
                metrics.partial_count += 1
                metrics.partial_total += total
        
        elif rtype == "expense":
            metrics.expense_count += 1
            metrics.total_expenses += total
            
            expense_data[product]["quantity"] += qty
            expense_data[product]["total"] += total
            expense_data[product]["count"] += 1
        
        elif rtype == "stock_in":
            metrics.stock_in_count += 1
            product_data[product]["quantity"] += qty
        
        elif rtype == "adjustment":
            metrics.adjustment_count += 1
    
    # Net profit
    metrics.net_profit = metrics.total_revenue - metrics.total_expenses
    
    # Order value statistics
    order_values = [r["total"] for r in records if r["type"] == "order" and r["total"] > 0]
    if order_values:
        metrics.avg_order_value = statistics.mean(order_values)
        metrics.median_order_value = statistics.median(order_values)
    
    # Top products by quantity
    products_by_qty = []
    for product, data in product_data.items():
        if data["quantity"] > 0 or data["revenue"] > 0:
            avg_price = statistics.mean(data["prices"]) if data["prices"] else (data["revenue"] / data["quantity"] if data["quantity"] > 0 else 0)
            products_by_qty.append(ProductSummary(
                product=product,
                total_quantity=data["quantity"],
                total_revenue=data["revenue"],
                transaction_count=data["count"],
                avg_price=avg_price,
            ))
    
    metrics.top_products_by_qty = sorted(
        [p.to_dict() for p in products_by_qty if p.total_quantity > 0],
        key=lambda x: x["total_quantity"],
        reverse=True
    )[:10]
    
    metrics.top_products_by_revenue = sorted(
        [p.to_dict() for p in products_by_qty if p.total_revenue > 0],
        key=lambda x: x["total_revenue"],
        reverse=True
    )[:10]
    
    # Expense breakdown
    expenses_list = []
    for product, data in expense_data.items():
        expenses_list.append({
            "product": product,
            "total_quantity": data["quantity"],
            "total_amount": data["total"],
            "transaction_count": data["count"],
        })
    metrics.expense_by_product = sorted(expenses_list, key=lambda x: x["total_amount"], reverse=True)
    
    return metrics
