"""Depth Lab AI Agent - Main Entry Point"""
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


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
    table = Table(title="Available Commands", show_header=True)
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("init", "Initialize database")
    table.add_row("scrape", "Run lead scraper")
    table.add_row("send", "Send cold emails")
    table.add_row("followup", "Send follow-up emails")
    table.add_row("pipeline", "Show CRM pipeline")
    table.add_row("stats", "Show statistics")
    table.add_row("daemon", "Run scheduler (24/7)")
    table.add_row("help", "Show this help")
    table.add_row("quit", "Exit the agent")

    console.print(table)


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
        console.print(f"\n[green]✅ Found {len(leads)} new leads[/green]")

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
            console.print("[yellow]No new leads to email[/yellow]")

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
            console.print("[yellow]No pending follow-ups[/yellow]")

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

        console.print("\n[bold cyan]📊 DEPTH LAB - STATISTICS[/bold cyan]")
        console.print(f"  Total Leads:      {total['total_leads']}")
        console.print(f"  Total Emails:     {total['total_emails']}")
        console.print(f"  Total Replies:    {total['total_replies']}")
        console.print(f"  Conversions:      {total['total_conversions']}")
        console.print(f"  Reply Rate:       {total['reply_rate']}")
        console.print(f"  Conversion Rate:  {total['conversion_rate']}")
        console.print(f"\n[bold]Today's Stats:[/bold]")
        console.print(f"  Emails Sent:      {daily['emails_sent']}")
        console.print(f"  Leads Found:      {daily['leads_found']}")

    elif command == "daemon":
        from database.models import init_database
        from scheduler.runner import run_scheduler
        init_database()
        run_scheduler()

    elif command == "help":
        show_help()

    elif command == "quit":
        console.print("[green]Goodbye! 👋[/green]")
        return

    else:
        console.print(f"[red]Unknown command: {command}[/red]")
        show_help()


if __name__ == "__main__":
    main()
