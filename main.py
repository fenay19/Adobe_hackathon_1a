import fitz  # PyMuPDF
import os
import json
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime

def extract_outline(pdf_path):
    """Extracts title and outline from a PDF file."""
    doc = fitz.open(pdf_path)
    text_blocks = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:  # ✅ FIX: Skip blocks without lines (images, empty spaces)
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        text_blocks.append({
                            "text": text,
                            "size": span["size"],
                            "bold": (span["flags"] & 2) != 0,
                            "page": page_num
                        })

    if not text_blocks:
        return {"title": "", "outline": []}

    # Cluster font sizes to identify heading levels
    sizes = np.array([b["size"] for b in text_blocks]).reshape(-1, 1)
    unique_sizes = sorted(list(set(sizes.flatten())), reverse=True)
    n_clusters = min(3, len(unique_sizes))

    if n_clusters > 1:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(sizes)
    else:
        kmeans = None

    # Map font sizes to heading levels (H1, H2, H3)
    size_to_level = {}
    if len(unique_sizes) > 0:
        size_to_level[unique_sizes[0]] = "H1"
    if len(unique_sizes) > 1:
        size_to_level[unique_sizes[1]] = "H2"
    if len(unique_sizes) > 2:
        size_to_level[unique_sizes[2]] = "H3"

    # Extract Title (largest font)
    title = next((b["text"] for b in text_blocks if b["size"] == unique_sizes[0]), "")

    # Build Outline
    outline = []
    seen = set()
    for b in text_blocks:
        level = size_to_level.get(b["size"])
        if level and len(b["text"].split()) <= 15:  # Limit heading length
            key = (b["text"], b["page"])
            if key not in seen:
                outline.append({"level": level, "text": b["text"], "page": b["page"]})
                seen.add(key)

    return {"title": title, "outline": outline}

def process_directory(input_dir, output_dir):
    """Processes all PDFs in the input directory."""
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            print(f"[{datetime.now()}] Processing {file}...")
            result = extract_outline(pdf_path)
            output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"[{datetime.now()}] Saved -> {output_path}")

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    process_directory(input_dir, output_dir)
