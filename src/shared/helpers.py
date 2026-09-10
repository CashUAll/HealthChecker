"""Reusable helper functions"""


def normalize_text(text: str) -> str:
    """Normalize text for comparisons"""
    replacements = {"ă": "a", "â": "a", "î": "i", "ș": "s", "ț": "t", " ": "_"}
    result = text.lower().strip()
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


def extract_symptom_from_question(question: str) -> str:
    """Extract symptom from a question"""
    symptom = question.replace("Do you have ", "").replace("Do you feel ", "")
    symptom = symptom.replace("Aveți ", "").replace("?", "").strip()
    return normalize_text(symptom)