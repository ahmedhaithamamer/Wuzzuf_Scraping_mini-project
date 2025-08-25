# Simple Configuration for Wuzzuf Job Scraper

# Search Settings
SEARCH_KEYWORD = "software engineering"  # Change this to your preferred engineering field
LOCATION = ""  # Leave empty for all locations, or add specific location like "Cairo", "Dubai"
MAX_PAGES = 3  # Number of pages to scrape

# Scraping Settings
HEADLESS_MODE = False  # Set to True to run without browser window
DELAY_BETWEEN_PAGES = (2, 4)  # Random delay range in seconds

# Output Settings
OUTPUT_PREFIX = "wuzzuf_jobs"  # Prefix for output files
SAVE_CSV = True  # Save to CSV
SAVE_JSON = True  # Save to JSON

# Engineering Fields (examples)
ENGINEERING_FIELDS = [
    "software engineering",
    "mechanical engineering", 
    "civil engineering",
    "electrical engineering",
    "data engineering",
    "AI engineering",
    "robotics engineering"
]
