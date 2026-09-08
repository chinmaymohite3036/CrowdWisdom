# CrowdWisdomTrading Video Ads Agent

An AI-powered multi-agent pipeline that researches successful trading advertisements, identifies marketing patterns and trader pain points, generates an ad storyboard, and produces a finished video advertisement for CrowdWisdomTrading.

## 🎬 Final Video

**[Watch the final 50-second ad](https://drive.google.com/file/d/1wZ9Uk_SrIP7qfWjURxoBxueC6q3AANPg/view?usp=drive_link)**

### Creative Concept — Noise → Signal

The ad focuses on a core problem faced by active and retail traders: information overload.

It visually moves from:

**Market Noise → Conflicting Signals → Overload → Professional Trader Insights → Clarity**

The final message is:

> **FIND THE SIGNAL.**

The visual style uses an archival paper-diorama aesthetic with layered paper elements, halftone textures, red/mustard accents, animated statistics, and tactile depth.

---

## 🧠 Agent Pipeline

```text
                    ┌──────────────────┐
                    │   Hermes Agent   │
                    │  Orchestration   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Ads Research    Pain Research   Marketing
          Agent            Agent         Analyst
              │              │              │
           Apify           Tavily       OpenRouter
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                       Script Agent
                             │
                         OpenRouter
                             │
                             ▼
                       Video Agent
                             │
                    OpenMontage + Remotion
                             │
                             ▼
                    Final Advertisement
```

### 1. Ads Researcher

Uses the **Apify Meta Ads Library actor** to collect recent advertisements related to the trading niche.

The researcher extracts information such as:

* Ad ID
* Advertiser/page
* Start and end dates
* Active status
* Creative format
* Ad copy
* CTA
* Landing-page information

The collected data is stored in:

```text
data/ads_raw.json
data/ads_research.json
```

### 2. Marketing Analyst

Analyzes the researched advertisements to identify:

* Target audience
* Pain points
* Marketing angles
* CTAs
* Messaging patterns
* Creative directions

Output:

```text
data/marketing_analysis.json
```

### 3. Pain & ICP Researcher

Uses **Tavily** to research current trader problems, especially:

* Information overload
* Difficulty filtering market information
* Conflicting signals
* Need for professional market intelligence

Output:

```text
data/pain_points.json
```

### 4. Script Agent

Combines the advertisement research, marketing analysis, pain-point research, and CrowdWisdomTrading information into a human-readable storyboard.

The generated script contains:

* Scene descriptions
* Timing
* Visual direction
* On-screen text
* Camera movement
* Marketing message
* Verified product claims

Output:

```text
data/final_script.json
```

### 5. Video Agent

The final storyboard is implemented as a deterministic **Remotion** composition.

Remotion was selected because it provides precise control over:

* Typography
* Layout
* Animation
* Counters
* Paper elements
* Scene timing
* Brand messaging

The final composition is rendered locally as a 50-second 1920×1080 MP4.

---

## 🎨 Creative Direction

### Visual Style

The advertisement uses a **VOX-inspired archival paper diorama** style:

* Aged paper textures
* Halftone imagery
* Layered paper cards
* Torn-paper elements
* Typewriter-style labels
* Bold condensed typography
* Red and mustard accent colors
* Physical depth and shadows
* Editorial/newsroom atmosphere

### Story Structure

| Scene | Purpose                                |
| ----- | -------------------------------------- |
| 1     | Establish information overload         |
| 2     | Show conflicting market signals        |
| 3     | Show trader uncertainty                |
| 4     | Introduce professional trader insights |
| 5     | Transform noise into a clear signal    |
| 6     | Deliver the CrowdWisdomTrading CTA     |

---

## 🛠️ Technologies

* **Python**
* **Hermes Agent Framework**
* **OpenRouter**
* **Apify Meta Ads Library**
* **Tavily**
* **OpenMontage**
* **Remotion**
* **FFmpeg**
* **React / TypeScript**

---

## 📁 Project Structure

```text
CrowdWisdomAdsAgent/
│
├── agents/
│   ├── ads_researcher.py
│   ├── marketing_analyst.py
│   ├── pain_researcher.py
│   └── script_agent.py
│
├── data/
│   ├── ads_raw.json
│   ├── ads_research.json
│   ├── marketing_analysis.json
│   ├── pain_points.json
│   └── final_script.json
│
├── scripts/
│
├── videos/
│   └── (local video output; excluded from Git)
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The local `openmontage/`, `.venv/`, `.env`, and generated video files are intentionally excluded from version control.

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd CrowdWisdomAdsAgent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file:

```env
APIFY_API_TOKEN=your_apify_token
TAVILY_API_KEY=your_tavily_key
OPENROUTER_API_KEY=your_openrouter_key
```

API credentials are intentionally excluded from the repository.

---

## ▶️ Running the Research Pipeline

The individual agents can be executed from the project environment.

The research pipeline produces the intermediate JSON artifacts used by the script generation stage:

```text
Ads Research
     ↓
Marketing Analysis
     ↓
Pain / ICP Research
     ↓
Script Generation
     ↓
Video Composition
```

The final video is rendered using the Remotion composition.

---

## ⚠️ Research Limitation

The Meta Ads Library research data available through the selected Apify actor did not consistently expose reliable spend, reach, or impression metrics for every collected advertisement.

Therefore, the research pipeline does **not** falsely claim that an advertisement was objectively the "best performing" ad.

Instead, the selection uses available signals such as:

* Recency
* Active status
* Creative format
* Copy quality
* CTA clarity
* Longevity
* Available metadata

This keeps the research process transparent rather than inventing performance data.

---

## 🛡️ Messaging & Claim Safety

The generated advertisement intentionally avoids unsupported financial claims.

It does **not** promise:

* Guaranteed profits
* Specific investment returns
* Trading success
* Risk-free trading
* Testimonials that were not provided
* Free trials or offers that were not verified

The creative focuses on CrowdWisdomTrading's professional-trader insight and market-intelligence positioning.

---

## 🎯 Result

The final result is a 50-second video advertisement designed to communicate one simple idea:

> **The problem isn't finding more market information. It's knowing what deserves your attention.**

**FIND THE SIGNAL.**

---

## 👤 Project

Built as an internship assessment for the CrowdWisdomTrading AI Ads Agent position.
