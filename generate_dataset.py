import random
import pandas as pd

# Disease -> Common Symptoms
DISEASES = {
    "Malaria": [
        "fever",
        "high_fever",
        "chills",
        "headache",
        "body_pain",
        "fatigue",
        "nausea",
        "vomiting",
    ],

    "Typhoid Fever": [
        "fever",
        "headache",
        "abdominal_pain",
        "weakness",
        "loss_of_appetite",
        "constipation",
        "diarrhea",
    ],

    "COVID-19": [
        "fever",
        "dry_cough",
        "fatigue",
        "loss_of_smell",
        "loss_of_taste",
        "difficulty_breathing",
        "headache",
    ],

    "Common Cold": [
        "runny_nose",
        "sneezing",
        "sore_throat",
        "cough",
        "headache",
    ],

    "Influenza": [
        "fever",
        "cough",
        "headache",
        "body_pain",
        "fatigue",
        "chills",
    ],

    "Pneumonia": [
        "fever",
        "productive_cough",
        "shortness_of_breath",
        "chest_pain",
        "fatigue",
    ],

    "Cholera": [
        "diarrhea",
        "vomiting",
        "dehydration",
        "weakness",
    ],

    "Ebola Virus Disease": [
        "high_fever",
        "headache",
        "body_pain",
        "vomiting",
        "diarrhea",
        "bleeding",
        "weakness",
    ],
}

ALL_SYMPTOMS = sorted(
    set(symptom for symptoms in DISEASES.values() for symptom in symptoms)
)

records = []

RECORDS_PER_DISEASE = 1000

for disease, symptoms in DISEASES.items():

    for _ in range(RECORDS_PER_DISEASE):

        row = {symptom: 0 for symptom in ALL_SYMPTOMS}

        # Core symptoms
        for symptom in symptoms:
            if random.random() < 0.9:
                row[symptom] = 1

        # Add a little noise
        other_symptoms = list(set(ALL_SYMPTOMS) - set(symptoms))

        noise = random.sample(
            other_symptoms,
            random.randint(0, 2),
        )

        for symptom in noise:
            row[symptom] = 1

        row["disease"] = disease

        records.append(row)

df = pd.DataFrame(records)

df.to_csv(
    "dataset/disease_dataset.csv",
    index=False,
)

print("Dataset generated successfully!")
print(df.head())
print(f"\nTotal Records: {len(df)}")
