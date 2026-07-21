"""Depth Lab AI Agent - CRM Pipeline"""
from database.db import get_leads_by_stage, update_lead_stage, get_total_stats


PIPELINE_STAGES = [
    "new_lead",
    "email_sent",
    "followup",
    "replied",
    "qualified",
    "proposal_sent",
    "closed_won",
    "closed_lost",
]


def get_pipeline_overview():
    """Get overview of all pipeline stages"""
    overview = {}
    for stage in PIPELINE_STAGES:
        leads = get_leads_by_stage(stage)
        overview[stage] = {
            "count": len(leads),
            "leads": leads,
        }
    return overview


def move_to_next_stage(lead_id, current_stage):
    """Move a lead to the next pipeline stage"""
    stage_index = PIPELINE_STAGES.index(current_stage)
    if stage_index < len(PIPELINE_STAGES) - 1:
        next_stage = PIPELINE_STAGES[stage_index + 1]
        update_lead_stage(lead_id, next_stage)
        return next_stage
    return current_stage


def print_pipeline():
    """Print the pipeline in a nice format"""
    overview = get_pipeline_overview()
    stats = get_total_stats()

    print("\n" + "=" * 60)
    print("📊 DEPTH LAB - CRM PIPELINE")
    print("=" * 60)

    for stage in PIPELINE_STAGES:
        data = overview[stage]
        count = data['count']
        bar = "█" * min(count, 20)
        print(f"  {stage:<20} | {count:>3} | {bar}")

    print("-" * 60)
    print(f"  Total Leads:      {stats['total_leads']}")
    print(f"  Total Emails:     {stats['total_emails']}")
    print(f"  Total Replies:    {stats['total_replies']}")
    print(f"  Conversions:      {stats['total_conversions']}")
    print(f"  Reply Rate:       {stats['reply_rate']}")
    print(f"  Conversion Rate:  {stats['conversion_rate']}")
    print("=" * 60)


if __name__ == "__main__":
    print_pipeline()
