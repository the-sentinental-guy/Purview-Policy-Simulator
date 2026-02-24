"""NLP processor for extracting intent and entities from policy queries."""
import re
from typing import Any, Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer


class NLPProcessor:
    """Processes natural language queries to extract intent and entities."""

    _INTENT_KEYWORDS: Dict[str, List[str]] = {
        "protect": ["protect", "prevent", "block", "restrict", "secure", "stop", "prohibit"],
        "detect": ["detect", "identify", "find", "scan", "discover", "flag"],
        "monitor": ["monitor", "track", "audit", "watch", "log", "alert", "notify"],
        "retain": ["retain", "keep", "archive", "preserve", "hold", "store", "save"],
        "classify": ["classify", "label", "categorise", "categorize", "tag", "mark"],
        "investigate": ["investigate", "review", "analyse", "analyze", "inspect", "report"],
        "prevent": ["prevent", "enforce", "compliance", "ensure", "mandate", "require"],
    }

    _ENTITY_PATTERNS: Dict[str, List[str]] = {
        "data_types": [
            "credit card", "debit card", "card number", "cvv", "pan",
            "ssn", "social security", "national insurance",
            "phi", "protected health information", "medical record", "health data",
            "pii", "personal information", "personal data",
            "source code", "intellectual property", "ip address",
            "passport", "driver's license", "drivers license",
            "bank account", "routing number", "iban", "swift",
            "tax id", "ein", "tin",
            "biometric", "fingerprint", "facial recognition",
        ],
        "locations": [
            "exchange", "email",
            "sharepoint",
            "teams",
            "devices", "endpoint",
            "onedrive", "one drive",
            "power bi",
        ],
        "frameworks": [
            "pci-dss", "pci dss", "pci",
            "hipaa",
            "gdpr",
            "sox", "sarbanes-oxley",
            "ccpa",
            "glba",
            "ferpa",
            "nist",
            "iso 27001",
            "fisma",
            "fedramp",
        ],
        "risk_scenarios": [
            "departing employee", "leaving employee", "terminated employee",
            "data leak", "data leakage", "data loss",
            "exfiltration", "data exfil",
            "insider threat", "insider risk",
            "unauthorised access", "unauthorized access",
            "privilege escalation",
            "shadow it",
            "data breach",
        ],
    }

    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            stop_words="english",
            lowercase=True,
        )

    def preprocess(self, text: str) -> str:
        """Clean and normalise text for processing."""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s\-]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def extract_intent(self, query: str) -> str:
        """Extract primary intent from query keywords."""
        cleaned = self.preprocess(query)
        scores: Dict[str, int] = {intent: 0 for intent in self._INTENT_KEYWORDS}
        for intent, keywords in self._INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in cleaned:
                    scores[intent] += 1
        best = max(scores, key=lambda k: scores[k])
        return best if scores[best] > 0 else "protect"

    def extract_entities(self, query: str) -> Dict[str, List[str]]:
        """Extract named entities (data types, locations, frameworks, risk scenarios)."""
        cleaned = self.preprocess(query)
        result: Dict[str, List[str]] = {category: [] for category in self._ENTITY_PATTERNS}
        for category, patterns in self._ENTITY_PATTERNS.items():
            for pattern in patterns:
                if pattern in cleaned and pattern not in result[category]:
                    result[category].append(pattern)
        return result

    def vectorize(self, texts: List[str]) -> Any:
        """Fit and transform a list of texts into a TF-IDF matrix."""
        return self._vectorizer.fit_transform(texts)

    def get_query_vector(self, query: str, fitted_vectorizer: TfidfVectorizer) -> Any:
        """Transform a single query using an already-fitted vectorizer."""
        return fitted_vectorizer.transform([self.preprocess(query)])
