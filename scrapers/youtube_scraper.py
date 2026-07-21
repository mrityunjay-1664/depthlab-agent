"""Depth Lab AI Agent - YouTube Lead Scraper"""
import httpx
import re
import time
import random
from bs4 import BeautifulSoup
from database.db import add_lead, get_daily_stats, update_daily_stats
from config.settings import MIN_SUBSCRIBERS, MAX_SUBSCRIBERS, MAX_SCRAPES_PER_DAY


def parse_subscriber_count(text):
    """Convert '1.2M subscribers' to integer"""
    text = text.lower().replace("subscribers", "").strip()
    if 'm' in text:
        return int(float(text.replace('m', '').strip()) * 1000000)
    elif 'k' in text:
        return int(float(text.replace('k', '').strip()) * 1000)
    else:
        return int(text.replace(',', '').strip())


def extract_email_from_about(about_html):
    """Extract email from YouTube about page"""
    soup = BeautifulSoup(about_html, 'html.parser')
    text = soup.get_text()

    # Look for email patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None


def search_youtube_channels(query, max_results=25):
    """Search YouTube for channels matching query"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    channels = []

    try:
        # YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={query}+creator"
        client = httpx.Client(headers=headers, follow_redirects=True, timeout=15)
        response = client.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find channel links
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if '/channel/' in href or '/@' in href:
                    channel_url = f"https://www.youtube.com{href}" if href.startswith('/') else href
                    if channel_url not in [c.get('url') for c in channels]:
                        channels.append({
                            'url': channel_url,
                            'name': link.get_text(strip=True),
                        })

        client.close()
    except Exception as e:
        print(f"Error searching YouTube: {e}")

    return channels[:max_results]


def get_channel_details(channel_url):
    """Get channel details including subscriber count and email"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        client = httpx.Client(headers=headers, follow_redirects=True, timeout=15)
        response = client.get(channel_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get channel name
            name = soup.find('title')
            name = name.get_text().replace(' - YouTube', '').strip() if name else 'Unknown'

            # Get subscriber count from meta tags
            subscriber_count = 0
            for meta in soup.find_all('meta'):
                content = meta.get('content', '')
                if 'subscriber' in content.lower():
                    subscriber_count = parse_subscriber_count(content)
                    break

            # Try to find email in page
            email = None
            page_text = soup.get_text()
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, page_text)
            if emails:
                email = emails[0]

            client.close()

            return {
                'name': name,
                'url': channel_url,
                'subscribers': subscriber_count,
                'email': email,
            }

        client.close()
    except Exception as e:
        print(f"Error getting channel details: {e}")

    return None


def scrape_youtube_leads(niches=None):
    """Main scraper function - finds YouTube creators as leads"""
    if niches is None:
        niches = [
            "tech review",
            "gaming content",
            "education",
            "vlog",
            "fitness",
            "cooking",
            "travel",
            "finance",
        ]

    # Check daily limit
    stats = get_daily_stats()
    if stats['leads_found'] >= MAX_SCRAPES_PER_DAY:
        print(f"⚠️ Daily scrape limit reached ({MAX_SCRAPES_PER_DAY})")
        return []

    leads_found = 0
    all_leads = []

    for niche in niches:
        if leads_found >= MAX_SCRAPES_PER_DAY:
            break

        print(f"🔍 Searching: {niche} creators...")
        channels = search_youtube_channels(niche)

        for channel in channels:
            if leads_found >= MAX_SCRAPES_PER_DAY:
                break

            details = get_channel_details(channel['url'])
            if details:
                subs = details['subscribers']
                if MIN_SUBSCRIBERS <= subs <= MAX_SUBSCRAPERS:
                    # Add to database
                    lead_id = add_lead(
                        name=details['name'],
                        email=details['email'],
                        company=details['name'],
                        source="youtube",
                        segment="youtubers",
                    )
                    leads_found += 1
                    all_leads.append({
                        'id': lead_id,
                        'name': details['name'],
                        'email': details['email'],
                        'subscribers': subs,
                    })
                    print(f"  ✅ Added: {details['name']} ({subs:,} subs)")

            # Rate limiting
            time.sleep(random.uniform(2, 5))

    # Update daily stats
    update_daily_stats(leads_found=leads_found)

    print(f"\n📊 Found {leads_found} new leads today")
    return all_leads


if __name__ == "__main__":
    from database.models import init_database
    init_database()
    leads = scrape_youtube_leads()
    print(f"\nTotal leads found: {len(leads)}")
