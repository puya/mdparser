"""
Command-line interface for the Markdown Parser tool.

This module provides a user-friendly CLI for extracting headings, emphasized text,
and performing text searches on Markdown files. Optimized for AI-agent usage
with clear status messages and structured output.
"""

import argparse
import os
import sys

from .extractors import extract_emphasized, extract_headings, find_and_extract
from .parser import get_raw_content, parse_markdown_file
from .utils import error_msg, format_output, set_verbosity, status_msg, success_msg


def validate_file(file_path: str) -> None:
    """
    Validate that a file exists and is readable.

    Args:
        file_path: Path to the file to validate

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If the file cannot be read
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not os.path.isfile(file_path):
        raise OSError(f"Path is not a file: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise OSError(f"File is not readable: {file_path}")


def validate_heading_level(level: int) -> None:
    """
    Validate that a heading level is within the valid range (1-6).

    Args:
        level: The heading level to validate

    Raises:
        ValueError: If the level is not between 1 and 6
    """
    if not (1 <= level <= 6):
        raise ValueError(f"Heading level must be between 1 and 6, got {level}")


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description=(
            "mdparser extracts structured information from Markdown files including headings,\n"
            "emphasized text (bold/italic), and text patterns with context. Outputs in markdown,\n"
            "plain text, or structured JSON formats.\n\n"
            "This tool can extract headings at specified levels, emphasized text (bold/italic),\n"
            "and perform text searches with context extraction. Optimized for AI-agent usage\n"
            "with clear status messages and structured output formats.\n\n"
            "Examples:\n"
            "  mdparser document.md --headings 3\n"
            "  mdparser document.md --emphasized-bold\n"
            '  mdparser document.md --find "### 1.1" --lines-after 5\n'
            '  mdparser document.md --find \'"CIF"\' --within-section "6. DEFINITIONS" --lines-after 1\n'
            "  mdparser document.md --headings 2 --format json --output headings.json\n"
            "  mdparser document.md --emphasized-bold --emphasized-under \"Section 3\"\n"
            "  mdparser document.md --find \"pattern\" --lines-before 2 --lines-after 3\n\n"
            "Output Formats:\n"
            "  - markdown: Preserves original markdown formatting (default)\n"
            "  - text: Plain text with hierarchical indentation\n"
            "  - json: Structured JSON with metadata (operation, parameters, results, count, status)\n\n"
            "Exit Codes:\n"
            "  0: Success\n"
            "  1: Error (file not found, invalid parameters, etc.)\n"
            "  2: No matches found\n\n"
            "Note: Status messages go to stderr, results to stdout (use --quiet to suppress status)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "For more information and detailed examples, see the README.md file.\n"
            "JSON output includes: operation, file, parameters, results array, count, and status."
        ),
    )

    # Positional argument: file path
    parser.add_argument("file", type=str, help="Path to the Markdown file to process")

    # Heading extraction options
    heading_group = parser.add_argument_group("Heading Extraction")
    heading_group.add_argument(
        "--headings",
        type=int,
        metavar="LEVELS",
        choices=range(1, 7),
        help="Extract headings up to level N (1-6). Example: --headings 3 extracts levels 1, 2, and 3",
    )
    heading_group.add_argument(
        "--include-content-lines",
        type=int,
        metavar="N",
        help="Include N lines of content after headings at the deepest extracted level (e.g., --headings 3 --include-content-lines 2 includes 2 lines for level 3 headings)",
    )
    heading_group.add_argument(
        "--include-content-chars",
        type=int,
        metavar="N",
        help="Include N characters of content after headings at the deepest extracted level (e.g., --headings 3 --include-content-chars 100). If both --include-content-lines and --include-content-chars are specified, lines takes precedence.",
    )

    # Emphasized text extraction options
    emphasized_group = parser.add_argument_group("Emphasized Text Extraction")
    emphasized_group.add_argument(
        "--emphasized",
        action="store_true",
        help="Extract all emphasized text (both bold and italic)",
    )
    emphasized_group.add_argument(
        "--emphasized-bold", action="store_true", help="Extract only bold text (**text**)"
    )
    emphasized_group.add_argument(
        "--emphasized-italic",
        action="store_true",
        help="Extract only italic text (*text* or _text_)",
    )
    emphasized_group.add_argument(
        "--emphasized-under",
        type=str,
        metavar="HEADING",
        help="Extract emphasized text under a specific heading",
    )

    # Text search options
    search_group = parser.add_argument_group("Text Search")
    search_group.add_argument(
        "--find",
        type=str,
        metavar="TEXT",
        help="Find text pattern and extract context (supports regex)",
    )
    search_group.add_argument(
        "--lines-after",
        type=int,
        metavar="N",
        default=0,
        help="Number of lines to extract after match (default: 0)",
    )
    search_group.add_argument(
        "--lines-before",
        type=int,
        metavar="N",
        default=0,
        help="Number of lines to extract before match (default: 0)",
    )
    search_group.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Case-sensitive search (default: case-insensitive)",
    )
    search_group.add_argument(
        "--within-section",
        type=str,
        metavar="HEADING",
        help='Limit search to content under a specific heading (e.g., "6. DEFINITIONS")',
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "-o", "--output", type=str, metavar="FILE", help="Write output to file instead of stdout"
    )
    output_group.add_argument(
        "--format",
        type=str,
        choices=["markdown", "text", "json"],
        default="markdown",
        help="Output format: markdown, text, or json (default: markdown)",
    )

    # Verbosity options
    verbosity_group = parser.add_argument_group("Verbosity")
    verbosity_group.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed operation messages and progress"
    )
    verbosity_group.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress status messages (only show results)"
    )

    return parser


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code: 0 for success, 1 for errors, 2 for no matches found
    """
    parser = create_parser()
    args = parser.parse_args()

    # Set verbosity
    set_verbosity(verbose=args.verbose, quiet=args.quiet)

    # Validate file
    try:
        validate_file(args.file)
    except (OSError, FileNotFoundError) as e:
        error_msg(str(e))
        return 1

    # Determine operation
    operation = None
    results = []
    parameters = {}

    try:
        # Heading extraction
        if args.headings is not None:
            validate_heading_level(args.headings)
            status_msg(f"Extracting headings up to level {args.headings}...")
            document = parse_markdown_file(args.file)
            # If content inclusion options are set, include content for the deepest level
            include_content_level = None
            include_content_lines = None
            include_content_chars = None
            if args.include_content_lines is not None or args.include_content_chars is not None:
                include_content_level = args.headings
                include_content_lines = args.include_content_lines
                include_content_chars = args.include_content_chars
            results = extract_headings(
                document,
                max_level=args.headings,
                include_content_for_level=include_content_level,
                include_content_lines=include_content_lines,
                include_content_chars=include_content_chars,
            )
            operation = "extract_headings"
            parameters = {"max_level": args.headings}
            if include_content_level:
                parameters["include_content_for_level"] = include_content_level
                if include_content_lines is not None:
                    parameters["include_content_lines"] = include_content_lines
                if include_content_chars is not None:
                    parameters["include_content_chars"] = include_content_chars

        # Emphasized text extraction
        elif args.emphasized or args.emphasized_bold or args.emphasized_italic:
            if args.emphasized:
                emphasis_type = "all"
            elif args.emphasized_bold:
                emphasis_type = "bold"
            else:
                emphasis_type = "italic"

            status_msg(f"Extracting {emphasis_type} emphasized text...")
            document = parse_markdown_file(args.file)
            results = extract_emphasized(
                document, type=emphasis_type, heading_filter=args.emphasized_under
            )
            operation = "extract_emphasized"
            parameters = {"type": emphasis_type, "heading_filter": args.emphasized_under}

        # Text search
        elif args.find:
            status_msg(f"Searching for pattern: {args.find}")
            if args.within_section:
                status_msg(f"Limiting search to section: {args.within_section}")
            content = get_raw_content(args.file)
            results = find_and_extract(
                content,
                pattern=args.find,
                lines_before=args.lines_before,
                lines_after=args.lines_after,
                case_sensitive=args.case_sensitive,
                within_section=args.within_section,
            )
            operation = "find_and_extract"
            parameters = {
                "pattern": args.find,
                "lines_before": args.lines_before,
                "lines_after": args.lines_after,
                "case_sensitive": args.case_sensitive,
                "within_section": args.within_section,
            }

        else:
            error_msg("No operation specified. Use --headings, --emphasized, or --find")
            parser.print_help()
            return 1

        # Check if we have results
        if not results:
            status_msg("No matches found")
            if args.format == "json":
                # Still output JSON even if no matches
                output = format_output(results, operation, args.file, parameters, args.format)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(output)
                else:
                    print(output)
            return 2

        # Format output
        success_msg(f"Found {len(results)} result(s)")
        output = format_output(results, operation, args.file, parameters, args.format)

        # Write output
        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(output)
                success_msg(f"Output written to {args.output}")
            except OSError as e:
                error_msg(f"Error writing to file {args.output}: {e}")
                return 1
        else:
            print(output)

        return 0

    except ValueError as e:
        error_msg(f"Invalid parameter: {e}")
        return 1
    except Exception as e:
        error_msg(f"Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
