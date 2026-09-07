import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

token = os.getenv("APIFY_API_TOKEN")

if not token:
    raise ValueError("APIFY_API_TOKEN is missing from .env")

client = ApifyClient(token)

print("Connecting to Apify...")

actor = client.actor("s-r/meta-ads-library")

run = actor.call(
    run_input={
        "search": "trading",
        "country": "US",
        "active_only": True,
        "max_ads": 5
    }
)

if run is None:
    raise RuntimeError("Actor run failed")

items = client.dataset(run.default_dataset_id).list_items().items

print(f"Retrieved {len(items)} ads.")

for i, item in enumerate(items, start=1):
    print(f"\n--- Ad {i} ---")
    print(item)