import React from 'react'

export default function DocumentViewer({ fileUrl, extractedData }) {
  return (
    <div className="grid grid-cols-2 gap-4 mt-6">
      <div className="bg-slate-800 rounded-xl p-4">
        <h3 className="text-xs font-mono text-slate-500 uppercase
          tracking-widest mb-3">Original Document</h3>
        {fileUrl ? (
          <iframe src={fileUrl} className="w-full h-96 rounded"
            title="Document Preview" />
        ) : (
          <div className="h-96 flex items-center justify-center
            text-slate-600">No preview available</div>
        )}
      </div>
      <div className="bg-slate-800 rounded-xl p-4">
        <h3 className="text-xs font-mono text-slate-500 uppercase
          tracking-widest mb-3">Extracted Data</h3>
        <pre className="text-xs text-slate-300 overflow-auto h-96
          whitespace-pre-wrap">
          {JSON.stringify(extractedData, null, 2)}
        </pre>
      </div>
    </div>
  )
}