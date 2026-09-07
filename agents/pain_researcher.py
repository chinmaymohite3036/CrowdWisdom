import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


def get_tavily_key():
    key = os.getenv("TAVILY_API_KEY")

    if not key:
        raise ValueError("TAVILY_API_KEY is missing from .env")

    return key


def search_tavily(query, max_results=5):
    api_key = get_tavily_key()

    response = requests.post(
        "https://api.tavily.com/search",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": max_results,
            "include_answer": True,
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def research_trader_pain_points():
    queries = [
        "retail traders information overload market news social media trading decisions",
        "retail traders challenges too much market information trading decisions",
        "how traders use professional market intelligence sentiment information",
    ]

    research = []

    for query in queries:
        print(f"Researching: {query}")

        result = search_tavily(query)

        research.append({
            "query": query,
            "answer": result.get("answer"),
            "results": [
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content"),
                }
                for item in result.get("results", [])
            ],
        })

    return research


if __name__ == "__main__":
    research = research_trader_pain_points()

    with open(
        "data/pain_points.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            research,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("Pain-point research completed.")
    print("Saved to data/pain_points.json")