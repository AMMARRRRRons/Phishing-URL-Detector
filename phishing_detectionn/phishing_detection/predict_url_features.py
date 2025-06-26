from features_extraction import extract_features
import joblib
import numpy as np

model = joblib.load('phishing_model.pkl')

url = input("Entrez une URL à tester : ")
features = extract_features(url)
features = np.array(features).reshape(1, -1)

prediction = model.predict(features)

if prediction[0] == 1:
    print("⚠️ Phishing détecté !")
else:
    print("✅ Site légitime.")

