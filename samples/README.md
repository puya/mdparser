# Sample Outputs

This folder contains sample outputs from running `mdparser` on the test document (`tests/test_document.md`).

## Generated Files

### Headings Level 3 Extraction

- **`headings_level3.md`** - Markdown format output (preserves original formatting)
- **`headings_level3.txt`** - Plain text format with hierarchical indentation
- **`headings_level3.json`** - Structured JSON format with metadata

### Headings Level 3 with Content

- **`headings_level3_with_first_line.md`** - Markdown format with 1 line of content included after each level 3 heading
- **`headings_level3_with_2lines.md`** - Markdown format with 2 lines of content included after each level 3 heading
- **`headings_level3_with_chars.md`** - Markdown format with 100 characters of content included after each level 3 heading
- **`headings_level3_with_chars_50.md`** - Markdown format with 50 characters of content included after each level 3 heading

## Commands Used

### Basic extraction:
```bash
mdparser tests/test_document.md --headings 3 --format <format> -o samples/headings_level3.<ext>
```

### With content lines for deepest level:
```bash
# Include 1 line of content after each level 3 heading
mdparser tests/test_document.md --headings 3 --include-content-lines 1 -o samples/headings_level3_with_first_line.md

# Include 2 lines of content
mdparser tests/test_document.md --headings 3 --include-content-lines 2 -o samples/headings_level3_with_2lines.md

# Include 100 characters of content
mdparser tests/test_document.md --headings 3 --include-content-chars 100 -o samples/headings_level3_with_chars.md
```

## Results Summary

- **Total headings found**: 19
- **Levels extracted**: 1, 2, and 3
- **Breakdown**:
  - Level 1 headings: 1
  - Level 2 headings: 9
  - Level 3 headings: 9

## Notes

These samples demonstrate the different output formats available:
- **Markdown**: Preserves original markdown syntax
- **Text**: Plain text with indentation for hierarchy
- **JSON**: Structured data with metadata (operation, parameters, results, count, status)

