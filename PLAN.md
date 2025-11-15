# Markdown Parser CLI Tool

## Overview

Build a Python CLI tool that processes large Markdown files to extract structured information (headings, emphasized text, sections) without requiring full file reads. **The tool must be optimized for AI-agent usage** with clear status messages, structured output, and machine-readable formats.

## Research Findings

### Markdown Parsing Libraries Evaluated

1. **Mistune** (https://github.com/lepture/mistune)

   - **Performance**: Fastest Python markdown parser (~56ms for README processing)
   - **AST Support**: Can generate AST with `renderer='ast'` option
   - **Compliance**: Not fully CommonMark compliant (trade-off for speed)
   - **Extensibility**: Plugin system for custom directives
   - **API**: `mistune.create_markdown(renderer='ast')` returns AST tokens

2. **Mistletoe** (https://github.com/miyuchina/mistletoe) ⭐ RECOMMENDED

   - **Performance**: Fastest CommonMark-compliant parser in pure Python
   - **AST Support**: Built-in `ASTRenderer` and `walk()` method for tree traversal
   - **Compliance**: Fully CommonMark spec-compliant
   - **Extensibility**: Easy custom token definitions, multiple renderers
   - **API**: `document.walk()` method, `ASTRenderer()` for AST output
   - **Bonus**: Already includes CLI utility that can be extended
   - **Example**: Extract headings with `isinstance(node, mistletoe.block_token.Heading)`
   - **Example**: Extract emphasized text with `isinstance(node, mistletoe.span_token.Strong/Emphasis)`

3. **Marko** (https://github.com/frostming/marko)

   - **Performance**: Slower (3x slower than Python-Markdown, significantly slower than Mistune)
   - **AST Support**: Parses into AST structure
   - **Compliance**: Full CommonMark compliance
   - **Extensibility**: Highly extensible with custom extensions
   - **Use Case**: Best for when maximum extensibility is needed over performance

### Recommendation

**Mistletoe** is recommended as the primary choice because:

- Fastest CommonMark-compliant parser (good balance of speed and correctness)
- Excellent API for extraction (`walk()` method, AST renderer)
- Already has CLI foundation
- Clear examples for extracting headings and emphasized text
- Spec compliance ensures accurate parsing of complex markdown

**Mistune** as alternative if absolute maximum speed is required and CommonMark compliance is not critical.

### CLI Framework

- **argparse**: Built-in Python CLI framework (no dependencies)
- **click**: Modern, more user-friendly API (recommended if adding dependency is acceptable)

### Package Management

- **UV**: Use UV for modern, fast package management, dependency resolution, and builds
- **pyproject.toml**: Configure project using UV's standard format

## Implementation Plan

### 1. Project Structure

```
mdparser/
├── mdparser/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── parser.py            # Markdown parsing logic using Mistletoe
│   ├── extractors.py        # Extraction functions (headings, emphasized, sections)
│   └── utils.py             # Utility functions (file handling, output formatting, status messages)
├── tests/
│   └── test_extractors.py
├── pyproject.toml           # UV project configuration (dependencies, build settings)
├── .python-version          # Python version specification for UV
├── PLAN.md                  # This plan document saved in the project folder
└── README.md
```

### 2. Core Functionality

#### 2.1 Heading Extraction

- Extract headings at specified levels (1, 1-2, 1-2-3, etc.)
- Preserve heading hierarchy in output
- Include heading line numbers for reference (using Mistletoe's token positions)
- Support filtering by level range (e.g., levels 1-3)
- Implementation: Use `document.walk()` and filter `mistletoe.block_token.Heading` nodes

#### 2.2 Emphasized Text Extraction

- Extract bold text (`**text**`) using `mistletoe.span_token.Strong`
- Extract italic text (`*text*` or `_text_`) using `mistletoe.span_token.Emphasis`
- Option to extract from specific sections (under headings) or entire document
- Preserve context (which heading section it belongs to)
- Implementation: Use `document.walk()` and filter span tokens, track current heading context

#### 2.3 Text Search and Context Extraction

- Find text pattern in document (regex support)
- Extract N lines before/after match
- Extract entire section from heading to next heading
- Support case-sensitive/case-insensitive search
- Implementation: Parse markdown, search in raw text or AST, extract surrounding context

#### 2.4 Output Management

- Output to terminal (stdout) by default
- Option to write to file (`-o` or `--output`)
- Preserve markdown formatting in output
- Support different output formats (markdown, plain text, JSON)
- **AI-Agent Friendly Features**:
  - Structured JSON output format for easy parsing
  - Clear status messages printed to stderr (so stdout contains only results)
  - Progress indicators for large files
  - Informative success/error messages with consistent format
  - Verbose mode (`--verbose`) for detailed operation logs
  - Quiet mode (`--quiet`) to suppress status messages

### 3. CLI Design

#### Command Structure

```bash
mdparser <file> [OPTIONS]

Options:
  --headings LEVELS       Extract headings up to level N (1-6)
                          Example: --headings 3 (extracts levels 1, 2, 3)
  
  --emphasized            Extract all emphasized text (bold/italic)
  --emphasized-bold       Extract only bold text
  --emphasized-italic     Extract only italic text
  --emphasized-under HEADING  Extract emphasized text under specific heading
  
  --find TEXT             Find text pattern and extract context
  --lines-after N         Number of lines to extract after match (default: 0)
  --lines-before N        Number of lines to extract before match (default: 0)
  --case-sensitive        Case-sensitive search (default: case-insensitive)
  
  --output FILE           Write output to file instead of stdout
  --format FORMAT         Output format: markdown, text, json (default: markdown)
  --verbose               Show detailed operation messages and progress
  --quiet                 Suppress status messages (only show results)
  
  --help                  Show help message with examples
```

#### Example Usage

```bash
# Extract all level 1 and 2 headings
mdparser document.md --headings 2

# Extract headings and write to file
mdparser document.md --headings 3 --output headings.txt

# Extract all bold text
mdparser document.md --emphasized-bold

# Find section starting with "### 1.1" and extract 5 lines after
mdparser document.md --find "### 1.1" --lines-after 5

# Extract emphasized text under a specific heading
mdparser document.md --emphasized-under "1. FOUNDATION OF RELATIONSHIP"
```

### 4. Technical Implementation

#### 4.1 Dependencies & Package Management

- **UV**: Use UV for package management, dependency resolution, and build/packaging
- **pyproject.toml**: Configure project dependencies and build settings using UV
- Dependencies:
  - `mistletoe`: Primary markdown parsing library (recommended)
  - `argparse` or `click`: CLI framework (argparse is built-in, click optional)
  - `re`: Built-in regex support (no additional dependency needed)
- Installation: `uv pip install` or `uv sync` for dependency management
- Build: Use `uv build` for creating distributable packages

#### 4.2 Parser Module (`parser.py`)

- Use `mistletoe.Document()` to parse markdown file
- Implement `document.walk()` for tree traversal
- Extract heading hierarchy with levels using `mistletoe.block_token.Heading`
- Identify emphasized text nodes using `mistletoe.span_token.Strong` and `mistletoe.span_token.Emphasis`
- Build section tree (headings → content mapping) by tracking heading context during walk

#### 4.3 Extractors Module (`extractors.py`)

- `extract_headings(document, max_level)`: Walk AST, filter headings by level
- `extract_emphasized(document, type='all', heading_filter=None)`: Walk AST, filter span tokens, optionally filter by heading context
- `find_and_extract(md_content, pattern, lines_before, lines_after, case_sensitive)`: Search raw text or AST, extract surrounding lines

#### 4.4 CLI Module (`cli.py`)

- Parse command-line arguments using argparse or click
- Validate inputs (file exists, valid levels, etc.)
- Call appropriate extractor functions
- Handle output formatting and writing
- Comprehensive error handling and user-friendly messages
- **AI-Agent Optimized Features**:
  - Print status messages to stderr using `print(..., file=sys.stderr)`
  - Use structured JSON output format with metadata (operation type, count, file info)
  - Clear error messages with actionable information
  - Progress indicators for long operations
  - Consistent message format: `[STATUS] message` or `[SUCCESS] message` or `[ERROR] message`
  - Exit codes: 0 for success, 1 for errors, 2 for no matches found

#### 4.5 Status Message System (`utils.py`)

- `status_msg(message, level='INFO')`: Print status messages to stderr
- `success_msg(message)`: Print success messages
- `error_msg(message)`: Print error messages
- `progress_msg(message, percent=None)`: Print progress indicators
- All messages follow format: `[LEVEL] message`
- Respect `--verbose` and `--quiet` flags

#### 4.6 Defensive Programming

- File existence validation
- Empty file handling
- Invalid heading level validation
- No matches found handling (exit code 2)
- Encoding issues (UTF-8 support)
- Large file handling (Mistletoe handles this efficiently)
- Graceful error messages with suggestions

### 5. AI-Agent Usability Features

#### 5.1 Status Messages

- All status messages printed to stderr (so stdout contains only results)
- Format: `[STATUS] <message>` for operations, `[SUCCESS] <message>` for completion, `[ERROR] <message>` for errors
- Examples:
  - `[STATUS] Parsing markdown file: document.md`
  - `[STATUS] Extracting headings up to level 3...`
  - `[SUCCESS] Found 25 headings`
  - `[ERROR] File not found: document.md`

#### 5.2 Structured Output Format

- JSON format includes metadata:
  ```json
  {
    "operation": "extract_headings",
    "file": "document.md",
    "parameters": {"max_level": 3},
    "results": [...],
    "count": 25,
    "status": "success"
  }
  ```

- Plain text format: Clean, parseable output
- Markdown format: Preserves original formatting

#### 5.3 Error Handling

- Clear error messages with context
- Exit codes: 0 (success), 1 (error), 2 (no matches found)
- Error messages include suggestions when possible
- All errors printed to stderr, not stdout

#### 5.4 Progress Indicators

- For large files: Show progress (e.g., "Processing... 50%")
- Verbose mode shows detailed operation steps
- Progress messages go to stderr

### 6. Documentation

- README with installation instructions (UV-based)
- Usage examples
- Help menu (`--help`) with examples
- Inline code comments
- Docstrings for all functions
- AI-agent usage examples in documentation
- **PLAN.md**: Save this plan document in the project root folder

### 7. Testing Strategy

- Unit tests for extraction functions
- Test with sample markdown files (use contract files from workspace)
- Edge cases: empty files, no headings, no matches
- CLI argument validation tests
- Test AI-agent usability: verify structured output, status messages, error handling
- Test stderr/stdout separation

## File Locations

- Main script: `mdparser/cli.py`
- Parser logic: `mdparser/parser.py`
- Extraction functions: `mdparser/extractors.py`
- Utility functions: `mdparser/utils.py`
- Project config: `pyproject.toml` (UV configuration)
- Plan document: `PLAN.md` (saved in project root)
- README: `README.md`

## Decision Points

- **Parser library**: **Mistletoe** (recommended) for best balance of speed and CommonMark compliance
- **CLI framework**: `argparse` for no dependencies, or `click` for better UX
- **Single vs multi-file**: Modular structure for maintainability
- **Status messages**: Always to stderr, structured format for AI parsing
- **Package management**: **UV** for modern, fast dependency management and builds
- **Plan documentation**: Save PLAN.md in project root for reference

