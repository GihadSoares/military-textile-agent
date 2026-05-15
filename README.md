# Military Textile Intelligence Agent

An AI-powered daily intelligence agent that monitors military textile and parachute technology news. Built with **Firecrawl** (web scraping) and **OpenAI GPT-4o-mini** (analysis). Runs automatically every day via **GitHub Actions** — no server required.

## What It Does

- Scrapes a curated list of defense & textile websites every morning
- Uses GPT-4o-mini to filter and analyze content for relevance to:
  - Military parachuting & aerial delivery systems
  - Aramids, high-tenacity polymers, and technical fibers
  - Specialized canopy coatings & advanced materials
- Sends a consolidated intelligence report to your Telegram/Email/Discord via Make.com webhook

## Repository Structure

```
military-textile-agent/
├── main.py                          # Main agent script
├── sources.txt                      # List of URLs to monitor (one per line)
├── requirements.txt                 # Python dependencies
├── .env.example                     # Template for your API keys
└── .github/
    └── workflows/
        └── daily_report.yml         # GitHub Actions: runs every day at 08:00 UTC
```

## Quick Start (Local)

**1. Clone and set up:**
```bash
git clone https://github.com/GihadSoares/military-textile-agent.git
cd military-textile-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Configure your API keys:**
```bash
cp .env.example .env
# Edit .env and add your real keys
```

Get your keys:
- OpenAI: https://platform.openai.com/api-keys
- Firecrawl: https://www.firecrawl.dev/

**3. Run:**
```bash
python main.py
```

## Automated Daily Reports (GitHub Actions)

The agent runs automatically every day at **08:00 AM UTC** (05:00 Brasilia time).

**Setup — add your API keys as GitHub Secrets:**

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add:
   - `OPENAI_API_KEY` — your OpenAI key
   - `FIRECRAWL_API_KEY` — your Firecrawl key
   - `MAKE_WEBHOOK_URL` — your Make.com webhook URL (optional, for notifications)

3. The workflow will now run daily. You can also trigger it manually from the **Actions** tab.

## Adding/Removing Sources

Edit `sources.txt` — one URL per line. Lines starting with `#` are comments and will be ignored.

## Notification Setup (Make.com)

1. Create a free account at [Make.com](https://make.com)
2. Create a new scenario with a **Webhook** trigger
3. Copy the webhook URL and add it as the `MAKE_WEBHOOK_URL` secret
4. Connect the webhook to Telegram, Gmail, Discord, or any channel you prefer

## Dependencies

| Package | Purpose |
|---|---|
| `openai` | GPT-4o-mini analysis |
| `firecrawl-py` | Clean web scraping |
| `python-dotenv` | Load .env keys |
| `requests` | Webhook notifications |
