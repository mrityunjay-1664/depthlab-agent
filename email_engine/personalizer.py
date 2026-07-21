"""Depth Lab AI Agent - Email Personalizer"""
import random
from config.settings import CLAUDE_API_KEY


# Template-based opening lines (FREE alternative to Claude)
OPENING_LINES = {
    "youtubers": [
        "Loved your recent video - the content quality is amazing!",
        "Your channel caught my attention with great editing potential!",
        "I've been following your content and see a huge opportunity!",
        "Your videos have great ideas - the editing could match them!",
        "As a fellow creator, I noticed something special about your work!",
    ],
    "brands": [
        "Your brand stood out while I was researching the market!",
        "I love what {company} is building - great product line!",
        "Your brand has real potential to shine on social media!",
        "I noticed {company} and see a great visual opportunity!",
        "Your products deserve premium video content!",
    ],
    "agencies": [
        "I see great potential for a VFX partnership!",
        "Your agency's work caught my attention!",
        "We could be the perfect backend partner for your agency!",
        "I noticed your agency handles video content - let's talk!",
        "A fellow creative agency reaching out with an offer!",
    ],
    "filmmakers": [
        "Your filmmaking skills are impressive!",
        "I saw your recent project - stunning visuals!",
        "Your creative vision deserves professional VFX support!",
        "I love your storytelling approach!",
        "Your work shows real cinematic talent!",
    ],
}


def get_personalized_opening(lead_data, template_type):
    """Generate personalized opening line (template-based, FREE)"""
    name = lead_data.get('name', 'there').split()[0] if lead_data.get('name') else 'there'
    company = lead_data.get('company', 'your company')

    # Try Claude API first (if available)
    if CLAUDE_API_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            prompt = f"""Generate ONE short opening line for a cold email.
Lead: {name}, Company: {company}, Type: {template_type}
Return ONLY the opening line, under 15 words."""
            message = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text.strip()
        except Exception:
            pass  # Fall back to template-based

    # Template-based (FREE)
    openings = OPENING_LINES.get(template_type, OPENING_LINES["youtubers"])
    opening = random.choice(openings)
    opening = opening.replace("{company}", company)
    return opening


def personalize_template(template, lead_data):
    """Replace placeholders in email template with lead data"""
    personalized = template.copy()

    name = lead_data.get('name', 'there')
    first_name = name.split()[0] if name else 'there'
    company = lead_data.get('company', 'your company')
    topic = lead_data.get('notes', 'your content') or 'your content'

    # Get personalized opening
    opening = get_personalized_opening(lead_data, personalized.get('subject', ''))

    # Replace placeholders
    replacements = {
        "{{first_name}}": first_name,
        "{{company_name}}": company,
        "{{channel_name}}": company,
        "{{topic}}": topic,
        "{{project_name}}": topic,
        "{{opening_line}}": opening,
    }

    for key, value in replacements.items():
        personalized['subject'] = personalized['subject'].replace(key, value)
        personalized['body'] = personalized['body'].replace(key, value)

    return personalized


if __name__ == "__main__":
    test_lead = {
        "name": "Rahul Verma",
        "company": "Tech Reviews India",
        "source": "youtube",
        "segment": "youtubers",
        "notes": "Recent video on iPhone 16 review",
    }
    from config.templates import TEMPLATES
    result = personalize_template(TEMPLATES['youtubers'], test_lead)
    print(f"Subject: {result['subject']}")
    print(f"\nBody:\n{result['body'][:300]}...")
