"""Scoring system for disease matching"""
from typing import List, Tuple

from src.business.models.disease import Disease
from src.shared.constants import MIN_SCORE_THRESHOLD, MAX_RESULTS


class ScoringService:
    """Calculates scores for diseases"""

    def __init__(self, min_threshold: float = MIN_SCORE_THRESHOLD):
        self.min_threshold = min_threshold

    def calculate_scores(
            self,
            diseases: List[Disease],
            symptoms: List[str]
    ) -> List[Tuple[Disease, float]]:
        """Calculate scores for all diseases"""
        results = []

        for disease in diseases:
            score = disease.match_score(symptoms)
            if score >= self.min_threshold:
                results.append((disease, score))

        return sorted(results, key=lambda x: x[1], reverse=True)

    def get_top_matches(
            self,
            diseases: List[Disease],
            symptoms: List[str],
            top_n: int = MAX_RESULTS
    ) -> List[Tuple[Disease, float]]:
        """Return top N matches"""
        all_scores = self.calculate_scores(diseases, symptoms)
        return all_scores[:top_n]