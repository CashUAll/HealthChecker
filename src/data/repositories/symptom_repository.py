"""Repository pentru accesul la întrebări și simptome"""
import json
from pathlib import Path
from typing import List, Optional


class SymptomRepository:
    """Repository pentru simptome și întrebări"""

    def __init__(self, questions_path: Optional[Path] = None):
        if questions_path is None:
            self.questions_path = Path(__file__).parent.parent.parent.parent / "data" / "medical" / "questions.json"
        else:
            self.questions_path = questions_path

        self._questions: List[str] = []
        self._load_data()

    def _load_data(self):
        """Încarcă întrebările din JSON"""
        try:
            with open(self.questions_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._questions = data.get("questions", [])
        except FileNotFoundError:
            print(f"Fișierul {self.questions_path} nu există. Se creează date implicite.")
            self._create_default_data()

    def _create_default_data(self):
        """Creează întrebări implicite"""
        self._questions = [
            "Aveți febră?",
            "Aveți tuse?",
            "Aveți dureri de cap?",
            "Aveți dureri în gât?",
            "Aveți oboseală?",
        ]

    def get_questions(self) -> List[str]:
        """Returnează lista de întrebări"""
        return self._questions.copy()

    def get_question_by_index(self, index: int) -> Optional[str]:
        """Returnează întrebarea de la indexul specificat"""
        if 0 <= index < len(self._questions):
            return self._questions[index]
        return None

    def get_symptom_from_question(self, question: str) -> str:
        """Extrage simptomul din textul întrebării"""
        from src.shared.helpers import extract_symptom_from_question
        return extract_symptom_from_question(question)