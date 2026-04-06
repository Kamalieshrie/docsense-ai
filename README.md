# DocSense AI — Smart Document Analyzer

100% Free · No paid APIs · Fully local

## What It Does
- Accepts ANY document — PDF, PNG, JPG, DOCX, WEBP
- Fixes blurry, tilted, stained, torn documents automatically
- Classifies document type automatically
- Extracts ALL data with exact column mapping
- Runs calculations and verifies totals
- Stores documents in auto-organized folders
- Semantic search — find docs by meaning not filename

## Supported Document Types
- Bank Statements
- Invoices & Bills
- Receipts & Shopping bills
- Medical Bills
- Certificates & Mark Sheets
- ID Proofs (Aadhaar, PAN, Passport)
- Bank Cheques
- Resumes / CVs
- Property Documents
- Contracts

## Tech Stack
| Layer | Technology | Cost |
|-------|-----------|------|
| Backend | FastAPI | Free |
| OCR | PaddleOCR PP-OCRv5 | Free |
| AI | Gemini 2.5 Flash | Free (1500/day) |
| Image Repair | OpenCV | Free |
| Vector Search | ChromaDB | Free |
| Database | SQLite | Free |
| Frontend | React + Vite + Tailwind | Free |

## Project Structure
```
docsense-ai/
├── backend/
│   ├── app/
│   │   ├── pipeline/   → 6 files (image repair, OCR, column mapping)
│   │   ├── llm/        → 4 files (Gemini AI, prompts, schemas)
│   │   ├── agents/     → 5 files (bank, invoice, cheque, certificate)
│   │   ├── storage/    → 4 files (ChromaDB, SQLite, file manager)
│   │   └── routes/     → 3 files (upload, search, documents)
│   └── main.py
└── frontend/
    └── src/
        ├── App.jsx
        └── components/ → 5 files
```

## Total Cost
₹0 / $0 forever