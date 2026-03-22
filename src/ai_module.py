import os
import time
import requests

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def _build_prompt(m):
    return (
        "You are a Digital Sovereignty expert.\n"
        "Analyze the following community organization using the AAA Index:\n\n"
        "Organization: " + m.organization + "\n"
        "Autonomy score: " + str(m.autonomy) + "/20\n"
        "Algorithm score: " + str(m.algorithm) + "/20\n"
        "Agency score: " + str(m.agency) + "/20\n"
        "Risk flags: " + str(m.risk_flags) + "\n"
        "Weakest dimension: " + m.lowest_dimension + "\n\n"
        "Provide:\n"
        "1. A brief diagnosis of the weakest dimension (2-3 sentences).\n"
        "2. Three concrete technical recommendations to strengthen digital sovereignty.\n"
        "Be specific, practical, and use open-source tools where possible."
    )

def generate_diagnostic(metrics, retries=3):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY environment variable is not set.")

    payload = {"contents": [{"parts": [{"text": _build_prompt(metrics)}]}]}
    url = GEMINI_URL + "?key=" + api_key

    for attempt in range(retries):
        try:
            r = requests.post(url, json=payload, timeout=30)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
            elif r.status_code == 429:
                wait = 60 * (attempt + 1)
                print("Rate limit. Waiting " + str(wait) + "s...")
                time.sleep(wait)
            else:
                return "API error " + str(r.status_code)
        except requests.exceptions.Timeout:
            print("Timeout on attempt " + str(attempt + 1))
            time.sleep(10)
        except Exception as e:
            return "Error: " + str(e)

    return "Failed after maximum retries."
