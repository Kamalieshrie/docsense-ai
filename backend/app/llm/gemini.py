# ============================================================
# gemini.py — Stable SDK for cloud deployment
# ============================================================
import json
import io
from typing import Dict, Any, List
from PIL import Image
import google.generativeai as genai

from app.config      import GEMINI_API_KEY, DEFAULT_MODEL
from app.llm.prompts import PROMPTS, CLASSIFY_PROMPT

genai.configure(api_key=GEMINI_API_KEY)
_model = genai.GenerativeModel(DEFAULT_MODEL)


def _image_to_part(pil_image: Image.Image):
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    buf.seek(0)
    return {"mime_type": "image/png", "data": buf.read()}


def classify_document(pil_image: Image.Image) -> str:
    """Step 1 — What type of document is this?"""
    try:
        img_part = _image_to_part(pil_image)
        response = _model.generate_content([img_part, CLASSIFY_PROMPT])
        doc_type = response.text.strip().lower().replace(" ", "_")
        return doc_type if doc_type in PROMPTS else "unknown"
    except Exception as e:
        print(f"[Gemini classify error] {e}")
        return "unknown"


def classify_and_extract(
    image:      Image.Image,
    ocr_text:   str,
    table_rows: List[Dict],
    page_num:   int = 1,
) -> Dict[str, Any]:
    """Step 2 — Classify then extract with type-specific prompt."""

    # Classify
    doc_type = classify_document(image)
    print(f"  [Gemini] Page {page_num} → {doc_type}")

    # Build prompt
    prompt_template = PROMPTS.get(doc_type, PROMPTS["unknown"])
    prompt = prompt_template.format(
        ocr_text=ocr_text[:6000]
    )

    # Extract with 3 retries
    for attempt in range(3):
        try:
            img_part = _image_to_part(image)
            response = _model.generate_content([img_part, prompt])
            text = response.text.strip()

            # Strip markdown fences if present
            if text.startswith("```"):
                lines = text.split("\n")
                text  = "\n".join(lines[1:-1])

            data = json.loads(text)
            data["document_type"] = doc_type
            return data

        except json.JSONDecodeError:
            print(f"  [Gemini] Attempt {attempt+1}: JSON parse failed, retrying...")
        except Exception as e:
            print(f"  [Gemini] Attempt {attempt+1}: {e}")

    return {
        "document_type": doc_type,
        "error": "Extraction failed after 3 attempts"
    }