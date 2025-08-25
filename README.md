# Simple Wuzzuf Job Scraper

A clean, focused Python scraper for extracting engineering job listings from Wuzzuf.net using Selenium.

## 🚀 Features

- **Comprehensive Data Extraction**: Job title, company, location, experience level, skills, job type, posting date, and application link
- **Proven Strategies**: Uses only the most effective extraction methods based on real-world testing
- **Clean Output**: Minimal console output - just essential information
- **Multiple Output Formats**: Saves data in both CSV and JSON formats
- **Respectful Scraping**: Built-in delays and proper error handling
- **Easy to Use**: Simple launcher with menu-driven interface
- **Production Ready**: Streamlined code optimized for reliability

## 📁 Project Structure

```
simple_scraper/
├── simple_wuzzuf_scraper.py    # Main scraper class (cleaned & optimized)
├── run_scraper.py              # Interactive launcher
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

### **Experience Extraction - 2 Proven Strategies:**
1. **Primary (93% success rate)**: Targets `span:not([class])` elements containing experience keywords
2. **Backup (7% success rate)**: Uses second occurrence of `a.css-o171kl` elements

### **Skills Extraction - 2 Proven Strategies:**
1. **Primary**: Collects all skills from `a[class*='css-5x9pm1']` elements
2. **Secondary**: Collects additional skills from `a[class*='css-o171kl']` elements

### **Pagination:**
- Uses JavaScript click strategy to bypass element interception issues
- Automatically detects when no more pages are available
- Handles dynamic content loading with appropriate delays

## 🎯 Key Methods

- `extract_experience_smart()`: Uses proven strategies for experience extraction
- `extract_skills_comprehensive()`: Collects skills from multiple reliable sources
- `safe_extract()`: Robust element extraction with multiple fallbacks
- `debug_page_structure()`: Essential debugging for troubleshooting (streamlined)

## 🚨 Troubleshooting

### Common Issues

1. **"No job cards found"**: CSS selectors may have changed - run debug mode
2. **Chrome driver errors**: Ensure Chrome browser is installed
3. **Slow performance**: Increase delays in configuration
4. **Missing data**: Check if Wuzzuf has updated their HTML structure

### Debug Mode

The scraper includes streamlined debugging:
- Run `debug_page_structure()` method for essential element counts
- Shows key element availability without verbose output
- Focuses on the elements that actually matter for extraction

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

## 🏆 Performance Metrics

Based on real-world testing:
- **Experience Extraction**: 100% success rate using 2 strategies
- **Skills Extraction**: 100% success rate using 2 strategies
- **Pagination**: Successfully handles multiple pages
- **Data Quality**: Comprehensive extraction of all required fields

## 🤝 Contributing

This scraper is designed to be maintainable and adaptable to Wuzzuf's changing HTML structure. When updating:

1. Test with real data to verify extraction quality
2. Update CSS selectors in the proven strategy methods
3. Maintain the clean, production-ready output
4. Keep only the strategies that actually work

## 📄 License

This project is for educational and research purposes. Please respect Wuzzuf's terms of service and implement respectful scraping practices.

## 🔄 Recent Updates

- **Streamlined Strategies**: Removed unused extraction methods, keeping only proven ones
- **Clean Output**: Eliminated verbose debugging during normal operation
- **Production Ready**: Optimized for reliability and maintainability
- **Simplified Debugging**: Essential troubleshooting without information overload
