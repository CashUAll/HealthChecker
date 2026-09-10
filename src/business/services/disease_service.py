"""Service for managing diseases"""
from typing import List, Optional, Tuple

from src.business.models.disease import Disease
from src.business.services.scoring_service import ScoringService
from src.data.repositories.disease_repository import DiseaseRepository


class DiseaseService:
    """Service for disease operations"""

    def __init__(self):
        self.repository = DiseaseRepository()
        self.scoring_service = ScoringService()
        self._current_age = 0
        self._current_sex = "both"

    def set_user_demographics(self, age: int, sex: str):
        """Set user demographics"""
        self._current_age = age
        self._current_sex = sex

    def get_all(self) -> List[Disease]:
        """Return all diseases (filtered by age and sex)"""
        if self._current_age > 0 and self._current_sex:
            return self.repository.get_relevant_for(self._current_age, self._current_sex)
        return self.repository.get_all()

    def get_by_id(self, disease_id: int) -> Optional[Disease]:
        """Return a disease by ID"""
        return self.repository.get_by_id(disease_id)

    def get_diseases_with_scores(self, symptoms: List[str]) -> List[Tuple[Disease, float]]:
        """Return diseases with calculated scores (filtered)"""
        diseases = self.get_all()
        return self.scoring_service.calculate_scores(diseases, symptoms)

    def get_top_matches(self, symptoms: List[str], top_n: int = 5) -> List[Tuple[Disease, float]]:
        """Return top N matches (filtered)"""
        diseases = self.get_all()
        return self.scoring_service.get_top_matches(diseases, symptoms, top_n)