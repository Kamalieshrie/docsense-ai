# ============================================================
# ocr_engine.py — EasyOCR (Windows + Python 3.13 compatible)
# ============================================================
from PIL import Image
import numpy as np
from typing import List, Dict, Any
import easyocr

_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    return _reader


def extract_words_with_positions(pil_image: Image.Image) -> List[Dict[str, Any]]:
    img_array = np.array(pil_image)
    reader    = _get_reader()
    result    = reader.readtext(img_array)

    words = []
    for (box, text, conf) in result:
        if conf > 0.3:
            xs = [p[0] for p in box]
            ys = [p[1] for p in box]
            words.append({
                "text":       text,
                "x":          int(min(xs)),
                "y":          int(min(ys)),
                "w":          int(max(xs) - min(xs)),
                "h":          int(max(ys) - min(ys)),
                "confidence": float(conf),
            })
    return words


def get_full_text(pil_image: Image.Image) -> str:
    words = extract_words_with_positions(pil_image)
    words.sort(key=lambda w: (w["y"] // 20, w["x"]))
    return " ".join(w["text"] for w in words)