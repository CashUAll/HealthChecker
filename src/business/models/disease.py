"""Modelul pentru o boală"""
from typing import Dict, List, Optional, Tuple


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
            description: Optional[str] = None,
            age_groups: List[str] = None,  # ["child", "adult", "elderly"]
            sex_specific: str = "both"  # "male", "female", "both"
    ):
        self.id = id
        self.name = name
        self.icd10_code = icd10_code
        self.specialty = specialty
        self.severity = severity
        self.symptoms = symptoms
        self.description = description
        self.age_groups = age_groups or ["child", "teen", "adult", "elderly"]
        self.sex_specific = sex_specific  # "male", "female", "both"

    def match_score(self, user_symptoms: List[str]) -> float:
        """Calculează scorul de potrivire (0-100)"""
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

    def is_relevant_for(self, age: int, sex: str) -> bool:
        """
        Verifică dacă boala este relevantă pentru vârsta și sexul dat.

        Args:
            age: Vârsta utilizatorului
            sex: "male" sau "female"

        Returns:
            True dacă boala este relevantă
        """
        # Verifică sexul
        if self.sex_specific != "both" and self.sex_specific != sex:
            return False

        # Verifică grupa de vârstă
        from src.shared.constants import AGE_GROUPS

        user_group = None
        for group, (min_age, max_age) in AGE_GROUPS.items():
            if min_age <= age <= max_age:
                user_group = group
                break

        if user_group is None:
            return False

        return user_group in self.age_groups

    def __repr__(self) -> str:
        return f"Disease(id={self.id}, name='{self.name}')"