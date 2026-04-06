import React, { useEffect, useState } from 'react'
import ExtractionDisplay from './ExtractionDisplay'

export default function Library({ refresh }) {
  const [docs,     setDocs]     = useState([])
  const [loading,  setLoading]  = useState(false)
  const [selected, setSelected] = useState(null)
  const [filter,   setFilter]   = useState('all')

  const fetchDocs = () => {
    setLoading(true)
    fetch('http://localhost:8000/api/documents')
      .then(r => r.json())
      .then(d => { setDocs(d.documents || []); setLoading(false) })
      .catch(() => setLoading(false))
  }

  useEffect(() => { fetchDocs() }, [refresh])

  const handleDelete = async (docId, e) => {
    e.stopPropagation()
    if (!confirm('Delete this document permanently?')) return
    await fetch(`http://localhost:8000/api/documents/${docId}`,
      { method: 'DELETE' })
    if (selected?.id === docId) setSelected(null)
    fetchDocs()
  }

  const typeIcon = (t) => ({
    bank_statement: '🏦', invoice: '🧾', receipt: '🛒',
    medical_bill: '🏥', certificate: '🎓', id_proof: '🪪',
    cheque: '💳', resume: '📋', unknown: '📄'
  }[t] || '📄')

  const types = ['all', ...new Set(docs.map(d => d.doc_type))]
  const filtered = filter === 'all'
    ? docs
    : docs.filter(d => d.doc_type === filter)

  if (selected) {
    return (
      <div>
        {/* Back button */}
        <button
          onClick={() => setSelected(null)}
          className="mb-4 flex items-center gap-2 text-slate-400
            hover:text-cyan-400 transition-colors text-sm">
          ← Back to Library
        </button>

        {/* Document header */}
        <div className="bg-slate-800 border border-slate-700
          rounded-xl p-4 mb-4">
          <div className="flex items-center justify-between flex-wrap gap-3">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-2xl">{typeIcon(selected.doc_type)}</span>
                <h2 className="text-white font-semibold text-lg">
                  {selected.storage_path?.split(/[/\\]/).pop() || 'Document'}
                </h2>
              </div>
              <div className="flex gap-4 text-slate-500 text-xs flex-wrap">
                <span className="text-cyan-400 font-mono uppercase">
                  {selected.doc_type?.replace(/_/g,' ')}
                </span>
                {selected.owner_name && <span>👤 {selected.owner_name}</span>}
                {selected.institution && <span>🏛 {selected.institution}</span>}
                {selected.date && <span>📅 {selected.date}</span>}
                <span>🕐 {new Date(selected.created_at).toLocaleDateString()}</span>
              </div>
            </div>
            <button
              onClick={(e) => { handleDelete(selected.id, e); setSelected(null) }}
              className="bg-red-500/10 text-red-400 border border-red-400/20
                px-4 py-2 rounded-lg text-sm hover:bg-red-500/20
                transition-colors">
              🗑 Delete
            </button>
          </div>
        </div>

        {/* Full extracted data */}
        {selected.extracted && Object.keys(selected.extracted).length > 0
          ? <ExtractionDisplay data={selected.extracted} />
          : (
            <div className="text-center text-slate-500 py-12">
              No extracted data available
            </div>
          )
        }
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
        <h2 className="text-white font-semibold">
          Document Library
          <span className="text-slate-500 text-sm font-normal ml-2">
            ({filtered.length} documents)
          </span>
        </h2>
        <button onClick={fetchDocs}
          className="text-xs text-slate-500 hover:text-cyan-400
            transition-colors border border-slate-700 px-3 py-1.5
            rounded-lg">
          ↻ Refresh
        </button>
      </div>

      {/* Type filter */}
      <div className="flex gap-2 flex-wrap mb-5">
        {types.map(t => (
          <button key={t}
            onClick={() => setFilter(t)}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono
              transition-colors ${filter === t
                ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-400/30'
                : 'bg-slate-800 text-slate-500 border border-slate-700 hover:text-white'}`}>
            {t === 'all' ? '📂 All' : `${typeIcon(t)} ${t.replace(/_/g,' ')}`}
          </button>
        ))}
      </div>

      {loading && (
        <div className="text-center text-slate-500 py-12">Loading...</div>
      )}

      {!loading && filtered.length === 0 && (
        <div className="text-center py-16 text-slate-600">
          <div className="text-5xl mb-4">📂</div>
          <div className="text-lg mb-2">No documents yet</div>
          <div className="text-sm">Upload documents from the Upload tab</div>
        </div>
      )}

      {/* Document grid */}
      <div className="grid grid-cols-1 gap-3">
        {filtered.map(doc => (
          <div key={doc.id}
            onClick={() => setSelected(doc)}
            className="bg-slate-800 border border-slate-700 rounded-xl
              p-4 cursor-pointer hover:border-cyan-400/40
              hover:bg-slate-750 transition-all group">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-3 min-w-0">
                <span className="text-2xl shrink-0">
                  {typeIcon(doc.doc_type)}
                </span>
                <div className="min-w-0">
                  {/* Clickable file name */}
                  <div className="text-white font-medium text-sm
                    group-hover:text-cyan-400 transition-colors truncate">
                    {doc.storage_path?.split(/[/\\]/).pop() || doc.id}
                  </div>
                  <div className="flex gap-3 mt-1 flex-wrap">
                    <span className="text-xs font-mono bg-cyan-400/10
                      text-cyan-400 border border-cyan-400/20
                      px-2 py-0.5 rounded">
                      {doc.doc_type?.replace(/_/g,' ').toUpperCase()}
                    </span>
                    {doc.owner_name && (
                      <span className="text-slate-500 text-xs">
                        👤 {doc.owner_name}
                      </span>
                    )}
                    {doc.institution && (
                      <span className="text-slate-500 text-xs">
                        🏛 {doc.institution}
                      </span>
                    )}
                    {doc.date && (
                      <span className="text-slate-500 text-xs">
                        📅 {doc.date}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <span className="text-slate-600 text-xs hidden md:block">
                  {doc.created_at
                    ? new Date(doc.created_at).toLocaleDateString()
                    : ''}
                </span>
                <button
                  onClick={(e) => handleDelete(doc.id, e)}
                  className="opacity-0 group-hover:opacity-100
                    bg-red-500/10 text-red-400 border border-red-400/20
                    px-2 py-1 rounded text-xs hover:bg-red-500/20
                    transition-all">
                  🗑
                </button>
                <span className="text-slate-600 text-sm
                  group-hover:text-cyan-400 transition-colors">
                  →
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}