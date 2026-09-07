"""Sistem de scoring pentru potrivirea bolilor"""
from typing import List, Tuple

from src.business.models.disease import Disease
from src.shared.constants import MIN_SCORE_THRESHOLD, MAX_RESULTS


class ScoringService:
    """Calculează scoruri pentru boli"""

    def __init__(self, min_threshold: float = MIN_SCORE_THRESHOLD):
        self.min_threshold = min_threshold

    def calculate_scores(
            self,
            diseases: List[Disease],
            symptoms: List[str]
    ) -> List[Tuple[Disease, float]]:
        """
        Calculează scorurile pentru toate bolile.

        Args:
            diseases: Lista de boli
            symptoms: Lista simptomelor utilizatorului

        Returns:
            Lista de tuple (boală, scor) sortată descrescător
        """
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
        """
        Returnează primele N potriviri.

        Args:
            diseases: Lista de boli
            symptoms: Lista simptomelor utilizatorului
            top_n: Numărul maxim de rezultate

        Returns:
            Lista cu primele N boli și scorurile lor
        """
        all_scores = self.calculate_scores(diseases, symptoms)
        return all_scores[:top_n]