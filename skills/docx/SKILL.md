# Skill: DOCX Document

Guidelines for reading, writing, and modifying `.docx` Word documents using `python-docx`.
Covers creating documents from scratch, reading existing files, modifying content,
styling text, tables, images, headers/footers, sections, and helper patterns for agents.

**Dependency:** `pip install python-docx` (add to stage `dependencies` in `manifest.yaml`).

**Alternative:** For markdown-to-docx conversion with brand templates, use `pandoc` with a
reference document (see § 10 below).

---

## When to use

- Agent produces a Word document as output (reports, proposals, contracts, letters)
- Agent reads an uploaded `.docx` file as input (data extraction, content analysis)
- Agent modifies an existing `.docx` template (fill placeholders, append sections, update fields)
- Agent converts structured data into a formatted document with headings, tables, and images

---

## 1. Creating a new document

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Title
doc.add_heading("Monthly Report", level=0)

# Subtitle paragraph
subtitle = doc.add_paragraph("Generated automatically by Nuvio Agent")
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Body paragraphs
doc.add_heading("Executive Summary", level=1)
doc.add_paragraph(
    "This report covers the key metrics and performance indicators "
    "for the month of January 2026."
)

# Bullet list
doc.add_heading("Key Findings", level=2)
doc.add_paragraph("Revenue increased by 15%", style="List Bullet")
doc.add_paragraph("Customer churn decreased to 2.1%", style="List Bullet")
doc.add_paragraph("NPS score reached 72", style="List Bullet")

# Numbered list
doc.add_heading("Action Items", level=2)
doc.add_paragraph("Review pricing strategy", style="List Number")
doc.add_paragraph("Launch retention campaign", style="List Number")
doc.add_paragraph("Schedule quarterly review", style="List Number")

# Page break
doc.add_page_break()

doc.save("report.docx")
```

### Using a reference/template document

```python
# Start from a branded template (preserves styles, headers, footers)
doc = Document("_config/templates/brand-reference.docx")
doc.add_heading("Chapter 1", level=1)
doc.add_paragraph("Body text inherits the template's Normal style.")
doc.save("output.docx")
```

---

## 2. Reading an existing document

```python
from docx import Document

doc = Document("input.docx")

# Iterate all paragraphs
for para in doc.paragraphs:
    print(f"[{para.style.name}] {para.text}")

# Access specific paragraph
first_para = doc.paragraphs[0]
print(first_para.text)

# Read all tables
for table in doc.tables:
    for row in table.rows:
        row_data = [cell.text for cell in row.cells]
        print(row_data)

# Read sections
for section in doc.sections:
    print(f"Width: {section.page_width}, Height: {section.page_height}")

# Iterate content in document order (paragraphs + tables interleaved)
for block in doc.iter_inner_content():
    if hasattr(block, "text"):
        print(f"Paragraph: {block.text}")
    else:
        print(f"Table: {len(block.rows)} rows x {len(block.columns)} cols")
```

### Extract text with formatting info

```python
for para in doc.paragraphs:
    for run in para.runs:
        fmt = []
        if run.bold:
            fmt.append("bold")
        if run.italic:
            fmt.append("italic")
        if run.underline:
            fmt.append("underline")
        print(f"  Run: '{run.text}' [{', '.join(fmt) or 'normal'}]")
```

### File-like objects (in-memory pipelines)

```python
from io import BytesIO

# Read from bytes
data = get_file_bytes()  # e.g. from HTTP upload
doc = Document(BytesIO(data))

# Save to bytes
buf = BytesIO()
doc.save(buf)
file_bytes = buf.getvalue()
```

**Important:** When opening files with `open()`, use binary mode (`'rb'`) for compatibility.

---

## 3. Modifying an existing document

```python
doc = Document("template.docx")

# Replace placeholder text in paragraphs
for para in doc.paragraphs:
    if "{{company_name}}" in para.text:
        for run in para.runs:
            run.text = run.text.replace("{{company_name}}", "Acme Corp")

# Append content
doc.add_heading("New Section", level=1)
doc.add_paragraph("This section was added programmatically.")

# Insert paragraph before an existing one
target = doc.paragraphs[3]
target.insert_paragraph_before("Inserted before paragraph 4.")

# Clear a paragraph (remove content, keep formatting)
doc.paragraphs[0].clear()

doc.save("template_modified.docx")
```

### Robust placeholder replacement (cross-run)

Placeholders like `{{name}}` may be split across multiple runs by Word. Use this
pattern to handle that:

```python
def replace_placeholder(paragraph, placeholder: str, value: str) -> None:
    """Replace a placeholder that may span multiple runs."""
    full_text = paragraph.text
    if placeholder not in full_text:
        return
    # Rebuild with single run preserving first run's formatting
    fmt_run = paragraph.runs[0] if paragraph.runs else None
    paragraph.clear()
    new_text = full_text.replace(placeholder, value)
    new_run = paragraph.add_run(new_text)
    if fmt_run:
        new_run.bold = fmt_run.bold
        new_run.italic = fmt_run.italic
        new_run.font.size = fmt_run.font.size
        new_run.font.name = fmt_run.font.name
        if fmt_run.font.color and fmt_run.font.color.rgb:
            new_run.font.color.rgb = fmt_run.font.color.rgb
```

---

## 4. Text and character formatting

### Paragraph-level formatting

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.shared import Pt, Inches

para = doc.add_paragraph("Formatted paragraph")

# Alignment
para.alignment = WD_ALIGN_PARAGRAPH.CENTER  # LEFT, CENTER, RIGHT, JUSTIFY

# Indentation
fmt = para.paragraph_format
fmt.left_indent = Inches(0.5)
fmt.right_indent = Inches(0.25)
fmt.first_line_indent = Inches(0.25)

# Spacing
fmt.space_before = Pt(12)
fmt.space_after = Pt(6)

# Line spacing
fmt.line_spacing = Pt(18)                     # absolute
fmt.line_spacing = 1.5                        # relative (1.5x)
fmt.line_spacing_rule = WD_LINE_SPACING.EXACTLY  # SINGLE, ONE_POINT_FIVE, DOUBLE, EXACTLY, AT_LEAST, MULTIPLE

# Pagination control
fmt.keep_together = True       # keep paragraph on single page
fmt.keep_with_next = True      # keep with following paragraph
fmt.page_break_before = True   # force new page before
fmt.widow_control = True       # prevent orphaned lines
```

### Run-level (character) formatting

```python
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_UNDERLINE

para = doc.add_paragraph()
run = para.add_run("Styled text")

# Font basics
run.font.name = "Calibri"
run.font.size = Pt(11)

# Emphasis (tri-state: True, False, None=inherit)
run.bold = True
run.italic = True
run.underline = True                         # single underline
run.underline = WD_UNDERLINE.DASH            # SINGLE, DOUBLE, DOTTED, DASH, WAVY, etc.

# Color
run.font.color.rgb = RGBColor(0x1A, 0x3A, 0x5C)   # hex: 1A3A5C

# Theme color
from docx.enum.dml import MSO_THEME_COLOR
run.font.color.theme_color = MSO_THEME_COLOR.ACCENT_1

# Capitalization
run.font.all_caps = True
run.font.small_caps = True

# Position
run.font.superscript = True
run.font.subscript = True

# Strikethrough
run.font.strike = True
run.font.double_strike = True

# Highlight
from docx.enum.text import WD_COLOR_INDEX
run.font.highlight_color = WD_COLOR_INDEX.YELLOW

# Additional effects
run.font.emboss = True
run.font.shadow = True
run.font.outline = True
run.font.hidden = True
```

### Applying paragraph and character styles

```python
# Paragraph style (by name)
para = doc.add_paragraph("Quoted text", style="Quote")
para.style = doc.styles["Heading 2"]

# Character style (on run)
run = para.add_run("emphasized", style="Emphasis")
run.style = doc.styles["Strong"]
```

### Tab stops

```python
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Inches

tab_stops = para.paragraph_format.tab_stops
tab_stops.add_tab_stop(Inches(1.5))
tab_stops.add_tab_stop(Inches(4.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
```

---

## 5. Tables

### Creating a table

```python
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn

# Create table with header row
headers = ["Name", "Role", "Email"]
data = [
    ["Alice", "Engineer", "alice@example.com"],
    ["Bob", "Designer", "bob@example.com"],
]

table = doc.add_table(rows=1, cols=len(headers))
table.style = "Light Shading Accent 1"
table.alignment = WD_TABLE_ALIGNMENT.CENTER

# Header row
for i, h in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = h
    cell.paragraphs[0].runs[0].bold = True

# Data rows
for row_data in data:
    cells = table.add_row().cells
    for i, val in enumerate(row_data):
        cells[i].text = str(val)
```

### Column widths

```python
from docx.shared import Inches

table.autofit = False
for row in table.rows:
    row.cells[0].width = Inches(2.0)
    row.cells[1].width = Inches(1.5)
    row.cells[2].width = Inches(3.0)
```

### Row height

```python
from docx.enum.table import WD_ROW_HEIGHT_RULE

row = table.rows[0]
row.height = Cm(1.2)
row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY  # AUTO, AT_LEAST, EXACTLY
```

### Cell vertical alignment

```python
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT

cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER  # TOP, CENTER, BOTTOM
```

### Merging cells

```python
# Merge a range of cells
top_left = table.cell(0, 0)
bottom_right = table.cell(0, 2)
merged = top_left.merge(bottom_right)
merged.text = "Merged Header"
```

### Nested tables

```python
cell = table.cell(1, 2)
nested = cell.add_table(rows=2, cols=2)
nested.cell(0, 0).text = "Nested A"
```

### Cell shading (via XML — no high-level API)

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_cell_shading(cell, color: str) -> None:
    """Set cell background color. color is hex string like '1A3A5C'."""
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), color)
    shading.set(qn("w:val"), "clear")
    tc_pr.append(shading)

set_cell_shading(table.cell(0, 0), "1A3A5C")
```

---

## 6. Images

```python
from docx.shared import Inches, Cm

# Add image as a block-level element (full-width paragraph)
doc.add_picture("chart.png", width=Inches(5.0))

# Height auto-scales to preserve aspect ratio; or set both:
doc.add_picture("logo.png", width=Inches(2.0), height=Inches(1.0))

# Add image inline within a run (useful for inline icons)
para = doc.add_paragraph()
run = para.add_run()
run.add_picture("icon.png", width=Inches(0.3))

# Add image from bytes
from io import BytesIO
img_bytes = download_image(url)
doc.add_picture(BytesIO(img_bytes), width=Inches(4.0))
```

**Supported formats:** PNG, JPEG, GIF, BMP, TIFF, EMF, WMF.

---

## 7. Sections, page layout, and margins

```python
from docx.shared import Inches
from docx.enum.section import WD_ORIENT, WD_SECTION

# Access default section
section = doc.sections[0]

# Page margins
section.top_margin = Inches(1.0)
section.bottom_margin = Inches(1.0)
section.left_margin = Inches(1.25)
section.right_margin = Inches(1.25)

# Page size (Letter = 8.5 x 11 inches)
section.page_width = Inches(8.5)
section.page_height = Inches(11)

# Landscape orientation
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = Inches(11)
section.page_height = Inches(8.5)

# Add a new section (starts a new page)
new_section = doc.add_section(WD_SECTION.NEW_PAGE)  # ODD_PAGE, EVEN_PAGE, CONTINUOUS
new_section.orientation = WD_ORIENT.PORTRAIT
```

---

## 8. Headers and footers

```python
section = doc.sections[0]

# --- Header ---
header = section.header
header.is_linked_to_previous = False  # required for multi-section docs
header_para = header.paragraphs[0]
header_para.text = "Company Name\tConfidential\tPage X"
header_para.style = doc.styles["Header"]

# Add styled header
header_para.clear()
run = header_para.add_run("Acme Corp")
run.bold = True
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# --- Footer ---
footer = section.footer
footer.is_linked_to_previous = False
footer_para = footer.paragraphs[0]
footer_para.text = "Generated by Nuvio Agent"
footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Remove header/footer (reverts to previous section's)
header.is_linked_to_previous = True   # WARNING: deletes header content irreversibly
```

**Note:** Tab characters (`\t`) in headers/footers create left/center/right zones when
using the built-in "Header" style.

---

## 9. Hyperlinks (via XML — limited high-level API)

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_hyperlink(paragraph, text: str, url: str, color: str = "0563C1") -> None:
    """Add a clickable hyperlink to a paragraph."""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")

    c = OxmlElement("w:color")
    c.set(qn("w:val"), color)
    rPr.append(c)

    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)

    new_run.append(rPr)
    new_run.text = text

    # Set text element properly
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)

    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

# Usage
para = doc.add_paragraph("Visit ")
add_hyperlink(para, "our website", "https://example.com")
```

---

## 10. Pandoc alternative (markdown → docx)

For agents that produce content in markdown, `pandoc` converts to `.docx` using a
reference document for branding. This is simpler than building documents programmatically.

```bash
pandoc manuscript.md \
  --reference-doc=brand-reference.docx \
  --output=output.docx \
  --table-of-contents \
  --toc-depth=2
```

`brand-reference.docx` is pre-built with the brand's heading styles, body font, and page
margins. It lives in `_config/templates/`. Never modify the reference doc programmatically.

### Paragraph and heading mapping

| Markdown element      | Word style name    |
|-----------------------|--------------------|
| `# Heading 1`        | Heading 1          |
| `## Heading 2`       | Heading 2          |
| `### Heading 3`      | Heading 3          |
| Body paragraph        | Normal             |
| `> blockquote`       | Quote              |
| `` ``` code ``` ``   | Code               |
| `**bold**`           | Character style Bold |
| `*italic*`           | Character style Emphasis |
| `[text](url)`        | Hyperlink          |

### Footnotes (pandoc markdown)

```markdown
SpaceX targets crewed missions in the next decade.[^video-001]

[^video-001]: Source: [Instagram reel](https://www.instagram.com/reel/AAA/) · Record ID: video-001
```

---

## 11. Document metadata

```python
from docx import Document
from datetime import datetime

doc = Document()
props = doc.core_properties

# Set metadata
props.author = "Nuvio Agent"
props.title = "Monthly Report"
props.subject = "Performance Metrics"
props.keywords = "report, metrics, monthly"
props.comments = "Auto-generated document"
props.category = "Reports"
props.created = datetime.now()
props.modified = datetime.now()
props.last_modified_by = "Nuvio Agent"

doc.save("report.docx")
```

---

## 12. Helper patterns for agents

### Reusable styled heading + body writer

```python
def add_section_block(doc, heading: str, body: str, level: int = 1) -> None:
    """Add a heading followed by a body paragraph."""
    doc.add_heading(heading, level=level)
    doc.add_paragraph(body)
```

### Dict list to table

```python
def dicts_to_table(doc, data: list[dict], style: str = "Light Shading Accent 1"):
    """Write a list of dicts as a styled table. Keys become headers."""
    if not data:
        return None
    keys = list(data[0].keys())

    table = doc.add_table(rows=1, cols=len(keys))
    table.style = style

    # Header row
    for i, key in enumerate(keys):
        cell = table.rows[0].cells[i]
        cell.text = str(key)
        cell.paragraphs[0].runs[0].bold = True

    # Data rows
    for record in data:
        cells = table.add_row().cells
        for i, key in enumerate(keys):
            cells[i].text = str(record.get(key, ""))

    return table
```

### Table to dict list (reading)

```python
def table_to_dicts(table) -> list[dict]:
    """Read a table into a list of dicts using the first row as keys."""
    rows = list(table.rows)
    if len(rows) < 2:
        return []
    headers = [cell.text.strip() for cell in rows[0].cells]
    return [
        dict(zip(headers, [cell.text.strip() for cell in row.cells]))
        for row in rows[1:]
    ]
```

### Bulk placeholder replacement

```python
def replace_all_placeholders(doc, replacements: dict[str, str]) -> None:
    """Replace all {{key}} placeholders in paragraphs and tables."""
    for para in doc.paragraphs:
        for key, value in replacements.items():
            placeholder = "{{" + key + "}}"
            if placeholder in para.text:
                replace_placeholder(para, placeholder, value)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for key, value in replacements.items():
                        placeholder = "{{" + key + "}}"
                        if placeholder in para.text:
                            replace_placeholder(para, placeholder, value)
```

### Bytes output (for in-memory pipelines)

```python
from io import BytesIO

def document_to_bytes(doc) -> bytes:
    """Serialize a document to bytes without writing to disk."""
    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()

def document_from_bytes(data: bytes):
    """Load a document from bytes."""
    from docx import Document
    return Document(BytesIO(data))
```

---

## 13. Quality checks

Before writing the final `.docx` file:

1. **Heading hierarchy** — no H3 without a parent H2, no H2 without a parent H1.
2. **Section count** — verify expected number of sections exist (`len(doc.sections)`).
3. **Paragraph count** — total paragraphs match expected structure.
4. **Table integrity** — each table has a header row and the expected number of columns.
5. **Image presence** — verify embedded images by checking `doc.inline_shapes` count.
6. **Placeholder cleanup** — no remaining `{{...}}` placeholders in final output.
7. **File size** — a 50-page document without images should be < 5 MB.
8. **Encoding** — cell/paragraph values support Unicode natively; no special handling needed.

---

## Common pitfalls

| Pitfall | Fix |
|---------|-----|
| Placeholder split across runs | Word may split `{{name}}` into `{{`, `name`, `}}` in separate runs. Use cross-run replacement (see § 3) |
| Starting from `Document()` loses template styles | Use `Document("template.docx")` to inherit branded styles |
| Assuming `doc.tables` includes nested tables | `doc.tables` returns top-level only; access nested via `cell.tables` |
| Setting column width on one row only | Set width on every row's cells — Word may ignore single-row widths |
| Missing `is_linked_to_previous = False` | Headers/footers inherit from previous section by default; set explicitly |
| Using `.doc` files | python-docx only supports `.docx`/`.docm`. For `.doc`, convert with LibreOffice first |
| Overwriting source file while reading | Load fully before saving to the same path, or save to a temp file |
| Large images without width constraint | Always set `width` on `add_picture()` to prevent overflow |
| Forgetting binary mode on `open()` | Use `open("f.docx", "rb")` — text mode corrupts the ZIP container |
