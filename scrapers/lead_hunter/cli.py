"""Lead Hunter CLI - Command line interface for the lead hunter"""
from scrapers.lead_hunter.hunter import LeadHunter, run_hunter
from database.db import get_total_stats, get_leads_by_status


def show_hunter_menu():
    """Show the lead hunter menu"""
    print("\n" + "=" * 60)
    print("  LEAD HUNTER - Find Video Editing Clients")
    print("=" * 60)
    print("  1. Hunt ALL platforms (Reddit, LinkedIn, Indeed, Upwork)")
    print("  2. Hunt Reddit only")
    print("  3. Hunt LinkedIn Jobs only")
    print("  4. Hunt Indeed only")
    print("  5. Hunt Upwork only")
    print("  6. View found leads")
    print("  7. View stats")
    print("  0. Back to main menu")
    print("=" * 60)


def hunt_reddit():
    """Hunt leads from Reddit only"""
    print("\n  Searching Reddit for video editing needs...")
    hunter = LeadHunter()
    leads = []
    from scrapers.lead_hunter.platforms import SEARCH_QUERIES
    for query in SEARCH_QUERIES['reddit'][:5]:
        found = hunter.search_reddit(query)
        leads.extend(found)
    if leads:
        saved = hunter.save_leads(leads)
        print(f"  Found {len(leads)} leads, saved {saved}")
    else:
        print("  No leads found")


def hunt_linkedin():
    """Hunt leads from LinkedIn Jobs only"""
    print("\n  Searching LinkedIn Jobs...")
    hunter = LeadHunter()
    leads = hunter.search_linkedin_jobs()
    if leads:
        saved = hunter.save_leads(leads)
        print(f"  Found {len(leads)} leads, saved {saved}")
    else:
        print("  No leads found")


def hunt_indeed():
    """Hunt leads from Indeed only"""
    print("\n  Searching Indeed...")
    hunter = LeadHunter()
    leads = hunter.search_indeed()
    if leads:
        saved = hunter.save_leads(leads)
        print(f"  Found {len(leads)} leads, saved {saved}")
    else:
        print("  No leads found")


def hunt_upwork():
    """Hunt leads from Upwork only"""
    print("\n  Searching Upwork...")
    hunter = LeadHunter()
    leads = hunter.search_upwork()
    if leads:
        saved = hunter.save_leads(leads)
        print(f"  Found {len(leads)} leads, saved {saved}")
    else:
        print("  No leads found")


def view_leads():
    """View found leads"""
    leads = get_leads_by_status("new")
    if not leads:
        print("\n  No new leads found yet")
        return

    print(f"\n  Found {len(leads)} leads:")
    print("-" * 60)
    for i, lead in enumerate(leads[:20], 1):
        print(f"  {i}. {lead['name']} ({lead['source']})")
        if lead.get('email'):
            print(f"     Email: {lead['email']}")
    if len(leads) > 20:
        print(f"  ... and {len(leads) - 20} more")


def view_stats():
    """View lead hunting stats"""
    stats = get_total_stats()
    print(f"\n  Lead Hunter Stats:")
    print(f"  Total Leads: {stats['total_leads']}")
    print(f"  Total Emails: {stats['total_emails']}")
    print(f"  Reply Rate: {stats['reply_rate']}")


def run_lead_hunter_cli():
    """Main CLI loop for lead hunter"""
    while True:
        show_hunter_menu()
        choice = input("\n  Select option: ").strip()

        if choice == "1":
            run_hunter()
        elif choice == "2":
            hunt_reddit()
        elif choice == "3":
            hunt_linkedin()
        elif choice == "4":
            hunt_indeed()
        elif choice == "5":
            hunt_upwork()
        elif choice == "6":
            view_leads()
        elif choice == "7":
            view_stats()
        elif choice == "0":
            break
        else:
            print("  Invalid option")


if __name__ == "__main__":
    run_lead_hunter_cli()
