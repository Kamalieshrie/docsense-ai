import React, { useCallback, useState } from 'react'

export default function UploadZone({ onUpload }) {
  const [dragging, setDragging] = useState(false)

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) onUpload(file)
  }, [onUpload])

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => document.getElementById('file-input').click()}
      className={`border-2 border-dashed rounded-xl p-12 text-center
        cursor-pointer transition-all mb-6
        ${dragging
          ? 'border-cyan-400 bg-cyan-400/5'
          : 'border-slate-700 hover:border-slate-500'}`}
    >
      <div className="text-4xl mb-3">📄</div>
      <p className="text-slate-300 font-medium mb-1">
        Drop any document here
      </p>
      <p className="text-slate-500 text-sm">
        PDF · PNG · JPG · DOCX · WEBP — any size, any quality
      </p>
      <input
        id="file-input"
        type="file"
        accept=".pdf,.png,.jpg,.jpeg,.docx,.webp"
        onChange={(e) => e.target.files[0] && onUpload(e.target.files[0])}
        className="hidden"
      />
    </div>
  )
}