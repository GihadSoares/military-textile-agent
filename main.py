import os
import requests
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from openai import OpenAI

# Load keys from a .env file
load_dotenv()

# Initialize services
firecrawl = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
WEBHOOK_URL = os.getenv('MAKE_WEBHOOK_URL', '')  # Optional: set in .env


def analyze_article(url):
    print(f"--- Fetching: {url} ---")

    # 1. Scrape the URL
    try:
        scrape_result = firecrawl.scrape_url(url, params={'formats': ['markdown']})
        markdown_content = scrape_result.get('markdown', '')
    except Exception as e:
        print(f"[ERROR] Could not scrape {url}: {e}")
        return None

    if not markdown_content.strip():
        print(f"[WARN] No content returned for {url}")
        return None

    # 2. Ask GPT to analyze
    prompt = f"""
You are a military textile technology analyst.
Analyze the following article for trends in military parachuting, paragliding materials,
aramids, high-tenacity polymers, or specialized canopy coatings.

If relevant, provide:
1. A brief summary.
2. Key materials or technologies mentioned.
3. Strategic significance (why does this matter for the military?).

If irrelevant, just return "IRRELEVANT".

Source URL: {url}

Article Content:
{markdown_content[:15000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def load_sources(filepath='sources.txt'):
    """Load URLs from a text file, one per line."""
    if not os.path.exists(filepath):
        print(f"[ERROR] {filepath} not found. Please create it with one URL per line.")
        return []
    with open(filepath, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return urls


def send_to_webhook(webhook_url, text):
    """Send results to a Make.com (or any) webhook."""
    if not webhook_url:
        return
    try:
        requests.post(webhook_url, json={"text": text}, timeout=10)
        print("[INFO] Result sent to webhook.")
    except Exception as e:
        print(f"[ERROR] Webhook failed: {e}")


# --- EXECUTION ---
if __name__ == "__main__":
    urls_to_scrape = load_sources('sources.txt')

    if not urls_to_scrape:
        print("No URLs to process. Exiting.")
        exit(1)

    all_results = []

    for url in urls_to_scrape:
        result = analyze_article(url)
        if result and result.strip() != 'IRRELEVANT':
            entry = f"SOURCE: {url}\n\n{result}"
            all_results.append(entry)
            print(entry)
        else:
            print(f"[SKIP] {url} -> IRRELEVANT or no content")
        print("\n" + "="*50 + "\n")

    # Send consolidated report to webhook
    if all_results and WEBHOOK_URL:
        full_report = "\n\n" + "="*60 + "\n\n".join(all_results)
        send_to_webhook(WEBHOOK_URL, full_report)

    print(f"Done. {len(all_results)} relevant article(s) found out of {len(urls_to_scrape)} sources.")
