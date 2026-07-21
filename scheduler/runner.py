"""Depth Lab AI Agent - Scheduler"""
import schedule
import time
from datetime import datetime


def daily_scrape_job():
    """Daily lead scraping job"""
    print(f"\n🕐 [{datetime.now().strftime('%H:%M')}] Running daily scrape...")
    from scrapers.youtube_scraper import scrape_youtube_leads
    scrape_youtube_leads()


def daily_send_job():
    """Daily cold email job"""
    print(f"\n🕐 [{datetime.now().strftime('%H:%M')}] Running daily emails...")
    from database.db import get_leads_by_status
    from email_engine.sender import send_batch_emails
    from config.templates import TEMPLATES

    leads = get_leads_by_status("new")
    if leads:
        send_batch_emails(leads, TEMPLATES, "youtubers")
    else:
        print("  No new leads to email")


def daily_followup_job():
    """Daily follow-up job"""
    print(f"\n🕐 [{datetime.now().strftime('%H:%M')}] Running follow-ups...")
    from database.db import get_pending_followups
    from email_engine.sender import send_personalized_email
    from email.personalizer import personalize_template
    from config.templates import FOLLOWUP_TEMPLATES

    pending = get_pending_followups()
    if pending:
        for lead in pending:
            template = FOLLOWUP_TEMPLATES.get(lead['followup_type'])
            if template:
                personalized = personalize_template(template, lead)
                send_personalized_email(lead, personalized)
    else:
        print("  No pending follow-ups")


def daily_pipeline_job():
    """Daily pipeline update"""
    print(f"\n🕐 [{datetime.now().strftime('%H:%M')}] Updating pipeline...")
    from crm.pipeline import print_pipeline
    print_pipeline()


def run_scheduler():
    """Run the scheduler"""
    print("🚀 Depth Lab AI Agent - Scheduler Started!")
    print("=" * 50)

    # Schedule jobs
    schedule.every().day.at("09:00").do(daily_scrape_job)
    schedule.every().day.at("10:00").do(daily_send_job)
    schedule.every().day.at("14:00").do(daily_followup_job)
    schedule.every().day.at("18:00").do(daily_pipeline_job)

    print("📅 Scheduled jobs:")
    print("  09:00 - Lead scraping")
    print("  10:00 - Cold emails")
    print("  14:00 - Follow-ups")
    print("  18:00 - Pipeline update")
    print("=" * 50)

    # Run once immediately
    daily_pipeline_job()

    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
