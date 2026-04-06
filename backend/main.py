# ============================================================
# main.py — DocSense AI FastAPI Entry Point
# ============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, search, documents

app = FastAPI(
    title="DocSense AI",
    description="Smart Document Analyzer — 100% Free",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router,    prefix="/api")
app.include_router(search.router,    prefix="/api")
app.include_router(documents.router, prefix="/api")

@app.get("/api/health")
async def health():
    return {"status": "healthy", "app": "DocSense AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)