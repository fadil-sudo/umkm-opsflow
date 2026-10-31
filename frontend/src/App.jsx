import { useState, useRef, useCallback, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || '/api'

const urlParams = new URLSearchParams(window.location.search)
const shareCode = urlParams.get('sharecode')
const shareCodeSuffix = shareCode ? `?sharecode=${shareCode}` : ''

function apiUrl(path) {
  return `${API_URL}${path}${shareCodeSuffix}`
}

function formatRupiah(num) {
  if (num === undefined || num === null) return 'Rp 0'
  return 'Rp ' + num.toLocaleString('id-ID')
}

function SeverityBadge({ severity }) {
  const styles = {
    error: 'bg-red-100 text-red-700 border-red-200',
    warning: 'bg-amber-100 text-amber-700 border-amber-200',
    info: 'bg-blue-100 text-blue-700 border-blue-200',
  }
  return (
    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${styles[severity] || styles.info}`}>
      {severity?.toUpperCase()}
    </span>
  )
}

function PriorityBadge({ priority }) {
  const styles = {
    high: 'bg-red-100 text-red-700',
    medium: 'bg-amber-100 text-amber-700',
    low: 'bg-green-100 text-green-700',
  }
  return (
    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${styles[priority] || styles.low}`}>
      {priority?.toUpperCase()}
    </span>
  )
}

function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000)
    return () => clearTimeout(timer)
  }, [onClose])

  const bg = type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-gray-800'

  return (
    <div className={`fixed bottom-6 right-6 z-50 ${bg} text-white px-4 py-3 rounded-lg shadow-lg text-sm font-medium animate-bounce`}>
      {message}
      <button onClick={onClose} className="ml-3 opacity-70 hover:opacity-100">×</button>
    </div>
  )
}

function GuideModal({ onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-white rounded-xl shadow-2xl max-w-lg w-full mx-4 p-6" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900">📖 Panduan UMKM OpsFlow</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-xl">×</button>
        </div>
        <div className="space-y-4 text-sm text-gray-600">
          <div>
            <p className="font-semibold text-gray-800 mb-1">1. Upload Data</p>
            <p>Drag & drop file CSV atau Excel berisi data transaksi harian UMKM Anda. Format yang didukung: tanggal, produk, jumlah, harga, total, pelanggan, status bayar.</p>
          </div>
          <div>
            <p className="font-semibold text-gray-800 mb-1">2. Pipeline Otomatis</p>
            <p>Sistem akan memparse, memvalidasi, mendeteksi ambiguitas, menghitung metrik, dan menghasilkan action items.</p>
          </div>
          <div>
            <p className="font-semibold text-gray-800 mb-1">3. Review Hasil</p>
            <p>Cek tab <strong>Validasi</strong> untuk masalah data, <strong>Klarifikasi</strong> untuk pertanyaan yang perlu dijawab, dan <strong>Tindakan</strong> untuk draft pesan follow-up.</p>
          </div>
          <div>
            <p className="font-semibold text-gray-800 mb-1">4. Setujui / Abaikan</p>
            <p>Di tab Tindakan, klik <strong>Setujui</strong> untuk menandai draft pesan siap dikirim, atau <strong>Abaikan</strong> jika tidak perlu ditindaklanjuti.</p>
          </div>
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-amber-800">
            <p className="font-semibold">⚠️ Human-in-the-Loop</p>
            <p>Tidak ada tindakan eksternal yang dieksekusi tanpa persetujuan Anda. Semua draft pesan harus disetujui manual.</p>
          </div>
        </div>
        <button onClick={onClose} className="mt-6 w-full py-2 bg-opsflow-600 text-white rounded-lg text-sm font-medium hover:bg-opsflow-700">
          Mengerti
        </button>
      </div>
    </div>
  )
}

export default function App() {
  const [file, setFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')
  const [actionStatuses, setActionStatuses] = useState({})
  const [actionLog, setActionLog] = useState([])
  const [toast, setToast] = useState(null)
  const [showGuide, setShowGuide] = useState(false)
  const [showLogPanel, setShowLogPanel] = useState(false)
  const inputRef = useRef(null)

  const showToast = (message, type = 'success') => {
    setToast({ message, type })
  }

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
      setResult(null)
      setError(null)
      setActionStatuses({})
      setActionLog([])
    }
  }, [])

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setResult(null)
      setError(null)
      setActionStatuses({})
      setActionLog([])
    }
  }

  const handleSubmit = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)
    setActionStatuses({})
    setActionLog([])

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(apiUrl('/process'), {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || `HTTP ${res.status}`)
      }
      setResult(data)
      setActiveTab('overview')
      showToast(`Berhasil memproses ${data.records_count || 0} baris!`, 'success')
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = (idx) => {
    setActionStatuses(prev => ({ ...prev, [idx]: 'approved' }))
    const action = result?.actions?.[idx]
    if (action) {
      setActionLog(prev => [...prev, { ...action, decision: 'approved', time: new Date().toLocaleTimeString('id-ID') }])
      showToast(`✅ "${action.title}" disetujui — draft pesan disiapkan!`, 'success')
      if (action.draft_message) {
        navigator.clipboard?.writeText(action.draft_message).catch(() => {})
      }
    }
  }

  const handleIgnore = (idx) => {
    setActionStatuses(prev => ({ ...prev, [idx]: 'ignored' }))
    const action = result?.actions?.[idx]
    if (action) {
      setActionLog(prev => [...prev, { ...action, decision: 'ignored', time: new Date().toLocaleTimeString('id-ID') }])
      showToast(`❌ "${action.title}" diabaikan`, 'info')
    }
  }

  const approvedCount = actionLog.filter(a => a.decision === 'approved').length
  const ignoredCount = actionLog.filter(a => a.decision === 'ignored').length

  const tabs = [
    { id: 'overview', label: 'Ringkasan', count: null },
    { id: 'issues', label: 'Validasi', count: result?.issues?.length },
    { id: 'clarifications', label: 'Klarifikasi', count: result?.clarifications?.length },
    { id: 'actions', label: 'Tindakan', count: result?.actions?.length },
  ]

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col hidden md:flex">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-opsflow-600 flex items-center justify-center text-white font-bold text-sm">
              O
            </div>
            <h1 className="font-bold text-lg text-gray-900">OpsFlow</h1>
          </div>
          <p className="text-xs text-gray-500 mt-1">AI Agent untuk UMKM</p>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-3 py-2">Menu</div>
          <button className="w-full text-left px-3 py-2 rounded-lg bg-opsflow-50 text-opsflow-700 font-medium text-sm">
            Proses Data
          </button>
          <button
            onClick={() => setShowGuide(true)}
            className="w-full text-left px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-50 text-sm transition-colors"
          >
            Panduan
          </button>
          <button
            onClick={() => setShowLogPanel(!showLogPanel)}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center justify-between ${
              showLogPanel ? 'bg-opsflow-50 text-opsflow-700 font-medium' : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span>Log Tindakan</span>
            {actionLog.length > 0 && (
              <span className="text-xs bg-opsflow-600 text-white px-1.5 py-0.5 rounded-full">{actionLog.length}</span>
            )}
          </button>
        </nav>
        {actionLog.length > 0 && (
          <div className="px-4 py-3 border-t border-gray-200">
            <div className="text-xs space-y-1">
              <div className="flex justify-between text-green-700">
                <span>✅ Disetujui</span>
                <span className="font-bold">{approvedCount}</span>
              </div>
              <div className="flex justify-between text-gray-500">
                <span>❌ Diabaikan</span>
                <span className="font-bold">{ignoredCount}</span>
              </div>
            </div>
          </div>
        )}
        <div className="p-4 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <p className="font-medium text-gray-700">UMKM OpsFlow</p>
            <p className="mt-0.5">Tencent Cloud Hackathon 2026</p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Proses Data Harian</h2>
            <p className="text-sm text-gray-500">Upload CSV/XLSX → Validasi → Laporan → Tindakan</p>
          </div>
          <div className="flex items-center gap-3">
            {actionLog.length > 0 && (
              <button
                onClick={() => setShowLogPanel(!showLogPanel)}
                className="text-xs px-3 py-1.5 bg-opsflow-100 text-opsflow-700 rounded-full font-medium hover:bg-opsflow-200 transition-colors"
              >
                Log: {approvedCount} setuju, {ignoredCount} abaikan
              </button>
            )}
            <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded-full font-medium">Online</span>
          </div>
        </header>

        {/* Body: Main + Right Panel */}
        <div className="flex-1 flex overflow-hidden">
          {/* Scrollable Main */}
          <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
            <div className="max-w-4xl mx-auto space-y-6">

              {/* Upload Area */}
              <div
                className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
                  dragActive
                    ? 'border-opsflow-500 bg-opsflow-50'
                    : file
                    ? 'border-green-400 bg-green-50'
                    : 'border-gray-300 bg-white hover:border-gray-400'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current?.click()}
              >
                <input
                  ref={inputRef}
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  className="hidden"
                  onChange={handleChange}
                />
                <div className="mx-auto w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mb-3">
                  <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {file ? (
                  <div>
                    <p className="text-sm font-medium text-gray-900">{file.name}</p>
                    <p className="text-xs text-gray-500 mt-1">{(file.size / 1024).toFixed(1)} KB</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-gray-700">Drag & drop file CSV/XLSX di sini</p>
                    <p className="text-xs text-gray-500 mt-1">atau klik untuk pilih file</p>
                  </div>
                )}
              </div>

              {file && (
                <div className="flex justify-center">
                  <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="px-6 py-2.5 bg-opsflow-600 hover:bg-opsflow-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-lg text-sm transition-colors flex items-center gap-2"
                  >
                    {loading && (
                      <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    )}
                    {loading ? 'Memproses...' : 'Jalankan Pipeline'}
                  </button>
                </div>
              )}

              {/* Error */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-700">
                  <p className="font-semibold">Terjadi kesalahan</p>
                  <p className="mt-1">{error}</p>
                </div>
              )}

              {/* Results */}
              {result && (
                <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                  {/* Status Bar */}
                  <div className={`px-6 py-3 border-b border-gray-200 flex items-center justify-between ${
                    result.status === 'success' ? 'bg-green-50' : result.status === 'partial' ? 'bg-amber-50' : 'bg-red-50'
                  }`}>
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${
                        result.status === 'success' ? 'bg-green-500' : result.status === 'partial' ? 'bg-amber-500' : 'bg-red-500'
                      }`} />
                      <span className="text-sm font-medium text-gray-700 capitalize">
                        Status: {result.status === 'success' ? 'Berhasil' : result.status === 'partial' ? 'Sebagian' : 'Error'}
                      </span>
                    </div>
                    <div className="text-xs text-gray-500">
                      {result.records_count} baris → {result.validated_count} valid
                      {result.rejected_count > 0 && ` | ${result.rejected_count} ditolak`}
                    </div>
                  </div>

                  {/* Tabs */}
                  <div className="border-b border-gray-200">
                    <div className="flex px-2">
                      {tabs.map((tab) => (
                        <button
                          key={tab.id}
                          onClick={() => setActiveTab(tab.id)}
                          className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                            activeTab === tab.id
                              ? 'border-opsflow-600 text-opsflow-700'
                              : 'border-transparent text-gray-500 hover:text-gray-700'
                          }`}
                        >
                          {tab.label}
                          {tab.count !== null && tab.count > 0 && (
                            <span className="ml-1.5 text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded-full">
                              {tab.count}
                            </span>
                          )}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Tab Content */}
                  <div className="p-6">
                    {activeTab === 'overview' && (
                      <div className="space-y-6">
                        {result.metrics && (
                          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div className="bg-gray-50 rounded-lg p-4">
                              <p className="text-xs text-gray-500 uppercase tracking-wide">Total Pendapatan</p>
                              <p className="text-xl font-bold text-green-600 mt-1">{formatRupiah(result.metrics.total_revenue)}</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-4">
                              <p className="text-xs text-gray-500 uppercase tracking-wide">Total Pengeluaran</p>
                              <p className="text-xl font-bold text-red-600 mt-1">{formatRupiah(result.metrics.total_expenses)}</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-4">
                              <p className="text-xs text-gray-500 uppercase tracking-wide">Laba Bersih</p>
                              <p className={`text-xl font-bold mt-1 ${result.metrics.net_profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {formatRupiah(result.metrics.net_profit)}
                              </p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-4">
                              <p className="text-xs text-gray-500 uppercase tracking-wide">Pesanan Belum Bayar</p>
                              <p className="text-xl font-bold text-amber-600 mt-1">{result.metrics.unpaid_count}</p>
                              <p className="text-xs text-gray-500 mt-0.5">{formatRupiah(result.metrics.unpaid_total)}</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-4">
                              <p className="text-xs text-gray-500 uppercase tracking-wide">Jumlah Transaksi</p>
                              <p className="text-xl font-bold text-gray-800 mt-1">{result.metrics.transaction_count}</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-4">
                              <p className="text-xs text-gray-500 uppercase tracking-wide">Rata-rata per Transaksi</p>
                              <p className="text-xl font-bold text-gray-800 mt-1">{formatRupiah(result.metrics.avg_transaction)}</p>
                            </div>
                          </div>
                        )}

                        {result.parse_warnings?.length > 0 && (
                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <p className="text-sm font-semibold text-blue-800 mb-2">Peringatan Parsing</p>
                            <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
                              {result.parse_warnings.map((w, i) => (
                                <li key={i}>{w}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}

                    {activeTab === 'issues' && (
                      <div className="space-y-3">
                        {result.issues?.length === 0 ? (
                          <p className="text-sm text-gray-500 text-center py-8">Tidak ada masalah validasi. Data bersih!</p>
                        ) : (
                          result.issues.map((issue, idx) => (
                            <div key={idx} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                              <div className="flex items-start justify-between gap-3">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-1">
                                    <SeverityBadge severity={issue.severity} />
                                    <span className="text-xs text-gray-500">Baris {issue.source_row || issue.row_id || '?'}</span>
                                    <span className="text-xs text-gray-400">• {issue.field}</span>
                                  </div>
                                  <p className="text-sm font-medium text-gray-800">{issue.issue}</p>
                                  <p className="text-sm text-gray-600 mt-1">{issue.detail}</p>
                                  {issue.suggested_action && (
                                    <p className="text-xs text-gray-500 mt-2">💡 {issue.suggested_action}</p>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))
                        )}
                      </div>
                    )}

                    {activeTab === 'clarifications' && (
                      <div className="space-y-3">
                        {result.clarifications?.length === 0 ? (
                          <p className="text-sm text-gray-500 text-center py-8">Tidak ada klarifikasi yang diperlukan.</p>
                        ) : (
                          result.clarifications.map((q, idx) => (
                            <div key={idx} className="border border-gray-200 rounded-lg p-4">
                              <div className="flex items-center gap-2 mb-2">
                                <PriorityBadge priority={q.severity} />
                              </div>
                              <p className="text-sm font-medium text-gray-800">{q.question}</p>
                              <p className="text-sm text-gray-600 mt-1">{q.context}</p>
                              {q.suggested_resolution && (
                                <p className="text-xs text-gray-500 mt-2">💡 {q.suggested_resolution}</p>
                              )}
                            </div>
                          ))
                        )}
                      </div>
                    )}

                    {activeTab === 'actions' && (
                      <div className="space-y-3">
                        {result.actions?.length === 0 ? (
                          <p className="text-sm text-gray-500 text-center py-8">Tidak ada tindakan yang dihasilkan.</p>
                        ) : (
                          result.actions.map((action, idx) => {
                            const status = actionStatuses[idx]
                            const isApproved = status === 'approved'
                            const isIgnored = status === 'ignored'
                            return (
                              <div
                                key={idx}
                                className={`border rounded-lg p-4 transition-all ${
                                  isApproved
                                    ? 'border-green-300 bg-green-50'
                                    : isIgnored
                                    ? 'border-gray-200 bg-gray-50 opacity-60'
                                    : 'border-gray-200 hover:bg-gray-50'
                                }`}
                              >
                                <div className="flex items-start justify-between gap-3">
                                  <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                      <PriorityBadge priority={action.priority} />
                                      <span className="text-xs text-gray-400">{action.category}</span>
                                      {isApproved && (
                                        <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-green-100 text-green-700">
                                          ✅ Disetujui
                                        </span>
                                      )}
                                      {isIgnored && (
                                        <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-gray-200 text-gray-600">
                                          ❌ Diabaikan
                                        </span>
                                      )}
                                    </div>
                                    <p className={`text-sm font-semibold ${isIgnored ? 'text-gray-500 line-through' : 'text-gray-800'}`}>
                                      {action.title}
                                    </p>
                                    <p className={`text-sm mt-1 ${isIgnored ? 'text-gray-400 line-through' : 'text-gray-600'}`}>
                                      {action.description}
                                    </p>
                                    {action.draft_message && !isIgnored && (
                                      <div className={`mt-3 border rounded p-3 text-sm font-mono whitespace-pre-wrap ${
                                        isApproved ? 'bg-green-100 border-green-200 text-green-800' : 'bg-white border-gray-200 text-gray-700'
                                      }`}>
                                        {action.draft_message}
                                      </div>
                                    )}
                                  </div>
                                </div>
                                {!isApproved && !isIgnored && (
                                  <div className="mt-3 flex items-center gap-2">
                                    <button
                                      onClick={() => handleApprove(idx)}
                                      className="text-xs px-3 py-1.5 rounded-md bg-opsflow-600 text-white hover:bg-opsflow-700 transition-colors"
                                    >
                                      Setujui
                                    </button>
                                    <button
                                      onClick={() => handleIgnore(idx)}
                                      className="text-xs px-3 py-1.5 rounded-md border border-gray-300 text-gray-600 hover:bg-gray-50 transition-colors"
                                    >
                                      Abaikan
                                    </button>
                                  </div>
                                )}
                              </div>
                            )
                          })
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {!file && !result && !error && (
                <div className="text-center py-12">
                  <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
                    <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900">Siap Memproses</h3>
                  <p className="text-sm text-gray-500 mt-2 max-w-md mx-auto">
                    Upload file CSV atau Excel berisi data transaksi harian UMKM Anda. Sistem akan otomatis memvalidasi, menghitung metrik, dan menghasilkan laporan beserta tindak lanjut.
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Right Log Panel */}
          {showLogPanel && (
            <div className="w-80 bg-white border-l border-gray-200 overflow-y-auto scrollbar-thin flex flex-col">
              <div className="p-4 border-b border-gray-200 flex items-center justify-between">
                <h3 className="font-semibold text-gray-900 text-sm">📋 Log Tindakan</h3>
                <button onClick={() => setShowLogPanel(false)} className="text-gray-400 hover:text-gray-600">×</button>
              </div>
              <div className="flex-1 p-4 space-y-3">
                {actionLog.length === 0 ? (
                  <p className="text-sm text-gray-400 text-center py-8">Belum ada tindakan yang diproses.</p>
                ) : (
                  actionLog.map((log, idx) => (
                    <div key={idx} className={`border rounded-lg p-3 text-sm ${
                      log.decision === 'approved' ? 'border-green-200 bg-green-50' : 'border-gray-200 bg-gray-50'
                    }`}>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-bold">
                          {log.decision === 'approved' ? '✅' : '❌'}
                        </span>
                        <span className="text-xs text-gray-400">{log.time}</span>
                      </div>
                      <p className="font-medium text-gray-800">{log.title}</p>
                      <p className="text-xs text-gray-500 mt-0.5">{log.category} • {log.priority}</p>
                      {log.decision === 'approved' && log.draft_message && (
                        <div className="mt-2 p-2 bg-white border border-green-200 rounded text-xs font-mono text-gray-700 whitespace-pre-wrap">
                          {log.draft_message}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
              {actionLog.length > 0 && (
                <div className="p-4 border-t border-gray-200">
                  <button
                    onClick={() => {
                      const approved = actionLog.filter(a => a.decision === 'approved')
                      if (approved.length === 0) {
                        showToast('Belum ada tindakan yang disetujui', 'error')
                        return
                      }
                      let summary = `=== LAPORAN TINDAKAN UMKM OPSFLOW ===\n\n`
                      summary += `Disetujui: ${approved.length}\nDiabaikan: ${actionLog.filter(a => a.decision === 'ignored').length}\n\n`
                      approved.forEach((a, i) => {
                        summary += `[${i + 1}] ${a.title}\n${a.draft_message || '-'}\n\n`
                      })
                      navigator.clipboard?.writeText(summary).then(() => {
                        showToast('Ringkasan tindakan disalin ke clipboard!', 'success')
                      }).catch(() => showToast('Gagal menyalin', 'error'))
                    }}
                    className="w-full py-2 bg-opsflow-600 text-white rounded-lg text-sm font-medium hover:bg-opsflow-700"
                  >
                    📋 Salin Ringkasan
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      {/* Toast */}
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

      {/* Guide Modal */}
      {showGuide && <GuideModal onClose={() => setShowGuide(false)} />}
    </div>
  )
}
