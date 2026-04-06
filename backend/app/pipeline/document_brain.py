# ============================================================
# document_brain.py
# Master orchestrator — runs all 6 layers in sequence
# ============================================================
from PIL import Image
from typing import Dict, Any, List

from app.pipeline.image_repairer   import repair
from app.pipeline.ocr_engine       import extract_words_with_positions, get_full_text
from app.pipeline.column_mapper    import map_to_table
from app.pipeline.section_detector import detect_sections
from app.llm.gemini                import classify_and_extract
from app.llm.post_processor        import clean_result


def process_page(pil_image: Image.Image, page_num: int = 1) -> Dict[str, Any]:
    # Layer 1 — Repair image
    repaired = repair(pil_image)

    # Layer 2 — OCR
    words    = extract_words_with_positions(repaired)
    raw_text = get_full_text(repaired)

    # Layer 3 — Column + Section mapping
    detect_sections(words)
    table_rows = map_to_table(words)

    # Layer 4 — AI extraction
    raw_result = classify_and_extract(
        image=repaired,
        ocr_text=raw_text,
        table_rows=table_rows,
        page_num=page_num,
    )

    # Layer 5 — Post process
    return clean_result(raw_result)


def process_document(pages: List[Image.Image]) -> Dict[str, Any]:
    if not pages:
        return {"error": "No pages found"}

    all_pages = [process_page(p, i + 1) for i, p in enumerate(pages)]

    if len(all_pages) == 1:
        return all_pages[0]

    # Merge multi-page results
    merged = all_pages[0].copy()
    for page_data in all_pages[1:]:
        for key, val in page_data.items():
            if isinstance(val, list) and key in merged and isinstance(merged[key], list):
                merged[key].extend(val)
            elif key not in merged:
                merged[key] = val
    merged["total_pages"] = len(all_pages)
    return merged