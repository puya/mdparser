"""
Utility functions for status messages, output formatting, and file handling.

This module provides AI-agent friendly status messaging that prints to stderr,
ensuring stdout contains only the actual results.
"""

import json
import sys
from typing import Any, Dict, List, Optional

# Global verbosity settings
_verbose = False
_quiet = False


def set_verbosity(verbose: bool = False, quiet: bool = False) -> None:
    """
    Set global verbosity settings.

    Args:
        verbose: If True, show detailed operation messages
        quiet: If True, suppress all status messages
    """
    global _verbose, _quiet
    _verbose = verbose
    _quiet = quiet


def status_msg(message: str, level: str = "STATUS") -> None:
    """
    Print a status message to stderr.

    Args:
        message: The message to print
        level: The message level (STATUS, INFO, etc.)
    """
    if not _quiet:
        print(f"[{level}] {message}", file=sys.stderr)


def success_msg(message: str) -> None:
    """
    Print a success message to stderr.

    Args:
        message: The success message to print
    """
    if not _quiet:
        print(f"[SUCCESS] {message}", file=sys.stderr)


def error_msg(message: str) -> None:
    """
    Print an error message to stderr.

    Args:
        message: The error message to print
    """
    print(f"[ERROR] {message}", file=sys.stderr)


def progress_msg(message: str, percent: Optional[float] = None) -> None:
    """
    Print a progress message to stderr.

    Args:
        message: The progress message to print
        percent: Optional percentage (0-100) to include in the message
    """
    if not _quiet:
        if percent is not None:
            print(f"[PROGRESS] {message} ({percent:.1f}%)", file=sys.stderr)
        else:
            print(f"[PROGRESS] {message}", file=sys.stderr)


def verbose_msg(message: str) -> None:
    """
    Print a verbose message to stderr (only if verbose mode is enabled).

    Args:
        message: The verbose message to print
    """
    if _verbose and not _quiet:
        print(f"[VERBOSE] {message}", file=sys.stderr)


def format_output(
    results: List[Dict[str, Any]],
    operation: str,
    file_path: str,
    parameters: Dict[str, Any],
    output_format: str = "markdown",
) -> str:
    """
    Format extraction results in the specified output format.

    Args:
        results: List of result dictionaries from extraction functions
        operation: The operation that was performed (e.g., "extract_headings")
        file_path: Path to the source file
        parameters: Parameters used for the operation
        output_format: Output format ("markdown", "text", "json")

    Returns:
        Formatted output string
    """
    if output_format == "json":
        return format_json_output(results, operation, file_path, parameters)
    elif output_format == "text":
        return format_text_output(results, operation)
    else:  # markdown
        return format_markdown_output(results, operation)


def format_json_output(
    results: List[Dict[str, Any]], operation: str, file_path: str, parameters: Dict[str, Any]
) -> str:
    """
    Format results as JSON with metadata.

    Args:
        results: List of result dictionaries
        operation: The operation performed
        file_path: Source file path
        parameters: Operation parameters

    Returns:
        JSON string
    """
    output = {
        "operation": operation,
        "file": file_path,
        "parameters": parameters,
        "results": results,
        "count": len(results),
        "status": "success" if results else "no_matches",
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def format_text_output(results: List[Dict[str, Any]], operation: str) -> str:
    """
    Format results as plain text.

    Args:
        results: List of result dictionaries
        operation: The operation performed

    Returns:
        Plain text string
    """
    lines = []

    if operation == "extract_headings":
        for item in results:
            lines.append(f"{'  ' * (item['level'] - 1)}{item['text']}")

    elif operation == "extract_emphasized":
        for item in results:
            prefix = "**" if item["type"] == "bold" else "*"
            context = f" (under: {item['heading_context']})" if item.get("heading_context") else ""
            lines.append(f"{prefix}{item['text']}{prefix}{context}")

    elif operation == "find_and_extract":
        for item in results:
            lines.append(f"Line {item['line_number']}: {item['match']}")
            if item.get("context"):
                lines.append(f"Context:\n{item['context']}")
                lines.append("")

    return "\n".join(lines)


def format_markdown_output(results: List[Dict[str, Any]], operation: str) -> str:
    """
    Format results as Markdown, preserving original formatting.

    Args:
        results: List of result dictionaries
        operation: The operation performed

    Returns:
        Markdown string
    """
    lines = []

    if operation == "extract_headings":
        for item in results:
            lines.append(item["raw"])

    elif operation == "extract_emphasized":
        for item in results:
            prefix = "**" if item["type"] == "bold" else "*"
            context = (
                f"\n*(under: {item['heading_context']})*" if item.get("heading_context") else ""
            )
            lines.append(f"{prefix}{item['text']}{prefix}{context}")

    elif operation == "find_and_extract":
        for item in results:
            lines.append(f"**Match on line {item['line_number']}:** `{item['match']}`")
            if item.get("context"):
                lines.append("```")
                lines.append(item["context"])
                lines.append("```")
                lines.append("")

    return "\n".join(lines)
