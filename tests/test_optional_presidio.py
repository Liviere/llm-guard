"""Tests verifying that llm-guard can be imported and non-Presidio scanners
can be used without the ``presidio-analyzer`` / ``presidio-anonymizer``
packages installed.

Because the test environment *does* have Presidio installed (via the ``pii``
extra), we simulate its absence by temporarily patching ``sys.modules`` so
that ``presidio_analyzer`` and ``presidio_anonymizer`` resolve to ``None``
and then reloading the relevant modules.
"""

from __future__ import annotations

import importlib
import sys
from unittest import mock

import pytest


# ---------------------------------------------------------------------------
# Helper: context-manager that hides Presidio from the import machinery
# ---------------------------------------------------------------------------

def _hide_presidio():
    """Return a mock.patch.dict that makes Presidio unimportable.

    We set every ``presidio_*`` key in ``sys.modules`` to ``None`` which
    causes ``import presidio_analyzer`` (etc.) to raise ``ImportError``.
    """
    presidio_keys = [k for k in sys.modules if k.startswith("presidio")]
    # Map every existing key to None so subsequent imports fail
    hide = {k: None for k in presidio_keys}
    # Also ensure the top-level packages are blocked even if they weren't
    # loaded yet.
    hide.setdefault("presidio_analyzer", None)
    hide.setdefault("presidio_anonymizer", None)
    hide.setdefault("presidio_anonymizer.core", None)
    hide.setdefault("presidio_anonymizer.core.text_replace_builder", None)
    return mock.patch.dict(sys.modules, hide)


# ---------------------------------------------------------------------------
# Tests: package-level imports work without Presidio
# ---------------------------------------------------------------------------

class TestImportsWithoutPresidio:
    """Verify that the main package and scanner packages can be imported
    even when Presidio is not available."""

    def test_import_llm_guard(self):
        """``import llm_guard`` must succeed without Presidio."""
        import llm_guard  # noqa: F401 – already imported, just verify no error

    def test_import_input_scanners(self):
        """``import llm_guard.input_scanners`` must succeed without Presidio."""
        import llm_guard.input_scanners  # noqa: F401

    def test_import_output_scanners(self):
        """``import llm_guard.output_scanners`` must succeed without Presidio."""
        import llm_guard.output_scanners  # noqa: F401


# ---------------------------------------------------------------------------
# Tests: Presidio-backed scanners raise clear errors when deps are missing
# ---------------------------------------------------------------------------

class TestPresidioMissingErrors:
    """When Presidio is not installed, attempting to *instantiate* a
    Presidio-backed scanner must raise ``ImportError`` with a message
    that tells the user how to install the missing packages."""

    def test_anonymize_raises_without_presidio(self):
        with _hide_presidio():
            # Force reload so the guarded try/except runs without Presidio
            mod = importlib.reload(
                importlib.import_module("llm_guard.input_scanners.anonymize")
            )
            assert mod._PRESIDIO_AVAILABLE is False

            from llm_guard.vault import Vault

            with pytest.raises(ImportError, match=r"pip install llm-guard\[pii\]"):
                mod.Anonymize(Vault())

    def test_sensitive_raises_without_presidio(self):
        with _hide_presidio():
            mod = importlib.reload(
                importlib.import_module("llm_guard.output_scanners.sensitive")
            )
            assert mod._PRESIDIO_AVAILABLE is False

            with pytest.raises(ImportError, match=r"pip install llm-guard\[pii\]"):
                mod.Sensitive()
