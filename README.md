# Simple Wuzzuf Job Scraper

A clean, focused Python scraper for extracting engineering job listings from Wuzzuf.net using Selenium.

## 🚀 Features

- **Comprehensive Data Extraction**: Job title, company, location, experience level, skills, job type, posting date, and application link
- **Smart Element Targeting**: Uses multiple strategies to find elements even when CSS classes change
- **Clean Output**: No debug clutter - just essential information
- **Multiple Output Formats**: Saves data in both CSV and JSON formats
- **Respectful Scraping**: Built-in delays and proper error handling
- **Easy to Use**: Simple launcher with menu-driven interface

## 📁 Project Structure

```
simple_scraper/
├── simple_wuzzuf_scraper.py    # Main scraper class
├── run_scraper.py              # Interactive launcher
├── test_scraper.py             # Test suite
├── simple_config.py            # Configuration settings
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🛠️ Installation

1. **Install Python dependencies**:
   ```bash
   cd simple_scraper
   pip install -r requirements.txt
   ```

2. **Chrome browser**: Make sure you have Google Chrome installed (the scraper will auto-download ChromeDriver)

## 🎯 Usage

### Option 1: Interactive Launcher (Recommended)
```bash
cd simple_scraper
python run_scraper.py
```

Choose from:
- 🎯 Quick Search (software engineering)
- 🏢 Location Search (Cairo)
- 🔧 Custom Search
- 📊 Show Current Data
- ⚙️ Show Current Config

### Option 2: Direct Script Execution
```bash
cd simple_scraper
python simple_wuzzuf_scraper.py
```

### Option 3: Test the Scraper
```bash
cd simple_scraper
python test_scraper.py
```

## ⚙️ Configuration

Edit `simple_config.py` to customize:
- Search keywords
- Location preferences
- Number of pages to scrape
- Headless mode settings

## 📊 Output

The scraper generates:
- **CSV file**: `{prefix}_{timestamp}.csv` - Easy to open in Excel/Google Sheets
- **JSON file**: `{prefix}_{timestamp}.json` - Structured data for analysis

## 🔧 How It Works

1. **Smart Element Detection**: Uses multiple CSS selectors and fallback strategies
2. **Experience Extraction**: Targets specific span elements and validates content
3. **Skills Collection**: Gathers all skills from multiple element classes
4. **Data Cleaning**: Filters out irrelevant text and deduplicates skills
5. **Error Handling**: Gracefully handles missing elements and network issues

## 🎯 Key Methods

- `extract_experience_smart()`: Intelligent experience level extraction
- `extract_skills_comprehensive()`: Collects all skills from multiple sources
- `safe_extract()`: Robust element extraction with multiple fallbacks
- `debug_page_structure()`: Analyzes page HTML for troubleshooting

## 🚨 Troubleshooting

### Common Issues

1. **"No job cards found"**: CSS selectors may have changed - run debug mode
2. **Chrome driver errors**: Ensure Chrome browser is installed
3. **Slow performance**: Increase delays in configuration
4. **Missing data**: Check if Wuzzuf has updated their HTML structure

### Debug Mode

The scraper includes built-in debugging:
- Run `test_scraper.py` to analyze page structure
- Check console output for element detection issues
- Use `debug_page_structure()` method for detailed analysis

## 📝 Example Output

```json
{
  "title": "Senior Software Engineer",
  "company": "Tech Company",
  "location": "Cairo, Egypt",
  "job_type": "Full Time",
  "experience_level": "5 - 10 Yrs of Exp",
  "skills": ["Python", "JavaScript", "React", "Django"],
  "posting_date": "2 days ago",
  "application_link": "https://wuzzuf.net/jobs/...",
  "scraped_at": "2024-01-15 14:30:00"
}
```

## 🤝 Contributing

This scraper is designed to be maintainable and adaptable to Wuzzuf's changing HTML structure. When updating:

1. Test with `test_scraper.py` first
2. Update CSS selectors in the extraction methods
3. Maintain the clean, debug-free output
4. Keep the multiple fallback strategies

## 📄 License

This project is for educational and research purposes. Please respect Wuzzuf's terms of service and implement respectful scraping practices.
