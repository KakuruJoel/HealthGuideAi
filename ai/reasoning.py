HIGH_RISK_SYMPTOMS = [
    "difficulty_breathing",
    "chest_pain",
    "loss_of_consciousness",
    "bleeding",
    "blood_in_stool",
    "blood_in_urine",
    "persistent_vomiting"
]

MODERATE_RISK_SYMPTOMS = [
    "high_fever",
    "shortness_of_breath",
    "rapid_heartbeat",
    "confusion",
    "severe_headache"
]

def assess_risk(symptoms):

    score = 0

    for symptom in symptoms:

        if symptom in HIGH_RISK_SYMPTOMS:
            score += 4

        elif symptom in MODERATE_RISK_SYMPTOMS:
            score += 2

        else:
            score += 1

    if score >= 12:
        return "Emergency"

    if score >= 8:
        return "High"

    if score >= 5:
        return "Moderate"

    return "Low"


FOLLOW_UP_QUESTIONS = {
    "Malaria": [
        "How many days have you had the fever?",
        "Have you recently been bitten by mosquitoes?",
        "Have you taken a malaria test?"
    ],

    "Typhoid Fever": [
        "Have you had abdominal pain?",
        "Have you eaten contaminated food recently?",
        "How long has the fever lasted?"
    ],

    "Influenza": [
        "Do you have a sore throat?",
        "Are you coughing?",
        "Do you have a runny nose?"
    ],

    "COVID-19": [
        "Have you lost your sense of smell?",
        "Have you been in contact with someone who was sick?",
        "Do you have difficulty breathing?"
    ],

    "Ebola Virus Disease": [
        "Have you had contact with an Ebola patient?",
        "Are you experiencing unexplained bleeding?",
        "Have you recently traveled to an outbreak area?"
    ]
}

def get_followup_questions(disease):

    return FOLLOW_UP_QUESTIONS.get(disease, [])
