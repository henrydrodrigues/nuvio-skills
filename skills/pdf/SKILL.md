# Skill: PDF Document

Guidelines for producing, reading, and manipulating `.pdf` files. Primary approach
is **fpdf2** (pure Python, no native dependencies) for table/text PDFs and simple
reports. For reading/merging existing PDFs, use **pypdf**. For math-heavy academic
documents, use **pandoc + LaTeX**.

**Dependencies** (add to stage `dependencies` in `manifest.yaml`):

- Generation: `fpdf2`
- Reading/merging: `pypdf`
- For pandoc path: system `pandoc` + TeX distribution (`texlive-xetex`)

> **Why fpdf2 over WeasyPrint?** WeasyPrint requires native GTK/Pango/GLib libraries
> (`libgobject-2.0`, `libpango-1.0`) that cannot be installed via `pip`. This makes it
> fail on Windows, minimal containers, and serverless environments. fpdf2 is pure Python
> — `pip install fpdf2` is all that's needed.

---

## When to use

- Agent produces a PDF as output (reports, invoices, proposals, certificates, dashboards)
- Agent reads an uploaded `.pdf` file as input (text extraction, data parsing)
- Agent merges, splits, or manipulates existing PDF files
- Agent produces tabular PDFs (sentiment tables, financial reports, inventories)

---

## 1. Creating a PDF with fpdf2

### Simple table PDF

```python
from fpdf import FPDF

def write_table_pdf(path: str, headers: list[str], rows: list[list[str]]) -> None:
    """Write a styled table PDF using fpdf2."""
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(26, 58, 92)  # #1A3A5C
    pdf.cell(0, 12, "Report Title", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)

    # Column widths — distribute evenly or customize
    col_count = len(headers)
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_w = page_width / col_count
    row_h = 8

    # Header row
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(26, 58, 92)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        nx = "LMARGIN" if i == col_count - 1 else "RIGHT"
        ny = "NEXT" if i == col_count - 1 else "TOP"
        pdf.cell(col_w, row_h, h, border=1, fill=True, align="L", new_x=nx, new_y=ny)

    # Data rows
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 51, 51)
    for row_idx, row in enumerate(rows):
        if row_idx % 2 == 0:
            pdf.set_fill_color(248, 249, 250)
        else:
            pdf.set_fill_color(255, 255, 255)
        for i, cell in enumerate(row):
            nx = "LMARGIN" if i == col_count - 1 else "RIGHT"
            ny = "NEXT" if i == col_count - 1 else "TOP"
            pdf.cell(col_w, row_h, str(cell)[:80], border=1, fill=True, align="L", new_x=nx, new_y=ny)

    pdf.output(path)
```

### Text report with sections

```python
from fpdf import FPDF

def write_report_pdf(path: str, title: str, sections: list[dict]) -> None:
    """Write a multi-section text report.

    Each section: {"heading": str, "body": str}
    """
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(26, 58, 92)
    pdf.cell(0, 14, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(8)

    for section in sections:
        # Heading
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(26, 58, 92)
        pdf.cell(0, 10, section["heading"], new_x="LMARGIN", new_y="NEXT")

        # Body
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(51, 51, 51)
        pdf.multi_cell(0, 6, section["body"])
        pdf.ln(4)

    pdf.output(path)
```

---

## 2. Page layout and styling

### Page sizes

```python
from fpdf import FPDF

# A4 portrait (default)
pdf = FPDF(orientation="P", unit="mm", format="A4")

# A4 landscape
pdf = FPDF(orientation="L", unit="mm", format="A4")

# Letter
pdf = FPDF(orientation="P", unit="mm", format="Letter")

# Custom size (width x height in mm)
pdf = FPDF(orientation="P", unit="mm", format=(210, 297))
```

### Margins

```python
pdf = FPDF()
pdf.set_margins(left=20, top=25, right=20)
pdf.set_auto_page_break(auto=True, margin=25)  # bottom margin
```

### Headers and footers

```python
from fpdf import FPDF

class BrandedPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(136, 136, 136)
        self.cell(0, 10, "Company Name", align="L")
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(170, 170, 170)
        self.cell(0, 10, "Confidential", align="C")

pdf = BrandedPDF()
pdf.alias_nb_pages()
pdf.add_page()
```

---

## 3. Fonts

fpdf2 ships with Helvetica, Times, Courier, Symbol, ZapfDingbats. For custom fonts:

```python
pdf = FPDF()
pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)
pdf.set_font("DejaVu", "", 11)
```

### Unicode support

fpdf2 supports Unicode out of the box with TTF fonts:

```python
pdf.add_font("NotoSans", "", "fonts/NotoSans-Regular.ttf", uni=True)
pdf.set_font("NotoSans", "", 11)
pdf.cell(0, 10, "Português: ção, ã, é, ü")  # works with TTF
```

---

## 4. Images

```python
pdf.image("logo.png", x=10, y=10, w=30)          # from file
pdf.image("chart.png", x=10, w=180)                # full width
pdf.image("https://example.com/img.png", w=100)    # from URL
```

---

## 5. Multi-cell and wrapping

```python
# Auto-wrapping text
pdf.multi_cell(0, 6, long_text)

# Text in a box with border
pdf.multi_cell(90, 6, text, border=1)

# Justified text
pdf.multi_cell(0, 6, text, align="J")
```

---

## 6. Colors and drawing

```python
# Fill color (background)
pdf.set_fill_color(26, 58, 92)

# Text color
pdf.set_text_color(255, 255, 255)

# Draw color (borders, lines)
pdf.set_draw_color(200, 200, 200)

# Line
pdf.line(10, 50, 200, 50)

# Rectangle
pdf.rect(10, 60, 50, 30, style="DF")  # D=draw, F=fill, DF=both
```

---

## 7. Reading existing PDFs (pypdf)

### Extract text

```python
from pypdf import PdfReader

reader = PdfReader("input.pdf")

# Page count
print(f"Pages: {len(reader.pages)}")

# Extract text from all pages
for page in reader.pages:
    print(page.extract_text())
```

### Read metadata

```python
reader = PdfReader("input.pdf")
meta = reader.metadata

print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Pages: {len(reader.pages)}")
```

---

## 8. Merging and splitting PDFs (pypdf)

### Merge multiple PDFs

```python
from pypdf import PdfWriter

writer = PdfWriter()
writer.append("report-part1.pdf")
writer.append("report-part2.pdf")
writer.append("appendix.pdf", pages=(0, 5))  # first 5 pages only

writer.write("combined.pdf")
writer.close()
```

### Split a PDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("large.pdf")

# Extract pages 5-10
writer = PdfWriter()
for page in reader.pages[4:10]:
    writer.add_page(page)
writer.write("pages_5_to_10.pdf")
writer.close()
```

---

## 9. Helper patterns for agents

### Dict list to table PDF

```python
from fpdf import FPDF

def dicts_to_pdf(data: list[dict], output_path: str, title: str = "Report") -> None:
    """Convert a list of dicts to a styled table PDF."""
    if not data:
        return
    headers = list(data[0].keys())

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(26, 58, 92)
    pdf.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    # Auto-calculate column widths
    page_w = pdf.w - pdf.l_margin - pdf.r_margin
    col_w = page_w / len(headers)
    row_h = 8

    # Header
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(26, 58, 92)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        last = i == len(headers) - 1
        pdf.cell(col_w, row_h, str(h), border=1, fill=True,
                 new_x="LMARGIN" if last else "RIGHT",
                 new_y="NEXT" if last else "TOP")

    # Rows
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 51, 51)
    for idx, record in enumerate(data):
        pdf.set_fill_color(248, 249, 250) if idx % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        for i, h in enumerate(headers):
            last = i == len(headers) - 1
            pdf.cell(col_w, row_h, str(record.get(h, ""))[:80], border=1, fill=True,
                     new_x="LMARGIN" if last else "RIGHT",
                     new_y="NEXT" if last else "TOP")

    pdf.output(output_path)
```

### Extract all text from a PDF

```python
from pypdf import PdfReader

def pdf_to_text(path: str) -> str:
    """Extract all text from a PDF file."""
    reader = PdfReader(path)
    return "\n\n".join(page.extract_text() or "" for page in reader.pages)
```

---

## 10. Quality checks

Before writing the final `.pdf` file:

1. **Page count** — within expected range (rough rule: ~300 words/page for A4 body at 11pt).
2. **Table headers** — visually check they repeat on every page for multi-page tables.
3. **Font rendering** — non-ASCII characters render correctly (use TTF fonts with `uni=True` for Unicode).
4. **File size** — a 50-page document without images should be < 3 MB.
5. **Page numbers** — display correctly and match total page count.

---

## Common pitfalls

| Pitfall | Fix |
|---------|-----|
| Non-ASCII characters render as `?` or boxes | Use `add_font("Name", "", "font.ttf", uni=True)` with a TTF font that covers the needed glyphs |
| Table rows split across pages | Use `pdf.set_auto_page_break(auto=True, margin=20)` — fpdf2 handles page breaks automatically |
| Text truncated in cells | Use `multi_cell()` instead of `cell()` for wrapping, or truncate explicitly with `[:80]` |
| Large PDF file size with images | Resize images before embedding; use JPEG over PNG for photos |
| pypdf returns empty text from scanned PDFs | Image-only PDFs need OCR (e.g., Tesseract). pypdf only extracts text-based content |
| WeasyPrint fails on Windows/containers | Use fpdf2 instead — pure Python, no native dependencies |
