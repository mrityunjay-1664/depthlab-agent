"""Multi-Platform Lead Hunter - Find video editing clients across ALL platforms"""
import httpx
import re
import json
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
from database.db import add_lead, get_daily_stats, update_daily_stats
from scrapers.lead_hunter.platforms import (
    NEED_SIGNALS,
    SEARCH_QUERIES,
    PLATFORM_URLS,
)


class LeadHunter:
    """Hunt leads across multiple platforms"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        self.leads_found = []

    def search_twitter(self, query, max_results=10):
        """Search Twitter/X for people looking for video editors"""
        leads = []
        try:
            search_url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
            client = httpx.Client(headers=self.headers, follow_redirects=True, timeout=15)
            response = client.get(search_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract tweets mentioning video editing needs
                for tweet in soup.find_all('div', {'data-testid': 'tweet'}):
                    text = tweet.get_text()
                    if any(signal in text.lower() for signal in NEED_SIGNALS['direct_need']):
                        # Try to extract username
                        username_elem = tweet.find('a', href=re.compile(r'/[A-Za-z0-9_]+$'))
                        if username_elem:
                            leads.append({
                                'name': username_elem.get_text(strip=True),
                                'platform': 'twitter',
                                'text': text[:200],
                                'source': 'twitter_search',
                            })

            client.close()
        except Exception as e:
            print(f"  Twitter search error: {e}")

        return leads[:max_results]

    def search_reddit(self, query, max_results=10):
        """Search Reddit for people looking for video editors"""
        leads = []
        try:
            search_url = f"https://www.reddit.com/search.json?q={query}&sort=new&limit={max_results}"
            headers = {**self.headers, "User-Agent": "DepthLabBot/1.0"}
            client = httpx.Client(headers=headers, follow_redirects=True, timeout=15)
            response = client.get(search_url)

            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])

                for post in posts:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    author = post_data.get('author', '')

                    if any(signal in (title + selftext).lower() for signal in NEED_SIGNALS['direct_need']):
                        leads.append({
                            'name': author,
                            'platform': 'reddit',
                            'title': title,
                            'text': selftext[:200],
                            'url': f"https://reddit.com{post_data.get('permalink', '')}",
                            'source': 'reddit_search',
                        })

            client.close()
        except Exception as e:
            print(f"  Reddit search error: {e}")

        return leads[:max_results]

    def search_linkedin_jobs(self, max_results=10):
        """Search LinkedIn job listings for video editing needs"""
        leads = []
        try:
            client = httpx.Client(headers=self.headers, follow_redirects=True, timeout=15)
            response = client.get(PLATFORM_URLS['linkedin_jobs'])

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find job cards
                for card in soup.find_all('div', class_=re.compile(r'job-search-card')):
                    title_elem = card.find('h3')
                    company_elem = card.find('h4')

                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True) if company_elem else 'Unknown'
                        link = card.find('a', href=True)
                        url = link['href'] if link else ''

                        leads.append({
                            'name': company,
                            'platform': 'linkedin',
                            'title': title,
                            'url': url,
                            'source': 'linkedin_jobs',
                            'segment': 'business_need',
                        })

            client.close()
        except Exception as e:
            print(f"  LinkedIn search error: {e}")

        return leads[:max_results]

    def search_indeed(self, max_results=10):
        """Search Indeed for video editing job postings"""
        leads = []
        try:
            client = httpx.Client(headers=self.headers, follow_redirects=True, timeout=15)
            response = client.get(PLATFORM_URLS['indeed'])

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                for card in soup.find_all('div', class_=re.compile(r'job_seen_beacon|result')):
                    title_elem = card.find('h2', class_=re.compile(r'jobTitle'))
                    company_elem = card.find('span', class_=re.compile(r'companyName'))

                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True) if company_elem else 'Unknown'
                        link = card.find('a', href=True)
                        url = f"https://in.indeed.com{link['href']}" if link else ''

                        leads.append({
                            'name': company,
                            'platform': 'indeed',
                            'title': title,
                            'url': url,
                            'source': 'indeed_jobs',
                            'segment': 'business_need',
                        })

            client.close()
        except Exception as e:
            print(f"  Indeed search error: {e}")

        return leads[:max_results]

    def search_upwork(self, max_results=10):
        """Search Upwork for video editing gigs"""
        leads = []
        try:
            client = httpx.Client(headers=self.headers, follow_redirects=True, timeout=15)
            response = client.get(PLATFORM_URLS['upwork'])

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                for card in soup.find_all('section', class_=re.compile(r'job-tile-list')):
                    title_elem = card.find('a', class_=re.compile(r'up-n-link'))
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        leads.append({
                            'name': 'Upwork Client',
                            'platform': 'upwork',
                            'title': title,
                            'url': f"https://www.upwork.com{url}" if url.startswith('/') else url,
                            'source': 'upwork_gigs',
                            'segment': 'business_need',
                        })

            client.close()
        except Exception as e:
            print(f"  Upwork search error: {e}")

        return leads[:max_results]

    def save_leads(self, leads):
        """Save found leads to database"""
        saved_count = 0
        for lead in leads:
            try:
                lead_id = add_lead(
                    name=lead.get('name', 'Unknown'),
                    email=lead.get('email'),
                    company=lead.get('name', 'Unknown'),
                    source=lead.get('platform', 'unknown'),
                    segment=lead.get('segment', 'direct_need'),
                )
                saved_count += 1
            except Exception as e:
                print(f"  Error saving lead: {e}")

        return saved_count

    def hunt_all_platforms(self):
        """Main method - hunt leads across ALL platforms"""
        print("\n" + "=" * 60)
        print("  LEAD HUNTER - Multi-Platform Search")
        print("=" * 60)

        # Check daily limit
        stats = get_daily_stats()
        if stats['leads_found'] >= 100:
            print("  Daily limit reached (100 leads)")
            return []

        all_leads = []

        # 1. Reddit Search
        print("\n  Searching Reddit...")
        for query in SEARCH_QUERIES['reddit'][:3]:
            leads = self.search_reddit(query)
            all_leads.extend(leads)
            print(f"    Found {len(leads)} leads from Reddit")
            time.sleep(random.uniform(2, 4))

        # 2. LinkedIn Jobs
        print("\n  Searching LinkedIn Jobs...")
        leads = self.search_linkedin_jobs()
        all_leads.extend(leads)
        print(f"    Found {len(leads)} leads from LinkedIn")

        # 3. Indeed Jobs
        print("\n  Searching Indeed...")
        leads = self.search_indeed()
        all_leads.extend(leads)
        print(f"    Found {len(leads)} leads from Indeed")

        # 4. Upwork Gigs
        print("\n  Searching Upwork...")
        leads = self.search_upwork()
        all_leads.extend(leads)
        print(f"    Found {len(leads)} leads from Upwork")

        # Save all leads
        if all_leads:
            saved = self.save_leads(all_leads)
            update_daily_stats(leads_found=saved)
            print(f"\n  Total leads found: {len(all_leads)}")
            print(f"  Saved to database: {saved}")
        else:
            print("\n  No leads found in this run")

        return all_leads


def run_hunter():
    """Run the lead hunter"""
    hunter = LeadHunter()
    return hunter.hunt_all_platforms()


if __name__ == "__main__":
    run_hunter()
