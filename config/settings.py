"""Depth Lab AI Agent - Configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

# Company Details
COMPANY_NAME = os.getenv("COMPANY_NAME", "Depth Lab")
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "depthlab61@gmail.com")
COMPANY_PHONE = os.getenv("COMPANY_PHONE", "+91 84005 56785")
COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://depthlab.netlify.app")

# API Keys
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID", "")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET", "")
GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN", "")
GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")

# Email Limits (Gmail safe limits)
MAX_EMAILS_PER_DAY = 50
MAX_EMAILS_PER_HOUR = 20
MIN_DELAY_BETWEEN_EMAILS = 45  # seconds
MAX_DELAY_BETWEEN_EMAILS = 120  # seconds

# Business Hours (IST)
BUSINESS_START_HOUR = 9
BUSINESS_END_HOUR = 17

# Follow-up Schedule (days)
FOLLOWUP_DAY_1 = 3
FOLLOWUP_DAY_2 = 7
FOLLOWUP_DAY_3 = 14

# Lead Scraper Settings
MIN_SUBSCRIBERS = 10000
MAX_SUBSCRIBERS = 500000
MAX_SCRAPES_PER_DAY = 50

# Database
DATABASE_PATH = "depthlab.db"

# Services & Pricing
SERVICES = [
    "Visual Effects (VFX)",
    "Motion Graphics",
    "Video Editing",
    "Compositing",
    "Instagram Reels Editing",
]

PRICING = {
    "starter": {"name": "Starter", "price": 999, "reels": 3},
    "professional": {"name": "Professional", "price": 1999, "reels": 8},
    "enterprise": {"name": "Enterprise", "price": 2999, "reels": 15},
}
