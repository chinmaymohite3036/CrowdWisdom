import os
import json
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from apify_client import ApifyClient


load_dotenv()


def get_apify_client():
    token = os.getenv("APIFY_API_TOKEN")

    if not token:
        raise ValueError("APIFY_API_TOKEN is missing from .env")

    return ApifyClient(token)


def search_ads(client, query, max_ads=10):
    print(f"Searching Meta ads for: {query}")

    actor = client.actor("s-r/meta-ads-library")

    run = actor.call(
        run_input={
            "search": query,
            "country": "US",
            "active_only": True,
            "max_ads": max_ads,
        }
    )

    if run is None:
        raise RuntimeError(f"Apify search failed for query: {query}")

    items = client.dataset(run.default_dataset_id).list_items().items

    print(f"Found {len(items)} ads for '{query}'")

    return items


def research_ads(client, queries, max_ads_per_query=10):
    all_ads = []

    for query in queries:
        ads = search_ads(
            client,
            query,
            max_ads=max_ads_per_query
        )

        all_ads.extend(ads)

    return all_ads


def save_raw_ads(ads, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ads, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(ads)} ads to {filepath}")


def filter_recent_ads(ads, days=30):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    recent_ads = []

    for ad in ads:
        start_date = ad.get("start_date")

        if not start_date:
            continue

        try:
            start = datetime.fromisoformat(
                start_date.replace("Z", "+00:00")
            )

            # If the date has no timezone, treat it as UTC.
            if start.tzinfo is None:
                start = start.replace(tzinfo=timezone.utc)

        except ValueError:
            continue

        if start >= cutoff:
            recent_ads.append(ad)

    print(f"Found {len(recent_ads)} ads from the last {days} days.")

    return recent_ads

def clean_ads(ads):
    cleaned_ads = []
    seen_ids = set()

    for ad in ads:
        ad_id = ad.get("ad_id")

        if not ad_id or ad_id in seen_ids:
            continue

        seen_ids.add(ad_id)

        cleaned_ads.append({
            "ad_id": ad_id,
            "page_name": ad.get("page_name"),
            "title": ad.get("title"),
            "body_text": ad.get("body_text"),
            "start_date": ad.get("start_date"),
            "end_date": ad.get("end_date"),
            "is_active": ad.get("is_active"),
            "display_format": ad.get("display_format"),
            "cta_text": ad.get("cta_text"),
            "cta_type": ad.get("cta_type"),
            "publisher_platform": ad.get("publisher_platform", []),
            "page_like_count": ad.get("page_like_count"),
            "collation_count": ad.get("collation_count"),
            "videos": ad.get("videos", []),
            "query": ad.get("query"),
            "link_url": ad.get("link_url"),
        })

    print(f"Cleaned ads: {len(cleaned_ads)}")

    return cleaned_ads


if __name__ == "__main__":
    client = get_apify_client()

    queries = [
        "trading",
        "stock trading",
        "AI trading",
        "market insights",
        "trading signals",
    ]

    ads = research_ads(
        client,
        queries,
        max_ads_per_query=5
    )

    save_raw_ads(
        ads,
        "data/ads_raw.json"
    )

    recent_ads = filter_recent_ads(ads)

    cleaned_ads = clean_ads(recent_ads)

    with open("data/ads_research.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_ads, f, indent=2, ensure_ascii=False)

    print(f"Saved research dataset with {len(cleaned_ads)} ads.")