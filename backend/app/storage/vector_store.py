# ============================================================
# vector_store.py
# ChromaDB — semantic search by document meaning
# Find: "my SBI October statement" even if saved as scan_003.pdf
# ============================================================
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from pathlib import Path

_client    = None
_model     = None
_COLL_NAME = "docsense_documents"


def _get_client():
    global _client
    if _client is None:
        Path("./storage/chromadb").mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(path="./storage/chromadb")
    return _client


def _get_model():
    global _model
    if _model is None:
        # 22MB free local model — downloads once automatically
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _get_collection():
    return _get_client().get_or_create_collection(_COLL_NAME)


def store_document(doc_id: str, text: str, metadata: Dict[str, Any]):
    """Store document embedding in ChromaDB."""
    try:
        embedding  = _get_model().encode(text).tolist()
        collection = _get_collection()
        collection.upsert(
            ids        = [doc_id],
            embeddings = [embedding],
            documents  = [text[:2000]],
            metadatas  = [{k: str(v) for k, v in metadata.items()}],
        )
    except Exception as e:
        print(f"[VectorStore] Error storing: {e}")


def semantic_search(query: str, n_results: int = 10) -> List[Dict]:
    """Find documents by meaning — not filename."""
    try:
        embedding  = _get_model().encode(query).tolist()
        collection = _get_collection()
        results    = collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results.get("metadatas", [[]])[0]
    except Exception as e:
        print(f"[VectorStore] Search error: {e}")
        return []