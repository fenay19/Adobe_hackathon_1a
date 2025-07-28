# 🧠 Adobe India Hackathon - Round 1A  
## 📄 PDF Outline Extractor

### 🚀 Objective
Extract a hierarchical table of contents (headings/subheadings) from well-structured PDF files and return them as a structured JSON format.

---

## 🧩 Our Approach

We solved this by analyzing the **font sizes** and **layout positions** of text blocks in each page of the PDF. Key assumptions:
- Headings use **larger fonts**
- Subheadings use slightly smaller fonts
- Body text has the smallest and most frequent font size

Steps we followed:
1. Used **PyMuPDF (fitz)** to extract text blocks with their coordinates and font sizes.
2. Grouped unique font sizes and sorted them in descending order.
3. Mapped larger fonts to `level 1`, smaller to `level 2`, and so on.
4. Built a tree-like outline based on font level + page number.

This method works well for structured PDFs like research papers, reports, and theses.

---

## 🧠 Libraries & Tools Used

| Tool | Purpose |
|------|---------|
| `Python 3.10` | Programming language |
| `PyMuPDF` (`fitz`) | Text and layout extraction from PDFs |
| `Docker` | To containerize the solution for consistent execution |

---

## 📁 Folder Structure

pdf-outline-extractor/
├── app/
│ └── main.py # Main outline extraction logic
├── input/ # Input PDFs go here
├── output/ # JSON output will be saved here
├── requirements.txt # Dependencies
├── Dockerfile # Docker image builder
└── README.md # You're reading this!



## 🐳 Docker Setup

### 🔨 1. Build Docker Image
```bash
docker build -t pdf-outline-extractor .
docker run --rm -v "${PWD}\input:/app/input" -v "${PWD}\output:/app/output" pdf-outline-extractor
✅ After running, check output/output.json.
