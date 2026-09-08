"""Fereastra principală a aplicației"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt

from src.business.services.disease_service import DiseaseService
from src.business.services.scoring_service import ScoringService
from src.data.repositories.symptom_repository import SymptomRepository
from src.shared.constants import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.disease_service = DiseaseService()
        self.scoring_service = ScoringService()
        self.symptom_repo = SymptomRepository()

        self.user_symptoms = []
        self.current_question_index = 0
        self.questions = []

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("🏥 HealthChecker")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Identifică posibile afecțiuni pe baza simptomelor")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        layout.addWidget(card)

        self.question_label = QLabel("Apăsați Start pentru a începe")
        self.question_label.setObjectName("question")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        card_layout.addWidget(self.question_label)

        self.start_btn = QPushButton("🚀 Start")
        self.start_btn.setObjectName("start_button")
        self.start_btn.clicked.connect(self.start_quiz)
        card_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)

        self.yes_btn = QPushButton("✓ Da")
        self.yes_btn.clicked.connect(lambda: self.answer_question(True))
        self.yes_btn.hide()
        card_layout.addWidget(self.yes_btn, alignment=Qt.AlignCenter)

        self.no_btn = QPushButton("✗ Nu")
        self.no_btn.setObjectName("no_button")
        self.no_btn.clicked.connect(lambda: self.answer_question(False))
        self.no_btn.hide()
        card_layout.addWidget(self.no_btn, alignment=Qt.AlignCenter)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel#title {
                color: #89b4fa;
                font-size: 28px;
                font-weight: bold;
            }
            QLabel#subtitle {
                color: #a6adc8;
                font-size: 14px;
            }
            QLabel#question {
                color: #cdd6f4;
                font-size: 20px;
                padding: 20px;
            }
            QFrame#card {
                background-color: #313244;
                border-radius: 12px;
                padding: 20px;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 30px;
                border-radius: 8px;
                min-width: 200px;
            }
            QPushButton:hover { background-color: #b4befe; }
            QPushButton#no_button {
                background-color: #f38ba8;
            }
            QPushButton#no_button:hover { background-color: #fab387; }
            QPushButton#start_button {
                background-color: #a6e3a1;
                font-size: 18px;
                padding: 15px 40px;
            }
        """)

    def start_quiz(self):
        self.user_symptoms = []
        self.current_question_index = 0
        self.questions = self.symptom_repo.get_questions()

        self.start_btn.hide()
        self.yes_btn.show()
        self.no_btn.show()
        self.show_question()

    def show_question(self):
        if self.current_question_index < len(self.questions):
            self.question_label.setText(self.questions[self.current_question_index])
        else:
            self.show_results()

    def answer_question(self, answer: bool):
        if answer and self.current_question_index < len(self.questions):
            from src.shared.helpers import extract_symptom_from_question
            question = self.questions[self.current_question_index]
            symptom = extract_symptom_from_question(question)
            self.user_symptoms.append(symptom)

        self.current_question_index += 1
        self.show_question()

    def show_results(self):
        self.yes_btn.hide()
        self.no_btn.hide()

        diseases = self.disease_service.get_all()
        results = self.scoring_service.get_top_matches(diseases, self.user_symptoms)

        if results:
            text = "📊 Rezultate posibile:\n\n"
            for i, (disease, score) in enumerate(results, 1):
                emoji = "🔴" if score > 70 else "🟡" if score > 40 else "🟢"
                text += f"{i}. {emoji} {disease.name} - {score:.0f}%\n"
                text += f"   Specialitate: {disease.specialty}\n\n"
            text += "\n⚠️ Aceste rezultate sunt doar orientative.\n"
            text += "Consultați întotdeauna un medic pentru diagnostic!"
        else:
            text = "Nu am găsit potriviri exacte.\n"
            text += "Vă recomandăm să consultați un medic generalist."

        self.question_label.setText(text)
        self.start_btn.setText("🔄 Reîncepe")
        self.start_btn.show()