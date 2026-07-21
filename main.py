"""Depth Lab AI Agent - Main Entry Point"""
import sys


def show_banner():
    """Show the agent banner"""
    banner = """
=============================================
     DEPTH LAB AI AGENT
     VFX & Motion Design Studio

     Automated Client Acquisition System
=============================================
    """
    print(banner)


def show_help():
    """Show available commands"""
    print("""
Available Commands:
====================
  CORE COMMANDS:
    init        Initialize database
    scrape      Run YouTube lead scraper
    send        Send cold emails
    followup    Send follow-up emails
    pipeline    Show CRM pipeline
    stats       Show statistics
    daemon      Run scheduler (24/7)

  LEAD HUNTER (NEW):
    hunt        Hunt leads across ALL platforms
    hunt-all    Hunt all platforms automatically
    hunt-reddit Hunt Reddit only
    hunt-linked Hunt LinkedIn Jobs only
    hunt-indeed Hunt Indeed only
    hunt-upwork Hunt Upwork only
    view-leads  View found leads

  OTHER:
    help        Show this help
    quit        Exit the agent
    """)


def main():
    """Main entry point"""
    show_banner()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        show_help()
        return

    if command == "init":
        from database.models import init_database
        init_database()

    elif command == "scrape":
        from database.models import init_database
        from scrapers.youtube_scraper import scrape_youtube_leads
        init_database()
        leads = scrape_youtube_leads()
        print(f"\nFound {len(leads)} new leads")

    elif command == "send":
        from database.models import init_database
        from database.db import get_leads_by_status
        from email_engine.sender import send_batch_emails
        from config.templates import TEMPLATES
        init_database()
        leads = get_leads_by_status("new")
        if leads:
            send_batch_emails(leads, TEMPLATES, "youtubers")
        else:
            print("No new leads to email")

    elif command == "followup":
        from database.models import init_database
        from database.db import get_pending_followups
        from email_engine.sender import send_personalized_email
        from email_engine.personalizer import personalize_template
        from config.templates import FOLLOWUP_TEMPLATES
        init_database()
        pending = get_pending_followups()
        if pending:
            for lead in pending:
                template = FOLLOWUP_TEMPLATES.get(lead['followup_type'])
                if template:
                    personalized = personalize_template(template, lead)
                    send_personalized_email(lead, personalized)
        else:
            print("No pending follow-ups")

    elif command == "pipeline":
        from database.models import init_database
        from crm.pipeline import print_pipeline
        init_database()
        print_pipeline()

    elif command == "stats":
        from database.models import init_database
        from database.db import get_total_stats, get_daily_stats
        init_database()
        total = get_total_stats()
        daily = get_daily_stats()

        print("\n=== DEPTH LAB - STATISTICS ===")
        print(f"  Total Leads:      {total['total_leads']}")
        print(f"  Total Emails:     {total['total_emails']}")
        print(f"  Total Replies:    {total['total_replies']}")
        print(f"  Conversions:      {total['total_conversions']}")
        print(f"  Reply Rate:       {total['reply_rate']}")
        print(f"  Conversion Rate:  {total['conversion_rate']}")
        print(f"\nToday's Stats:")
        print(f"  Emails Sent:      {daily['emails_sent']}")
        print(f"  Leads Found:      {daily['leads_found']}")

    # Lead Hunter commands
    elif command == "hunt":
        from database.models import init_database
        from scrapers.lead_hunter.cli import run_lead_hunter_cli
        init_database()
        run_lead_hunter_cli()

    elif command == "hunt-all":
        from database.models import init_database
        from scrapers.lead_hunter.hunter import run_hunter
        init_database()
        run_hunter()

    elif command == "hunt-reddit":
        from database.models import init_database
        from scrapers.lead_hunter.cli import hunt_reddit
        init_database()
        hunt_reddit()

    elif command == "hunt-linked":
        from database.models import init_database
        from scrapers.lead_hunter.cli import hunt_linkedin
        init_database()
        hunt_linkedin()

    elif command == "hunt-indeed":
        from database.models import init_database
        from scrapers.lead_hunter.cli import hunt_indeed
        init_database()
        hunt_indeed()

    elif command == "hunt-upwork":
        from database.models import init_database
        from scrapers.lead_hunter.cli import hunt_upwork
        init_database()
        hunt_upwork()

    elif command == "view-leads":
        from database.models import init_database
        from scrapers.lead_hunter.cli import view_leads
        init_database()
        view_leads()

    elif command == "daemon":
        from database.models import init_database
        from scheduler.runner import run_scheduler
        init_database()
        run_scheduler()

    elif command == "help":
        show_help()

    elif command == "quit":
        print("Goodbye!")
        return

    else:
        print(f"Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()
