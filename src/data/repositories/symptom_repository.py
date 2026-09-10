"""Repository for accessing questions and symptoms"""
import json
from pathlib import Path
from typing import List, Optional


class SymptomRepository:
    """Repository for symptoms and questions"""

    def __init__(self, questions_path: Optional[Path] = None):
        if questions_path is None:
            self.questions_path = Path(__file__).parent.parent.parent.parent / "data" / "medical" / "questions.json"
        else:
            self.questions_path = questions_path

        self._questions: List[str] = []
        self._load_data()

    def _load_data(self):
        """Load questions from JSON"""
        try:
            with open(self.questions_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._questions = data.get("questions", [])
        except FileNotFoundError:
            print(f"File {self.questions_path} not found. Creating default data.")
            self._create_default_data()

    def _create_default_data(self):
        """Create default questions"""
        self._questions = [
            "Do you have a fever?",
            "Do you have a cough?",
            "Do you have a headache?",
            "Do you have a sore throat?",
            "Do you feel tired?",
        ]

    def get_questions(self) -> List[str]:
        """Return the list of questions"""
        return self._questions.copy()

    def get_question_by_index(self, index: int) -> Optional[str]:
        """Return the question at the specified index"""
        if 0 <= index < len(self._questions):
            return self._questions[index]
        return None

    def get_symptom_from_question(self, question: str) -> str:
        """Extract symptom from question text"""
        from src.shared.helpers import extract_symptom_from_question
        return extract_symptom_from_question(question)