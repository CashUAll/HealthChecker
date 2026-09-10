"""Repository for accessing disease data"""
import json
from pathlib import Path
from typing import List, Optional

from src.business.models.disease import Disease


class DiseaseRepository:
    """Repository for diseases"""

    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            self.data_path = Path(__file__).parent.parent.parent.parent / "data" / "medical" / "diseases.json"
        else:
            self.data_path = data_path

        self._diseases: List[Disease] = []
        self._load_data()

    def _load_data(self):
        """Load data from JSON"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._diseases = []
            for item in data.get("diseases", []):
                disease = Disease(
                    id=item.get("id", 0),
                    name=item.get("name", ""),
                    specialty=item.get("specialty", "General"),
                    symptoms=item.get("symptoms", {}),
                    icd10_code=item.get("icd10", ""),
                    severity=item.get("severity", 1),
                    description=item.get("description", None),
                    age_groups=item.get("age_groups", ["child", "teen", "adult", "elderly"]),
                    sex_specific=item.get("sex_specific", "both"),
                    category=item.get("category", "General")
                )
                self._diseases.append(disease)

        except FileNotFoundError:
            print(f"File {self.data_path} not found. Creating default data.")
            self._create_default_data()

    def _create_default_data(self):
        """Create default data for testing"""
        self._diseases = [
            Disease(
                id=1,
                name="Influenza",
                specialty="Infectious Diseases",
                symptoms={"fever": 0.9, "cough": 0.8, "headache": 0.7, "fatigue": 0.8}
            ),
            Disease(
                id=2,
                name="Common Cold",
                specialty="ENT",
                symptoms={"stuffy_nose": 0.9, "sneeze": 0.8, "sore_throat": 0.7}
            ),
        ]

    def get_all(self) -> List[Disease]:
        """Return all diseases"""
        return self._diseases.copy()

    def get_by_id(self, disease_id: int) -> Optional[Disease]:
        """Return a disease by ID"""
        for disease in self._diseases:
            if disease.id == disease_id:
                return disease
        return None

    def get_relevant_for(self, age: int, sex: str) -> List[Disease]:
        """Return only diseases relevant for the given age and sex"""
        return [
            disease for disease in self._diseases
            if disease.is_relevant_for(age, sex)
        ]