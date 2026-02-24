"""Confidence score models."""
from pydantic import BaseModel, Field
from typing import List


class ConfidenceScore(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    level: str  # HIGH, MEDIUM, LOW, VERY_LOW
    reasoning: str
    factors: List[str] = []

    @classmethod
    def from_score(cls, score: float, reasoning: str, factors: List[str] = None) -> "ConfidenceScore":
        if score >= 0.85:
            level = "HIGH"
        elif score >= 0.60:
            level = "MEDIUM"
        elif score >= 0.30:
            level = "LOW"
        else:
            level = "VERY_LOW"
        return cls(
            score=score,
            level=level,
            reasoning=reasoning,
            factors=factors or []
        )
