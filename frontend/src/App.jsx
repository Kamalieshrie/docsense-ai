import React, { useState } from 'react'
import UploadZone        from './components/UploadZone'
import ExtractionDisplay from './components/ExtractionDisplay'
import SearchBar         from './components/SearchBar'
import Library           from './components/FolderTree'

export default function App() {
  const [result,  setResult]  = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)
  const [tab,     setTab]     = useState('upload')
  const [refresh, setRefresh] = useState(0)
  const [dupMsg,  setDupMsg]  = useState(null)

  async function handleUpload(file) {
    setLoading(true)
    setError(null)
    setResult(null)
    setDupMsg(null)
    const form = new FormData()
    form.append('file', file)
    try {
      const res  = await fetch('https://docsense-ai-drr7.onrender.com/api/upload', {
        method: 'POST', body: form
      })
      const data = await res.json()

      if (data.status === 'success') {
        setResult(data.result)
        setRefresh(r => r + 1)
      } else if (data.status === 'duplicate') {
        setDupMsg(data.message)
        if (data.result) setResult(data.result)
        setRefresh(r => r + 1)
      } else {
        setError(data.detail || 'Extraction failed')
      }
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen p-6 max-w-5xl mx-auto">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-cyan-400 mb-1">
          DocSense AI
        </h1>
        <p className="text-slate-400 text-sm">
          Smart Document Analyzer — 100% Free
        </p>
      </header>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-slate-800 pb-4">
        <button onClick={() => setTab('upload')}
          className={`px-6 py-2.5 rounded-lg text-sm font-medium
            transition-all ${tab === 'upload'
              ? 'bg-cyan-500 text-black shadow-lg shadow-cyan-500/20'
              : 'bg-slate-800 text-slate-400 hover:text-white'}`}>
          📤 Upload
        </button>
        <button onClick={() => { setTab('library'); setRefresh(r => r+1) }}
          className={`px-6 py-2.5 rounded-lg text-sm font-medium
            transition-all ${tab === 'library'
              ? 'bg-cyan-500 text-black shadow-lg shadow-cyan-500/20'
              : 'bg-slate-800 text-slate-400 hover:text-white'}`}>
          📚 Library
        </button>
      </div>

      {tab === 'upload' && (
        <>
          <SearchBar />
          <UploadZone onUpload={handleUpload} />

          {loading && (
            <div className="mt-6 text-center text-cyan-400 animate-pulse text-sm">
              🔍 Analyzing document — all 6 layers running...
            </div>
          )}

          {dupMsg && (
            <div className="mt-4 p-3 bg-yellow-900/20 border
              border-yellow-500/30 rounded-lg text-yellow-400 text-sm">
              ⚡ {dupMsg} — showing previously extracted result below
            </div>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-900/30 border
              border-red-500/40 rounded-lg text-red-400 text-sm">
              ⚠️ {error}
            </div>
          )}

          {result && <ExtractionDisplay data={result} />}
        </>
      )}

      {tab === 'library' && <Library refresh={refresh} />}
    </div>
  )
}
