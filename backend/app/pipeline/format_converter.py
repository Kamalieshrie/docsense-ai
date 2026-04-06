# ============================================================
# format_converter.py
# Converts PDF, DOCX, JPG, PNG → list of PIL Images
# ============================================================
import fitz
from PIL import Image
from pathlib import Path
from typing import List
import io


def convert_to_images(file_path: str) -> List[Image.Image]:
    ext = Path(file_path).suffix.lower()

    # ── Direct image files ──────────────────────────────────
    if ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"]:
        img = Image.open(file_path).convert("RGB")
        return [img]

    # ── PDF → render each page at 3x zoom ──────────────────
    if ext == ".pdf":
        pages = []
        pdf = fitz.open(file_path)
        matrix = fitz.Matrix(3.0, 3.0)
        for page in pdf:
            pix = page.get_pixmap(matrix=matrix)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            pages.append(img)
        pdf.close()
        return pages

    # ── DOCX → extract embedded images ─────────────────────
    if ext == ".docx":
        from docx import Document as DocxDoc
        doc = DocxDoc(file_path)
        images = []
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                img_data = rel.target_part.blob
                img = Image.open(io.BytesIO(img_data)).convert("RGB")
                images.append(img)
        return images if images else []

    raise ValueError(f"Unsupported format: {ext}")