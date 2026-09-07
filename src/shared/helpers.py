"""Funcții ajutătoare reutilizabile"""


def normalize_text(text: str) -> str:
    """Normalizează textul pentru comparații"""
    replacements = {"ă": "a", "â": "a", "î": "i", "ș": "s", "ț": "t", " ": "_"}
    result = text.lower().strip()
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


def extract_symptom_from_question(question: str) -> str:
    """Extrage simptomul dintr-o întrebare"""
    symptom = question.replace("Aveți ", "").replace("?", "").strip()
    return normalize_text(symptom)