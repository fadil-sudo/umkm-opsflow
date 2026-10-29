#!/usr/bin/env python3
"""
UMKM OpsFlow — Streamlit Web UI
Tencent Cloud Hackathon Indonesia 2026
"""

import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import streamlit as st
from opsflow import run_pipeline

st.set_page_config(
    page_title="UMKM OpsFlow",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4a4a6a;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .action-high {
        border-left: 4px solid #dc3545;
        padding: 0.75rem;
        background: #fff5f5;
        margin-bottom: 0.5rem;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    .action-medium {
        border-left: 4px solid #ffc107;
        padding: 0.75rem;
        background: #fffbf0;
        margin-bottom: 0.5rem;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    .action-low {
        border-left: 4px solid #28a745;
        padding: 0.75rem;
        background: #f0fff4;
        margin-bottom: 0.5rem;
        border-radius: 0 0.5rem 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/commercial.png", width=60)
    st.title("UMKM OpsFlow")
    st.markdown("**Agent Laporan Operasional Harian**")
    st.markdown("---")
    
    st.markdown("### 📋 Panduan")
    st.markdown("""
    1. **Upload** file CSV order/nota
    2. **Klik** "Proses Data"
    3. **Lihat** laporan & tindakan
    4. **Setujui** draf pesan sebelum kirim
    """)
    
    st.markdown("---")
    st.markdown("**Challenge:** The Office Agent — Automate Better")
    st.markdown("**Hackathon:** Tencent Cloud AI CAN DO IT 2026")

# Main header
st.markdown('<div class="main-header">📊 UMKM OpsFlow</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ubah catatan order/nota berantakan menjadi laporan operasional harian yang tervalidasi</div>', unsafe_allow_html=True)

# Tabs
tab_upload, tab_demo, tab_about = st.tabs(["📤 Upload & Proses", "🎬 Data Demo", "ℹ️ Tentang"])

with tab_upload:
    st.markdown("### Upload File CSV")
    
    uploaded_file = st.file_uploader(
        "Pilih file CSV order/nota harian",
        type=["csv"],
        help="Format: tanggal, produk, jumlah, total, metode, catatan"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        process_btn = st.button("🚀 Proses Data", type="primary", use_container_width=True)
    
    if uploaded_file is not None and process_btn:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / uploaded_file.name
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()
            
            input_path.write_bytes(uploaded_file.getvalue())
            
            with st.spinner("Agent sedang memproses data..."):
                result = run_pipeline(str(input_path), str(output_dir))
            
            if result.get("error"):
                st.markdown(f'<div class="error-box"><b>❌ Error:</b> {result["error"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box"><b>✅ Berhasil!</b> Data telah diproses.</div>', unsafe_allow_html=True)
                
                # Metrics row
                metrics = result.get("metrics", {})
                if metrics:
                    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                    with mcol1:
                        st.metric("💰 Pendapatan", f"Rp {metrics.get('total_revenue', 0):,}")
                    with mcol2:
                        st.metric("💸 Pengeluaran", f"Rp {metrics.get('total_expenses', 0):,}")
                    with mcol3:
                        net = metrics.get('net_cashflow', 0)
                        st.metric("📈 Net Cashflow", f"Rp {net:,}", delta="Profit" if net >= 0 else "Loss")
                    with mcol4:
                        st.metric("📋 Record", f"{result.get('validated_count', 0)}/{result.get('records_count', 0)}")
                
                # Clarifications
                clarifications = result.get("clarifications", [])
                if clarifications:
                    st.markdown("---")
                    st.markdown("### 🔴 Pertanyaan Klarifikasi")
                    st.info("Agent mendeteksi ambiguitas. Mohon periksa sebelum melanjutkan.")
                    for c in clarifications:
                        severity_emoji = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(c.get("severity"), "⚪")
                        with st.expander(f"{severity_emoji} [{c.get('severity', '').upper()}] {c.get('question', '')}"):
                            st.write(f"**Konteks:** {c.get('context', '-')}")
                            if c.get("suggested_resolution"):
                                st.write(f"**Saran:** {c.get('suggested_resolution')}")
                
                # Issues
                issues = result.get("issues", [])
                if issues:
                    st.markdown("---")
                    st.markdown("### ⚠️ Validasi Data")
                    error_count = sum(1 for i in issues if i.get("severity") == "error")
                    warning_count = sum(1 for i in issues if i.get("severity") == "warning")
                    info_count = sum(1 for i in issues if i.get("severity") == "info")
                    
                    icol1, icol2, icol3 = st.columns(3)
                    with icol1:
                        st.markdown(f'<div class="error-box">❌ Error: {error_count}</div>', unsafe_allow_html=True)
                    with icol2:
                        st.markdown(f'<div class="warning-box">⚠️ Warning: {warning_count}</div>', unsafe_allow_html=True)
                    with icol3:
                        st.markdown(f'<div class="info-box">ℹ️ Info: {info_count}</div>', unsafe_allow_html=True)
                    
                    with st.expander("Lihat detail masalah"):
                        for issue in issues:
                            sev = issue.get("severity", "")
                            icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(sev, "")
                            st.write(f"{icon} **{issue.get('field', '')}** — {issue.get('issue', '')}")
                            st.caption(f"Baris: {issue.get('source_row', '-')} | Detail: {issue.get('detail', '-')} | Tindakan: {issue.get('suggested_action', '-')}")
                
                # Actions
                actions = result.get("actions", [])
                if actions:
                    st.markdown("---")
                    st.markdown("### ✅ Item Tindakan")
                    for action in actions:
                        priority = action.get("priority", "low")
                        css_class = f"action-{priority}"
                        icon = {"high": "🔴", "medium": "🟠", "low": "🟢"}.get(priority, "⚪")
                        st.markdown(f'''
                        <div class="{css_class}">
                            <b>{icon} [{priority.upper()}] {action.get("title", "")}</b><br>
                            <small>{action.get("description", "")}</small><br>
                            <small><i>Kategori: {action.get("category", "")}</i></small>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        if action.get("draft_needed"):
                            with st.expander("📝 Lihat Draf Pesan"):
                                draft = action.get("draft_context", {})
                                if draft.get("recipient"):
                                    st.write(f"**Penerima:** {draft['recipient']}")
                                if draft.get("content"):
                                    st.text_area("Isi pesan:", draft["content"], height=100, key=f"draft_{action.get('title', '')[:20]}")
                                st.warning("⚠️ Pesan ini belum dikirim. Klik 'Setujui & Kirim' untuk melanjutkan (mock).")
                                approve = st.button("✅ Setujui & Kirim (Mock)", key=f"approve_{action.get('title', '')[:20]}")
                                if approve:
                                    st.success("✅ Tindakan disetujui. Dalam produksi, pesan akan dikirim.")
                
                # Report preview
                st.markdown("---")
                st.markdown("### 📄 Laporan Harian")
                report_path = output_dir / "daily_report.md"
                if report_path.exists():
                    report_content = report_path.read_text(encoding="utf-8")
                    st.markdown(report_content)
                
                # Download buttons
                st.markdown("---")
                st.markdown("### 💾 Unduh Hasil")
                dcol1, dcol2, dcol3 = st.columns(3)
                
                with dcol1:
                    if report_path.exists():
                        st.download_button(
                            "📄 Laporan (MD)",
                            report_path.read_text(encoding="utf-8"),
                            file_name="daily_report.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                
                with dcol2:
                    metrics_path = output_dir / "metrics.json"
                    if metrics_path.exists():
                        st.download_button(
                            "📊 Metrics (JSON)",
                            metrics_path.read_text(encoding="utf-8"),
                            file_name="metrics.json",
                            mime="application/json",
                            use_container_width=True
                        )
                
                with dcol3:
                    action_path = output_dir / "action_items.csv"
                    if action_path.exists():
                        st.download_button(
                            "📋 Actions (CSV)",
                            action_path.read_bytes(),
                            file_name="action_items.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

with tab_demo:
    st.markdown("### 🎬 Data Demo")
    st.info("Pilih salah satu dataset demo di bawah ini untuk melihat cara kerja agent.")
    
    demo_data_dir = Path(__file__).parent / "data"
    demo_files = sorted(demo_data_dir.glob("*.csv")) if demo_data_dir.exists() else []
    
    if demo_files:
        selected_demo = st.selectbox(
            "Pilih dataset demo:",
            options=[f.name for f in demo_files],
            format_func=lambda x: {
                "sample_orders_clean.csv": "✅ Data Bersih (semua valid)",
                "sample_orders_messy.csv": "⚠️ Data Berantakan (ada masalah)",
                "sample_ambiguous.csv": "❓ Data Ambigu (butuh klarifikasi)",
                "sample_prompt_injection.csv": "🛡️ Prompt Injection Test (keamanan)",
                "sample_orders_empty.csv": "📭 File Kosong (edge case)",
            }.get(x, x)
        )
        
        demo_path = demo_data_dir / selected_demo
        
        with st.expander("👁️ Preview Data"):
            import csv
            with open(demo_path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    st.write(f"**{len(rows)} baris**")
                    st.dataframe(rows, use_container_width=True)
                else:
                    st.warning("File kosong")
        
        if st.button("🚀 Proses Demo", type="primary"):
            with tempfile.TemporaryDirectory() as tmpdir:
                output_dir = Path(tmpdir) / "output"
                output_dir.mkdir()
                
                with st.spinner("Agent sedang memproses..."):
                    result = run_pipeline(str(demo_path), str(output_dir))
                
                if result.get("error"):
                    st.markdown(f'<div class="error-box"><b>❌ Error:</b> {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-box"><b>✅ Berhasil diproses!</b></div>', unsafe_allow_html=True)
                    
                    metrics = result.get("metrics", {})
                    if metrics:
                        mcol1, mcol2, mcol3 = st.columns(3)
                        with mcol1:
                            st.metric("Pendapatan", f"Rp {metrics.get('total_revenue', 0):,}")
                        with mcol2:
                            st.metric("Pengeluaran", f"Rp {metrics.get('total_expenses', 0):,}")
                        with mcol3:
                            st.metric("Net", f"Rp {metrics.get('net_cashflow', 0):,}")
                    
                    clarifications = result.get("clarifications", [])
                    if clarifications:
                        st.warning(f"🔴 {len(clarifications)} pertanyaan klarifikasi ditemukan!")
                        for c in clarifications:
                            st.write(f"**{c.get('question', '')}** — {c.get('context', '')}")
                    
                    issues = result.get("issues", [])
                    if issues:
                        st.info(f"⚠️ {len(issues)} masalah validasi ditemukan")
                    
                    actions = result.get("actions", [])
                    if actions:
                        st.success(f"✅ {len(actions)} item tindakan dihasilkan")
    else:
        st.warning("Tidak ada file demo ditemukan di folder data/")

with tab_about:
    st.markdown("### ℹ️ Tentang UMKM OpsFlow")
    st.markdown("""
    **UMKM OpsFlow** adalah agent AI yang mengubah catatan order dan nota UMKM yang berantakan 
    menjadi laporan operasional harian yang tervalidasi, dapat diaudit, dan siap ditindaklanjuti.
    
    #### 🎯 Fitur Utama
    - **Parsing Otomatis** — Baca CSV/XLSX dan ekstrak field penting
    - **Validasi Data** — Deteksi missing, duplikat, outlier, dan nilai aneh
    - **Klarifikasi Ambigu** — Tanya pengguna saat data tidak jelas
    - **Perhitungan Deterministik** — Semua angka dari Python, bukan tebakan LLM
    - **Jejak Audit** — Setiap angka bisa ditelusuri ke baris sumber
    - **Approval Gate** — Tidak ada tindakan eksternal tanpa persetujuan
    
    #### 🛡️ 5 Aturan Akuntabilitas
    1. **SOURCES** — Tunjukkan sumber setiap jawaban
    2. **PERMISSIONS** — Tetap dalam izin pengguna
    3. **APPROVAL** — Tanya sebelum bertindak
    4. **LIMITS** — Akui batasan, jangan tebak
    5. **RECORD** — Simpan catatan audit
    
    #### 🏆 Hackathon
    - **Event:** Tencent Cloud AI CAN DO IT / Hackathon Indonesia 2026
    - **Challenge:** B — The Office Agent (Automate Better)
    - **Platform:** Tencent WorkBuddy
    """)
    
    st.markdown("---")
    st.markdown("**Dibuat oleh:** fadil-sudo  ")
    st.markdown("**Repo:** https://github.com/fadil-sudo/umkm-opsflow")
