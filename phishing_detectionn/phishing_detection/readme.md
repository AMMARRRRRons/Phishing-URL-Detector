Phishing URL Detector
________________________________________________________________________________________________
Une application web de détection de sites de phishing utilisant un modèle de machine learning Random Forest.
________________________________________________________________________________________________
Description
________________________________________________________________________________________________
Ce projet propose une solution complète pour détecter si un site web est légitime ou potentiellement un site de phishing. Il repose sur :

    Un modèle d'apprentissage automatique (Random Forest) entraîné sur un dataset étiqueté.

    Une extraction de 31 caractéristiques techniques à partir de n'importe quelle URL.

    Une interface web intuitive permettant de tester une URL et de visualiser :

        - La prédiction (légitime ou phishing).

        - Les caractéristiques techniques.

        - Une explication détaillée via chatbot pour les signes de phishing détectés.
________________________________________________________________________________________________
 Fonctionnalités
________________________________________________________________________________________________
- Extraction automatique de 31 caractéristiques techniques depuis une URL.

- Prédiction via un modèle Random Forest entraîné.
- Interface web réactive en HTML/JavaScript.

- Mise en évidence des signes à risque avec explications automatisées.

- API REST construite avec FastAPI.

- Support CORS intégré (fonctionne en local et en réseau).
________________________________________________________________________________________________
 Installation
________________________________________________________________________________________________
Prérequis

	- Python 3.10+

	- pip
________________________________________________________________________________________________
Installer les dépendances
________________________________________________________________________________________________
	***pip install -r requirements.txt

Le fichier requirements.txt contient au minimum :

    ***fastapi

    ***uvicorn

    ***scikit-learn

    ***numpy

    ***pandas

    ***requests

    ***beautifulsoup4

    ***python-dotenv

    ***openai
________________________________________________________________________________________________
 Utilisation
________________________________________________________________________________________________
    Entraîner le modèle :

	***python model_training.py

→ Génère un fichier phishing_model.pkl

    Lancer le serveur backend (API FastAPI) :

	***uvicorn app:app --reload

	→ Le serveur est disponible à l'adresse http://localhost:8000

    Accéder à l'interface utilisateur :

	→ Ouvrir le navigateur à http://localhost:8000/

    Tester une URL :

	→ Entrer une URL dans le champ prévu et cliquer sur “Check URL”

	→ Résultat affiché avec caractéristiques détectées et explication en langage naturel si applicable.
________________________________________________________________________________________________
 Structure du projet
________________________________________________________________________________________________
phishing_detection/
├── app.py                   → API backend FastAPI
├── model_training.py        → Script d’entraînement du modèle Random Forest
├── features_extraction.py   → Extraction des caractéristiques depuis une URL
├── phishing_model.pkl       → Modèle entraîné (binaire)
├── frontend/
│   └── index.html           → Interface web utilisateur (HTML + JS)
├── predict_url_features.py  → Script CLI pour test unitaire
├── phishing_dataset.csv     → Dataset original
└── requirements.txt         → Dépendances Python
________________________________________________________________________________________________
 Fonctionnement technique
________________________________________________________________________________________________
     - Feature Extraction :
    Chaque URL est analysée pour extraire 31 attributs comme :

        Présence d’une adresse IP

        Longueur de l’URL

        Présence de @, redirections, etc.

     - Random Forest :
    Modèle entraîné sur un dataset labellisé pour différencier sites légitimes et phishing.

     - API :
    Une route POST /predict reçoit une URL et retourne un JSON avec :

        La prédiction (true / false)

        Les 31 caractéristiques

        Les caractéristiques considérées comme “à risque” avec explication.

     - Frontend :

        Application HTML / JS qui interagit avec l’API.

        Affiche les résultats + explication du modèle (via API Groq ou OpenRouter).
________________________________________________________________________________________________
Exemple d’appel API
________________________________________________________________________________________________
Commande curl :
_________________
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://phishing-site.com"}'

Réponse attendue :
_________________

{
  "phishing": true,
  "features": {
    "having_IP_Address": 1,
    "URL_Length": 1,
    ...
  },
  "risky_features": [
    {
      "feature": "having_IP_Address",
      "explanation": "URL contains an IP address which is suspicious"
    }
  ]
}
________________________________________________________________________________________________
Contributions
________________________________________________________________________________________________
Les contributions sont les bienvenues !
N’hésitez pas à :

    - Créer une issue

    - Proposer des améliorations

    - Soumettre des pull requests
________________________________________________________________________________________________
Ressources
________________________________________________________________________________________________
    Dataset utilisé :
    https://www.kaggle.com/datasets/nitsey/dataset-phising-website
________________________________________________________________________________________________
Auteur:

Ons Ammar
2025
