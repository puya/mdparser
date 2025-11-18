"""
Extraction functions for headings, emphasized text, and text search.

This module provides functions to extract specific elements from parsed
Markdown documents using Mistletoe's AST traversal capabilities.
"""

import re
from typing import Dict, List, Optional

from mistletoe import Document
from mistletoe.block_token import Heading, Paragraph
from mistletoe.span_token import Emphasis, Strong

from .utils import verbose_msg


def _walk_tokens(token):
    """
    Recursively walk through Mistletoe tokens.

    Yields all tokens in the document tree, including nested tokens.
    """
    yield token
    if hasattr(token, "children") and token.children is not None:
        for child in token.children:
            yield from _walk_tokens(child)


def extract_headings(
    document: Document,
    max_level: int = 6,
    include_content_for_level: Optional[int] = None,
    include_content_lines: Optional[int] = None,
    include_content_chars: Optional[int] = None,
) -> List[Dict[str, any]]:
    """
    Extract headings from a parsed Markdown document up to a specified level.

    Args:
        document: A Mistletoe Document object
        max_level: Maximum heading level to extract (1-6). Extracts levels 1 through max_level.
        include_content_for_level: If specified, include content after headings at this level
        include_content_lines: Number of lines to include (used with include_content_for_level)
        include_content_chars: Number of characters to include (used with include_content_for_level).
                              If both lines and chars are specified, lines takes precedence.

    Returns:
        A list of dictionaries, each containing:
        - level: The heading level (1-6)
        - text: The heading text content
        - raw: The raw markdown representation of the heading
        - content: (optional) Content after the heading, if include_content_for_level is set
    """
    headings = []

    verbose_msg(f"Extracting headings up to level {max_level}")
    if include_content_for_level:
        if include_content_lines:
            verbose_msg(
                f"Including {include_content_lines} line(s) of content for level {include_content_for_level} headings"
            )
        elif include_content_chars:
            verbose_msg(
                f"Including {include_content_chars} character(s) of content for level {include_content_for_level} headings"
            )

    # Iterate through document children in order to find content after headings
    children = document.children if hasattr(document, "children") else []

    for i, token in enumerate(children):
        if isinstance(token, Heading):
            if token.level <= max_level:
                # Extract text content from heading
                text_parts = []
                for child in token.children:
                    if hasattr(child, "content"):
                        text_parts.append(child.content)
                    elif isinstance(child, str):
                        text_parts.append(child)
                    else:
                        # For nested tokens, try to get content recursively
                        text_parts.append(_extract_text_from_token(child))

                heading_text = "".join(text_parts).strip()

                # Create markdown representation
                prefix = "#" * token.level
                raw_heading = f"{prefix} {heading_text}"

                heading_data = {"level": token.level, "text": heading_text, "raw": raw_heading}

                # If this is the specified level, find content after it
                if include_content_for_level and token.level == include_content_for_level:
                    content = _get_content_after_heading(
                        children, i, lines=include_content_lines, chars=include_content_chars
                    )
                    if content:
                        heading_data["content"] = content
                        # Update raw to include the content
                        raw_heading = f"{raw_heading}\n{content}"
                        heading_data["raw"] = raw_heading

                headings.append(heading_data)

    verbose_msg(f"Found {len(headings)} headings")
    return headings


def _get_content_after_heading(
    children: List, heading_index: int, lines: Optional[int] = None, chars: Optional[int] = None
) -> Optional[str]:
    """
    Get content after a heading at the given index.
    
    Looks for non-heading block tokens (like Paragraph) after the heading
    and extracts text content according to the specified limits.
    
    Args:
        children: List of document children tokens
        heading_index: Index of the heading token in children list
        lines: Number of lines to extract (takes precedence over chars)
        chars: Number of characters to extract (used if lines is not specified)
        
    Returns:
        Content as a string, or None if no content found
    """
    if lines is None and chars is None:
        return None

    # Collect all text content after the heading until we hit another heading
    content_parts = []
    heading_level = None

    # Look ahead through subsequent tokens
    for i in range(heading_index + 1, len(children)):
        token = children[i]

        # Stop if we hit another heading at same or higher level
        if isinstance(token, Heading):
            if heading_level is None:
                # Get the level of the original heading
                original_heading = children[heading_index]
                if isinstance(original_heading, Heading):
                    heading_level = original_heading.level
            if token.level <= heading_level:
                break

        # Extract text from paragraphs and other content blocks
        if isinstance(token, Paragraph) or (hasattr(token, "children") and token.children):
            text = _extract_text_from_token(token).strip()
            if text:
                content_parts.append(text)

    if not content_parts:
        return None

    # Combine all content
    full_content = "\n".join(content_parts)

    # Apply limits
    if lines is not None and lines > 0:
        # Extract specified number of lines
        content_lines = full_content.split("\n")
        extracted_lines = content_lines[:lines]
        return "\n".join(extracted_lines)
    elif chars is not None and chars > 0:
        # Extract specified number of characters
        return full_content[:chars]

    return None


def extract_emphasized(
    document: Document, type: str = "all", heading_filter: Optional[str] = None
) -> List[Dict[str, any]]:
    """
    Extract emphasized text (bold/italic) from a parsed Markdown document.

    Args:
        document: A Mistletoe Document object
        type: Type of emphasis to extract ('all', 'bold', 'italic')
        heading_filter: Optional heading text to filter by (only extract emphasized
                       text under this heading)

    Returns:
        A list of dictionaries, each containing:
        - type: 'bold' or 'italic'
        - text: The emphasized text content
        - heading_context: The heading under which this text appears (if available)
    """
    emphasized_items = []
    # Maintain a stack of headings to track current section hierarchy
    # Stack tracks headings in order, with most recent (current) heading last
    heading_stack = []

    verbose_msg(f"Extracting emphasized text (type: {type})")
    if heading_filter:
        verbose_msg(f"Filtering by heading: {heading_filter}")

    def _process_token(token):
        """
        Process a single token, updating heading context and extracting emphasized text.

        Args:
            token: Current token to process
        """
        nonlocal heading_stack

        # Track current heading for context
        # In Mistletoe, headings are block-level tokens that appear before their content
        if isinstance(token, Heading):
            heading_text = _extract_text_from_token(token)
            # Update heading stack: remove headings at same or deeper level
            # This handles cases where we encounter a new heading at same/lesser level
            while heading_stack and heading_stack[-1]["level"] >= token.level:
                heading_stack.pop()
            # Add current heading to stack
            heading_stack.append({"level": token.level, "text": heading_text})
            verbose_msg(f"Entering heading section: {heading_text} (level {token.level})")

        # Extract bold text
        if isinstance(token, Strong) and type in ("all", "bold"):
            # Get current heading context (most recent heading in stack)
            current_heading = heading_stack[-1]["text"] if heading_stack else None

            # Check if heading filter matches: check if filter is in any heading in the stack
            # (to handle subsections under the filtered heading)
            matches_filter = True
            if heading_filter:
                matches_filter = False
                for heading_info in heading_stack:
                    if heading_filter.lower() in heading_info["text"].lower():
                        matches_filter = True
                        break

            if matches_filter:
                text = _extract_text_from_token(token)
                emphasized_items.append(
                    {"type": "bold", "text": text, "heading_context": current_heading}
                )

        # Extract italic text
        elif isinstance(token, Emphasis) and type in ("all", "italic"):
            # Get current heading context (most recent heading in stack)
            current_heading = heading_stack[-1]["text"] if heading_stack else None

            # Check if heading filter matches: check if filter is in any heading in the stack
            # (to handle subsections under the filtered heading)
            matches_filter = True
            if heading_filter:
                matches_filter = False
                for heading_info in heading_stack:
                    if heading_filter.lower() in heading_info["text"].lower():
                        matches_filter = True
                        break

            if matches_filter:
                text = _extract_text_from_token(token)
                emphasized_items.append(
                    {"type": "italic", "text": text, "heading_context": current_heading}
                )

        # Recursively process children (for nested tokens like paragraphs containing emphasized text)
        if hasattr(token, "children") and token.children is not None:
            for child in token.children:
                _process_token(child)

    # Traverse document children in order (preserves document structure)
    # In Mistletoe, document.children contains top-level blocks (headings, paragraphs, etc.)
    # in document order
    for token in document.children:
        _process_token(token)

    verbose_msg(f"Found {len(emphasized_items)} emphasized text items")
    return emphasized_items


def find_and_extract(
    content: str,
    pattern: str,
    lines_before: int = 0,
    lines_after: int = 0,
    case_sensitive: bool = False,
    within_section: Optional[str] = None,
) -> List[Dict[str, any]]:
    """
    Find text pattern in markdown content and extract surrounding context.

    Args:
        content: The raw markdown content as a string
        pattern: The text pattern to search for (supports regex)
        lines_before: Number of lines to include before each match
        lines_after: Number of lines to include after each match
        case_sensitive: Whether the search should be case-sensitive
        within_section: Optional heading text to limit search to (only search within this section)

    Returns:
        A list of dictionaries, each containing:
        - match: The matched text
        - line_number: The line number where the match was found (1-indexed)
        - context: The surrounding lines (before + match + after)
        - context_lines: List of lines in the context
    """
    lines = content.split("\n")
    matches = []

    verbose_msg(f"Searching for pattern: {pattern}")
    verbose_msg(
        f"Case sensitive: {case_sensitive}, Context: {lines_before} before, {lines_after} after"
    )

    # If within_section is specified, identify the section boundaries
    section_start = None
    section_end = None
    if within_section:
        verbose_msg(f"Limiting search to section: {within_section}")
        # Find the section heading
        section_pattern = re.compile(r"^#+\s+" + re.escape(within_section) + r"\s*$", re.IGNORECASE)
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if section_pattern.match(stripped_line):
                section_start = i
                verbose_msg(f"Found section starting at line {i + 1}")
                # Find the next section of same or higher level
                heading_level = len(stripped_line) - len(stripped_line.lstrip("#"))
                for j in range(i + 1, len(lines)):
                    next_stripped = lines[j].strip()
                    if next_stripped.startswith("#"):
                        next_heading_level = len(next_stripped) - len(next_stripped.lstrip("#"))
                        if next_heading_level <= heading_level:
                            section_end = j
                            verbose_msg(f"Section ends at line {j + 1}")
                            break
                if section_end is None:
                    section_end = len(lines)
                    verbose_msg(f"Section extends to end of document (line {len(lines)})")
                break

        if section_start is None:
            verbose_msg(f"Warning: Section '{within_section}' not found, searching entire document")

    flags = 0 if case_sensitive else re.IGNORECASE

    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {pattern}. Error: {e}")

    for i, line in enumerate(lines):
        # Skip if we're filtering by section and this line is outside the section
        if within_section and section_start is not None:
            if i < section_start or (section_end is not None and i >= section_end):
                continue

        if regex.search(line):
            # Extract context lines (i is 0-indexed, line_number is 1-indexed)
            start_idx = max(0, i - lines_before)
            end_idx = min(len(lines), i + 1 + lines_after)
            line_number = i + 1  # Convert to 1-indexed for output

            context_lines = lines[start_idx:end_idx]
            context = "\n".join(context_lines).rstrip("\n")

            # Find the actual match in the line
            match_obj = regex.search(line)
            matched_text = match_obj.group(0) if match_obj else line.strip()

            matches.append(
                {
                    "match": matched_text,
                    "line_number": line_number,
                    "context": context,
                    "context_lines": context_lines,
                }
            )

    verbose_msg(f"Found {len(matches)} matches")
    return matches


def _extract_text_from_token(token) -> str:
    """
    Recursively extract text content from a Mistletoe token.

    This helper function handles nested tokens and extracts all text content.
    Note: Heading tokens have a content attribute that may not reflect the actual
    heading text, so we extract from children instead.

    Args:
        token: A Mistletoe token object

    Returns:
        The extracted text content as a string
    """
    # Special handling for Heading tokens - extract from children, not content attribute
    if isinstance(token, Heading):
        if hasattr(token, "children") and token.children:
            parts = []
            for child in token.children:
                parts.append(_extract_text_from_token(child))
            return "".join(parts)
        else:
            return ""

    if hasattr(token, "content"):
        return str(token.content)
    elif isinstance(token, str):
        return token
    elif hasattr(token, "children"):
        parts = []
        for child in token.children:
            parts.append(_extract_text_from_token(child))
        return "".join(parts)
    else:
        return str(token)
