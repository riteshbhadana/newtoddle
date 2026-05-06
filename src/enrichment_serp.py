import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SCALESERP_API_KEY")

SCALESERP_URL = "https://api.scaleserp.com/search"


def find_linkedin(name, school):
    name   = str(name).strip()
    school = str(school).split(";")[0].strip()

    query  = f'"{name}" "{school}" site:linkedin.com/in'
    params = {
        "api_key": API_KEY,
        "q":       query,
        "num":     5,
    }

    try:
        res = requests.get(SCALESERP_URL, params=params, timeout=15)

        if res.status_code == 401:
            print("ScaleSerp: Invalid API key")
            return fallback()
        if res.status_code == 429:
            print("ScaleSerp: Quota exceeded")
            return fallback()
        if res.status_code != 200:
            print(f"ScaleSerp HTTP error: {res.status_code}")
            return fallback()

        data    = res.json()
        results = data.get("organic_results", [])

        for r in results:
            url     = r.get("link", "")
            snippet = r.get("snippet", "")
            title   = r.get("title", "")

            if "linkedin.com/in/" not in url:
                continue

            current_school = extract_school_from_text(snippet + " " + title)

            return {
                "linkedin":       url,
                "current_school": current_school or "Unknown",
            }

    except requests.exceptions.Timeout:
        print("ScaleSerp timeout")
    except Exception as e:
        print(f"ScaleSerp error: {e}")

    return fallback()


# ── Heuristics to pull org/school name out of a LinkedIn snippet ──────────────
_CURR_PATTERN = re.compile(
    r'(?:Current|Present|Now)[^\w]*[:\-–]?\s*([A-Z][^·|•\n,]{2,50})',
    re.IGNORECASE,
)
_AT_PATTERN   = re.compile(r'\bat\s+([A-Z][^·|•\n,]{2,50})', re.IGNORECASE)
_DASH_PATTERN = re.compile(r'-\s*([A-Z][^·|•\n,]{2,50})', re.IGNORECASE)


def extract_school_from_text(text: str) -> str:
    for pattern in (_CURR_PATTERN, _AT_PATTERN, _DASH_PATTERN):
        m = pattern.search(text)
        if m:
            candidate = m.group(1).strip().rstrip(".")
            noise = {"linkedin", "view", "profile", "connect", "see", "more"}
            if candidate.lower().split()[0] not in noise:
                return candidate
    return ""


def fallback():
    return {
        "linkedin":       "Not Found",
        "current_school": "Unknown",
    }