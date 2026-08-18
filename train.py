import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("dataset/disease_dataset.csv")

# Features
X = df.drop("disease", axis=1)

# Target
y = df["disease"]

# Encode disease names
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded,
)

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("\n============================")
print("MODEL ACCURACY")
print("============================")
print(f"{accuracy*100:.2f}%")

print("\n============================")
print("CLASSIFICATION REPORT")
print("============================")
print(
    classification_report(
        y_test,
        predictions,
        target_names=encoder.classes_,
    )
)

print("\n============================")
print("CONFUSION MATRIX")
print("============================")
print(confusion_matrix(y_test, predictions))

# Save model
joblib.dump(model, "models/disease_model.pkl")
joblib.dump(encoder, "models/label_encoder.pkl")

print("\nModel saved successfully.")
