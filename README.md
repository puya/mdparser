# Markdown Parser CLI Tool

A Python CLI tool for extracting structured information from Markdown files, optimized for AI-agent usage with clear status messages and structured output formats.

## Features

- **Heading Extraction**: Extract headings at specified levels (1-6) with hierarchy preservation
- **Emphasized Text Extraction**: Extract bold and italic text, optionally filtered by heading context
- **Text Search**: Find text patterns (with regex support) and extract surrounding context
- **Section-Limited Search**: Limit searches to content within specific heading sections
- **Multiple Output Formats**: Markdown, plain text, or JSON output
- **AI-Agent Optimized**: Status messages to stderr, structured JSON output, clear error handling

## Installation

This project uses [UV](https://github.com/astral-sh/uv) for fast package management and builds.

### Prerequisites

- Python 3.8 or higher
- UV (install from https://github.com/astral-sh/uv)

### Install UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Recommended: Install as a CLI Tool (System-Wide) ⭐

**Best for**: CLI tools, system-wide access, isolated tool management

#### Editable Install (Development)

```bash
cd mdparser
uv tool install -e .
uv tool update-shell
```

- ✅ Changes to code are immediately reflected (no reinstall needed)
- ✅ Isolated tool environment
- ✅ System-wide `mdparser` command

#### Regular Install (Production)

```bash
cd mdparser
uv tool install .
uv tool update-shell
```

- ✅ Makes a copy of the code (works independently of source location)
- ✅ Good for stable/production versions

**Verify installation:**
```bash
uv tool list                    # Should show mdparser
which mdparser                  # Should show path in UV tools dir
mdparser --help                 # Should work from anywhere
```

**Uninstall:**
```bash
uv tool uninstall mdparser
```

For more installation options and details, see [INSTALLATION.md](INSTALLATION.md).

### Alternative: Install in Python Environment

```bash
cd mdparser
uv pip install -e .
```

This will make the `mdparser` command available system-wide in your Python environment.

## Usage

### Basic Syntax

```bash
mdparser <file> [OPTIONS]
```

### Extract Headings

Extract all level 1 and 2 headings:

```bash
mdparser document.md --headings 2
```

Extract headings up to level 3 and save to file:

```bash
mdparser document.md --headings 3 --output headings.txt
```

Extract headings in JSON format:

```bash
mdparser document.md --headings 3 --format json
```

### Extract Emphasized Text

Extract all emphasized text (bold and italic):

```bash
mdparser document.md --emphasized
```

Extract only bold text:

```bash
mdparser document.md --emphasized-bold
```

Extract only italic text:

```bash
mdparser document.md --emphasized-italic
```

Extract emphasized text under a specific heading:

```bash
mdparser document.md --emphasized-bold --emphasized-under "1. FOUNDATION OF RELATIONSHIP"
```

### Text Search

Find text pattern and extract context:

```bash
mdparser document.md --find "### 1.1"
```

Find pattern and extract 5 lines after:

```bash
mdparser document.md --find "### 1.1" --lines-after 5
```

Find pattern with context before and after:

```bash
mdparser document.md --find "Fabricator" --lines-before 2 --lines-after 3
```

Case-sensitive search:

```bash
mdparser document.md --find "Fabricator" --case-sensitive
```

**Search within a specific section:**

Limit search to content under a specific heading:

```bash
# Find "CIF" only within the Definitions section
mdparser document.md --find "\"CIF\"" --within-section "6. DEFINITIONS" --lines-after 1

# Find "Deliverables" only within Definitions section
mdparser document.md --find "\"Deliverables\"" --within-section "6. DEFINITIONS" --lines-after 1

# Find all occurrences of a term within a specific section
mdparser document.md --find "Fabricator" --within-section "6. DEFINITIONS"
```

This is particularly useful for extracting definitions or finding terms that appear multiple times but you only want matches from a specific section.

### Output Options

Write output to file:

```bash
mdparser document.md --headings 3 --output headings.txt
```

Output in JSON format:

```bash
mdparser document.md --headings 3 --format json
```

Output in plain text format:

```bash
mdparser document.md --headings 3 --format text
```

### Verbosity Options

Show detailed operation messages:

```bash
mdparser document.md --headings 3 --verbose
```

Suppress status messages (only show results):

```bash
mdparser document.md --headings 3 --quiet
```

## Output Formats

### Markdown Format (Default)

Preserves original markdown formatting:

```markdown
# ATTACHMENT B: TERMS AND CONDITIONS
## 1. FOUNDATION OF RELATIONSHIP
### 1.1 Mutual Understanding and Professional Standards
```

### Text Format

Clean, parseable plain text:

```
ATTACHMENT B: TERMS AND CONDITIONS
  1. FOUNDATION OF RELATIONSHIP
    1.1 Mutual Understanding and Professional Standards
```

### JSON Format

Structured JSON with metadata (AI-agent friendly):

```json
{
  "operation": "extract_headings",
  "file": "document.md",
  "parameters": {
    "max_level": 3
  },
  "results": [
    {
      "level": 1,
      "text": "ATTACHMENT B: TERMS AND CONDITIONS",
      "raw": "# ATTACHMENT B: TERMS AND CONDITIONS"
    }
  ],
  "count": 25,
  "status": "success"
}
```

## Status Messages

All status messages are printed to stderr, ensuring stdout contains only results. This makes the tool ideal for AI agents and scripting.

Message formats:
- `[STATUS] <message>` - Operation status
- `[SUCCESS] <message>` - Success messages
- `[ERROR] <message>` - Error messages
- `[PROGRESS] <message>` - Progress indicators
- `[VERBOSE] <message>` - Verbose details (only with --verbose)

## Exit Codes

- `0` - Success
- `1` - Error (file not found, invalid parameters, etc.)
- `2` - No matches found

## Examples

### Extract Table of Contents

```bash
# Extract all level 1 and 2 headings as a table of contents
mdparser document.md --headings 2 --format text > toc.txt

# Extract with JSON format for programmatic processing
mdparser document.md --headings 2 --format json > toc.json
```

### Find All Bold Terms

```bash
# Extract all bold text
mdparser document.md --emphasized-bold --format json > bold_terms.json

# Extract bold text only from a specific section
mdparser document.md --emphasized-bold --emphasized-under "6. DEFINITIONS" > definitions_bold.json
```

### Search for Specific Section

```bash
# Find a subsection and extract context
mdparser document.md --find "### 1.1" --lines-after 10 --format markdown

# Extract entire section with heading
mdparser document.md --find "## 6. DEFINITIONS" --lines-after 20
```

### Extract Definitions from a Section

```bash
# Find a specific definition within the Definitions section
mdparser document.md --find "\"CIF\"" --within-section "6. DEFINITIONS" --lines-after 1

# Find multiple definitions
mdparser document.md --find "\"Deliverables\"" --within-section "6. DEFINITIONS" --lines-after 1
mdparser document.md --find "\"Fabricator\"" --within-section "6. DEFINITIONS" --lines-after 1
```

### Extract Headings with Context

```bash
# Extract all level 2 headings with one line of context after each
mdparser document.md --find "^## " --lines-after 1

# Extract all level 3 headings with context
mdparser document.md --find "^### " --lines-after 1
```

### AI-Agent Usage Example

```bash
# Get structured JSON output for AI processing
mdparser document.md --headings 3 --format json --quiet > headings.json

# Extract all emphasized text with context
mdparser document.md --emphasized --format json --quiet > emphasized.json

# Search for specific terms with structured output
mdparser document.md --find "Fabricator" --within-section "6. DEFINITIONS" --format json --quiet > fabricator_def.json
```

### Complex Workflows

```bash
# Extract all definitions from a document
mdparser document.md --find "^## 6. DEFINITIONS" --lines-after 25 > all_definitions.md

# Find all section headings with their first paragraph
mdparser document.md --find "^## " --lines-after 3 > sections_with_intro.md

# Extract specific terms from multiple sections
mdparser document.md --find "Fabricator" --within-section "1. SCOPE OF AGREEMENT" > fabricator_in_scope.md
mdparser document.md --find "Fabricator" --within-section "6. DEFINITIONS" > fabricator_definition.md
```

## Complete Usage Reference

### All Available Options

```bash
mdparser <file> [OPTIONS]

Heading Extraction:
  --headings LEVELS       Extract headings up to level N (1-6)
                          Example: --headings 3 extracts levels 1, 2, 3

Emphasized Text Extraction:
  --emphasized            Extract all emphasized text (bold/italic)
  --emphasized-bold       Extract only bold text (**text**)
  --emphasized-italic    Extract only italic text (*text* or _text_)
  --emphasized-under HEADING  Extract emphasized text under specific heading

Text Search:
  --find TEXT             Find text pattern and extract context (supports regex)
  --lines-after N         Number of lines to extract after match (default: 0)
  --lines-before N        Number of lines to extract before match (default: 0)
  --case-sensitive        Case-sensitive search (default: case-insensitive)
  --within-section HEADING  Limit search to content under a specific heading
                          (e.g., "6. DEFINITIONS")

Output Options:
  -o, --output FILE       Write output to file instead of stdout
  --format FORMAT         Output format: markdown, text, json (default: markdown)

Verbosity:
  -v, --verbose           Show detailed operation messages and progress
  -q, --quiet             Suppress status messages (only show results)

  -h, --help              Show help message with examples
```

### Common Usage Patterns

#### Pattern 1: Extract Document Structure
```bash
# Get all headings as table of contents
mdparser document.md --headings 3 --format text

# Get headings with JSON for programmatic processing
mdparser document.md --headings 3 --format json --quiet > structure.json
```

#### Pattern 2: Find Specific Content
```bash
# Find a term anywhere in document
mdparser document.md --find "Fabricator"

# Find a term only in a specific section
mdparser document.md --find "Fabricator" --within-section "6. DEFINITIONS"

# Find with context (3 lines before, 5 lines after)
mdparser document.md --find "Fabricator" --lines-before 3 --lines-after 5
```

#### Pattern 3: Extract Definitions
```bash
# Extract all definitions from Definitions section
mdparser document.md --find "^## 6. DEFINITIONS" --lines-after 25

# Extract specific definition
mdparser document.md --find "\"CIF\"" --within-section "6. DEFINITIONS" --lines-after 1

# Extract multiple definitions
for term in "CIF" "Deliverables" "Fabricator"; do
  mdparser document.md --find "\"$term\"" --within-section "6. DEFINITIONS" --lines-after 1
done
```

#### Pattern 4: Extract Emphasized Terms
```bash
# All bold text
mdparser document.md --emphasized-bold

# Bold text from specific section
mdparser document.md --emphasized-bold --emphasized-under "6. DEFINITIONS"

# All emphasized (bold + italic) with JSON output
mdparser document.md --emphasized --format json --quiet > emphasized.json
```

#### Pattern 5: Extract Sections with Context
```bash
# All level 2 headings with first paragraph
mdparser document.md --find "^## " --lines-after 3

# All level 3 subsections with content
mdparser document.md --find "^### " --lines-after 2

# Specific section with full content
mdparser document.md --find "## 1. SCOPE OF AGREEMENT" --lines-after 50
```

#### Pattern 6: AI-Agent Workflow
```bash
# Extract document structure
mdparser document.md --headings 3 --format json --quiet > doc_structure.json

# Extract all definitions
mdparser document.md --find "^## 6. DEFINITIONS" --lines-after 25 --format json --quiet > definitions.json

# Extract key terms from specific sections
mdparser document.md --find "Fabricator" --within-section "1. SCOPE OF AGREEMENT" --format json --quiet > fabricator_scope.json
mdparser document.md --find "Fabricator" --within-section "6. DEFINITIONS" --format json --quiet > fabricator_def.json
```

## Error Handling

The tool provides clear error messages:

```bash
$ mdparser nonexistent.md --headings 2
[ERROR] File not found: nonexistent.md
```

```bash
$ mdparser document.md --headings 10
[ERROR] Invalid parameter: Heading level must be between 1 and 6, got 10
```

```bash
$ mdparser document.md --find "[invalid(regex" --within-section "6. DEFINITIONS"
[ERROR] Invalid parameter: Invalid regex pattern: [invalid(regex. Error: ...
```

## Development

### Project Structure

```
mdparser/
├── mdparser/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── parser.py            # Markdown parsing logic
│   ├── extractors.py        # Extraction functions
│   └── utils.py             # Utility functions
├── tests/
│   └── test_extractors.py
├── pyproject.toml           # UV project configuration
├── PLAN.md                  # Implementation plan
└── README.md
```

### Running Tests

```bash
# Install test dependencies
uv sync --dev

# Run tests
pytest tests/
```

### Building

```bash
uv build
```

## Dependencies

- **mistletoe**: Fast, CommonMark-compliant Markdown parser
- **argparse**: Built-in CLI framework (no external dependencies)

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## Support

For issues and questions, please open an issue on the project repository.

