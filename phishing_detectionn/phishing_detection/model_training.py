import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

# Charger les données
data = pd.read_csv('phishing_dataset.csv')

# Supprimer la colonne index inutile
data = data.drop(['index'], axis=1)

# Séparer les données et les labels
X = data.drop(['Result'], axis=1)
y = data['Result']

# Split en train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Modèle Random Forest
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)

# Évaluation
accuracy = accuracy_score(y_test, y_pred) * 100
cm = confusion_matrix(y_test, y_pred)

print(f"\nPrécision du modèle : {accuracy:.2f}%")
print("\nMatrice de confusion :\n", cm)

# Sauvegarder le modèle
joblib.dump(model, 'phishing_model.pkl')
print("\nModèle sauvegardé sous phishing_model.pkl")

