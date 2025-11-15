# Tests

This directory contains unit tests for the mdparser CLI tool.

## Test Files

- **`test_document.md`**: A comprehensive test markdown file with various patterns including:
  - Headings at all levels (1-6)
  - Bold and italic text in various contexts
  - Nested sections and subsections
  - Special characters and edge cases
  - Long content for context extraction testing

- **`test_extractors.py`**: Comprehensive unit tests covering:
  - Heading extraction at all levels
  - Emphasized text extraction (bold, italic, all)
  - Text search with context
  - Section-limited search
  - Output formatting (JSON, text, markdown)
  - Edge cases (empty files, no headings, invalid patterns)

## Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run with verbose output
uv run pytest tests/ -v

# Run specific test class
uv run pytest tests/test_extractors.py::TestHeadingExtraction

# Run with coverage
uv run pytest tests/ --cov=src/mdparser --cov-report=html
```

## Test Coverage

The tests cover:
- ✅ Heading extraction (levels 1-6)
- ✅ Emphasized text extraction (bold, italic, all)
- ✅ Section filtering for emphasized text
- ✅ Text search with context (before/after)
- ✅ Case-sensitive and case-insensitive search
- ✅ Regex pattern search
- ✅ Section-limited search
- ✅ Output formatting (JSON, text, markdown)
- ✅ Edge cases and error handling

All 28 tests pass successfully.

