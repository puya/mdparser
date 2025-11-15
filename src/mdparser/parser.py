"""
Markdown parser module using Mistletoe.

This module provides functions to parse Markdown files into an AST structure
that can be traversed to extract headings, emphasized text, and other elements.
"""

from typing import List

from mistletoe import Document

from .utils import status_msg, verbose_msg


def parse_markdown_file(file_path: str) -> Document:
    """
    Parse a Markdown file into a Mistletoe Document AST.

    Args:
        file_path: Path to the Markdown file to parse

    Returns:
        A Mistletoe Document object representing the parsed Markdown

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    verbose_msg(f"Opening file: {file_path}")

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            verbose_msg(f"File read successfully ({len(content)} characters)")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except OSError as e:
        raise OSError(f"Error reading file {file_path}: {e}")

    if not content.strip():
        verbose_msg("Warning: File appears to be empty")

    status_msg(f"Parsing markdown file: {file_path}")
    document = Document(content)
    verbose_msg("Markdown parsed successfully into AST")

    return document


def get_raw_content(file_path: str) -> str:
    """
    Get the raw content of a Markdown file as a string.

    This is useful for text search operations that need the raw text
    rather than the parsed AST.

    Args:
        file_path: Path to the Markdown file

    Returns:
        The raw content of the file as a string

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except OSError as e:
        raise OSError(f"Error reading file {file_path}: {e}")


def get_lines(file_path: str) -> List[str]:
    """
    Get the content of a Markdown file as a list of lines.

    This is useful for extracting context around matches (N lines before/after).

    Args:
        file_path: Path to the Markdown file

    Returns:
        A list of lines from the file

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except OSError as e:
        raise OSError(f"Error reading file {file_path}: {e}")
