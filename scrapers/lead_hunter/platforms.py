"""Multi-Platform Lead Hunter - Search keywords and signals for video editing needs"""

# Keywords that indicate someone NEEDS video editing
NEED_SIGNALS = {
    "direct_need": [
        "looking for video editor",
        "need video editor",
        "seeking video editor",
        "hiring video editor",
        "video editor wanted",
        "looking for editor",
        "need someone to edit",
        "searching for editor",
        "editor required",
        "video editing service needed",
        "need help with editing",
        "looking for editing help",
        "want to hire editor",
        "freelance video editor needed",
        "editing gig",
    ],
    "content_creator": [
        "content creator",
        "youtuber",
        "influencer",
        "social media creator",
        "reels creator",
        "tiktok creator",
        "vlogger",
        "podcaster",
        "digital creator",
        "video creator",
    ],
    "business_need": [
        "brand video",
        "product video",
        "ad video",
        "promo video",
        "marketing video",
        "social media content",
        "video marketing",
        "commercial video",
        "explainer video",
        "testimonial video",
    ],
    "frustration_signals": [
        "no time to edit",
        "editing takes too long",
        "struggling with editing",
        "need better quality",
        "editing is hard",
        "cant find editor",
        "bad editing",
        "editing help",
        "need professional editing",
        "looking for quality editor",
    ],
}

# Platform-specific search queries
SEARCH_QUERIES = {
    "linkedin": [
        '"looking for video editor"',
        '"need video editor"',
        '"hiring video editor"',
        '"video editing service"',
        '"content creator" AND "looking for"',
        '"brand video" AND "need"',
        '"social media" AND "video editor"',
        '"youtube" AND "editor needed"',
    ],
    "twitter": [
        "looking for video editor",
        "need video editor",
        "hiring editor",
        "video editing help",
        "need someone to edit",
        "editor wanted",
        "looking for editor",
        "video editor required",
    ],
    "reddit": [
        "looking for video editor",
        "need video editor",
        "hiring video editor",
        "video editing service",
        "editor needed",
        "freelance editor",
        "video editor for hire",
    ],
    "facebook_groups": [
        "video editor needed",
        "looking for editor",
        "hiring editor",
        "video editing service",
        "editor wanted",
    ],
    "instagram": [
        "#lookingforeditor",
        "#videoeditorneeded",
        "#hiringeditor",
        "#editorwanted",
        "#videoediting",
        "#needaneditor",
    ],
    "youtube_comments": [
        "nice editing",
        "who edited this",
        "where did you get edited",
        "need editor like you",
        "looking for editor",
    ],
}

# Platform URLs for scraping
PLATFORM_URLS = {
    "linkedin_jobs": "https://www.linkedin.com/jobs/search/?keywords=video+editor&location=India",
    "indeed": "https://in.indeed.com/jobs?q=video+editor&l=India",
    "naukri": "https://www.naukri.com/video-editor-jobs",
    "upwork": "https://www.upwork.com/search/jobs/?q=video+editing",
    "freelancer": "https://www.freelancer.com/jobs/video-editing/",
    "fiverr": "https://www.fiverr.com/search/gigs?query=video+editing",
    "twitter_search": "https://twitter.com/search?q=looking+for+video+editor",
    "reddit_search": "https://www.reddit.com/search/?q=looking+for+video+editor",
}

# Job title patterns (for LinkedIn/Jobs scraping)
JOB_TITLE_PATTERNS = [
    "video editor",
    "content editor",
    "social media editor",
    "youtube editor",
    "reels editor",
    "film editor",
    "post production",
    "video production",
    "creative editor",
    "digital editor",
]
