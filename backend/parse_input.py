"""
parse_input.py — Parse CSV/XLSX input into normalized records.

Standard Record Schema:
{
  "row_id": int,
  "date": "YYYY-MM-DD",
  "type": "order" | "expense" | "stock_in" | "adjustment",
  "product": str,
  "quantity": float,
  "unit_price": float,
  "total": float,
  "customer": str,
  "payment_status": "paid" | "unpaid" | "partial",
  "payment_method": str,
  "notes": str,
  "_source_row": int,      # Original row number in file
  "_parse_warnings": [str]  # Warnings during parsing
}
"""

import csv
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional


class ParseError(Exception):
    """Raised when file cannot be parsed at all."""
    pass


@dataclass
class Record:
    row_id: int
    date: str
    type: str
    product: str
    quantity: float
    unit_price: float
    total: float
    customer: str
    payment_status: str
    payment_method: str
    notes: str
    _source_row: int
    _parse_warnings: list = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)


# Column name mapping — handles common variations
COLUMN_ALIASES = {
    "date": ["date", "tanggal", "tgl", "tarikh", "transaction_date", "trx_date"],
    "type": ["type", "jenis", "tipe", "transaction_type", "trx_type", "category"],
    "product": ["product", "produk", "item", "nama", "name", "barang", "description"],
    "quantity": ["quantity", "qty", "jumlah", "jumlah_unit", "count", "volume"],
    "unit_price": ["unit_price", "harga", "price", "harga_satuan", "harga_unit", "price_per_unit"],
    "total": ["total", "jumlah_total", "subtotal", "amount", "nilai", "value"],
    "customer": ["customer", "pelanggan", "pembeli", "buyer", "client", "nama_customer"],
    "payment_status": ["payment_status", "status_bayar", "status", "bayar", "pembayaran"],
    "payment_method": ["payment_method", "metode", "metode_bayar", "payment", "pay_method"],
    "notes": ["notes", "catatan", "note", "keterangan", "remark", "remarks"],
}

# Default values
DEFAULT_TYPE = "order"
DEFAULT_PAYMENT_STATUS = "paid"
DEFAULT_PAYMENT_METHOD = "cash"


def _normalize_column(name: str) -> str:
    """Match a column name to standard field using aliases."""
    name_lower = name.strip().lower().replace(" ", "_")
    for standard, aliases in COLUMN_ALIASES.items():
        if name_lower in [a.lower().replace(" ", "_") for a in aliases]:
            return standard
    return ""


def _parse_date(val: str) -> tuple[str, list]:
    """Parse date string, return (ISO date, warnings)."""
    warnings = []
    val = val.strip()
    if not val:
        return "", ["empty date"]
    
    # Try common formats
    formats = [
        "%Y-%m-%d",    # 2026-10-27
        "%d/%m/%Y",    # 27/10/2026
        "%d-%m-%Y",    # 27-10-2026
        "%m/%d/%Y",    # 10/27/2026 (US)
        "%Y/%m/%d",    # 2026/10/27
        "%d.%m.%Y",    # 27.10.2026
        "%d %b %Y",    # 27 Oct 2026
        "%d %B %Y",    # 27 October 2026
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(val, fmt)
            return dt.strftime("%Y-%m-%d"), []
        except ValueError:
            continue
    
    # Try to extract date from string
    date_pattern = r'(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4})'
    match = re.search(date_pattern, val)
    if match:
        d, m, y = match.groups()
        if len(y) == 2:
            y = "20" + y
        try:
            dt = datetime(int(y), int(m), int(d))
            return dt.strftime("%Y-%m-%d"), [f"date extracted from '{val}'"]
        except ValueError:
            pass
    
    return "", [f"unparseable date: '{val}'"]


def _parse_float(val: str) -> tuple[float, list]:
    """Parse a number from string, handling Rp, thousand separators, etc."""
    warnings = []
    if val is None:
        return 0.0, ["empty value"]
    val = str(val).strip()
    if not val:
        return 0.0, ["empty value"]
    
    # Remove currency symbols and text
    val_clean = re.sub(r'[Rr][Pp]\.?\s*', '', val)
    val_clean = re.sub(r'[Ii][Dd][Rr]\s*', '', val_clean)
    val_clean = re.sub(r'[Rr][Uu][Pp][Ii][Aa][Hh]\s*', '', val_clean)
    
    # Handle both . and , as thousand separators or decimal
    # If both present, the last one is decimal
    if '.' in val_clean and ',' in val_clean:
        # Determine which is decimal (usually the last separator)
        last_dot = val_clean.rfind('.')
        last_comma = val_clean.rfind(',')
        if last_comma > last_dot:
            # Comma is decimal: remove dots, replace comma with dot
            val_clean = val_clean.replace('.', '').replace(',', '.')
        else:
            # Dot is decimal: remove commas
            val_clean = val_clean.replace(',', '')
    elif ',' in val_clean:
        # Could be decimal or thousand separator
        parts = val_clean.split(',')
        if len(parts) == 2 and len(parts[1]) <= 2:
            # Likely decimal
            val_clean = val_clean.replace(',', '.')
        else:
            # Likely thousand separator
            val_clean = val_clean.replace(',', '')
    
    # Remove any remaining non-numeric chars except . and -
    val_clean = re.sub(r'[^\d.\-]', '', val_clean)
    
    try:
        return float(val_clean), []
    except ValueError:
        return 0.0, [f"unparseable number: '{val}'"]


def _parse_payment_status(val: str) -> str:
    """Normalize payment status."""
    val = val.strip().lower()
    if val in ["paid", "lunas", "sudah bayar", "1", "done", "complete", "selesai"]:
        return "paid"
    if val in ["unpaid", "belum", "belum bayar", "0", "pending", "outstanding"]:
        return "unpaid"
    if val in ["partial", "sebagian", "cicil", "dp"]:
        return "partial"
    if val == "":
        return DEFAULT_PAYMENT_STATUS
    # Default to paid for unknown positive-sounding values
    return val if val else DEFAULT_PAYMENT_STATUS


def _parse_type(val: str) -> str:
    """Normalize transaction type."""
    val = val.strip().lower()
    if val in ["order", "penjualan", "sale", "sales", "jual", "pemesanan"]:
        return "order"
    if val in ["expense", "pengeluaran", "biaya", "cost", "purchase", "beli"]:
        return "expense"
    if val in ["stock_in", "stok_masuk", "restock", "inventory", "barang_masuk"]:
        return "stock_in"
    if val in ["adjustment", "penyesuaian", "adj", "koreksi"]:
        return "adjustment"
    if val == "":
        return DEFAULT_TYPE
    return val


def parse_csv(file_path: Path) -> tuple[list[dict], list[str]]:
    """Parse CSV file, return (records, warnings)."""
    warnings = []
    records = []
    
    # Try different encodings (utf-8-sig strips BOM)
    rows_data = None
    for encoding in ['utf-8-sig', 'utf-8', 'latin-1']:
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                if not headers:
                    raise ParseError("CSV file has no headers")
                # Strip BOM from headers if still present
                headers = [h.lstrip('\ufeff').strip() if h else h for h in headers]
                reader.fieldnames = headers
                # Read all rows while file is open
                rows_data = list(reader)
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise ParseError(f"Cannot read CSV: {e}")
    else:
        raise ParseError("Cannot decode CSV file with tried encodings")

    if rows_data is None:
        raise ParseError("No data read from CSV file")
    
    # Map columns
    column_map = {}
    for header in headers:
        standard = _normalize_column(header)
        if standard and standard not in column_map:
            column_map[standard] = header
    
    required = ["date", "total"]
    missing = [r for r in required if r not in column_map]
    if missing:
        raise ParseError(
            f"Missing required columns: {missing}. "
            f"Found columns: {list(headers)}. "
            f"Mapped: {column_map}"
        )
    
    if "type" not in column_map:
        warnings.append("No 'type' column found — defaulting all to 'order'")
    if "product" not in column_map:
        warnings.append("No 'product' column found")
    
    row_id = 0
    for source_row, row in enumerate(rows_data, start=2):  # row 1 is header
        # Skip empty rows
        if all(v is None or v.strip() == '' for v in row.values()):
            continue
        
        row_id += 1
        record_warnings = []
        
        def get_val(field_name):
            col = column_map.get(field_name)
            if col and col in row:
                return row[col].strip() if row[col] else ''
            return ''
        
        # Parse fields
        date_str = get_val("date")
        date, date_w = _parse_date(date_str)
        record_warnings.extend(date_w)
        
        type_str = get_val("type")
        rec_type = _parse_type(type_str)
        
        product = get_val("product") or "(unspecified)"
        
        qty_str = get_val("quantity")
        if qty_str:
            quantity, qty_w = _parse_float(qty_str)
            record_warnings.extend(qty_w)
        else:
            quantity = 1.0
            record_warnings.append("no quantity, defaulted to 1")
        
        price_str = get_val("unit_price")
        if price_str:
            unit_price, price_w = _parse_float(price_str)
            record_warnings.extend(price_w)
        else:
            unit_price = 0.0
        
        total_str = get_val("total")
        total, total_w = _parse_float(total_str)
        record_warnings.extend(total_w)
        
        # If total is 0 but we have qty*price, compute it
        if total == 0 and quantity > 0 and unit_price > 0:
            total = quantity * unit_price
            record_warnings.append(f"total computed from qty*price = {total}")
        
        # If total != qty*price, warn (but keep total as-is)
        if total > 0 and quantity > 0 and unit_price > 0:
            expected = quantity * unit_price
            if abs(total - expected) > 0.01 * max(total, expected):
                record_warnings.append(
                    f"total mismatch: stated {total} vs qty*price {expected}"
                )
        
        customer = get_val("customer")
        payment_status = _parse_payment_status(get_val("payment_status"))
        payment_method = get_val("payment_method") or DEFAULT_PAYMENT_METHOD
        notes = get_val("notes")
        
        record = Record(
            row_id=row_id,
            date=date,
            type=rec_type,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            total=total,
            customer=customer,
            payment_status=payment_status,
            payment_method=payment_method,
            notes=notes,
            _source_row=source_row,
            _parse_warnings=record_warnings,
        )
        records.append(record.to_dict())
    
    return records, warnings


def parse_xlsx(file_path: Path) -> tuple[list[dict], list[str]]:
    """Parse XLSX file using openpyxl."""
    try:
        from openpyxl import load_workbook
    except ImportError:
        # Fall back to CSV if openpyxl not available
        raise ParseError(
            "openpyxl not installed. Please install with: pip install openpyxl. "
            "Or use CSV input instead."
        )
    
    warnings = []
    wb = load_workbook(file_path, data_only=True)
    ws = wb.active
    
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise ParseError("XLSX file is empty")
    
    headers = [str(h).strip() if h else '' for h in rows[0]]
    
    # Map columns
    column_map = {}
    for i, header in enumerate(headers):
        standard = _normalize_column(header)
        if standard and standard not in column_map:
            column_map[standard] = i
    
    required = ["date", "total"]
    missing = [r for r in required if r not in column_map]
    if missing:
        raise ParseError(
            f"Missing required columns: {missing}. "
            f"Found columns: {headers}"
        )
    
    if "type" not in column_map:
        warnings.append("No 'type' column found — defaulting all to 'order'")
    
    records = []
    row_id = 0
    
    for source_row, row_values in enumerate(rows[1:], start=2):
        # Skip empty rows
        if all(v is None or str(v).strip() == '' for v in row_values):
            continue
        
        row_id += 1
        record_warnings = []
        
        def get_val(field_name):
            idx = column_map.get(field_name)
            if idx is not None and idx < len(row_values):
                v = row_values[idx]
                return str(v).strip() if v is not None else ''
            return ''
        
        date_str = get_val("date")
        if not date_str:
            # Try if it's already a datetime object
            idx = column_map.get("date")
            if idx is not None and idx < len(row_values) and isinstance(row_values[idx], datetime):
                date = row_values[idx].strftime("%Y-%m-%d")
                date_str = date
            else:
                date, date_w = _parse_date(date_str)
                record_warnings.extend(date_w)
        else:
            date, date_w = _parse_date(date_str)
            record_warnings.extend(date_w)
        
        type_str = get_val("type")
        rec_type = _parse_type(type_str)
        
        product = get_val("product") or "(unspecified)"
        
        qty_str = get_val("quantity")
        quantity, qty_w = _parse_float(qty_str) if qty_str else (1.0, ["no quantity"])
        record_warnings.extend(qty_w)
        
        price_str = get_val("unit_price")
        unit_price, price_w = _parse_float(price_str) if price_str else (0.0, [])
        record_warnings.extend(price_w)
        
        total_str = get_val("total")
        total, total_w = _parse_float(total_str)
        record_warnings.extend(total_w)
        
        if total == 0 and quantity > 0 and unit_price > 0:
            total = quantity * unit_price
            record_warnings.append(f"total computed from qty*price = {total}")
        
        customer = get_val("customer")
        payment_status = _parse_payment_status(get_val("payment_status"))
        payment_method = get_val("payment_method") or DEFAULT_PAYMENT_METHOD
        notes = get_val("notes")
        
        record = Record(
            row_id=row_id,
            date=date,
            type=rec_type,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            total=total,
            customer=customer,
            payment_status=payment_status,
            payment_method=payment_method,
            notes=notes,
            _source_row=source_row,
            _parse_warnings=record_warnings,
        )
        records.append(record.to_dict())
    
    return records, warnings


def parse_file(file_path: Path) -> tuple[list[dict], list[str]]:
    """
    Parse input file based on extension.
    
    Args:
        file_path: Path to CSV or XLSX file
        
    Returns:
        Tuple of (records list, warnings list)
        
    Raises:
        ParseError: If file cannot be parsed
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    ext = file_path.suffix.lower()
    
    if ext == '.csv':
        return parse_csv(file_path)
    elif ext in ['.xlsx', '.xls']:
        return parse_xlsx(file_path)
    else:
        raise ParseError(f"Unsupported file format: {ext}. Supported: .csv, .xlsx")
