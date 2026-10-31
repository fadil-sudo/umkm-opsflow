"""
clarify.py — Detect ambiguous situations that require user clarification.

This module implements the "LIMITS" accountability rule:
  "Raise a concise clarifying question when something is ambiguous,
   and refrain from asking when the answer is evident."

Examples from the hackathon handbook:
  - "Tolong kirim notulen ke Pak Budi" → org has two employees named Budi
  - "Jadwalin follow-up Jumat siang" → coincides with prayer time
  - Data has conflicting information that needs resolution

Ambiguity types detected:
  1. Duplicate customer names with different contexts
  2. Conflicting payment statuses for same customer
  3. Multiple products with similar names
  4. Dates that fall on public holidays or prayer times
  5. Missing critical context (no customer, no product, ambiguous type)
"""

from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


# Indonesian public holidays 2026 (simplified — major ones)
INDONESIAN_HOLIDAYS_2026 = {
    "2026-01-01",  # Tahun Baru
    "2026-02-17",  # Tahun Baru Imlek
    "2026-03-09",  # Hari Raya Nyepi
    "2026-03-31",  # Idul Fitri
    "2026-04-01",  # Idul Fitri
    "2026-04-02",  # Idul Fitri (collective leave)
    "2026-04-03",  # Idul Fitri (collective leave)
    "2026-05-01",  # Hari Buruh
    "2026-05-14",  # Waisak
    "2026-05-29",  # Kenaikan Isa Almasih
    "2026-06-01",  # Hari Lahir Pancasila
    "2026-06-07",  # Idul Adha
    "2026-08-17",  # Hari Kemerdekaan
    "2026-09-16",  # Maulid Nabi
    "2026-12-25",  # Natal
}

# Friday prayer time in WIB (approximate: 11:30 - 13:00)
FRIDAY_PRAYER_START = 11.5  # 11:30
FRIDAY_PRAYER_END = 13.0    # 13:00


@dataclass
class ClarificationQuestion:
    ambiguity_type: str
    question: str
    context: str
    suggested_resolution: str
    severity: str = "medium"  # "high" | "medium" | "low"
    
    def to_dict(self):
        return asdict(self)


def detect_ambiguities(records: list[dict], issues: list) -> list[ClarificationQuestion]:
    """
    Detect ambiguous situations that need user clarification.
    
    Returns list of ClarificationQuestion objects.
    Only raises questions when genuinely ambiguous (not for obvious cases).
    """
    questions = []
    
    # --- 1. Duplicate customer names with different unpaid amounts ---
    customer_records = {}
    for r in records:
        customer = r.get("customer", "").strip()
        if customer:
            if customer not in customer_records:
                customer_records[customer] = []
            customer_records[customer].append(r)
    
    # Check for customers with multiple different payment statuses on same day
    for customer, cust_records in customer_records.items():
        if len(cust_records) >= 2:
            # Check if same customer has both paid and unpaid on same date
            dates_with_mixed = {}
            for r in cust_records:
                date = r.get("date", "")
                status = r.get("payment_status", "").lower()
                if date:
                    if date not in dates_with_mixed:
                        dates_with_mixed[date] = set()
                    dates_with_mixed[date].add(status)
            
            for date, statuses in dates_with_mixed.items():
                if "paid" in statuses and "unpaid" in statuses:
                    questions.append(ClarificationQuestion(
                        ambiguity_type="mixed_payment_status",
                        question=f"Pelanggan '{customer}' memiliki order dengan status 'paid' dan 'unpaid' pada tanggal yang sama ({date}). Apakah ini benar?",
                        context=f"Ditemukan {len(cust_records)} transaksi untuk {customer} pada {date} dengan status pembayaran berbeda.",
                        suggested_resolution="Verifikasi status pembayaran yang benar untuk setiap order.",
                        severity="medium"
                    ))
                    break  # Only one question per customer
    
    # --- 2. Similar product names (potential typos/variants) ---
    product_names = {}
    for r in records:
        product = r.get("product", "").strip().lower()
        if product:
            # Simple fuzzy matching: products that share first 4 chars
            key = product[:4]
            if key not in product_names:
                product_names[key] = []
            product_names[key].append(product)
    
    for key, products in product_names.items():
        unique_products = list(set(products))
        if len(unique_products) >= 2:
            # Check if they're actually different (not exact duplicates)
            if len(unique_products) == 2:
                p1, p2 = unique_products[0], unique_products[1]
                # Only flag if they're very similar (e.g., "kopi" vs "kopi susu" not "kopi" vs "kue")
                if abs(len(p1) - len(p2)) <= 5 and (p1 in p2 or p2 in p1 or key in p1 and key in p2):
                    questions.append(ClarificationQuestion(
                        ambiguity_type="similar_product_names",
                        question=f"Apakah '{p1.title()}' dan '{p2.title()}' adalah produk yang sama?",
                        context=f"Ditemukan nama produk yang mirip dalam data. Ini bisa jadi varian penulisan atau produk berbeda.",
                        suggested_resolution="Tentukan apakah ini produk yang sama (gabungkan) atau berbeda (biarkan terpisah).",
                        severity="low"
                    ))
                    break
    
    # --- 3. Dates on public holidays ---
    for r in records:
        date = r.get("date", "")
        if date and date in INDONESIAN_HOLIDAYS_2026:
            questions.append(ClarificationQuestion(
                ambiguity_type="public_holiday",
                question=f"Transaksi pada {date} jatuh pada hari libur nasional. Apakah bisnis buka pada hari ini?",
                context=f"Tanggal {date} adalah hari libur nasional Indonesia. Transaksi pada hari libur mungkin perlu verifikasi.",
                suggested_resolution="Konfirmasi apakah transaksi ini valid atau tanggal perlu dikoreksi.",
                severity="low"
            ))
            break  # Only one holiday question
    
    # --- 4. Friday transactions during prayer time ---
    for r in records:
        date_str = r.get("date", "")
        time_str = r.get("time", "")  # May not exist in all data
        if date_str and time_str:
            try:
                dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                if dt.weekday() == 4:  # Friday = 4
                    hour = dt.hour + dt.minute / 60
                    if FRIDAY_PRAYER_START <= hour <= FRIDAY_PRAYER_END:
                        questions.append(ClarificationQuestion(
                            ambiguity_type="friday_prayer_time",
                            question=f"Transaksi pada Jumat pukul {time_str} bertepatan dengan waktu sholat Jumat. Apakah waktu ini benar?",
                            context="Waktu transaksi jatuh pada periode sholat Jumat (11:30-13:00 WIB).",
                            suggested_resolution="Verifikasi waktu transaksi atau konfirmasi bisnis buka pada jam tersebut.",
                            severity="low"
                        ))
                        break
            except ValueError:
                pass
    
    # --- 5. Records with completely missing critical info (but not caught by validation) ---
    # These are edge cases where data exists but is unusable
    records_with_no_context = []
    for r in records:
        if not r.get("product") and not r.get("customer") and r.get("total", 0) == 0:
            records_with_no_context.append(r)
    
    if records_with_no_context:
        questions.append(ClarificationQuestion(
            ambiguity_type="no_context",
            question=f"Ditemukan {len(records_with_no_context)} baris tanpa informasi produk, pelanggan, atau jumlah. Apakah baris ini perlu dihapus atau dilengkapi?",
            context="Baris ini tidak memiliki informasi yang cukup untuk diproses.",
            suggested_resolution="Hapus baris kosong atau lengkapi informasi yang hilang.",
            severity="medium"
        ))
    
    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    questions.sort(key=lambda q: severity_order.get(q.severity, 9))
    
    return questions


def format_clarification_report(questions: list[ClarificationQuestion]) -> str:
    """Format clarification questions for display in report."""
    if not questions:
        return ""
    
    lines = ["\n--- Pertanyaan Klarifikasi ---\n"]
    lines.append("Agent mendeteksi situasi yang membutuhkan klarifikasi dari Anda:\n")
    
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. [{q.severity.upper()}] {q.question}")
        lines.append(f"   Konteks: {q.context}")
        lines.append(f"   Saran: {q.suggested_resolution}\n")
    
    lines.append("Agent akan melanjutkan dengan asumsi default. Silakan review dan koreksi jika perlu.\n")
    
    return "\n".join(lines)
