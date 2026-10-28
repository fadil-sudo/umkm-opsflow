"""
UMKM OpsFlow — Main Orchestrator Script
Tencent Cloud Hackathon Indonesia 2026

This script runs the full pipeline:
  1. Parse input file (CSV/XLSX)
  2. Validate data
  3. Compute metrics (deterministic)
  4. Generate action items (rule-based)
  5. Export report and drafts

Usage:
  python opsflow.py --input data/sample_orders_messy.csv --output-dir output/

Output:
  output/daily_report.md       — Full daily report
  output/action_items.csv      — Action items in CSV
  output/draft_messages.md     — Draft follow-up messages
  output/validation_issues.csv — Data quality issues
  output/metrics.json          — Raw metrics (for audit)
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add scripts directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))

from parse_input import parse_file, ParseError
from validate import validate_records, ValidationIssue
from compute import compute_metrics, Metrics
from actions import generate_actions, ActionItem
from export import export_all, ReportData
from clarify import detect_ambiguities, format_clarification_report, ClarificationQuestion


def run_pipeline(input_path: str, output_dir: str) -> dict:
    """
    Run the full UMKM OpsFlow pipeline.
    
    Returns a dict with:
      - status: 'success' | 'partial' | 'error'
      - metrics: computed metrics dict
      - issues: validation issues list
      - actions: action items list
      - report_path: path to generated report
      - error: error message (if status != success)
    """
    input_file = Path(input_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    result = {
        "status": "error",
        "input_file": str(input_file),
        "timestamp": datetime.now().isoformat(),
        "metrics": None,
        "issues": [],
        "actions": [],
        "clarifications": [],
        "report_path": None,
        "error": None
    }
    
    # === STEP 1: Parse ===
    try:
        records, parse_warnings = parse_file(input_file)
        result["parse_warnings"] = parse_warnings
        result["records_count"] = len(records)
    except FileNotFoundError as e:
        result["error"] = str(e)
        result["status"] = "error"
        return result
    except ParseError as e:
        result["error"] = f"Parse error: {e}"
        result["status"] = "error"
        return result
    except Exception as e:
        result["error"] = f"Unexpected error during parsing: {e}"
        result["status"] = "error"
        return result
    
    if not records:
        result["error"] = "No valid records found in input file"
        result["status"] = "error"
        return result
    
    # === STEP 2: Validate ===
    issues, validated_records = validate_records(records)
    result["issues"] = [i.to_dict() for i in issues]
    result["validated_count"] = len(validated_records)
    result["rejected_count"] = len(records) - len(validated_records)
    
    error_count = sum(1 for i in issues if i.severity == "error")
    if error_count > 0 and len(validated_records) == 0:
        result["error"] = f"All {len(records)} records failed validation with errors"
        result["status"] = "error"
        return result
    
    # === STEP 2b: Detect ambiguities that need clarification ===
    clarifications = detect_ambiguities(validated_records, issues)
    result["clarifications"] = [q.to_dict() for q in clarifications]
    
    # === STEP 3: Compute ===
    metrics = compute_metrics(validated_records)
    result["metrics"] = metrics.to_dict()
    result["status"] = "partial" if result["rejected_count"] > 0 else "success"
    
    # === STEP 4: Actions ===
    actions = generate_actions(metrics, validated_records, issues)
    result["actions"] = [a.to_dict() for a in actions]
    
    # === STEP 5: Export ===
    report_data = ReportData(
        metrics=metrics,
        issues=issues,
        actions=actions,
        records=validated_records,
        input_file=str(input_file),
        parse_warnings=parse_warnings,
        total_input_rows=len(records),
        rejected_count=result["rejected_count"],
        clarifications=clarifications,
    )
    
    report_path = export_all(report_data, out_dir)
    result["report_path"] = str(report_path)
    
    # Final status
    if result["rejected_count"] == 0 and len(issues) == 0:
        result["status"] = "success"
    else:
        result["status"] = "partial"
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="UMKM OpsFlow — Daily Operations Report Generator"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input CSV or XLSX file"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="output",
        help="Directory for output files (default: output)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print result as JSON to stdout"
    )
    
    args = parser.parse_args()
    
    result = run_pipeline(args.input, args.output_dir)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        # Human-readable summary
        print(f"\n{'='*60}")
        print(f"  UMKM OpsFlow — Daily Operations Report")
        print(f"{'='*60}")
        print(f"  Input: {result['input_file']}")
        print(f"  Status: {result['status'].upper()}")
        
        if result.get("records_count"):
            print(f"  Records parsed: {result['records_count']}")
            print(f"  Records validated: {result.get('validated_count', 0)}")
            print(f"  Records rejected: {result.get('rejected_count', 0)}")
        
        if result["issues"]:
            print(f"  Validation issues: {len(result['issues'])}")
            for issue in result["issues"][:5]:
                print(f"    [{issue['severity']}] Row {issue.get('row_id','?')}: {issue['detail']}")
            if len(result["issues"]) > 5:
                print(f"    ... and {len(result['issues'])-5} more")
        
        if result["metrics"]:
            m = result["metrics"]
            print(f"\n  --- Metrics ---")
            print(f"  Total Revenue:   Rp {m.get('total_revenue', 0):,}")
            print(f"  Total Expenses:  Rp {m.get('total_expenses', 0):,}")
            print(f"  Net Profit:      Rp {m.get('net_profit', 0):,}")
            print(f"  Unpaid Orders:   {m.get('unpaid_count', 0)} (Rp {m.get('unpaid_total', 0):,})")
        
        if result["clarifications"]:
            print(f"\n  --- Clarification Questions ({len(result['clarifications'])}) ---")
            for q in result["clarifications"]:
                icon = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(q["severity"], "")
                print(f"  {icon} [{q['severity'].upper()}] {q['question']}")
                print(f"      Context: {q['context']}")
        
        if result["actions"]:
            print(f"\n  --- Action Items ({len(result['actions'])}) ---")
            for a in result["actions"]:
                print(f"  [{a['priority']}] {a['title']}")
                print(f"      {a['description']}")
        
        if result["report_path"]:
            print(f"\n  Report saved to: {result['report_path']}")
        
        if result["error"]:
            print(f"\n  ERROR: {result['error']}")
        
        print(f"{'='*60}\n")
    
    # Exit code: 0 for success/partial, 1 for error
    return 0 if result["status"] != "error" else 1


if __name__ == "__main__":
    sys.exit(main())
