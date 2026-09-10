#!/usr/bin/env python3
"""Generate 2000 common diseases for HealthChecker."""
import json
import random
from pathlib import Path

DISEASE_BASES = [
    "Influenza", "Common Cold", "COVID-19", "Pharyngitis", "Laryngitis",
    "Sinusitis", "Otitis Media", "Bronchitis", "Pneumonia", "Tuberculosis",
    "Strep Throat", "Mononucleosis", "Chickenpox", "Measles", "Mumps",
    "Hepatitis A", "Hepatitis B", "Hepatitis C", "HIV", "Asthma",
    "COPD", "Emphysema", "Pleurisy", "Sleep Apnea", "Allergic Rhinitis",
    "Gastritis", "Gastric Ulcer", "GERD", "IBS", "Crohn's Disease",
    "Ulcerative Colitis", "Celiac Disease", "Gallstones", "Pancreatitis",
    "Appendicitis", "Diverticulitis", "Hemorrhoids", "Constipation",
    "Hypertension", "Heart Failure", "Angina", "Arrhythmia",
    "Heart Attack", "Stroke", "Deep Vein Thrombosis", "Atherosclerosis",
    "Migraine", "Tension Headache", "Epilepsy", "Multiple Sclerosis",
    "Parkinson's Disease", "Alzheimer's Disease", "Neuropathy", "Sciatica",
    "Anxiety", "Depression", "Bipolar Disorder", "PTSD", "OCD",
    "Insomnia", "Panic Disorder", "ADHD", "Diabetes Type 1", "Diabetes Type 2",
    "Hypothyroidism", "Hyperthyroidism", "PCOS", "Osteoarthritis",
    "Rheumatoid Arthritis", "Osteoporosis", "Gout", "Herniated Disc",
    "Tendinitis", "Bursitis", "Carpal Tunnel Syndrome", "Plantar Fasciitis",
    "Conjunctivitis", "Glaucoma", "Cataracts", "Dry Eye", "UTI",
    "Kidney Stones", "Cystitis", "Prostatitis", "Acne", "Eczema",
    "Psoriasis", "Contact Dermatitis", "Urticaria", "Rosacea", "Vitiligo",
    "Warts", "Fungal Infection", "Food Allergy", "Drug Allergy",
    "Anaphylaxis", "Breast Cancer", "Lung Cancer", "Colon Cancer",
    "Prostate Cancer", "Leukemia", "Lymphoma", "Skin Cancer", "Anemia",
    "Iron Deficiency Anemia", "B12 Deficiency", "Thrombocytopenia", "Hemophilia"
]

# Category → Specialty mapping
SPECIALTY_BY_CATEGORY = {
    "Infectious": "Infectious Diseases",
    "Respiratory": "Pulmonology",
    "Digestive": "Gastroenterology",
    "Cardiovascular": "Cardiology",
    "Neurological": "Neurology",
    "Psychiatric": "Psychiatry",
    "Endocrine": "Endocrinology",
    "Orthopedic": "Orthopedics",
    "Ophthalmology": "Ophthalmology",
    "Urology": "Urology",
    "Dermatology": "Dermatology",
    "Allergy": "Allergy",
    "Oncology": "Oncology",
    "Hematology": "Hematology",
}

# ============================================================
# SYMPTOMS BY SPECIALTY (each specialty has its own symptoms)
# ============================================================
SYMPTOMS_BY_SPECIALTY = {
    "Dermatology": [
        "rash", "itching", "dry_skin", "oily_skin", "skin_redness",
        "skin_lesions", "blisters", "peeling_skin", "acne", "blackheads",
        "cysts", "boils", "warts", "hair_loss", "itchy_scalp",
        "dandruff", "changes_in_moles", "hives"
    ],
    "Orthopedics": [
        "joint_pain", "back_pain", "joint_stiffness", "morning_stiffness",
        "joint_swelling", "limited_movement", "muscle_cramps",
        "muscle_spasms", "back_stiffness", "shoulder_pain", "knee_pain",
        "knee_swelling", "ankle_pain", "ankle_swelling", "hip_pain",
        "neck_pain", "leg_pain", "arm_pain", "wrist_pain", "foot_pain",
        "muscle_pain", "swelling", "redness", "warmth"
    ],
    "Neurology": [
        "headache", "dizziness", "confusion", "memory_loss", "seizures",
        "numbness", "tingling", "tremor", "loss_of_balance",
        "speech_difficulty", "blurred_vision", "double_vision",
        "sensitivity_to_light", "loss_of_consciousness", "vertigo",
        "ringing_in_ears", "neck_pain"
    ],
    "Cardiology": [
        "chest_pain", "palpitations", "tachycardia", "bradycardia",
        "shortness_of_breath", "swelling_in_legs", "swelling_in_ankles",
        "cold_extremities", "fainting", "chest_tightness",
        "fatigue", "dizziness"
    ],
    "Pulmonology": [
        "cough", "dry_cough", "wet_cough", "coughing_blood",
        "shortness_of_breath", "wheezing", "chest_tightness",
        "phlegm", "chest_pain", "fever", "fatigue"
    ],
    "Gastroenterology": [
        "nausea", "vomiting", "diarrhea", "constipation", "bloating",
        "heartburn", "blood_in_stool", "dark_stool", "gas",
        "abdominal_cramps", "indigestion", "abdominal_pain",
        "loss_of_appetite", "weight_loss", "fatigue"
    ],
    "Endocrinology": [
        "fatigue", "weight_loss", "weight_gain", "excessive_thirst",
        "frequent_urination", "frequent_hunger", "cold_intolerance",
        "heat_intolerance", "excessive_sweating", "dry_mouth",
        "weakness", "dizziness"
    ],
    "Ophthalmology": [
        "red_eyes", "watery_eyes", "itchy_eyes", "eye_discharge",
        "blurred_vision", "eye_pain", "sensitivity_to_light",
        "double_vision", "headache"
    ],
    "Urology": [
        "frequent_urination", "painful_urination", "urgent_urination",
        "blood_in_urine", "dark_urine", "difficulty_urinating",
        "pelvic_pain", "testicular_pain", "erectile_dysfunction",
        "fever", "fatigue"
    ],
    "Allergy": [
        "sneezing", "runny_nose", "stuffy_nose", "itchy_eyes",
        "watery_eyes", "rash", "hives", "itching", "wheezing",
        "shortness_of_breath", "cough", "fatigue"
    ],
    "Infectious Diseases": [
        "fever", "fatigue", "chills", "night_sweats", "malaise",
        "weakness", "swollen_glands", "headache", "cough",
        "sore_throat", "muscle_pain", "nausea", "vomiting", "diarrhea"
    ],
    "Oncology": [
        "weight_loss", "fatigue", "night_sweats", "fever",
        "swollen_glands", "breast_lump", "breast_pain",
        "nipple_discharge", "changes_in_moles", "coughing_blood",
        "blood_in_stool", "blood_in_urine", "pain"
    ],
    "Hematology": [
        "fatigue", "weakness", "bruising", "bleeding", "slow_healing",
        "fever", "weight_loss", "night_sweats", "swollen_glands",
        "shortness_of_breath", "dizziness"
    ],
    "Psychiatry": [
        "anxiety", "depression", "insomnia", "irritability",
        "loss_of_interest", "suicidal_thoughts", "mood_swings",
        "difficulty_concentrating", "panic_attacks", "fatigue",
        "headache", "loss_of_appetite"
    ],
}

# ============================================================
# TREATMENTS BY SPECIALTY
# ============================================================
TREATMENTS_BY_SPECIALTY = {
    "Dermatology": [
        "Moisturizers", "Antifungal cream", "Antibiotic cream",
        "Corticosteroid cream", "Sunscreen", "Antihistamines",
        "Avoid irritants", "Keep skin clean and dry"
    ],
    "Orthopedics": [
        "Rest and ice", "Physical therapy", "Pain relievers (Ibuprofen)",
        "Muscle relaxants", "Compression", "Elevation",
        "Hot/cold compresses", "Surgery (if necessary)"
    ],
    "Neurology": [
        "Pain relievers", "Anti-seizure medication", "Muscle relaxants",
        "Physical therapy", "Rest in dark room", "Stress management",
        "Sleep hygiene"
    ],
    "Cardiology": [
        "Blood pressure medication", "Beta-blockers", "Diuretics",
        "Aspirin", "Cholesterol medication", "Lifestyle changes",
        "Low-sodium diet", "Regular exercise"
    ],
    "Pulmonology": [
        "Bronchodilators", "Inhaled corticosteroids", "Cough syrup",
        "Steam inhalation", "Rest and hydration", "Oxygen therapy (if severe)",
        "Avoid smoking"
    ],
    "Gastroenterology": [
        "Antacids", "Proton pump inhibitors", "Anti-diarrheal medication",
        "Laxatives", "Probiotics", "Bland diet", "Hydration",
        "Avoid spicy foods"
    ],
    "Endocrinology": [
        "Insulin", "Oral diabetes medication", "Thyroid medication",
        "Hormone therapy", "Dietary changes", "Regular exercise",
        "Blood sugar monitoring"
    ],
    "Ophthalmology": [
        "Antibiotic eye drops", "Antihistamine eye drops",
        "Artificial tears", "Cold compresses", "Eye protection",
        "Surgery (if necessary)"
    ],
    "Urology": [
        "Antibiotics", "Pain relievers", "Increased water intake",
        "Avoid caffeine and alcohol", "Warm compresses",
        "Surgery (if necessary)"
    ],
    "Allergy": [
        "Antihistamines", "Decongestants", "Nasal corticosteroids",
        "Allergy shots", "Avoid allergens", "Saline nasal spray"
    ],
    "Infectious Diseases": [
        "Antibiotics (if bacterial)", "Antivirals", "Rest and hydration",
        "Antipyretics (fever reducers)", "Isolation (if contagious)",
        "Vaccination (prevention)"
    ],
    "Oncology": [
        "Chemotherapy", "Radiation therapy", "Surgery",
        "Immunotherapy", "Targeted therapy", "Pain management",
        "Palliative care"
    ],
    "Hematology": [
        "Iron supplements", "Vitamin B12 supplements", "Blood transfusion",
        "Folate supplements", "Medication to stimulate blood cell production"
    ],
    "Psychiatry": [
        "Anti-anxiety medication", "Antidepressants", "Sleep aids",
        "Psychotherapy", "Counseling", "Stress management",
        "Lifestyle changes"
    ],
}

RECOMMENDATIONS_POOL = [
    "Consult a general practitioner", "See a specialist",
    "Get plenty of rest", "Stay hydrated", "Avoid strenuous activity",
    "Apply hot/cold compresses", "Monitor symptoms", "Keep a symptom diary",
    "Avoid triggers", "Maintain a healthy diet", "Exercise regularly",
    "Get vaccinated", "Practice good hygiene", "Avoid smoking",
    "Limit alcohol consumption", "Manage stress", "Get enough sleep",
    "Seek emergency care if symptoms worsen", "Follow up with your doctor",
    "Take medications as prescribed"
]

SPECIALISTS_POOL = [
    "General Practitioner", "Infectious Diseases", "ENT", "Pulmonology",
    "Gastroenterology", "Cardiology", "Neurology", "Psychiatry",
    "Endocrinology", "Orthopedics", "Ophthalmology", "Urology",
    "Allergy", "Dermatology", "Oncology", "Hematology",
    "Rheumatology", "Emergency Medicine"
]

URGENCY_LEVELS = ["Mild", "Moderate", "High", "Critical"]


def generate_diseases(count=2000):
    diseases = []
    random.seed(42)

    # Generate unique names
    all_names = []
    for base in DISEASE_BASES:
        all_names.append(base)
        if len(all_names) >= count:
            break

    counter = 1
    while len(all_names) < count:
        base = DISEASE_BASES[counter % len(DISEASE_BASES)]
        all_names.append(f"{base} - Variant {counter}")
        counter += 1

    selected_names = all_names[:count]

    for idx, name in enumerate(selected_names, start=1):
        # Pick category and specialty
        category = random.choice(list(SPECIALTY_BY_CATEGORY.keys()))
        specialty = SPECIALTY_BY_CATEGORY[category]

        severity = random.randint(1, 5)
        age_groups = random.sample(["child", "teen", "adult", "elderly"], k=random.randint(2, 4))
        sex_specific = random.choice(["both", "male", "female"])

        # ===== KEY FIX: Use specialty-specific symptoms =====
        symptom_pool = SYMPTOMS_BY_SPECIALTY.get(specialty, ["fatigue", "fever", "pain"])
        num_symptoms = min(random.randint(3, 6), len(symptom_pool))
        chosen = random.sample(symptom_pool, num_symptoms)
        symptoms = {s: round(random.uniform(0.5, 1.0), 1) for s in chosen}

        # ===== KEY FIX: Use specialty-specific treatments =====
        treatment_pool = TREATMENTS_BY_SPECIALTY.get(specialty, ["Rest and hydration"])
        treatments = random.sample(treatment_pool, k=min(random.randint(2, 4), len(treatment_pool)))

        recommendations = random.sample(RECOMMENDATIONS_POOL, k=random.randint(1, 3))
        specialists = random.sample(SPECIALISTS_POOL, k=random.randint(1, 2))
        urgency = random.choice(URGENCY_LEVELS)

        disease = {
            "id": idx,
            "name": name,
            "category": category,
            "specialty": specialty,
            "severity": severity,
            "age_groups": age_groups,
            "sex_specific": sex_specific,
            "symptoms": symptoms,
            "treatments": treatments,
            "recommendations": recommendations,
            "specialists": specialists,
            "urgency": urgency
        }
        diseases.append(disease)

    return diseases


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    output_file = base_dir / "data" / "medical" / "diseases.json"

    print("Generating 2000 diseases...")
    diseases = generate_diseases(2000)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"diseases": diseases}, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(diseases)} diseases in {output_file}")