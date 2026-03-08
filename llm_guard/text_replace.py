"""Lightweight text replacement utility.

This module provides a TextReplaceBuilder class that can be used to perform
index-based text replacements without depending on Presidio.
"""

from __future__ import annotations


class TextReplaceBuilder:
    """Build text with multiple index-based replacements.

    This is a lightweight replacement for
    ``presidio_anonymizer.core.text_replace_builder.TextReplaceBuilder`` that
    provides the same interface used by the non-PII scanners in *llm-guard*
    (``Regex``, ``BanCompetitors``, ``Secrets``).

    Replacements are applied in order, and indices are adjusted automatically
    to account for earlier substitutions that change text length.
    """

    def __init__(self, original_text: str) -> None:
        self._text = original_text

    def get_text_in_position(self, start: int, end: int) -> str:
        """Return the substring currently at *[start, end)*."""
        return self._text[start:end]

    def replace_text_get_insertion_index(
        self, new_text: str, start: int, end: int
    ) -> int:
        """Replace the text in *[start, end)* with *new_text*.

        Returns the new insertion index (``start``).
        """
        self._text = self._text[:start] + new_text + self._text[end:]
        return start

    @property
    def output_text(self) -> str:
        """Return the current state of the text."""
        return self._text
