---
name: xlsx
description: >
  Guidelines for reading, writing, and modifying .xlsx spreadsheet files using
  openpyxl. Covers creating workbooks, styling, formulas, tables, conditional
  formatting, and performance optimization for large files.
---

# Skill: XLSX Spreadsheet

Guidelines for reading, writing, and modifying `.xlsx` spreadsheet files using `openpyxl`.
Covers creating workbooks from scratch, reading existing files, modifying cells/rows/sheets,
styling, formulas, tables, and performance optimization for large files.

**Dependency:** `pip install openpyxl` (add to stage `dependencies` in `manifest.yaml`).
For protection against XML attacks on untrusted input: `pip install defusedxml`.

---

## When to use

- Agent produces an Excel spreadsheet as output (reports, dashboards, data exports)
- Agent reads an uploaded `.xlsx` file as input (data ingestion, transformation)
- Agent modifies an existing `.xlsx` template (fill placeholders, append rows, update cells)

---

## 1. Creating a new workbook

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

# Remove default sheet if creating named sheets
if "Sheet" in wb.sheetnames:
    del wb["Sheet"]

ws = wb.create_sheet("Report")

# Write header row
headers = ["Name", "Value", "Status"]
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = Font(bold=True, color="FFFFFF", size=11)
    cell.fill = PatternFill(fill_type="solid", fgColor="1A3A5C")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Write data rows
data = [["Alpha", 100, "OK"], ["Beta", 200, "Pending"]]
for row_idx, row_data in enumerate(data, 2):
    for col_idx, value in enumerate(row_data, 1):
        ws.cell(row=row_idx, column=col_idx, value=value)

# Auto-fit column widths (approximation)
for col_idx, h in enumerate(headers, 1):
    max_len = max(len(str(h)), *(len(str(row[col_idx - 1])) for row in data))
    ws.column_dimensions[get_column_letter(col_idx)].width = min(max_len + 4, 60)

wb.save("report.xlsx")
```

---

## 2. Reading an existing workbook

```python
from openpyxl import load_workbook

# Standard mode — full read/write access
wb = load_workbook("input.xlsx")
ws = wb.active  # or wb["SheetName"]

# Iterate rows (values only — no Cell objects)
for row in ws.iter_rows(min_row=2, values_only=True):
    name, value, status = row[0], row[1], row[2]

# Access specific cell
cell_value = ws["B3"].value
cell_value = ws.cell(row=3, column=2).value

# Read all sheet names
sheet_names = wb.sheetnames
```

### Read-only mode (large files, memory-efficient)

```python
wb = load_workbook("large_file.xlsx", read_only=True)
ws = wb.active
for row in ws.iter_rows(values_only=True):
    process(row)
wb.close()  # MUST close explicitly in read_only mode
```

**Important:** `read_only=True` returns `ReadOnlyCell` objects. You cannot modify the
workbook. Normal mode uses ~50x the file size in memory; read-only mode uses near-constant
memory.

---

## 3. Modifying an existing workbook

```python
wb = load_workbook("template.xlsx")
ws = wb["Data"]

# Update a cell
ws["B2"] = "Updated Value"
ws.cell(row=3, column=2, value=42)

# Append rows at the end
ws.append(["New Item", 300, "Active"])

# Insert rows/columns
ws.insert_rows(2, amount=3)    # insert 3 rows before row 2
ws.insert_cols(1, amount=1)    # insert 1 column before column A

# Delete rows/columns
ws.delete_rows(5, amount=2)    # delete 2 rows starting from row 5
ws.delete_cols(3, amount=1)    # delete column C

# Copy a sheet
wb.copy_worksheet(ws)

# Rename a sheet
ws.title = "Updated Data"

# Delete a sheet
del wb["OldSheet"]

wb.save("template_modified.xlsx")
```

---

## 4. Styling

### Cell styles

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers

# Font
cell.font = Font(name="Calibri", size=11, bold=True, italic=False, color="1A3A5C")

# Fill
cell.fill = PatternFill(fill_type="solid", fgColor="E8F4FD")

# Alignment
cell.alignment = Alignment(
    horizontal="center",   # left, center, right, justify
    vertical="center",     # top, center, bottom
    wrap_text=True,
    text_rotation=0,
)

# Border
thin_border = Border(
    left=Side(style="thin", color="000000"),
    right=Side(style="thin", color="000000"),
    top=Side(style="thin", color="000000"),
    bottom=Side(style="thin", color="000000"),
)
cell.border = thin_border

# Number format
cell.number_format = "#,##0.00"         # 1,234.56
cell.number_format = "R$ #,##0.00"      # R$ 1,234.56
cell.number_format = "0.0%"             # 85.0%
cell.number_format = "YYYY-MM-DD"       # 2026-01-15
```

### Conditional formatting

```python
from openpyxl.formatting.rule import CellIsRule

red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")

ws.conditional_formatting.add(
    "C2:C100",
    CellIsRule(operator="greaterThan", formula=["90"], fill=green_fill)
)
ws.conditional_formatting.add(
    "C2:C100",
    CellIsRule(operator="lessThan", formula=["50"], fill=red_fill)
)
```

---

## 5. Formulas

```python
# Write formula (Excel evaluates on open — openpyxl does NOT compute)
ws["D2"] = "=SUM(B2:C2)"
ws["D3"] = '=IF(C3>100,"High","Low")'
ws["E1"] = "=VLOOKUP(A1,Sheet2!A:B,2,FALSE)"

# When reading a file with formulas:
# - Default: returns the formula string
# - data_only=True: returns the cached value (last computed by Excel)
wb = load_workbook("with_formulas.xlsx", data_only=True)
ws = wb.active
computed_value = ws["D2"].value  # returns the number, not "=SUM(B2:C2)"
```

**Caveat:** `data_only=True` returns the value that was cached when the file was last
saved by Excel. If the file was never opened in Excel, cached values may be `None`.

---

## 6. Tables and named ranges

### Excel tables

```python
from openpyxl.worksheet.table import Table, TableStyleInfo

tab = Table(
    displayName="SalesData",
    ref="A1:D10",
)
tab.tableStyleInfo = TableStyleInfo(
    name="TableStyleMedium9",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=False,
)
ws.add_table(tab)
```

### Named ranges

```python
from openpyxl.workbook.defined_name import DefinedName

# Create a named range
ref = f"'{ws.title}'!$A$1:$D$10"
defn = DefinedName("SalesRange", attr_text=ref)
wb.defined_names.add(defn)
```

---

## 7. Merge cells, freeze panes, auto-filter

```python
# Merge cells
ws.merge_cells("A1:D1")
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=4)

# Unmerge
ws.unmerge_cells("A1:D1")

# Freeze panes (freeze row 1 = header always visible)
ws.freeze_panes = "A2"

# Auto-filter
ws.auto_filter.ref = "A1:D100"
```

---

## 8. Write-only mode (large output files)

When generating spreadsheets with thousands of rows, use write-only mode to keep memory
constant. Rows are flushed to disk as they are appended.

```python
wb = Workbook(write_only=True)
ws = wb.create_sheet("BigData")

# Must use ws.append() — no random cell access
ws.append(["Col A", "Col B", "Col C"])  # header
for i in range(100_000):
    ws.append([f"row-{i}", i * 2, i * 3])

wb.save("big_output.xlsx")
```

**Constraints of write-only mode:**
- No random cell access (`ws.cell()` or `ws["A1"]` not available)
- No merging, no tables, no conditional formatting
- Rows must be written sequentially via `ws.append()`
- Best for data-dump exports with simple formatting

---

## 9. Helper patterns for agents

### Reusable header writer

```python
def write_header(ws, row: int, headers: list[str],
                 font_color: str = "FFFFFF", bg_color: str = "1A3A5C") -> None:
    """Write a styled header row to a worksheet."""
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=h)
        cell.font = Font(bold=True, color=font_color)
        cell.fill = PatternFill(fill_type="solid", fgColor=bg_color)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
```

### Dict list to sheet

```python
def dicts_to_sheet(ws, data: list[dict], start_row: int = 1,
                   header_style: bool = True) -> None:
    """Write a list of dicts as rows. Keys become headers."""
    if not data:
        return
    keys = list(data[0].keys())

    # Header
    if header_style:
        write_header(ws, start_row, keys)
    else:
        for col, k in enumerate(keys, 1):
            ws.cell(row=start_row, column=col, value=k)

    # Data rows
    for row_idx, record in enumerate(data, start_row + 1):
        for col_idx, key in enumerate(keys, 1):
            ws.cell(row=row_idx, column=col_idx, value=record.get(key, ""))

    # Auto-width
    for col_idx, key in enumerate(keys, 1):
        max_len = max(
            len(str(key)),
            *(len(str(record.get(key, ""))) for record in data),
        )
        ws.column_dimensions[get_column_letter(col_idx)].width = min(max_len + 4, 60)
```

### Sheet to dict list (reading)

```python
def sheet_to_dicts(ws, header_row: int = 1) -> list[dict]:
    """Read a worksheet into a list of dicts using the header row as keys."""
    headers = []
    for cell in ws[header_row]:
        headers.append(str(cell.value).strip() if cell.value else f"col_{cell.column}")

    rows = []
    for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
        if all(v is None for v in row):
            continue  # skip empty rows
        rows.append(dict(zip(headers, row)))
    return rows
```

### Bytes output (for in-memory pipelines)

```python
from io import BytesIO

def workbook_to_bytes(wb) -> bytes:
    """Serialize a workbook to bytes without writing to disk."""
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

def workbook_from_bytes(data: bytes):
    """Load a workbook from bytes."""
    from openpyxl import load_workbook
    return load_workbook(BytesIO(data))
```

---

## 10. Quality checks

Before writing the final `.xlsx` file:

1. **Sheet count** — verify expected number of sheets exist (`len(wb.sheetnames)`).
2. **Header integrity** — first row of each data sheet matches expected column names.
3. **Row count sanity** — data row count matches the source data length.
4. **No empty sheets** — every sheet has at least a header row.
5. **File size** — a 10K-row spreadsheet with no images should be < 5 MB.
6. **Formula validity** — formulas start with `=` and reference valid cells/ranges.
7. **Encoding** — use `ensure_ascii=False` when embedding JSON; cell values support Unicode natively.

---

## Common pitfalls

| Pitfall | Fix |
|---------|-----|
| Forgetting `wb.close()` in read-only mode | Always close: `wb.close()` or use context manager |
| Assuming formula results are computed | openpyxl writes formulas; Excel computes them. Use `data_only=True` to read cached values |
| Memory blowup on large files | Use `read_only=True` for reading, `write_only=True` for writing |
| Modifying cells in read-only mode | Read-only workbooks are immutable — load without `read_only` to modify |
| Using `.xls` files | openpyxl only supports `.xlsx`/`.xlsm`. For `.xls`, use `xlrd` |
| Overwriting the source file while reading | Load fully before saving to the same path, or save to a temp file first |
| Column width guessing | openpyxl has no auto-fit; manually compute from max string length |
