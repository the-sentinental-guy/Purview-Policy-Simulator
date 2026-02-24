import logging
from typing import List, Tuple, Dict, Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from simulator.knowledge_base.dlp_templates import get_all_templates

logger = logging.getLogger(__name__)


class TemplateMatcher:
    def __init__(self):
        self.templates = get_all_templates()
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            stop_words="english",
            min_df=1,
        )
        self._build_index()

    def _build_index(self):
        corpus = [
            t.get("search_text", t.get("name", "") + " " + t.get("description", ""))
            for t in self.templates
        ]
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        logger.info(f"TF-IDF index built with {len(self.templates)} templates")

    def match(self, query: str, nlp_result: Dict[str, Any], top_k: int = 5) -> List[Tuple[Dict, float]]:
        query_vec = self.vectorizer.transform([query])
        cosine_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        bonus_scores = []
        for template in self.templates:
            bonus = 0.0
            template_text = template.get("search_text", "").lower()
            template_tags = [t.lower() for t in template.get("tags", [])]

            for kw in nlp_result.get("keywords", []):
                if kw in template_text:
                    bonus += 0.05

            for comp in nlp_result.get("compliance", []):
                if comp.replace("_", " ") in template_text or comp in template_tags:
                    bonus += 0.15

            for dt in nlp_result.get("data_types", []):
                if dt.replace("_", " ") in template_text or dt in template_tags:
                    bonus += 0.12

            for loc in nlp_result.get("locations", []):
                if loc in template_text or loc in template_tags:
                    bonus += 0.05

            for rs in nlp_result.get("risk_scenarios", []):
                if rs.replace("_", " ") in template_text or rs in template_tags:
                    bonus += 0.10

            bonus_scores.append(min(bonus, 0.4))

        combined = [c + b for c, b in zip(cosine_scores, bonus_scores)]

        indexed = sorted(enumerate(combined), key=lambda x: x[1], reverse=True)[:top_k]
        results = [(self.templates[i], score) for i, score in indexed if score > 0.01]
        return results
