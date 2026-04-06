import React from 'react'

export default function ExtractionDisplay({ data }) {
  if (!data) return null
  const type = data.document_type || 'unknown'
  const skip = ['document_type', 'calculations', 'discrepancies', 'total_pages']

  return (
    <div className="mt-6 bg-slate-900 border border-slate-700 rounded-xl p-6">

      {/* Header */}
      <div className="flex items-center gap-3 mb-6 flex-wrap">
        <span className="text-xs font-mono bg-cyan-400/10 text-cyan-400
          border border-cyan-400/20 px-3 py-1 rounded">
          {type.toUpperCase().replace(/_/g, ' ')}
        </span>
        {data.calculations?.balance_verified === true && (
          <span className="text-xs text-green-400 border
            border-green-400/30 px-3 py-1 rounded">
            ✅ Balance Verified
          </span>
        )}
        {data.discrepancies?.length > 0 && (
          <span className="text-xs text-red-400 border
            border-red-400/30 px-3 py-1 rounded">
            ⚠️ Discrepancy Found
          </span>
        )}
      </div>

      {/* Data sections */}
      <div className="space-y-6">
        {Object.entries(data)
          .filter(([k]) => !skip.includes(k))
          .map(([key, value]) => (
            <Section key={key} label={key} value={value} />
          ))}
      </div>

      {/* Calculations */}
      {data.calculations && (
        <div className="mt-6">
          <h3 className="text-xs font-mono text-slate-500 uppercase
            tracking-widest mb-3">Calculations</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {Object.entries(data.calculations).map(([k, v]) => (
              <div key={k} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-500 text-xs mb-1">
                  {k.replace(/_/g, ' ')}
                </div>
                <div className={`font-mono text-sm ${
                  v === true  ? 'text-green-400' :
                  v === false ? 'text-red-400'   : 'text-white'
                }`}>
                  {String(v)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Discrepancies */}
      {data.discrepancies?.length > 0 && (
        <div className="mt-4 p-3 bg-red-900/20 border
          border-red-500/30 rounded-lg">
          {data.discrepancies.map((d, i) => (
            <p key={i} className="text-red-400 text-sm">⚠️ {d}</p>
          ))}
        </div>
      )}
    </div>
  )
}

function Section({ label, value }) {
  const title = label.replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())

  // Array of objects → table
  if (Array.isArray(value) && value.length > 0
      && typeof value[0] === 'object') {
    return (
      <div>
        <h3 className="text-xs font-mono text-slate-500 uppercase
          tracking-widest mb-2">{title}</h3>
        <SmartTable rows={value} />
      </div>
    )
  }

  // Nested object → grid
  if (typeof value === 'object' && value !== null
      && !Array.isArray(value)) {
    return (
      <div>
        <h3 className="text-xs font-mono text-slate-500 uppercase
          tracking-widest mb-2">{title}</h3>
        <div className="grid grid-cols-2 gap-2">
          {Object.entries(value).map(([k, v]) => (
            <div key={k} className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-500 text-xs mb-1">
                {k.replace(/_/g, ' ')}
              </div>
              <div className="text-white text-sm font-mono">
                {String(v || '—')}
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  // Empty → skip
  if (value === null || value === '' ||
      (Array.isArray(value) && value.length === 0)) return null

  // Simple value → inline
  return (
    <div className="flex gap-3 items-start border-b
      border-slate-800 pb-2">
      <span className="text-slate-500 text-sm min-w-40">{title}</span>
      <span className="text-white text-sm font-mono">{String(value)}</span>
    </div>
  )
}

function SmartTable({ rows }) {
  const cols = [...new Set(rows.flatMap(r => Object.keys(r)))]

  const colColor = (col) => {
    const c = col.toLowerCase()
    if (['debit','withdrawal','dr'].some(k => c.includes(k)))
      return 'text-red-400'
    if (['credit','deposit','cr'].some(k => c.includes(k)))
      return 'text-green-400'
    if (['total','balance','amount','grand'].some(k => c.includes(k)))
      return 'text-cyan-400 font-bold'
    return 'text-white'
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead>
          <tr className="border-b border-slate-700">
            {cols.map(col => (
              <th key={col} className="text-left text-slate-400 pb-2
                pr-4 font-mono uppercase tracking-wider">
                {col.replace(/_/g, ' ')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className="border-b border-slate-800
              hover:bg-slate-800/50">
              {cols.map(col => (
                <td key={col} className={`py-2 pr-4 font-mono
                  ${colColor(col)}`}>
                  {row[col] || '—'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}