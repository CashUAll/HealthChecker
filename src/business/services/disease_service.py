"""Serviciu pentru gestionarea bolilor"""
from typing import List, Optional, Tuple

from src.business.models.disease import Disease
from src.business.services.scoring_service import ScoringService
from src.data.repositories.disease_repository import DiseaseRepository


class DiseaseService:
    """Serviciu pentru operațiuni cu boli"""

    def __init__(self):
        self.repository = DiseaseRepository()
        self.scoring_service = ScoringService()

    def get_all(self) -> List[Disease]:
        """Returnează toate bolile"""
        return self.repository.get_all()

    def get_by_id(self, disease_id: int) -> Optional[Disease]:
        """Returnează o boală după ID"""
        return self.repository.get_by_id(disease_id)

    def get_diseases_with_scores(self, symptoms: List[str]) -> List[Tuple[Disease, float]]:
        """Returnează bolile cu scoruri calculate"""
        diseases = self.get_all()
        return self.scoring_service.calculate_scores(diseases, symptoms)

    def get_top_matches(self, symptoms: List[str], top_n: int = 5) -> List[Tuple[Disease, float]]:
        """Returnează primele N potriviri"""
        diseases = self.get_all()
        return self.scoring_service.get_top_matches(diseases, symptoms, top_n)