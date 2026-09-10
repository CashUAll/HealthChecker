"""Main window for HealthChecker application"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QLineEdit, QProgressBar, QScrollArea,
    QSizePolicy
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

from src.business.services.disease_service import DiseaseService
from src.business.services.scoring_service import ScoringService
from src.business.services.question_selector import QuestionSelector
from src.data.repositories.symptom_repository import SymptomRepository
from src.shared.constants import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, BODY_REGIONS, SUBREGION_SPECIALTIES
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.disease_service = DiseaseService()
        self.scoring_service = ScoringService()
        self.symptom_repo = SymptomRepository()
        self.question_selector = None

        # User state
        self.user_age = 0
        self.user_sex = None
        self.user_symptoms = []
        self.current_question_index = 0
        self.questions = []
        self.selected_region = None
        self.selected_subregion = None

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(18)

        # Title
        title = QLabel("🏥 HealthChecker")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Identify possible conditions based on symptoms")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # ---------- SCROLL AREA FOR CARD CONTENT ----------
        self.scroll_card = QScrollArea()
        self.scroll_card.setWidgetResizable(True)
        self.scroll_card.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #1e1e2e;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #89b4fa;
                border-radius: 5px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover { background-color: #b4befe; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        # Card container
        card = QFrame()
        card.setObjectName("card")
        self.card_layout = QVBoxLayout(card)
        self.card_layout.setSpacing(18)
        self.card_layout.setContentsMargins(25, 25, 25, 25)

        self.scroll_card.setWidget(card)
        layout.addWidget(self.scroll_card)

        # ---------- DEMOGRAPHIC ----------
        self.demographic_widget = QWidget()
        demo_layout = QVBoxLayout(self.demographic_widget)
        demo_layout.setSpacing(14)

        demo_title = QLabel("👋 Tell us about yourself")
        demo_title.setObjectName("demo_title")
        demo_title.setAlignment(Qt.AlignCenter)
        demo_layout.addWidget(demo_title)

        demo_instructions = QLabel(
            "Enter your age and sex to improve accuracy."
        )
        demo_instructions.setAlignment(Qt.AlignCenter)
        demo_instructions.setWordWrap(True)
        demo_instructions.setStyleSheet("color: #a6adc8; font-size: 15px;")
        demo_layout.addWidget(demo_instructions)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #45475a; max-height: 1px;")
        demo_layout.addWidget(line)

        age_label = QLabel("📅 Age:")
        age_label.setStyleSheet("color: #cdd6f4; font-size: 17px; font-weight: bold;")
        demo_layout.addWidget(age_label)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Ex: 25")
        demo_layout.addWidget(self.age_input)

        sex_label = QLabel("👤 Sex:")
        sex_label.setStyleSheet("color: #cdd6f4; font-size: 17px; font-weight: bold;")
        demo_layout.addWidget(sex_label)

        sex_layout = QHBoxLayout()
        self.male_btn = QPushButton("Male")
        self.male_btn.setObjectName("male_button")
        self.male_btn.setCheckable(True)
        self.male_btn.clicked.connect(lambda: self.set_sex('male'))

        self.female_btn = QPushButton("Female")
        self.female_btn.setObjectName("female_button")
        self.female_btn.setCheckable(True)
        self.female_btn.clicked.connect(lambda: self.set_sex('female'))

        sex_layout.addWidget(self.male_btn)
        sex_layout.addWidget(self.female_btn)
        sex_layout.addStretch()
        demo_layout.addLayout(sex_layout)

        self.confirm_demo_btn = QPushButton("🚀 Continue to body selection")
        self.confirm_demo_btn.setObjectName("start_button")
        self.confirm_demo_btn.clicked.connect(self.confirm_demographics)
        demo_layout.addWidget(self.confirm_demo_btn)

        disclaimer = QLabel("ℹ️ Results are informational. Always consult a doctor.")
        disclaimer.setAlignment(Qt.AlignCenter)
        disclaimer.setStyleSheet("color: #a6adc8; font-size: 12px; padding: 6px;")
        demo_layout.addWidget(disclaimer)

        self.card_layout.addWidget(self.demographic_widget)

        # ---------- REGION SELECTION ----------
        self.region_widget = QWidget()
        self.region_widget.hide()
        region_layout = QVBoxLayout(self.region_widget)
        region_layout.setSpacing(15)

        self.back_to_main_from_regions = QPushButton("🏠 Main Menu")
        self.back_to_main_from_regions.clicked.connect(self.go_to_main_menu)
        self.back_to_main_from_regions.setMinimumHeight(40)
        self.back_to_main_from_regions.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: #1e1e2e;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 8px;
                border: 2px solid #f38ba8;
            }
            QPushButton:hover {
                background-color: #fab387;
                border-color: #fab387;
            }
        """)
        region_layout.addWidget(self.back_to_main_from_regions)

        region_title = QLabel("📍 Select the area that hurts:")
        region_title.setObjectName("question")
        region_title.setAlignment(Qt.AlignCenter)
        region_layout.addWidget(region_title)

        region_grid = QGridLayout()
        region_grid.setSpacing(12)

        regions_with_icons = [
            ("head", "🧠", "Head"),
            ("neck", "🦴", "Neck"),
            ("chest", "❤️", "Chest"),
            ("abdomen", "🫀", "Abdomen"),
            ("back", "🔙", "Back"),
            ("arms", "💪", "Arms"),
            ("legs", "🦵", "Legs"),
            ("skin", "🧴", "Skin"),
            ("general", "🔵", "Whole body"),
        ]

        row, col = 0, 0
        for region_id, icon, label in regions_with_icons:
            btn = QPushButton(f"{icon} {label}")
            btn.clicked.connect(lambda checked, r=region_id: self.select_region(r))
            btn.setMinimumHeight(55)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #45475a;
                    color: #cdd6f4;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 15px;
                    border-radius: 10px;
                    border: 2px solid #45475a;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #585b70;
                    border-color: #585b70;
                }
            """)
            region_grid.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        region_layout.addLayout(region_grid)
        self.card_layout.addWidget(self.region_widget)

        # ---------- SUB-REGION SELECTION ----------
        self.subregion_widget = QWidget()
        self.subregion_widget.hide()
        subregion_layout = QVBoxLayout(self.subregion_widget)
        subregion_layout.setSpacing(10)

        self.back_to_main_from_subregions = QPushButton("🏠 Main Menu")
        self.back_to_main_from_subregions.clicked.connect(self.go_to_main_menu)
        self.back_to_main_from_subregions.setMinimumHeight(40)
        self.back_to_main_from_subregions.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: #1e1e2e;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 8px;
                border: 2px solid #f38ba8;
            }
            QPushButton:hover {
                background-color: #fab387;
                border-color: #fab387;
            }
        """)
        subregion_layout.addWidget(self.back_to_main_from_subregions)

        self.subregion_title = QLabel("Choose sub-region:")
        self.subregion_title.setObjectName("question")
        self.subregion_title.setAlignment(Qt.AlignCenter)
        subregion_layout.addWidget(self.subregion_title)

        self.subregion_buttons_layout = QVBoxLayout()
        subregion_layout.addLayout(self.subregion_buttons_layout)

        self.back_to_regions_btn = QPushButton("⬅ Back to regions")
        self.back_to_regions_btn.clicked.connect(self.show_region_selection)
        self.back_to_regions_btn.setMinimumHeight(40)
        subregion_layout.addWidget(self.back_to_regions_btn)

        self.card_layout.addWidget(self.subregion_widget)

        # ---------- QUESTIONS ----------
        self.question_widget = QWidget()
        self.question_widget.hide()
        self.question_widget.setMinimumHeight(400)
        self.question_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        question_layout = QVBoxLayout(self.question_widget)
        question_layout.setSpacing(12)

        self.back_to_main_from_questions = QPushButton("🏠 Main Menu")
        self.back_to_main_from_questions.clicked.connect(self.go_to_main_menu)
        self.back_to_main_from_questions.setMinimumHeight(40)
        self.back_to_main_from_questions.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: #1e1e2e;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 8px;
                border: 2px solid #f38ba8;
            }
            QPushButton:hover {
                background-color: #fab387;
                border-color: #fab387;
            }
        """)
        question_layout.addWidget(self.back_to_main_from_questions)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        question_layout.addWidget(self.progress_bar)

        self.scroll_question_area = QScrollArea()
        self.scroll_question_area.setWidgetResizable(True)
        self.scroll_question_area.setMinimumHeight(200)
        self.scroll_question_area.setStyleSheet("""
            QScrollArea { background-color: transparent; border: none; }
            QScrollBar:vertical {
                background-color: #1e1e2e;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #89b4fa;
                border-radius: 5px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover { background-color: #b4befe; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self.question_label = QLabel("Press 'Start' to begin")
        self.question_label.setObjectName("question")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.scroll_question_area.setWidget(self.question_label)
        question_layout.addWidget(self.scroll_question_area)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.yes_btn = QPushButton("✅ Yes")
        self.yes_btn.setObjectName("yes_button")
        self.yes_btn.clicked.connect(lambda: self.answer_question(True))
        self.yes_btn.hide()

        self.no_btn = QPushButton("❌ No")
        self.no_btn.setObjectName("no_button")
        self.no_btn.clicked.connect(lambda: self.answer_question(False))
        self.no_btn.hide()

        self.skip_btn = QPushButton("❓ I don't know")
        self.skip_btn.setObjectName("skip_button")
        self.skip_btn.clicked.connect(lambda: self.answer_question(None))
        self.skip_btn.hide()

        btn_layout.addWidget(self.yes_btn)
        btn_layout.addWidget(self.skip_btn)
        btn_layout.addWidget(self.no_btn)
        btn_layout.addStretch()
        question_layout.addLayout(btn_layout)

        self.back_to_regions_from_questions = QPushButton("⬅ Back to regions")
        self.back_to_regions_from_questions.clicked.connect(self.go_back_to_regions)
        self.back_to_regions_from_questions.setMinimumHeight(40)
        self.back_to_regions_from_questions.hide()
        question_layout.addWidget(self.back_to_regions_from_questions, alignment=Qt.AlignCenter)

        self.start_btn = QPushButton("🚀 Start evaluation")
        self.start_btn.setObjectName("start_button")
        self.start_btn.clicked.connect(self.restart_app)
        question_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)

        self.card_layout.addWidget(self.question_widget)

        self.scroll_animation = QPropertyAnimation(self.scroll_question_area.verticalScrollBar(), b"value")
        self.scroll_animation.setDuration(300)
        self.scroll_animation.setEasingCurve(QEasingCurve.OutCubic)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel#title { color: #89b4fa; font-size: 28px; font-weight: bold; }
            QLabel#subtitle { color: #a6adc8; font-size: 14px; }
            QLabel#question {
                color: #cdd6f4;
                font-size: 22px;
                padding: 25px;
                background-color: #1e1e2e;
                border-radius: 12px;
                line-height: 1.8;
                min-height: 120px;
                border: 1px solid #45475a;
            }
            QLabel#demo_title { color: #89b4fa; font-size: 24px; font-weight: bold; }
            QFrame#card {
                background-color: #313244;
                border-radius: 15px;
                padding: 5px;
            }

            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 10px;
                min-width: 150px;
                border: 2px solid #45475a;
            }
            QPushButton:hover { background-color: #585b70; border-color: #585b70; }

            QPushButton#yes_button {
                background-color: #a6e3a1;
                color: #1e1e2e;
                border-color: #a6e3a1;
                font-size: 18px;
                padding: 14px 35px;
            }
            QPushButton#yes_button:hover { background-color: #89b4fa; border-color: #89b4fa; }

            QPushButton#no_button {
                background-color: #f38ba8;
                color: #1e1e2e;
                border-color: #f38ba8;
                font-size: 18px;
                padding: 14px 35px;
            }
            QPushButton#no_button:hover { background-color: #fab387; border-color: #fab387; }

            QPushButton#skip_button {
                background-color: #f9e2af;
                color: #1e1e2e;
                border-color: #f9e2af;
                font-size: 18px;
                padding: 14px 35px;
            }
            QPushButton#skip_button:hover { background-color: #89b4fa; border-color: #89b4fa; }

            QPushButton#start_button {
                background-color: #a6e3a1;
                color: #1e1e2e;
                font-size: 20px;
                padding: 16px 50px;
                border-color: #a6e3a1;
            }
            QPushButton#start_button:hover { background-color: #89b4fa; border-color: #89b4fa; }

            QPushButton#male_button {
                background-color: #45475a;
                color: #cdd6f4;
                font-size: 16px;
                padding: 12px 30px;
                border-radius: 10px;
                min-width: 120px;
                border: 2px solid #45475a;
            }
            QPushButton#male_button:hover { background-color: #585b70; border-color: #585b70; }

            QPushButton#female_button {
                background-color: #45475a;
                color: #cdd6f4;
                font-size: 16px;
                padding: 12px 30px;
                border-radius: 10px;
                min-width: 120px;
                border: 2px solid #45475a;
            }
            QPushButton#female_button:hover { background-color: #585b70; border-color: #585b70; }

            QLineEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
            }
            QLineEdit:focus { border-color: #89b4fa; }

            QProgressBar {
                background-color: #1e1e2e;
                border-radius: 8px;
                height: 18px;
                text-align: center;
                color: #cdd6f4;
                font-size: 12px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 8px;
            }
        """)

    # ---------- NAVIGATION ----------
    def go_to_main_menu(self):
        self.question_widget.hide()
        self.region_widget.hide()
        self.subregion_widget.hide()
        self.demographic_widget.show()
        self.scroll_card.verticalScrollBar().setValue(0)

    def go_back_to_regions(self):
        self.question_widget.hide()
        self.region_widget.show()
        self.subregion_widget.hide()
        self.scroll_card.verticalScrollBar().setValue(0)

    # ---------- DEMOGRAPHIC ----------
    def confirm_demographics(self):
        try:
            self.user_age = int(self.age_input.text())
            if self.user_age < 1 or self.user_age > 120:
                self.question_label.setText("⚠️ Age must be between 1 and 120.")
                return
        except ValueError:
            self.question_label.setText("⚠️ Please enter a valid age (number).")
            return

        if not self.user_sex:
            self.question_label.setText("⚠️ Please select your sex.")
            return

        self.disease_service.set_user_demographics(self.user_age, self.user_sex)
        self.demographic_widget.hide()
        self.region_widget.show()

    def set_sex(self, sex):
        self.user_sex = sex
        self.male_btn.setStyleSheet("")
        self.female_btn.setStyleSheet("")
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

    # ---------- REGION ----------
    def show_region_selection(self):
        self.region_widget.show()
        self.subregion_widget.hide()
        self.question_widget.hide()

    def select_region(self, region_id: str):
        self.selected_region = region_id
        region_data = BODY_REGIONS[region_id]
        subregions = region_data["subregions"]

        if region_id == "skin" or region_id == "general":
            self.start_quiz_for_subregion(subregions[0]["id"])
        elif len(subregions) > 1:
            self.show_subregions(subregions)
        else:
            self.start_quiz_for_subregion(subregions[0]["id"])

    def show_subregions(self, subregions):
        while self.subregion_buttons_layout.count():
            item = self.subregion_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                sub_layout = item.layout()
                while sub_layout.count():
                    sub_item = sub_layout.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                sub_layout.deleteLater()

        sub_grid = QGridLayout()
        sub_grid.setSpacing(10)

        row, col = 0, 0
        for sub in subregions:
            btn = QPushButton(sub["label"])
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, s=sub["id"]: self.start_quiz_for_subregion(s))
            sub_grid.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        self.subregion_buttons_layout.addLayout(sub_grid)
        self.region_widget.hide()
        self.subregion_widget.show()

    # ---------- QUIZ ----------
    def start_quiz_for_subregion(self, subregion_id: str):
        """Start the quiz for a specific sub-region with filtered diseases"""
        from src.shared.constants import SUBREGION_SPECIALTIES

        self.selected_subregion = subregion_id
        self.subregion_widget.hide()
        self.question_widget.show()

        self.question_widget.setMinimumHeight(400)
        self.question_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.back_to_regions_from_questions.show()

        self.user_symptoms = []
        self.current_question_index = 0

        # Get the specialties for this sub-region
        relevant_specialties = SUBREGION_SPECIALTIES.get(subregion_id, [])

        # Filter diseases by specialty
        all_diseases = self.disease_service.get_all()
        filtered_diseases = []

        for disease in all_diseases:
            if disease.specialty in relevant_specialties:
                filtered_diseases.append(disease)
            elif hasattr(disease, 'category') and disease.category in relevant_specialties:
                filtered_diseases.append(disease)

        # If no diseases found, use all
        if not filtered_diseases:
            filtered_diseases = all_diseases

        # Extract unique symptoms from filtered diseases
        unique_symptoms = set()
        for disease in filtered_diseases:
            for symptom in disease.symptoms.keys():
                unique_symptoms.add(symptom)

        # Generate questions from these symptoms
        if unique_symptoms:
            questions = []
            for symptom in sorted(unique_symptoms):
                readable = symptom.replace("_", " ")
                questions.append(f"Do you have {readable}?")
            self.questions = questions
        else:
            self.questions = self.symptom_repo.get_questions()

        if len(self.questions) > 30:
            self.questions = self.questions[:30]

        region_label = f"🔍 Symptoms for {subregion_id.replace('_', ' ').title()}"

        self.question_label.setText(
            f"{region_label}\n"
            f"📋 {len(self.questions)} questions found.\n"
            f"Answer Yes, No or I don't know."
        )

        self.question_selector = QuestionSelector(self.questions)
        self.question_selector.reset()

        self.progress_bar.setValue(0)

        self.start_btn.hide()
        self.yes_btn.show()
        self.no_btn.show()
        self.skip_btn.show()

        QTimer.singleShot(1000, self.show_question)

    def show_question(self):
        diseases = self.disease_service.get_all()
        next_question = self.question_selector.select_next_question(
            diseases, self.user_symptoms
        )

        if next_question:
            self.question_label.setText(next_question)
        else:
            self.show_results()

        total = len(self.questions)
        answered = len(self.question_selector.asked_questions)
        progress = int((answered / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(min(progress, 100))

        self.scroll_question_area.verticalScrollBar().setValue(0)

    def answer_question(self, answer: bool):
        current_question = self.question_label.text()

        if answer is True:
            from src.shared.helpers import extract_symptom_from_question
            symptom = extract_symptom_from_question(current_question)
            if symptom not in self.user_symptoms:
                self.user_symptoms.append(symptom)

        if current_question in self.questions:
            self.question_selector.asked_questions.add(current_question)

        self.show_question()

    def show_results(self):
        self.yes_btn.hide()
        self.no_btn.hide()
        self.skip_btn.hide()
        self.progress_bar.setValue(100)

        diseases = self.disease_service.get_all()
        results = self.scoring_service.get_top_matches(diseases, self.user_symptoms)

        if results:
            text = "📊 POSSIBLE RESULTS\n"
            text += "═" * 45 + "\n\n"

            for i, (disease, score) in enumerate(results, 1):
                if score > 70:
                    emoji = "🔴"
                    nivel = "HIGH PROBABILITY"
                elif score > 40:
                    emoji = "🟡"
                    nivel = "MODERATE PROBABILITY"
                else:
                    emoji = "🟢"
                    nivel = "LOW PROBABILITY"

                text += f"{emoji} {i}. {disease.name.upper()}\n"
                text += f"   Score: {score:.0f}% - {nivel}\n"
                text += f"   Specialty: {disease.specialty.upper()}\n"

                if hasattr(disease, 'treatments') and disease.treatments:
                    text += f"\n   💊 TREATMENTS & MEDICATIONS:\n"
                    for treatment in disease.treatments[:4]:
                        text += f"   • {treatment}\n"

                if hasattr(disease, 'recommendations') and disease.recommendations:
                    text += f"\n   📋 RECOMMENDATIONS:\n"
                    for rec in disease.recommendations[:3]:
                        text += f"   • {rec}\n"

                text += "\n" + "─" * 40 + "\n\n"

            text += "═" * 45 + "\n"
            text += "⚠️ ATTENTION: These results are INFORMATIONAL only!\n"
            text += "📞 Always consult a doctor for a proper diagnosis.\n"
            text += "🚨 In case of emergency, call 112!"
        else:
            text = "🔍 No exact matches found.\n\n"
            text += "📋 We recommend consulting a general practitioner.\n"
            text += "📞 They can refer you to the right specialist."

        self.question_label.setText(text)

        self.scroll_animation.setStartValue(self.scroll_question_area.verticalScrollBar().value())
        self.scroll_animation.setEndValue(0)
        self.scroll_animation.start()

        self.start_btn.setText("🔄 Restart")
        self.start_btn.show()

    # ---------- RESTART ----------
    def restart_app(self):
        self.question_widget.hide()
        self.region_widget.hide()
        self.subregion_widget.hide()
        self.demographic_widget.show()

        self.user_age = 0
        self.user_sex = None
        self.user_symptoms = []
        self.current_question_index = 0
        self.questions = []
        self.selected_region = None
        self.selected_subregion = None
        self.question_selector = None

        self.age_input.clear()
        self.male_btn.setStyleSheet("")
        self.female_btn.setStyleSheet("")
        self.male_btn.setChecked(False)
        self.female_btn.setChecked(False)

        self.progress_bar.setValue(0)
        self.question_label.setText("Press 'Start' to begin")
        self.start_btn.setText("🚀 Start evaluation")
        self.start_btn.show()

        self.scroll_card.verticalScrollBar().setValue(0)