"""Flask API Server for 3D Pipeline Dashboard"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import init_database, get_connection
from database.db import add_lead, get_total_stats, get_daily_stats

app = Flask(__name__, static_folder='static')
CORS(app)


@app.route('/')
def index():
    """Serve the 3D dashboard"""
    return send_from_directory('static', 'index.html')


@app.route('/api/pipeline')
def get_pipeline():
    """Get all leads organized by pipeline stage"""
    conn = get_connection()
    cursor = conn.cursor()

    stages = [
        "new_lead", "email_sent", "followup",
        "replied", "qualified", "proposal_sent",
        "closed_won", "closed_lost"
    ]

    pipeline = {}
    for stage in stages:
        cursor.execute("SELECT * FROM leads WHERE pipeline_stage = ?", (stage,))
        leads = [dict(row) for row in cursor.fetchall()]
        pipeline[stage] = leads

    conn.close()
    return jsonify(pipeline)


@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    total = get_total_stats()
    daily = get_daily_stats()
    return jsonify({**total, **daily})


@app.route('/api/lead', methods=['POST'])
def create_lead():
    """Add a new lead"""
    data = request.json
    lead_id = add_lead(
        name=data.get('name', ''),
        email=data.get('email'),
        phone=data.get('phone'),
        company=data.get('company'),
        source=data.get('source', 'manual'),
        segment=data.get('segment', 'new_lead'),
    )
    return jsonify({"id": lead_id, "message": "Lead created"})


@app.route('/api/lead/<int:lead_id>/stage', methods=['PUT'])
def update_stage(lead_id):
    """Update a lead's pipeline stage"""
    data = request.json
    new_stage = data.get('stage')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE leads SET pipeline_stage = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (new_stage, lead_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Stage updated"})


@app.route('/api/lead/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    """Delete a lead"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Lead deleted"})


@app.route('/api/leads')
def get_all_leads():
    """Get all leads"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY created_at DESC")
    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(leads)


if __name__ == '__main__':
    init_database()
    print("\n3D Pipeline Dashboard running at http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
