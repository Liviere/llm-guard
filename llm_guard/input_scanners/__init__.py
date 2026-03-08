"""Input scanners init"""

import importlib as _importlib

from .ban_code import BanCode
from .ban_competitors import BanCompetitors
from .ban_substrings import BanSubstrings
from .ban_topics import BanTopics
from .code import Code
from .emotion_detection import EmotionDetection
from .gibberish import Gibberish
from .invisible_text import InvisibleText
from .language import Language
from .prompt_injection import PromptInjection
from .regex import Regex
from .secrets import Secrets
from .sentiment import Sentiment
from .token_limit import TokenLimit
from .toxicity import Toxicity
from .util import get_scanner_by_name

# Presidio-backed scanners are loaded lazily so that importing this package
# does not require the ``presidio-analyzer`` / ``presidio-anonymizer``
# packages to be installed.
_LAZY_IMPORTS: dict[str, str] = {
    "Anonymize": ".anonymize",
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module = _importlib.import_module(_LAZY_IMPORTS[name], __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Anonymize",
    "BanCode",
    "BanCompetitors",
    "BanSubstrings",
    "BanTopics",
    "Code",
    "EmotionDetection",
    "Gibberish",
    "InvisibleText",
    "Language",
    "PromptInjection",
    "Regex",
    "Secrets",
    "Sentiment",
    "TokenLimit",
    "Toxicity",
    "get_scanner_by_name",
]
