"""Depth Lab AI Agent - Database Models"""
import sqlite3
from datetime import datetime
from config.settings import DATABASE_PATH


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    # Leads table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            company TEXT,
            source TEXT,
            segment TEXT,
            status TEXT DEFAULT 'new',
            pipeline_stage TEXT DEFAULT 'new_lead',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Email tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            template_name TEXT,
            subject TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            opened_at TIMESTAMP,
            clicked_at TIMESTAMP,
            replied_at TIMESTAMP,
            bounced BOOLEAN DEFAULT 0,
            followup_number INTEGER DEFAULT 0,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
    """)

    # Daily stats table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            emails_sent INTEGER DEFAULT 0,
            emails_opened INTEGER DEFAULT 0,
            emails_replied INTEGER DEFAULT 0,
            leads_found INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    init_database()
