#!/usr/bin/env python3
"""Generate questions.json from unique symptoms in diseases.json"""
import json
from pathlib import Path


def generate_questions():
    base_dir = Path(__file__).parent.parent
    diseases_path = base_dir / "data" / "medical" / "diseases.json"
    questions_path = base_dir / "data" / "medical" / "questions.json"

    with open(diseases_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_symptoms = set()
    for disease in data.get("diseases", []):
        for symptom in disease.get("symptoms", {}).keys():
            all_symptoms.add(symptom)

    # Generate questions from symptoms
    questions = []
    for symptom in sorted(all_symptoms):
        readable = symptom.replace("_", " ")
        questions.append(f"Do you have {readable}?")

    # Special questions (feelings, not "have")
    special_questions = [
        "Do you feel tired?",
        "Do you feel nauseous?",
        "Do you feel dizzy?",
        "Do you feel like fainting?",
        "Do you feel anxious?",
        "Do you feel depressed?",
        "Do you feel irritable?",
    ]

    # Remove duplicates while preserving order
    all_questions = list(dict.fromkeys(questions + special_questions))

    with open(questions_path, "w", encoding="utf-8") as f:
        json.dump({"questions": all_questions}, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(all_questions)} questions")
    print(f"Unique symptoms: {len(all_symptoms)}")


if __name__ == "__main__":
    generate_questions()