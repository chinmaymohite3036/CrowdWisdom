import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

OUTPUT_FILE = "data/final_script.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def call_llm(prompt):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """
You are a senior advertising creative director, cinematic storyboard
designer, and video-ad scriptwriter.

Your task is to create a premium 30-60 second advertisement for
CrowdWisdomTrading.

The advertisement must feel intelligent, cinematic, memorable and
professionally produced.

==================================================
CORE RULE: VERIFIED INFORMATION ONLY
==================================================

Use ONLY the CrowdWisdom information explicitly provided to you.

NEVER invent:
- product features
- pricing
- free trials
- discounts
- guarantees
- customer testimonials
- trading profits
- performance claims
- predictions
- downloadable offers
- webinars
- lead magnets
- statistics not provided
- fake UI features

Do not claim that CrowdWisdom predicts the market.

Do not claim that using CrowdWisdom guarantees profitable trades.

Do not make promises about financial returns.

If information is not verified, do not use it.

==================================================
CREATIVE CONCEPT
==================================================

The central creative concept is:

NOISE → SIGNAL

The advertisement begins with the overwhelming amount of information
a modern trader encounters:

- market news
- charts
- opinions
- social media
- alerts
- predictions
- conflicting signals

The problem is NOT simply lack of information.

The problem is information overload and deciding what deserves attention.

CrowdWisdom then enters the story as a source of professional trader
insights and market intelligence.

The visual story should transform:

CHAOS → FILTERING → CLARITY

Do not portray CrowdWisdom as a magical prediction machine.

==================================================
VISUAL STYLE — STRICT STYLE BIBLE
==================================================

The visual style is based on the provided:

"VOX STYLE MASTER SHEET —
VISUAL SYSTEM FOR A DOCUMENTARY-COLLAGE EXPLAINER SERIES"

This visual identity is LOCKED.

Do NOT introduce another art direction.

Use:

- aged archival tan paper
- muted vintage map textures
- ink-black typography
- black-and-white halftone imagery
- rough white keylines around cutout figures
- offset hot-red strokes
- torn paper edges
- archival photographs
- newspaper fragments
- typewriter-style annotation labels
- giant stat-style typography
- red underlines
- red arrows
- map pins
- visible print grain
- halftone dots
- tactile paper texture
- matte finish
- documentary/newsroom atmosphere

Color palette:

Archival Tan: #C9BB9C
Ink Black: #1A1A1A
Halftone Gray: #8C8C8C
Hot Red: #B62E1F
Mustard: #D9A441

IMPORTANT COLOR RULE:

Hot red is reserved for emphasis:
- strokes
- underlines
- arrows
- key highlights

Mustard is a secondary accent and should be used sparingly.

==================================================
DEEP PAPER DIORAMA
==================================================

The composition should NOT look like a flat poster.

Treat the visual elements as physical paper layers existing
in shallow 3D space.

Use:

- foreground paper elements
- middle-ground cutouts
- background maps/textures
- layered paper cards
- physical depth
- shallow depth of field
- camera movement through the layers

The camera should feel like it is physically moving through
a miniature paper diorama.

Use ONE major camera movement per scene.

Examples:

- push-in
- lateral drift
- dive
- orbit
- whip
- lateral track
- camera climb
- low fly-through
- macro slide

Do not combine multiple major camera movements in one scene.

Every scene should end with a visual settle.

==================================================
MOTION LANGUAGE
==================================================

Use the motion vocabulary from the style reference:

- cutouts spring into frame with slight overshoot
- counters tick upward
- red underlines swipe into place
- paper cards slide or snap into position
- arrows draw themselves
- elements stagger into the scene
- camera performs a slow cinematic movement

Possible transition devices:

ALERT WASH
STAMP
TICK-UP
TEAR
THREAD PULL

Do not use these mechanically in every scene.
Use them only where appropriate.

==================================================
THINGS TO AVOID
==================================================

Absolutely avoid:

- glossy 3D
- cyberpunk
- neon
- futuristic holograms
- generic fintech dashboards
- generic stock footage
- modern corporate office footage
- glassmorphism
- glowing blue interfaces
- floating holographic screens
- photorealistic CGI characters
- excessive colors
- random gradients
- cheesy trading graphics
- Lamborghinis / money clichés
- piles of cash
- rockets / moon imagery
- fake testimonials
- fake trading results
- invented logos
- distorted logos
- gibberish text
- watermarks

The final advertisement should feel like a premium documentary
explainer, not a generic AI-generated finance advertisement.

==================================================
TEXT RULE
==================================================

Keep on-screen text short.

Prefer powerful phrases such as:

"TOO MUCH NOISE"

"WHO DO YOU LISTEN TO?"

"FIND THE SIGNAL"

"PROFESSIONAL TRADER INSIGHT"

Use exact verified CrowdWisdom terminology where appropriate.

Do NOT fill scenes with paragraphs.

==================================================
STORY STRUCTURE
==================================================

Build approximately 5-6 scenes.

Recommended narrative:

SCENE 1:
Immediate visual hook.
Show information overload.

SCENE 2:
Escalate the chaos.
Conflicting opinions, alerts and signals surround the trader.

SCENE 3:
Create a moment of tension or silence.
Ask the central question:
"What deserves your attention?"

SCENE 4:
Introduce CrowdWisdom.
Show professional trader insights entering the visual world.

SCENE 5:
Transform chaos into clarity.
Show organized intelligence replacing the overwhelming noise.

SCENE 6:
Memorable final statement and CTA.

The final scene should be visually simple and powerful.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Use this structure:

{
  "concept": "...",
  "target_icp": "...",
  "core_message": "...",
  "estimated_duration_seconds": 50,
  "verified_crowdwisdom_claims": [],
  "scenes": [
    {
      "scene_number": 1,
      "duration_seconds": 7,
      "purpose": "...",
      "visual_description": "...",
      "on_screen_text": [],
      "image_prompt": "...",
      "video_prompt": "...",
      "audio": "...",
      "transition": "..."
    }
  ],
  "final_cta": "...",
  "safety_notes": []
}

The image_prompt must describe the visual composition in enough detail
for an image-generation model.

The video_prompt must describe the animation and camera movement
in enough detail for a video-generation model.

The visual prompts must remain faithful to the locked VOX documentary
collage / paper diorama style.

Make the advertisement feel like one coherent film rather than
six unrelated AI-generated shots.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.65,
        },
        timeout=120,
    )

    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    content = content.strip()

    # Remove markdown code fences if the model adds them
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0]

    return json.loads(content)


def build_prompt(ads, marketing, pain_points):

    crowdwisdom_facts = {
        "brand": "CrowdWisdomTrading",
        "verified_information": [
            "CrowdWisdomTrading aggregates insights from professional traders.",
            "The platform covers equities, FX, crypto and futures.",
            "The platform provides professional trader insights and market intelligence.",
            "The website states that its network includes more than 12,000 professional traders."
        ]
    }

    return f"""
Create the final video advertisement storyboard using the research
provided below.

========================
VERIFIED CROWdWISDOM FACTS
========================

{json.dumps(crowdwisdom_facts, indent=2)}

These are the ONLY product facts you may rely on.

========================
ADS RESEARCH
========================

{json.dumps(ads, indent=2)}

Use this research to understand advertising patterns,
audience targeting and creative approaches.

Do NOT copy another advertiser's claims or offers.

========================
MARKETING ANALYSIS
========================

{json.dumps(marketing, indent=2)}

Use this to understand:
- audience
- pain points
- hooks
- marketing patterns

However, any unverified CrowdWisdom offer or feature
must be discarded.

========================
PAIN / ICP RESEARCH
========================

{json.dumps(pain_points, indent=2)}

Use this to ground the problem shown in the advertisement.

========================
FINAL CREATIVE DIRECTION
========================

Create a premium documentary-style advertisement around:

NOISE → SIGNAL

A trader is surrounded by an overwhelming amount of market information.

The story should visually communicate that the challenge is not
necessarily finding more information.

The challenge is knowing what deserves attention.

CrowdWisdom enters as a source of professional trader insights
and market intelligence.

The transformation should feel visual:

CHAOS
↓
OVERLOAD
↓
TENSION
↓
CROWDWISDOM
↓
CLARITY

The advertisement should NOT promise profitable trades.

========================
VISUAL REFERENCE
========================

Follow the provided VOX STYLE MASTER SHEET.

The visual language must consistently use:

- archival tan paper
- black-and-white halftone figures
- rough keylines
- offset red strokes
- giant typography
- archival photos
- map textures
- torn paper
- typewriter labels
- red arrows and underlines
- print grain
- physical paper layers
- shallow 3D diorama depth

The visual style should feel tactile, editorial and cinematic.

Do not introduce futuristic or glossy fintech aesthetics.

========================
PRODUCTION REQUIREMENT
========================

Create approximately 5-6 scenes.

Target total duration:
45-55 seconds.

Each scene must contain:

- scene_number
- duration_seconds
- purpose
- visual_description
- on_screen_text
- image_prompt
- video_prompt
- audio
- transition

Each video prompt should use ONE major camera movement.

Every scene should end with a visual settle.

The final scene should have a strong memorable ending.
"""


def main():

    print("Loading research data...")

    ads = load_json("data/ads_research.json")
    marketing = load_json("data/marketing_analysis.json")
    pain_points = load_json("data/pain_points.json")

    print("Generating storyboard...")

    prompt = build_prompt(
        ads,
        marketing,
        pain_points
    )

    result = call_llm(prompt)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            result,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved final storyboard to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()