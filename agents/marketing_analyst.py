import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


def get_openrouter_key():
    key = os.getenv("OPENROUTER_API_KEY")

    if not key:
        raise ValueError("OPENROUTER_API_KEY is missing from .env")

    return key


def analyze_ads(ads):
    if not ads:
        raise ValueError("No ads available for analysis.")

    api_key = get_openrouter_key()

    prompt = f"""
You are a senior performance marketing analyst.

Analyze the following Meta ads from the trading/financial education niche.

Your goal is NOT to copy the ads. Extract reusable marketing insights
that can help create a new video ad for CrowdWisdomTrading.

CrowdWisdomTrading helps traders filter market noise using insights
from professional traders and provides actionable market intelligence.

For each ad, identify:
1. Target audience / ICP
2. Main pain point
3. Marketing angle
4. Hook
5. Offer/value proposition
6. CTA
7. Why the ad could work
8. Creative concept we could adapt

Then provide:
- common pain points
- common marketing patterns
- 3 original creative directions for CrowdWisdomTrading

Do not invent facts about the ads.
Do not claim an ad is successful unless the supplied data supports it.

Return ONLY valid JSON in this structure:

{{
  "ads_analysis": [],
  "common_pain_points": [],
  "marketing_patterns": [],
  "crowdwisdom_creative_directions": []
}}

ADS:
{json.dumps(ads, indent=2, ensure_ascii=False)}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
        },
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    content = result["choices"][0]["message"]["content"]

    # Remove markdown code fences if the model adds them
    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "", 1)
        content = content.replace("```", "", 1)
        content = content.strip()

    return json.loads(content)


if __name__ == "__main__":
    with open(
        "data/ads_research.json",
        "r",
        encoding="utf-8"
    ) as f:
        ads = json.load(f)

    analysis = analyze_ads(ads)

    with open(
        "data/marketing_analysis.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            analysis,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("Marketing analysis completed.")
    print("Saved to data/marketing_analysis.json")