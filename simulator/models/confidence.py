from typing import Tuple


class ConfidenceScorer:
    HIGH_THRESHOLD = 0.7
    MEDIUM_THRESHOLD = 0.4
    LOW_THRESHOLD = 0.2

    def score(self, tfidf_score: float, keyword_matches: int, category_match: bool) -> Tuple[float, str]:
        combined = tfidf_score
        combined += min(keyword_matches * 0.03, 0.15)
        if category_match:
            combined += 0.1
        combined = min(combined, 1.0)

        if combined >= self.HIGH_THRESHOLD:
            level = "HIGH"
        elif combined >= self.MEDIUM_THRESHOLD:
            level = "MEDIUM"
        elif combined >= self.LOW_THRESHOLD:
            level = "LOW"
        else:
            level = "VERY_LOW"

        return combined, level
