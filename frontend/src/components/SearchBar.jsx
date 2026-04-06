import React, { useState } from 'react'

export default function SearchBar() {
  const [query,   setQuery]   = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  async function handleSearch(e) {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    try {
      const res  = await fetch(
        `http://localhost:8000/api/search?q=${encodeURIComponent(query)}`
      )
      const data = await res.json()
      setResults(data.results || [])
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div className="mb-6">
      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSearch(e)}
          placeholder='Search: "my SBI October statement"'
          className="flex-1 bg-slate-800 border border-slate-600
            rounded-lg px-4 py-2.5 text-sm text-white
            placeholder-slate-500 focus:outline-none
            focus:border-cyan-400"
        />
        <button
          onClick={handleSearch}
          className="bg-cyan-500 hover:bg-cyan-400 text-black
            font-bold px-5 py-2.5 rounded-lg text-sm
            transition-colors"
        >
          {loading ? '...' : 'Search'}
        </button>
      </div>
      {results.length > 0 && (
        <div className="mt-3 bg-slate-800 border border-slate-700
          rounded-lg p-3">
          {results.map((r, i) => (
            <div key={i} className="py-2 border-b border-slate-700
              last:border-0">
              <span className="text-cyan-400 text-xs font-mono mr-2">
                {r.doc_type}
              </span>
              <span className="text-slate-300 text-sm">
                {r.storage_path}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}