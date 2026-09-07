"""Modelul pentru o boală"""
from typing import Dict, List, Optional


class Disease:
    """Model de business pentru o boală"""

    def __init__(
        self,
        id: int,
        name: str,
        specialty: str,
        symptoms: Dict[str, float],
        icd10_code: str = "",
        severity: int = 1,
        description: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.icd10_code = icd10_code
        self.specialty = specialty
        self.severity = severity
        self.symptoms = symptoms
        self.description = description

    def match_score(self, user_symptoms: List[str]) -> float:
        """
        Calculează scorul de potrivire (0-100)
        pentru simptomele utilizatorului
        """
        if not user_symptoms:
            return 0.0

        total_weight = sum(self.symptoms.values())
        if total_weight == 0:
            return 0.0

        matched_weight = 0.0
        for symptom in user_symptoms:
            if symptom in self.symptoms:
                matched_weight += self.symptoms[symptom]

        return min((matched_weight / total_weight) * 100, 100.0)

    def __repr__(self) -> str:
        return f"Disease(id={self.id}, name='{self.name}')"