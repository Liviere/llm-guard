"""LLM output scanners init"""

import importlib as _importlib

from .ban_code import BanCode
from .ban_competitors import BanCompetitors
from .ban_substrings import BanSubstrings
from .ban_topics import BanTopics
from .bias import Bias
from .code import Code
from .deanonymize import Deanonymize
from .emotion_detection import EmotionDetection
from .factual_consistency import FactualConsistency
from .gibberish import Gibberish
from .json import JSON
from .language import Language
from .language_same import LanguageSame
from .malicious_urls import MaliciousURLs
from .no_refusal import NoRefusal, NoRefusalLight
from .reading_time import ReadingTime
from .regex import Regex
from .relevance import Relevance
from .sentiment import Sentiment
from .toxicity import Toxicity
from .url_reachabitlity import URLReachability
from .util import get_scanner_by_name

# Presidio-backed scanners are loaded lazily so that importing this package
# does not require the ``presidio-analyzer`` / ``presidio-anonymizer``
# packages to be installed.
_LAZY_IMPORTS: dict[str, str] = {
    "Sensitive": ".sensitive",
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module = _importlib.import_module(_LAZY_IMPORTS[name], __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BanCode",
    "BanCompetitors",
    "BanSubstrings",
    "BanTopics",
    "Bias",
    "Code",
    "Deanonymize",
    "EmotionDetection",
    "JSON",
    "Language",
    "LanguageSame",
    "MaliciousURLs",
    "NoRefusal",
    "NoRefusalLight",
    "ReadingTime",
    "FactualConsistency",
    "Gibberish",
    "Regex",
    "Relevance",
    "Sensitive",
    "Sentiment",
    "Toxicity",
    "URLReachability",
    "get_scanner_by_name",
]
