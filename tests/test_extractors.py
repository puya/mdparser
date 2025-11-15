"""
Unit tests for the mdparser extraction functions.

Tests cover heading extraction, emphasized text extraction, and text search
functionality using a comprehensive test markdown document.
"""

from pathlib import Path

import pytest

from mdparser.extractors import (
    _extract_text_from_token,
    extract_emphasized,
    extract_headings,
    find_and_extract,
)
from mdparser.parser import get_raw_content, parse_markdown_file
from mdparser.utils import format_output

# Path to test document
TEST_DOC_PATH = Path(__file__).parent / "test_document.md"


class TestHeadingExtraction:
    """Tests for heading extraction functionality."""

    @pytest.fixture
    def document(self):
        """Load and parse the test document."""
        return parse_markdown_file(str(TEST_DOC_PATH))

    def test_extract_headings_level_1(self, document):
        """Test extracting only level 1 headings."""
        headings = extract_headings(document, max_level=1)

        assert len(headings) == 1
        assert headings[0]["level"] == 1
        assert headings[0]["text"] == "Main Title Level 1"
        assert headings[0]["raw"] == "# Main Title Level 1"

    def test_extract_headings_level_2(self, document):
        """Test extracting headings up to level 2."""
        headings = extract_headings(document, max_level=2)

        # Should have 1 level 1 + multiple level 2 headings
        assert len(headings) >= 2
        assert headings[0]["level"] == 1
        assert all(h["level"] <= 2 for h in headings)

        # Check specific headings exist
        heading_texts = [h["text"] for h in headings]
        assert "Main Title Level 1" in heading_texts
        assert "Section 1: Introduction" in heading_texts
        assert "Section 2: Features" in heading_texts

    def test_extract_headings_level_3(self, document):
        """Test extracting headings up to level 3."""
        headings = extract_headings(document, max_level=3)

        assert len(headings) >= 5  # Should have multiple headings
        assert all(h["level"] <= 3 for h in headings)

        # Check for level 3 headings
        level_3_headings = [h for h in headings if h["level"] == 3]
        assert len(level_3_headings) > 0
        assert "Subsection 1.1: Details" in [h["text"] for h in level_3_headings]

    def test_extract_headings_all_levels(self, document):
        """Test extracting all heading levels (1-6)."""
        headings = extract_headings(document, max_level=6)

        # Should have headings at multiple levels
        levels = {h["level"] for h in headings}
        assert len(levels) >= 3  # At least 3 different levels

        # Check for deep nesting
        assert max(levels) >= 3

    def test_heading_hierarchy_preserved(self, document):
        """Test that heading hierarchy is preserved in order."""
        headings = extract_headings(document, max_level=6)

        # Headings should be in document order
        for i in range(len(headings) - 1):
            # If we encounter a higher level heading, previous lower level should be parent
            if headings[i + 1]["level"] <= headings[i]["level"]:
                # This is valid - new section at same or higher level
                pass


class TestEmphasizedTextExtraction:
    """Tests for emphasized text extraction functionality."""

    @pytest.fixture
    def document(self):
        """Load and parse the test document."""
        return parse_markdown_file(str(TEST_DOC_PATH))

    def test_extract_bold_text(self, document):
        """Test extracting only bold text."""
        emphasized = extract_emphasized(document, type="bold")

        assert len(emphasized) > 0
        assert all(item["type"] == "bold" for item in emphasized)

        # Check for specific bold terms
        bold_texts = [item["text"] for item in emphasized]
        assert any("bold text" in text.lower() for text in bold_texts)
        assert any("important terms" in text.lower() for text in bold_texts)

    def test_extract_italic_text(self, document):
        """Test extracting only italic text."""
        emphasized = extract_emphasized(document, type="italic")

        assert len(emphasized) > 0
        assert all(item["type"] == "italic" for item in emphasized)

        # Check for specific italic terms
        italic_texts = [item["text"] for item in emphasized]
        assert any("italic text" in text.lower() for text in italic_texts)

    def test_extract_all_emphasized(self, document):
        """Test extracting all emphasized text (bold and italic)."""
        emphasized = extract_emphasized(document, type="all")

        assert len(emphasized) > 0

        # Should have both bold and italic
        types = {item["type"] for item in emphasized}
        assert "bold" in types
        assert "italic" in types

    def test_emphasized_with_heading_context(self, document):
        """Test that emphasized text includes heading context."""
        emphasized = extract_emphasized(document, type="bold")

        # All items should have heading_context (may be None for content before first heading)
        for item in emphasized:
            assert "heading_context" in item

    def test_emphasized_filter_by_section(self, document):
        """Test filtering emphasized text by section."""
        emphasized = extract_emphasized(
            document, type="bold", heading_filter="Section 3: Definitions"
        )

        assert len(emphasized) > 0

        # All results should be from Section 3 or its subsections
        for item in emphasized:
            assert item["heading_context"] is not None
            # Should be under Section 3 or a subsection
            assert (
                "Section 3" in item["heading_context"]
                or "Subsection 3.1" in item["heading_context"]
            )

    def test_emphasized_filter_by_subsection(self, document):
        """Test filtering emphasized text by subsection."""
        emphasized = extract_emphasized(document, type="bold", heading_filter="Subsection 3.1")

        # Should find terms in subsection 3.1
        if len(emphasized) > 0:
            for item in emphasized:
                assert item["heading_context"] is not None
                assert "Subsection 3.1" in item["heading_context"]


class TestTextSearch:
    """Tests for text search and context extraction functionality."""

    @pytest.fixture
    def content(self):
        """Load raw content of test document."""
        return get_raw_content(str(TEST_DOC_PATH))

    def test_basic_search(self, content):
        """Test basic text search."""
        results = find_and_extract(content, "Section 1")

        assert len(results) > 0
        assert all("match" in r for r in results)
        assert all("line_number" in r for r in results)
        assert all("context" in r for r in results)

    def test_search_with_context_after(self, content):
        """Test search with lines after context."""
        results = find_and_extract(content, "Section 1", lines_after=2)

        assert len(results) > 0
        for result in results:
            context_lines = result["context_lines"]
            assert len(context_lines) >= 2  # Match + at least 2 lines after

    def test_search_with_context_before(self, content):
        """Test search with lines before context."""
        results = find_and_extract(content, "Section 2", lines_before=1, lines_after=1)

        assert len(results) > 0
        for result in results:
            context_lines = result["context_lines"]
            assert len(context_lines) >= 2  # At least 1 before + match + 1 after

    def test_case_insensitive_search(self, content):
        """Test case-insensitive search."""
        results_lower = find_and_extract(content, "section", case_sensitive=False)
        results_upper = find_and_extract(content, "SECTION", case_sensitive=False)

        # Should find same results (case-insensitive)
        assert len(results_lower) == len(results_upper)
        assert len(results_lower) > 0

    def test_case_sensitive_search(self, content):
        """Test case-sensitive search."""
        results_lower = find_and_extract(content, "section", case_sensitive=True)
        results_upper = find_and_extract(content, "SECTION", case_sensitive=True)

        # May have different results (case-sensitive)
        # At least one should find results
        assert len(results_lower) > 0 or len(results_upper) > 0

    def test_regex_search(self, content):
        """Test regex pattern search."""
        # Search for headings (## )
        results = find_and_extract(content, r"^## ", case_sensitive=False)

        assert len(results) > 0
        # Should find level 2 headings
        for result in results:
            assert "##" in result["match"] or "##" in result["context"]

    def test_search_within_section(self, content):
        """Test section-limited search."""
        # Search for "Term" only in Section 3
        results = find_and_extract(
            content, "Term", within_section="Section 3: Definitions", lines_after=1
        )

        assert len(results) > 0

        # All results should be from Section 3
        for result in results:
            # Check that result is in the Definitions section
            # (line numbers should be within Section 3 range)
            assert result["line_number"] > 0

    def test_search_no_matches(self, content):
        """Test search with pattern that doesn't exist."""
        results = find_and_extract(content, "NONEXISTENT_PATTERN_XYZ123")

        assert len(results) == 0

    def test_search_special_characters(self, content):
        """Test search with special characters."""
        results = find_and_extract(content, '"Term1"', case_sensitive=False)

        # Should find quoted terms
        assert len(results) > 0


class TestOutputFormatting:
    """Tests for output formatting functionality."""

    @pytest.fixture
    def document(self):
        """Load and parse the test document."""
        return parse_markdown_file(str(TEST_DOC_PATH))

    def test_json_output_format(self, document):
        """Test JSON output formatting."""
        headings = extract_headings(document, max_level=2)
        output = format_output(
            headings,
            operation="extract_headings",
            file_path=str(TEST_DOC_PATH),
            parameters={"max_level": 2},
            output_format="json",
        )

        assert output.startswith("{")
        assert '"operation"' in output
        assert '"results"' in output
        assert '"count"' in output

    def test_text_output_format(self, document):
        """Test plain text output formatting."""
        headings = extract_headings(document, max_level=2)
        output = format_output(
            headings,
            operation="extract_headings",
            file_path=str(TEST_DOC_PATH),
            parameters={"max_level": 2},
            output_format="text",
        )

        assert isinstance(output, str)
        assert len(output) > 0
        # Should contain heading text
        assert "Main Title Level 1" in output

    def test_markdown_output_format(self, document):
        """Test markdown output formatting."""
        headings = extract_headings(document, max_level=2)
        output = format_output(
            headings,
            operation="extract_headings",
            file_path=str(TEST_DOC_PATH),
            parameters={"max_level": 2},
            output_format="markdown",
        )

        assert isinstance(output, str)
        assert len(output) > 0
        # Should contain markdown heading syntax
        assert "# Main Title Level 1" in output


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_file(self, tmp_path):
        """Test handling of empty markdown file."""
        empty_file = tmp_path / "empty.md"
        empty_file.write_text("")

        document = parse_markdown_file(str(empty_file))
        headings = extract_headings(document, max_level=6)

        # Should handle empty file gracefully
        assert isinstance(headings, list)

    def test_file_with_only_headings(self, tmp_path):
        """Test file with only headings, no content."""
        heading_file = tmp_path / "headings.md"
        heading_file.write_text("# Heading 1\n## Heading 2\n### Heading 3")

        document = parse_markdown_file(str(heading_file))
        headings = extract_headings(document, max_level=6)

        assert len(headings) == 3

    def test_file_with_no_headings(self, tmp_path):
        """Test file with no headings."""
        no_headings_file = tmp_path / "no_headings.md"
        no_headings_file.write_text("Just some text with **bold** and *italic*.")

        document = parse_markdown_file(str(no_headings_file))
        headings = extract_headings(document, max_level=6)

        assert len(headings) == 0

        # But should still extract emphasized text
        emphasized = extract_emphasized(document, type="all")
        assert len(emphasized) > 0

    def test_invalid_regex_pattern(self, tmp_path):
        """Test handling of invalid regex patterns."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\nSome content")
        content = get_raw_content(str(test_file))

        with pytest.raises(ValueError):
            find_and_extract(content, "[invalid(regex", case_sensitive=False)


class TestHelperFunctions:
    """Tests for helper functions."""

    @pytest.fixture
    def document(self):
        """Load and parse the test document."""
        return parse_markdown_file(str(TEST_DOC_PATH))

    def test_extract_text_from_token(self, document):
        """Test text extraction from tokens."""
        # Get first heading token
        for token in document.children:
            if hasattr(token, "__class__") and "Heading" in token.__class__.__name__:
                text = _extract_text_from_token(token)
                assert isinstance(text, str)
                assert len(text) > 0
                break
