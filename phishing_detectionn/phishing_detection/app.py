from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from features_extraction import extract_features
import joblib
import numpy as np
import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import traceback


env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)


model = joblib.load("phishing_model.pkl")


openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables.")


client = OpenAI(
    api_key=openai_api_key,
    base_url="https://api.groq.com/openai/v1"
)


class URLItem(BaseModel):
    url: str


FEATURE_NAMES = [
    "having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol",
    "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State",
    "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL",
    "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL",
    "Redirect", "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain",
    "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page",
    "Statistical_report"
]

RISKY_FEATURES = {
    "having_IP_Address": "URL contains an IP address instead of domain name.",
    "Shortining_Service": "URL uses a shortening service, often hides destination.",
    "having_At_Symbol": "URL contains '@', commonly used for redirections.",
    "double_slash_redirecting": "Multiple '//' after protocol may indicate redirection.",
    "Prefix_Suffix": "Domain contains '-', can mimic legitimate domains.",
    "having_Sub_Domain": "Too many subdomains may indicate suspicious structure.",
    "SSLfinal_State": "No valid HTTPS detected.",
    "Request_URL": "External resources dominate the page.",
    "URL_of_Anchor": "Anchors redirect to different domains.",
    "Links_in_tags": "Suspicious external links in tags.",
    "SFH": "Form action points to unknown or empty location.",
    "Submitting_to_email": "Page tries to submit info via email.",
    "Abnormal_URL": "Domain name does not match typical patterns.",
    "Redirect": "Too many redirects, may hide destination.",
    "on_mouseover": "Hides real links via onmouseover script.",
    "RightClick": "Disables right-click, often hides source code.",
    "popUpWidnow": "Uses pop-ups, common phishing technique.",
    "Iframe": "Uses invisible iframes, hides real content.",
    "DNSRecord": "Domain lacks valid DNS records.",
}


@app.post("/predict")
async def predict_phishing(data: URLItem):
    features = extract_features(data.url)
    features_array = np.array(features).reshape(1, -1)
    pred = model.predict(features_array)[0]
    features_dict = dict(zip(FEATURE_NAMES, features))

    risky_detected = [
        {"feature": key, "explanation": RISKY_FEATURES[key]}
        for key, val in features_dict.items()
        if key in RISKY_FEATURES and val == 1
    ]

    return {
        "phishing": bool(pred == 1),  # 1 = phishing, -1 = legitimate
        "features": features_dict,
        "risky_features": risky_detected
    }


app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
async def root():
    return FileResponse(os.path.join("frontend", "index.html"))


class RiskyFeaturesRequest(BaseModel):
    risky_features: list
    phishing: bool  

@app.post("/chatbot_explain")
async def chatbot_explain(request: RiskyFeaturesRequest):
    phishing = request.phishing
    risky_features = request.risky_features

    if phishing:
        bullet_points = "\n".join(
            [f"- {f['feature']}: {f['explanation']}" for f in risky_features]
        )
        prompt = f"""Tu es un assistant qui explique pourquoi une URL est suspecte de phishing. Voici les caractéristiques détectées :

{bullet_points}

Peux-tu expliquer brièvement pourquoi ces signes indiquent un site de phishing (sans commencer par "bien sur!" et avec chaque nouveau point , fais un retour à la ligne) ?"""
    else:

        prompt = """Tu es un assistant expert en cybersécurité. L'URL analysée est légitime.

Peux-tu fournir quelques conseils simples pour aider les utilisateurs à reconnaître un site de phishing, ainsi que quelques ressources en ligne fiables pour mieux comprendre la cybersécurité et éviter les attaques de phishing ? (sans dire "excellente question" et que vous etes expert en cybersécurité) la reponse directement .Ecris chaque idée sur une nouvelle ligne.Merci."""

    try:
        chat_response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Tu es un expert en cybersécurité."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_tokens=300,
        )
    except Exception as e:
        print("Groq API error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Groq API error: {e}")

    explanation = chat_response.choices[0].message.content.strip()
    return {"response": explanation}

