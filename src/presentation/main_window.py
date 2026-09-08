"""Fereastra principală a aplicației"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QLineEdit, QProgressBar
)
from PySide6.QtCore import Qt

from src.business.services.disease_service import DiseaseService
from src.business.services.scoring_service import ScoringService
from src.business.services.question_selector import QuestionSelector
from src.data.repositories.symptom_repository import SymptomRepository
from src.shared.constants import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Servicii
        self.disease_service = DiseaseService()
        self.scoring_service = ScoringService()
        self.symptom_repo = SymptomRepository()

        # Selector de întrebări (Akinator)
        self.question_selector = None

        # Stare utilizator
        self.user_age = 0
        self.user_sex = None
        self.user_symptoms = []
        self.current_question_index = 0
        self.questions = []

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        """Configurează interfața"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Titlu
        title = QLabel("🏥 HealthChecker")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitlu
        subtitle = QLabel("Identifică posibile afecțiuni pe baza simptomelor")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Card
        card = QFrame()
        card.setObjectName("card")
        self.card_layout = QVBoxLayout(card)
        self.card_layout.setSpacing(15)
        layout.addWidget(card)

        # ---------- ECRAIN DEMOGRAFIC ----------
        self.demographic_widget = QWidget()
        demo_layout = QVBoxLayout(self.demographic_widget)
        demo_layout.setSpacing(10)

        demo_title = QLabel("📋 Să începem! Spune-ne câteva detalii.")
        demo_title.setObjectName("question")
        demo_title.setAlignment(Qt.AlignCenter)
        demo_layout.addWidget(demo_title)

        # Câmp pentru vârstă
        age_label = QLabel("Vârsta:")
        age_label.setStyleSheet("color: #cdd6f4; font-size: 16px;")
        demo_layout.addWidget(age_label)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Exemplu: 25")
        self.age_input.setStyleSheet("""
            padding: 10px;
            font-size: 16px;
            border-radius: 8px;
            background-color: #1e1e2e;
            color: #cdd6f4;
            border: 1px solid #313244;
        """)
        demo_layout.addWidget(self.age_input)

        # Selector pentru sex
        sex_label = QLabel("Sexul:")
        sex_label.setStyleSheet("color: #cdd6f4; font-size: 16px;")
        demo_layout.addWidget(sex_label)

        sex_layout = QHBoxLayout()
        self.male_btn = QPushButton("🧑 Bărbat")
        self.male_btn.setObjectName("male_button")
        self.male_btn.setCheckable(True)
        self.male_btn.clicked.connect(lambda: self.set_sex('male'))

        self.female_btn = QPushButton("👩 Femeie")
        self.female_btn.setObjectName("female_button")
        self.female_btn.setCheckable(True)
        self.female_btn.clicked.connect(lambda: self.set_sex('female'))

        sex_layout.addWidget(self.male_btn)
        sex_layout.addWidget(self.female_btn)
        demo_layout.addLayout(sex_layout)

        # Buton de confirmare
        self.confirm_demo_btn = QPushButton("✅ Continuă")
        self.confirm_demo_btn.setObjectName("start_button")
        self.confirm_demo_btn.clicked.connect(self.start_quiz)
        demo_layout.addWidget(self.confirm_demo_btn)

        self.card_layout.addWidget(self.demographic_widget)

        # ---------- ÎNTREBARE ----------
        self.question_widget = QWidget()
        self.question_widget.hide()
        question_layout = QVBoxLayout(self.question_widget)
        question_layout.setSpacing(15)

        # Bară de progres
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1e1e2e;
                border-radius: 8px;
                height: 12px;
                text-align: center;
                color: #cdd6f4;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 8px;
            }
        """)
        question_layout.addWidget(self.progress_bar)

        self.question_label = QLabel("Apăsați Start pentru a începe")
        self.question_label.setObjectName("question")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        question_layout.addWidget(self.question_label)

        # Butoane
        self.start_btn = QPushButton("🚀 Start")
        self.start_btn.setObjectName("start_button")
        self.start_btn.clicked.connect(self.start_quiz)
        question_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)

        self.yes_btn = QPushButton("✅ Da")
        self.yes_btn.setObjectName("yes_button")
        self.yes_btn.clicked.connect(lambda: self.answer_question(True))
        self.yes_btn.hide()
        question_layout.addWidget(self.yes_btn, alignment=Qt.AlignCenter)

        self.no_btn = QPushButton("❌ Nu")
        self.no_btn.setObjectName("no_button")
        self.no_btn.clicked.connect(lambda: self.answer_question(False))
        self.no_btn.hide()
        question_layout.addWidget(self.no_btn, alignment=Qt.AlignCenter)

        self.card_layout.addWidget(self.question_widget)

    def apply_styles(self):
        """Aplică stilurile"""
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
                padding: 15px;
                background-color: #1e1e2e;
                border-radius: 10px;
            }
            QFrame#card {
                background-color: #313244;
                border-radius: 15px;
                padding: 25px;
            }
            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                font-size: 16px;
                font-weight: bold;
                padding: 14px 30px;
                border-radius: 10px;
                min-width: 180px;
                border: 2px solid #45475a;
            }
            QPushButton:hover {
                background-color: #585b70;
                border-color: #585b70;
            }
            QPushButton#yes_button {
                background-color: #a6e3a1;
                color: #1e1e2e;
                border-color: #a6e3a1;
                font-size: 18px;
                padding: 16px 40px;
            }
            QPushButton#yes_button:hover {
                background-color: #89b4fa;
                border-color: #89b4fa;
            }
            QPushButton#no_button {
                background-color: #f38ba8;
                color: #1e1e2e;
                border-color: #f38ba8;
                font-size: 18px;
                padding: 16px 40px;
            }
            QPushButton#no_button:hover {
                background-color: #fab387;
                border-color: #fab387;
            }
            QPushButton#start_button {
                background-color: #a6e3a1;
                color: #1e1e2e;
                font-size: 20px;
                padding: 18px 50px;
                border-color: #a6e3a1;
            }
            QPushButton#start_button:hover {
                background-color: #89b4fa;
                border-color: #89b4fa;
            }
            QPushButton#male_button {
                background-color: #45475a;
                color: #cdd6f4;
                font-size: 16px;
                padding: 14px 30px;
                border-radius: 10px;
                min-width: 150px;
                border: 2px solid #45475a;
            }
            QPushButton#male_button:hover {
                background-color: #585b70;
                border-color: #585b70;
            }
            QPushButton#female_button {
                background-color: #45475a;
                color: #cdd6f4;
                font-size: 16px;
                padding: 14px 30px;
                border-radius: 10px;
                min-width: 150px;
                border: 2px solid #45475a;
            }
            QPushButton#female_button:hover {
                background-color: #585b70;
                border-color: #585b70;
            }
            QLineEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #89b4fa;
            }
            QProgressBar {
                background-color: #1e1e2e;
                border-radius: 10px;
                height: 14px;
                text-align: center;
                color: #cdd6f4;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 10px;
            }
        """)

    def set_sex(self, sex):
        """Setează sexul utilizatorului și evidențiază butonul selectat."""
        self.user_sex = sex
        # Resetare stiluri
        self.male_btn.setStyleSheet("")
        self.female_btn.setStyleSheet("")
        # Setează stilurile pentru butonul selectat
        if sex == 'male':
            self.male_btn.setStyleSheet("""
                background-color: #89b4fa;
                color: #1e1e2e;
                border: 2px solid #89b4fa;
                font-weight: bold;
            """)
            self.female_btn.setStyleSheet("""
                background-color: #45475a;
                color: #cdd6f4;
                border: 2px solid #45475a;
            """)
        else:
            self.female_btn.setStyleSheet("""
                background-color: #f38ba8;
                color: #1e1e2e;
                border: 2px solid #f38ba8;
                font-weight: bold;
            """)
            self.male_btn.setStyleSheet("""
                background-color: #45475a;
                color: #cdd6f4;
                border: 2px solid #45475a;
            """)

    def start_quiz(self):
        """Pornește quiz-ul după confirmarea datelor demografice."""
        # Validare vârstă
        try:
            self.user_age = int(self.age_input.text())
            if self.user_age < 1 or self.user_age > 120:
                self.question_label.setText("⚠️ Vârsta trebuie să fie între 1 și 120.")
                return
        except ValueError:
            self.question_label.setText("⚠️ Te rog să introduci o vârstă validă (număr).")
            return

        # Validare sex
        if not self.user_sex:
            self.question_label.setText("⚠️ Te rog să selectezi sexul.")
            return

        # Setează datele demografice în serviciu
        self.disease_service.set_user_demographics(self.user_age, self.user_sex)

        # Mesaj de confirmare
        sex_text = "bărbat" if self.user_sex == 'male' else "femeie"
        self.question_label.setText(f"✅ Vârsta: {self.user_age} ani, Sex: {sex_text}\n\nÎncepem evaluarea...")

        # Ascunde ecranul demografic și pornește quiz-ul
        self.demographic_widget.hide()
        self.question_widget.show()

        self.user_symptoms = []
        self.current_question_index = 0
        self.questions = self.symptom_repo.get_questions()

        # Inițializează selectorul Akinator
        self.question_selector = QuestionSelector(self.questions)
        self.question_selector.reset()

        # Resetează bara de progres
        self.progress_bar.setValue(0)

        self.start_btn.hide()
        self.yes_btn.show()
        self.no_btn.show()
        self.show_question()

    def show_question(self):
        """Afișează următoarea întrebare (folosind algoritmul Akinator)"""
        # Obține toate bolile relevante (filtrate după vârstă și sex)
        diseases = self.disease_service.get_all()

        # Alege următoarea întrebare inteligent
        next_question = self.question_selector.select_next_question(
            diseases, self.user_symptoms
        )

        if next_question:
            self.question_label.setText(next_question)
        else:
            self.show_results()

        # Actualizează bara de progres
        total = len(self.questions)
        answered = len(self.question_selector.asked_questions)
        progress = int((answered / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(min(progress, 100))

    def answer_question(self, answer: bool):
        """Procesează răspunsul"""
        # Obține întrebarea curentă
        current_question = self.question_label.text()

        if answer:
            from src.shared.helpers import extract_symptom_from_question
            symptom = extract_symptom_from_question(current_question)
            if symptom not in self.user_symptoms:
                self.user_symptoms.append(symptom)

        # Marchează întrebarea ca fiind pusă
        if current_question in self.questions:
            self.question_selector.asked_questions.add(current_question)

        self.show_question()

    def show_results(self):
        """Afișează rezultatele"""
        self.yes_btn.hide()
        self.no_btn.hide()
        self.progress_bar.setValue(100)

        diseases = self.disease_service.get_all()
        results = self.scoring_service.get_top_matches(diseases, self.user_symptoms)

        if results:
            text = "📊 Rezultate posibile:\n\n"
            for i, (disease, score) in enumerate(results, 1):
                emoji = "🔴" if score > 70 else "🟡" if score > 40 else "🟢"
                text += f"{i}. {emoji} {disease.name} - {score:.0f}%\n"
                text += f"   Specialitate: {disease.specialty}\n\n"
                if hasattr(disease, 'treatments') and disease.treatments:
                    text += f"   💊 Tratamente sugerate:\n"
                    for treatment in disease.treatments[:2]:
                        text += f"   • {treatment}\n"
                    text += "\n"
                if hasattr(disease, 'recommendations') and disease.recommendations:
                    text += f"   📋 Recomandări:\n"
                    for rec in disease.recommendations[:2]:
                        text += f"   • {rec}\n"
                    text += "\n"
            text += "⚠️ Aceste rezultate sunt doar orientative.\n"
            text += "Consultați întotdeauna un medic pentru diagnostic!"
        else:
            text = "Nu am găsit potriviri exacte.\n"
            text += "Vă recomandăm să consultați un medic generalist."

        self.question_label.setText(text)
        self.start_btn.setText("🔄 Reîncepe")
        self.start_btn.show()