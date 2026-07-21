"""Depth Lab AI Agent - Email Templates"""

TEMPLATES = {
    "youtubers": {
        "subject": "{{first_name}}, your videos deserve better editing 🎬",
        "body": """Hi {{first_name}},

I came across your channel {{channel_name}} and loved your recent video on {{topic}}. Great content!

But I noticed the editing could be elevated to match your quality content. At Depth Lab, we help creators like you stand out with:

→ Cinematic color grading
→ Smooth transitions & effects
→ Professional motion graphics
→ Engaging thumbnails

We've worked with 30+ creators and delivered 50+ projects.

Special offer: First 3 reels at ₹999 only!

Check our work: https://depthlab.netlify.app

Would love to chat!

Best,
Depth Lab
depthlab61@gmail.com
+91 84005 56785""",
    },
    "brands": {
        "subject": "{{first_name}}, elevate your brand's visual presence 🎨",
        "body": """Hi {{first_name}},

I came across {{company_name}} and loved your products. Your brand has great potential!

I'm from Depth Lab, a VFX & Motion Design studio. We help brands create:

→ Social media reels that convert
→ Product showcase videos
→ Brand story videos
→ Ad creatives for campaigns

Our clients see 40% better engagement after working with us.

Pricing starts at just ₹999 for 3 reels.

Portfolio: https://depthlab.netlify.app

Let's discuss how we can help {{company_name}} grow?

Best,
Depth Lab
depthlab61@gmail.com
+91 84005 56785""",
    },
    "agencies": {
        "subject": "{{first_name}}, partnership opportunity - VFX outsourcing 🤝",
        "body": """Hi {{first_name}},

I'm reaching out from Depth Lab, a VFX & Motion Design studio based in India.

We specialize in white-label video editing for agencies like yours:

→ Unlimited revisions
→ 24-hour turnaround
→ Consistent quality
→ Bulk pricing available

If your agency handles video content for clients, we can be your reliable backend partner.

Portfolio: https://depthlab.netlify.app

Would love to explore how we can support {{company_name}}'s growth.

Best,
Depth Lab
depthlab61@gmail.com
+91 84005 56785""",
    },
    "filmmakers": {
        "subject": "{{first_name}}, professional VFX for your next project 🎥",
        "body": """Hi {{first_name}},

I saw your work on {{project_name}} - stunning visuals!

I'm from Depth Lab, a VFX & Motion Design studio. We help filmmakers like you with:

→ Green screen compositing
→ Visual effects (VFX)
→ Color grading & correction
→ Title sequences & motion graphics

We've delivered 50+ projects with cinematic quality.

Pricing starts at just ₹999.

Portfolio: https://depthlab.netlify.app

Let's discuss your next project!

Best,
Depth Lab
depthlab61@gmail.com
+91 84005 56785""",
    },
}

FOLLOWUP_TEMPLATES = {
    "followup_1": {
        "subject": "Quick follow-up 🎬",
        "body": """Hi {{first_name}},

Just following up on my last email about helping {{company_name}} with video editing.

We're offering 20% off for new clients this month.

Let me know if you'd like to discuss!

Best,
Depth Lab""",
    },
    "followup_2": {
        "subject": "Last chance - 20% off 🎁",
        "body": """Hi {{first_name}},

This is my final follow-up regarding our video editing services for {{company_name}}.

Our 20% discount ends soon. Don't miss out!

Portfolio: https://depthlab.netlify.app

Best,
Depth Lab""",
    },
    "followup_3": {
        "subject": "Closing the loop 🤝",
        "body": """Hi {{first_name}},

I understand you're busy. I'll close this thread for now.

If you ever need VFX or video editing services, we're here to help.

Best of luck with {{company_name}}!

Best,
Depth Lab""",
    },
}
