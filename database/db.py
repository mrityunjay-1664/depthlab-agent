"""Depth Lab AI Agent - Database Operations"""
from datetime import datetime, timedelta
from database.models import get_connection


def add_lead(name, email=None, phone=None, company=None, source=None, segment=None):
    """Add a new lead to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads (name, email, phone, company, source, segment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, phone, company, source, segment))
    conn.commit()
    lead_id = cursor.lastrowid
    conn.close()
    return lead_id


def get_leads_by_stage(stage):
    """Get all leads in a specific pipeline stage"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE pipeline_stage = ?", (stage,))
    leads = cursor.fetchall()
    conn.close()
    return [dict(lead) for lead in leads]


def get_leads_by_status(status):
    """Get all leads with a specific status"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE status = ?", (status,))
    leads = cursor.fetchall()
    conn.close()
    return [dict(lead) for lead in leads]


def update_lead_stage(lead_id, new_stage):
    """Update a lead's pipeline stage"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads SET pipeline_stage = ?, updated_at = ?
        WHERE id = ?
    """, (new_stage, datetime.now(), lead_id))
    conn.commit()
    conn.close()


def log_email(lead_id, template_name, subject, followup_number=0):
    """Log an email send"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO email_tracking (lead_id, template_name, subject, followup_number)
        VALUES (?, ?, ?, ?)
    """, (lead_id, template_name, subject, followup_number))
    conn.commit()
    conn.close()


def get_pending_followups():
    """Get leads that need follow-up emails"""
    conn = get_connection()
    cursor = conn.cursor()

    # Get leads that were emailed but haven't replied
    cursor.execute("""
        SELECT l.*, et.sent_at, et.followup_number
        FROM leads l
        JOIN email_tracking et ON l.id = et.lead_id
        WHERE l.pipeline_stage IN ('email_sent', 'followup')
        AND et.replied_at IS NULL
        AND et.bounced = 0
        ORDER BY et.sent_at ASC
    """)
    leads = cursor.fetchall()
    conn.close()

    pending = []
    for lead in leads:
        lead_dict = dict(lead)
        sent_at = datetime.fromisoformat(lead_dict['sent_at'])
        days_since = (datetime.now() - sent_at).days
        followup_num = lead_dict['followup_number']

        if followup_num == 0 and days_since >= 3:
            pending.append({**lead_dict, 'followup_type': 'followup_1'})
        elif followup_num == 1 and days_since >= 7:
            pending.append({**lead_dict, 'followup_type': 'followup_2'})
        elif followup_num == 2 and days_since >= 14:
            pending.append({**lead_dict, 'followup_type': 'followup_3'})

    return pending


def get_daily_stats():
    """Get today's email stats"""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')

    cursor.execute("SELECT * FROM daily_stats WHERE date = ?", (today,))
    stats = cursor.fetchone()
    conn.close()

    if stats:
        return dict(stats)
    return {"emails_sent": 0, "emails_opened": 0, "emails_replied": 0, "leads_found": 0}


def update_daily_stats(emails_sent=0, leads_found=0):
    """Update today's stats"""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')

    cursor.execute("""
        INSERT INTO daily_stats (date, emails_sent, leads_found)
        VALUES (?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            emails_sent = emails_sent + ?,
            leads_found = leads_found + ?
    """, (today, emails_sent, leads_found, emails_sent, leads_found))
    conn.commit()
    conn.close()


def get_total_stats():
    """Get overall stats"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM leads")
    total_leads = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM email_tracking")
    total_emails = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM email_tracking WHERE replied_at IS NOT NULL")
    total_replies = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM leads WHERE pipeline_stage = 'closed_won'")
    total_conversions = cursor.fetchone()['total']

    conn.close()

    return {
        "total_leads": total_leads,
        "total_emails": total_emails,
        "total_replies": total_replies,
        "total_conversions": total_conversions,
        "reply_rate": f"{(total_replies/total_emails*100):.1f}%" if total_emails > 0 else "0%",
        "conversion_rate": f"{(total_conversions/total_leads*100):.1f}%" if total_leads > 0 else "0%",
    }
