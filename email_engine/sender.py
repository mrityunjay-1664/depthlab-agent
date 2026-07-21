"""Depth Lab AI Agent - Email Sender using Gmail API"""
import time
import random
from datetime import datetime
from database.db import log_email, get_daily_stats, update_daily_stats
from config.settings import (
    MAX_EMAILS_PER_DAY,
    MAX_EMAILS_PER_HOUR,
    MIN_DELAY_BETWEEN_EMAILS,
    MAX_DELAY_BETWEEN_EMAILS,
    BUSINESS_START_HOUR,
    BUSINESS_END_HOUR,
)


def is_business_hours():
    """Check if current time is within business hours (IST)"""
    # For now, always return True (can add timezone logic later)
    return True


def can_send_email():
    """Check if we can send more emails today"""
    stats = get_daily_stats()
    if stats['emails_sent'] >= MAX_EMAILS_PER_DAY:
        print(f"⚠️ Daily limit reached ({MAX_EMAILS_PER_DAY} emails)")
        return False
    return True


def send_email_via_gmail(to_email, subject, body):
    """Send email using Gmail API (simplified - needs OAuth setup)"""
    # This is a placeholder - actual implementation requires:
    # 1. Google Cloud Console project
    # 2. Gmail API enabled
    # 3. OAuth2 credentials
    # 4. token.json file

    print(f"📧 Sending to: {to_email}")
    print(f"   Subject: {subject}")
    print(f"   Body preview: {body[:100]}...")

    # For now, simulate sending
    # In production, use:
    # from google.oauth2.credentials import Credentials
    # from googleapiclient.discovery import build
    # service = build('gmail', 'v1', credentials=creds)
    # message = create_message(to_email, subject, body)
    # service.users().messages().send(userId='me', body=message).execute()

    return True


def send_personalized_email(lead, template):
    """Send a personalized email to a lead"""
    if not can_send_email():
        return False

    if not lead.get('email'):
        print(f"⚠️ No email for {lead['name']}, skipping")
        return False

    if not is_business_hours():
        print("⚠️ Outside business hours, skipping")
        return False

    # Send the email
    success = send_email_via_gmail(
        to_email=lead['email'],
        subject=template['subject'],
        body=template['body'],
    )

    if success:
        # Log the email
        log_email(
            lead_id=lead['id'],
            template_name=template.get('template_name', 'cold_outreach'),
            subject=template['subject'],
        )

        # Update stats
        update_daily_stats(emails_sent=1)

        print(f"✅ Email sent to {lead['name']} ({lead['email']})")

        # Random delay between emails
        delay = random.uniform(MIN_DELAY_BETWEEN_EMAILS, MAX_DELAY_BETWEEN_EMAILS)
        print(f"   Waiting {delay:.0f} seconds before next email...")
        time.sleep(delay)

        return True

    return False


def send_batch_emails(leads, templates, segment):
    """Send emails to a batch of leads"""
    template = templates.get(segment)
    if not template:
        print(f"❌ No template for segment: {segment}")
        return

    sent_count = 0
    for lead in leads:
        if not can_send_email():
            print(f"\n🛑 Stopping - daily limit reached")
            break

        from email.personalizer import personalize_template
        personalized = personalize_template(template, lead)
        personalized['template_name'] = segment

        if send_personalized_email(lead, personalized):
            sent_count += 1

    print(f"\n📊 Sent {sent_count} emails today")


if __name__ == "__main__":
    print("Email sender module - use main.py to run")
