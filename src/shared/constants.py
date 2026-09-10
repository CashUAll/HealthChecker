"""Global constants for the application"""

APP_NAME = "HealthChecker"
APP_VERSION = "0.1.0"

WINDOW_WIDTH = 850
WINDOW_HEIGHT = 720

MIN_SCORE_THRESHOLD = 10.0
MAX_RESULTS = 5

# Age groups for filtering
AGE_GROUPS = {
    "child": (0, 12),
    "teen": (13, 17),
    "adult": (18, 59),
    "elderly": (60, 120)
}

# Body map for symptom selection
BODY_REGIONS = {
    "head": {
        "label": "Head",
        "subregions": [
            {"id": "scalp", "label": "Scalp"},
            {"id": "forehead", "label": "Forehead"},
            {"id": "eyes", "label": "Eyes"},
            {"id": "nose", "label": "Nose"},
            {"id": "ears", "label": "Ears"},
            {"id": "face", "label": "Face"},
            {"id": "mouth", "label": "Mouth"},
            {"id": "jaw", "label": "Jaw"}
        ]
    },
    "neck": {
        "label": "Neck",
        "subregions": [
            {"id": "front_neck", "label": "Front"},
            {"id": "back_neck", "label": "Back"},
            {"id": "throat", "label": "Throat"}
        ]
    },
    "chest": {
        "label": "Chest",
        "subregions": [
            {"id": "upper_chest", "label": "Upper"},
            {"id": "lower_chest", "label": "Lower"},
            {"id": "breasts", "label": "Breasts"}
        ]
    },
    "abdomen": {
        "label": "Abdomen",
        "subregions": [
            {"id": "upper_abdomen", "label": "Upper"},
            {"id": "lower_abdomen", "label": "Lower"},
            {"id": "pelvis", "label": "Pelvis"}
        ]
    },
    "back": {
        "label": "Back",
        "subregions": [
            {"id": "upper_back", "label": "Upper"},
            {"id": "middle_back", "label": "Middle"},
            {"id": "lower_back", "label": "Lower"}
        ]
    },
    "arms": {
        "label": "Arms",
        "subregions": [
            {"id": "shoulders", "label": "Shoulders"},
            {"id": "upper_arms", "label": "Upper arms"},
            {"id": "elbows", "label": "Elbows"},
            {"id": "forearms", "label": "Forearms"},
            {"id": "wrists", "label": "Wrists"},
            {"id": "hands", "label": "Hands"}
        ]
    },
    "legs": {
        "label": "Legs",
        "subregions": [
            {"id": "hips", "label": "Hips"},
            {"id": "thighs", "label": "Thighs"},
            {"id": "knees", "label": "Knees"},
            {"id": "calves", "label": "Calves"},
            {"id": "ankles", "label": "Ankles"},
            {"id": "feet", "label": "Feet"}
        ]
    },
    "skin": {
        "label": "Skin",
        "subregions": [
            {"id": "general_skin", "label": "General"}
        ]
    },
    "general": {
        "label": "Whole body",
        "subregions": [
            {"id": "whole_body", "label": "Entire body"}
        ]
    }
}

# Mapping between sub-regions and symptoms (question keywords) - ENGLISH
REGION_SYMPTOMS = {
    # ============ HEAD ============
    "scalp": [
        "headache", "hair loss", "itchy scalp"
    ],
    "forehead": [
        "headache", "fever", "dizziness"
    ],
    "eyes": [
        "red eyes", "watery eyes", "blurred vision",
        "eye pain", "sensitivity to light"
    ],
    "nose": [
        "stuffy nose", "sneeze", "nosebleed", "nasal discharge",
        "loss of smell", "sinus pressure"
    ],
    "ears": [
        "ear pain", "hearing loss", "ringing in your ears", "ear discharge"
    ],
    "face": [
        "facial pain", "facial swelling"
    ],
    "mouth": [
        "sore throat", "difficulty swallowing", "hoarseness"
    ],
    "jaw": [
        "facial pain", "difficulty swallowing"
    ],

    # ============ NECK ============
    "front_neck": [
        "sore throat", "swollen lymph nodes", "difficulty swallowing",
        "hoarseness"
    ],
    "back_neck": [
        "sore throat", "stiff neck"
    ],
    "throat": [
        "sore throat", "difficulty swallowing", "hoarseness",
        "fever"
    ],

    # ============ CHEST ============
    "upper_chest": [
        "chest pain", "difficulty breathing", "cough",
        "palpitations"
    ],
    "lower_chest": [
        "chest pain", "nausea"
    ],
    "breasts": [],

    # ============ ABDOMEN ============
    "upper_abdomen": [
        "abdominal pain", "nausea", "bloating",
        "loss of appetite"
    ],
    "lower_abdomen": [
        "abdominal pain", "bloating", "constipation", "diarrhea"
    ],
    "pelvis": [
        "abdominal pain", "frequent urination"
    ],

    # ============ BACK ============
    "upper_back": [
        "back pain"
    ],
    "middle_back": [
        "back pain"
    ],
    "lower_back": [
        "back pain", "numbness", "tingling"
    ],

    # ============ ARMS ============
    "shoulders": [
        "shoulder pain", "limited movement"
    ],
    "upper_arms": [],
    "elbows": [],
    "forearms": [],
    "wrists": [],
    "hands": [
        "tingling", "numbness"
    ],

    # ============ LEGS ============
    "hips": [],
    "thighs": [],
    "knees": [
        "knee pain", "knee swelling"
    ],
    "calves": [],
    "ankles": [
        "ankle pain", "ankle swelling"
    ],
    "feet": [],

    # ============ SKIN ============
    "general_skin": [
        "skin rashes", "itchy skin", "dry skin",
        "acne", "blackheads", "skin cracks", "cysts",
        "hives", "skin redness", "skin lesions", "blisters",
        "peeling skin"
    ],

    # ============ WHOLE BODY ============
    "whole_body": [
        "fever", "tired", "weight loss", "night sweats",
        "chills", "muscle aches", "anxious", "depressed", "insomnia",
        "irritable", "excessive thirst", "frequent urination"
    ]
}

# Mapping between sub-regions and medical specialties
SUBREGION_SPECIALTIES = {
    "scalp": ["Dermatology", "Neurology"],
    "forehead": ["Neurology", "ENT"],
    "eyes": ["Ophthalmology"],
    "nose": ["ENT", "Allergy"],
    "ears": ["ENT"],
    "face": ["ENT", "Dermatology"],
    "mouth": ["ENT"],
    "jaw": ["ENT"],
    "front_neck": ["ENT", "Endocrinology"],
    "back_neck": ["Orthopedics", "Neurology"],
    "throat": ["ENT"],
    "upper_chest": ["Pulmonology", "Cardiology"],
    "lower_chest": ["Cardiology", "Gastroenterology"],
    "breasts": ["Oncology", "Gynecology"],
    "upper_abdomen": ["Gastroenterology"],
    "lower_abdomen": ["Gastroenterology"],
    "pelvis": ["Urology", "Gynecology"],
    "upper_back": ["Orthopedics"],
    "middle_back": ["Orthopedics"],
    "lower_back": ["Orthopedics", "Neurology"],
    "shoulders": ["Orthopedics"],
    "upper_arms": ["Orthopedics"],
    "elbows": ["Orthopedics"],
    "forearms": ["Orthopedics"],
    "wrists": ["Orthopedics"],
    "hands": ["Orthopedics", "Neurology"],
    "hips": ["Orthopedics", "Rheumatology"],
    "thighs": ["Orthopedics"],
    "knees": ["Orthopedics", "Rheumatology"],
    "calves": ["Orthopedics"],
    "ankles": ["Orthopedics"],
    "feet": ["Orthopedics"],
    "general_skin": ["Dermatology", "Allergy"],
    "whole_body": ["General", "Infectious Diseases", "Hematology"],
}

# Mapping between sub-regions and medical specialties (only existing in diseases.json)
SUBREGION_SPECIALTIES = {
    # Head
    "scalp": ["Dermatology", "Neurology"],
    "forehead": ["Neurology"],
    "eyes": ["Ophthalmology"],
    "nose": ["Allergy"],
    "ears": ["Neurology"],
    "face": ["Dermatology"],
    "mouth": ["Gastroenterology"],
    "jaw": ["Neurology"],

    # Neck
    "front_neck": ["Endocrinology"],
    "back_neck": ["Orthopedics", "Neurology"],
    "throat": ["Pulmonology"],

    # Chest
    "upper_chest": ["Pulmonology", "Cardiology"],
    "lower_chest": ["Cardiology", "Gastroenterology"],
    "breasts": ["Oncology"],

    # Abdomen
    "upper_abdomen": ["Gastroenterology"],
    "lower_abdomen": ["Gastroenterology"],
    "pelvis": ["Urology"],

    # Back
    "upper_back": ["Orthopedics"],
    "middle_back": ["Orthopedics"],
    "lower_back": ["Orthopedics", "Neurology"],

    # Arms
    "shoulders": ["Orthopedics"],
    "upper_arms": ["Orthopedics"],
    "elbows": ["Orthopedics"],
    "forearms": ["Orthopedics"],
    "wrists": ["Orthopedics"],
    "hands": ["Orthopedics", "Neurology"],

    # Legs
    "hips": ["Orthopedics"],
    "thighs": ["Orthopedics"],
    "knees": ["Orthopedics"],
    "calves": ["Orthopedics"],
    "ankles": ["Orthopedics"],
    "feet": ["Orthopedics"],

    # Skin
    "general_skin": ["Dermatology", "Allergy"],

    # General
    "whole_body": ["Infectious Diseases", "Hematology", "Cardiology"],
}