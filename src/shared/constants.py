"""Constante globale ale aplicației"""

APP_NAME = "HealthChecker"
APP_VERSION = "0.1.0"

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 550

MIN_SCORE_THRESHOLD = 10.0
MAX_RESULTS = 5

# Grupe de vârstă pentru filtrare
AGE_GROUPS = {
    "child": (0, 12),
    "teen": (13, 17),
    "adult": (18, 59),
    "elderly": (60, 120)
}