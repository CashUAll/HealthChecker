"""Smart question selector (Akinator style)"""
from typing import List, Set
from src.business.models.disease import Disease


class QuestionSelector:
    """Selects the next question to eliminate the most diseases"""

    def __init__(self, all_questions: List[str]):
        self.all_questions = all_questions
        self.asked_questions: Set[str] = set()

    def reset(self):
        """Reset selector for a new session"""
        self.asked_questions = set()

    def select_next_question(
            self,
            possible_diseases: List[Disease],
            user_symptoms: List[str]
    ) -> str:
        """Select the question that eliminates the most diseases"""
        if not possible_diseases:
            return None

        if len(possible_diseases) <= 3:
            return None

        available = [q for q in self.all_questions if q not in self.asked_questions]
        if not available:
            return None

        candidates = available[:30] if len(available) > 30 else available

        best_question = None
        best_eliminated = -1

        for question in candidates:
            symptom = self._extract_symptom(question)
            diseases_if_yes = self._count_diseases_with_symptom(
                possible_diseases, symptom
            )
            diseases_if_no = len(possible_diseases) - diseases_if_yes
            eliminated = min(diseases_if_yes, diseases_if_no)

            if eliminated > best_eliminated:
                best_eliminated = eliminated
                best_question = question

        return best_question

    def _extract_symptom(self, question: str) -> str:
        """Extract symptom from question"""
        from src.shared.helpers import extract_symptom_from_question
        return extract_symptom_from_question(question)

    def _count_diseases_with_symptom(
            self,
            diseases: List[Disease],
            symptom: str
    ) -> int:
        """Count how many diseases have a given symptom"""
        count = 0
        for disease in diseases:
            if symptom in disease.symptoms:
                count += 1
        return count