"""Tests for the lightweight TextReplaceBuilder utility."""

import pytest

from llm_guard.text_replace import TextReplaceBuilder


class TestTextReplaceBuilder:
    def test_basic_replacement(self):
        builder = TextReplaceBuilder("Hello World!")
        builder.replace_text_get_insertion_index("[REDACTED]", 6, 11)
        assert builder.output_text == "Hello [REDACTED]!"

    def test_no_replacement(self):
        builder = TextReplaceBuilder("Hello World!")
        assert builder.output_text == "Hello World!"

    def test_multiple_replacements_reverse_order(self):
        """Replacements applied in reverse order (end-to-start) to maintain indices."""
        text = "My SSN is 123-45-6789 and card is 4111-1111-1111-1111"
        builder = TextReplaceBuilder(text)
        # Replace card first (later in text) then SSN
        builder.replace_text_get_insertion_index("[CARD]", 34, 53)
        builder.replace_text_get_insertion_index("[SSN]", 10, 21)
        assert builder.output_text == "My SSN is [SSN] and card is [CARD]"

    def test_get_text_in_position(self):
        builder = TextReplaceBuilder("Hello World!")
        assert builder.get_text_in_position(0, 5) == "Hello"
        assert builder.get_text_in_position(6, 11) == "World"

    def test_replace_returns_start_index(self):
        builder = TextReplaceBuilder("abcdef")
        idx = builder.replace_text_get_insertion_index("XX", 2, 4)
        assert idx == 2
        assert builder.output_text == "abXXef"

    def test_replacement_with_longer_text(self):
        builder = TextReplaceBuilder("ab")
        builder.replace_text_get_insertion_index("[REDACTED_PERSON_1]", 0, 2)
        assert builder.output_text == "[REDACTED_PERSON_1]"

    def test_replacement_with_shorter_text(self):
        builder = TextReplaceBuilder("a long piece of text")
        builder.replace_text_get_insertion_index("X", 2, 18)
        assert builder.output_text == "a Xxt"

    def test_empty_string(self):
        builder = TextReplaceBuilder("")
        assert builder.output_text == ""
