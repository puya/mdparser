# Test Results Summary

This document summarizes all the test outputs generated from `sample-doc.md` to verify the Markdown Parser CLI tool functionality.

## Test Files Generated

### 1. Heading Extraction Tests

#### `test_output_headings_level1.md`
- **Test**: Extract only level 1 headings (`--headings 1`)
- **Expected Result**: Should extract only `# GATEWAY SCULPTURE FABRICATION AGREEMENT`
- **Status**: ✅ PASS - Correctly extracted the single level 1 heading

#### `test_output_headings_level1.json`
- **Test**: Same as above but in JSON format
- **Status**: ✅ PASS - JSON output correctly structured with metadata

#### `test_output_headings_level2.md`
- **Test**: Extract headings up to level 2 (`--headings 2`)
- **Expected Result**: Should extract:
  - `# GATEWAY SCULPTURE FABRICATION AGREEMENT` (level 1)
  - All `##` headings: Fabrication Contract, RECITALS, 1. SCOPE OF AGREEMENT, 2. PROJECT SPECIFICATIONS, 3. CONTACT INFORMATION, 4. FINANCIAL TERMS, 5. TIMELINE, 6. DEFINITIONS
- **Status**: ✅ PASS - All level 1 and 2 headings correctly extracted

#### `test_output_headings_level3.md`
- **Test**: Extract headings up to level 3 (`--headings 3`)
- **Expected Result**: Should extract all level 1, 2, and 3 headings including:
  - Level 1: GATEWAY SCULPTURE FABRICATION AGREEMENT
  - Level 2: All main sections
  - Level 3: All subsections like 1.1, 1.2, 1.3, 2.1, 2.2, etc.
- **Status**: ✅ PASS - Complete heading hierarchy extracted correctly

#### `test_output_headings_level3.json`
- **Test**: Same as above but in JSON format
- **Status**: ✅ PASS - JSON output with complete heading structure

### 2. Heading Extraction with Context

#### `test_output_headings_with_context.md`
- **Test**: Find all level 2 headings (`^## `) with 1 line after for context
- **Command**: `--find "^## " --lines-after 1`
- **Expected Result**: Should show each `##` heading followed by its first content line
- **Status**: ✅ PASS - All level 2 headings found with context

#### `test_output_subheadings_with_context.md`
- **Test**: Find all level 3 headings (`^### `) with 1 line after for context
- **Command**: `--find "^### " --lines-after 1`
- **Expected Result**: Should show each `###` subsection heading followed by its first content line
- **Status**: ✅ PASS - All level 3 headings found with context

#### `test_output_section1_with_context.md`
- **Test**: Find specific section "## 1. SCOPE OF AGREEMENT" with 2 lines after
- **Command**: `--find "^## 1. SCOPE OF AGREEMENT" --lines-after 2`
- **Expected Result**: Should show the heading and the first 2 lines of content
- **Status**: ✅ PASS - Section heading with context extracted

#### `test_output_subsection_1.1_with_context.md`
- **Test**: Find subsection "### 1.1" with 1 line after
- **Command**: `--find "^### 1.1" --lines-after 1`
- **Expected Result**: Should show "### 1.1 Services and Deliverables" followed by its first content line
- **Status**: ✅ PASS - Subsection with context extracted

### 3. Definition Extraction Tests

#### `test_output_definition_deliverables.md`
- **Test**: Find the definition of "Deliverables" in the Definitions section
- **Command**: `--find "\"Deliverables\"" --lines-after 1`
- **Expected Result**: Should find line 130: `**"Deliverables"** means all items to be provided by the Fabricator, including the completed Sculpture, documentation, certificates, and reports.`
- **Status**: ✅ PASS - Correctly found the definition on line 130

#### `test_output_definition_deliverables.json`
- **Test**: Same as above but in JSON format
- **Status**: ✅ PASS - JSON output correctly shows the match with line number and context

#### `test_output_definition_fabricator.md`
- **Test**: Find all occurrences of "Fabricator" definition
- **Command**: `--find "\"Fabricator\"" --lines-after 1`
- **Expected Result**: Should find:
  1. Line 11: First mention in the contract parties section
  2. Line 134: Definition in the Definitions section: `**"Fabricator"** means Sino Sculpture Group Limited, its employees, agents, approved subcontractors, and authorized representatives.`
- **Status**: ✅ PASS - Both occurrences found correctly

#### `test_output_definitions_section.md`
- **Test**: Extract the entire Definitions section (## 6. DEFINITIONS) with 20 lines after
- **Command**: `--find "## 6. DEFINITIONS" --lines-after 20`
- **Expected Result**: Should show the Definitions heading and all definitions including:
  - CIF
  - Commission
  - Completion Date
  - Confidential Information
  - Defect
  - Deliverables
  - Effective Date
  - Fabricator
  - Force Majeure
- **Status**: ✅ PASS - Complete Definitions section extracted

### 4. Emphasized Text Extraction

#### `test_output_bold_text.md`
- **Test**: Extract all bold text (`**text**`) from the document
- **Command**: `--emphasized-bold`
- **Expected Result**: Should find all bold text including:
  - Company names: "We the Humans Experiences Inc.", "Sino Sculpture Group Limited"
  - Section headers: "ARTIST (WTH):", "FABRICATOR:"
  - Definition terms: "CIF", "Commission", "Completion Date", etc.
- **Status**: ✅ PASS - All bold text correctly extracted with heading context

## Verification Results

### ✅ All Tests Passed

All extraction tests have been verified against the known content of `sample-doc.md`:

1. **Heading Extraction**: All heading levels (1, 2, 3) are correctly extracted with proper hierarchy
2. **Context Extraction**: Headings with surrounding lines are correctly captured
3. **Definition Search**: Specific definitions ("Deliverables", "Fabricator") are correctly located
4. **Section Extraction**: Complete sections (like Definitions) are correctly extracted
5. **Emphasized Text**: All bold text is correctly identified and extracted
6. **Output Formats**: Both Markdown and JSON formats work correctly

## Test Commands Reference

```bash
# Extract headings
mdparser tests/sample-doc.md --headings 1
mdparser tests/sample-doc.md --headings 2
mdparser tests/sample-doc.md --headings 3

# Extract headings with context
mdparser tests/sample-doc.md --find "^## " --lines-after 1
mdparser tests/sample-doc.md --find "^### " --lines-after 1

# Find specific definitions
mdparser tests/sample-doc.md --find "\"Deliverables\"" --lines-after 1
mdparser tests/sample-doc.md --find "\"Fabricator\"" --lines-after 1

# Extract entire section
mdparser tests/sample-doc.md --find "## 6. DEFINITIONS" --lines-after 20

# Extract bold text
mdparser tests/sample-doc.md --emphasized-bold

# JSON output
mdparser tests/sample-doc.md --headings 3 --format json
mdparser tests/sample-doc.md --find "\"Deliverables\"" --lines-after 1 --format json
```

## Notes

- All test outputs are saved in the `tests/` directory
- Status messages are suppressed using `--quiet` flag for clean output
- JSON outputs include metadata (operation, file, parameters, count, status)
- Markdown outputs preserve original formatting
- Line numbers in search results are 1-indexed (human-readable)

