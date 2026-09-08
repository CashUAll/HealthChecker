"""Repository pentru accesul la datele despre boli"""
import json
from pathlib import Path
from typing import List, Optional

from src.business.models.disease import Disease


class DiseaseRepository:
    """Repository pentru boli"""

    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            self.data_path = Path(__file__).parent.parent.parent.parent / "data" / "medical" / "diseases.json"
        else:
            self.data_path = data_path

        self._diseases: List[Disease] = []
        self._load_data()

    def _load_data(self):
        """Încarcă datele din JSON"""
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
                    sex_specific=item.get("sex_specific", "both")
                )
                self._diseases.append(disease)

        except FileNotFoundError:
            print(f"Fișierul {self.data_path} nu există. Se creează date implicite.")
            self._create_default_data()

    def _create_default_data(self):
        """Creează date implicite pentru testare"""
        self._diseases = [
            Disease(
                id=1,
                name="Gripă",
                specialty="Boli Infecțioase",
                symptoms={"febra": 0.9, "tuse": 0.8, "dureri_cap": 0.7, "oboseala": 0.8},
                age_groups=["child", "teen", "adult", "elderly"],
                sex_specific="both"
            ),
            Disease(
                id=2,
                name="Răceală comună",
                specialty="ORL",
                symptoms={"nas_infundat": 0.9, "stranut": 0.8, "dureri_gat": 0.7},
                age_groups=["child", "teen", "adult", "elderly"],
                sex_specific="both"
            ),
        ]

    def get_all(self) -> List[Disease]:
        """Returnează toate bolile"""
        return self._diseases.copy()

    def get_by_id(self, disease_id: int) -> Optional[Disease]:
        """Returnează o boală după ID"""
        for disease in self._diseases:
            if disease.id == disease_id:
                return disease
        return None

    def get_relevant_for(self, age: int, sex: str) -> List[Disease]:
        """
        Returnează doar bolile relevante pentru vârsta și sexul specificat.
        """
        return [
            disease for disease in self._diseases
            if disease.is_relevant_for(age, sex)
        ]