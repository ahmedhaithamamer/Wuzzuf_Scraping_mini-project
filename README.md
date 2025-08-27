# 🚀 Wuzzuf Job Scraper Pro

A professional, integrated GUI application for scraping job listings from Wuzzuf.net with advanced data analysis and visualization capabilities.

## ✨ Features

### 🔍 **Advanced Scraping**
- **Configurable Search**: Custom keywords, locations, and page limits
- **Real-time Monitoring**: Live progress tracking and detailed logging
- **Headless Mode**: Option to run without browser window
- **Multi-threaded**: Non-blocking scraping with responsive UI
- **Smart Pagination**: Intelligent page navigation and duplicate detection

### 📊 **Data Analysis**
- **Interactive Data Viewer**: Clean table display with scrollbars
- **Advanced Filtering**: Search across all columns or specific fields
- **Real-time Statistics**: Row counts, data types, and memory usage
- **Export Functionality**: Save filtered or complete datasets (CSV/JSON)
- **Data Visualization**: Interactive charts and graphs
- **Market Insights**: Automated analysis and trend identification
- **Chart Export**: Save visualizations in multiple formats (PNG, PDF, SVG)

### 🎨 **Modern Interface**
- **Professional Design**: Dark theme with modern color scheme and animations
- **Tabbed Interface**: Organized sections for different functions
- **Responsive Layout**: Adapts to different window sizes
- **Status Monitoring**: Real-time feedback, progress updates, and live notifications
- **Enhanced Header**: Quick stats display and animated title
- **Live Clock**: Real-time clock display in status bar

## 🏗️ Architecture

The application is built with a modular architecture:

```
wuzzuf_gui.py          # Main GUI application with integrated scraper
simple_wuzzuf_scraper.py # Core scraping engine
read_csv.py            # Simple launcher script
simple_config.py       # Configuration settings
requirements.txt       # Python dependencies
```

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone or download the project
cd Wuzzuf_Scraping_mini-project

# Install dependencies
pip install -r requirements.txt
```

### 2. **Launch the Application**
```bash
# Option 1: Use the launcher
python read_csv.py

# Option 2: Direct launch
python wuzzuf_gui.py
```

### 3. **First Run**
- The application will automatically detect existing CSV files
- Navigate to the **🔍 Scraping** tab to start collecting new data
- Use the **📊 Data Viewer** tab to analyze existing data
- Explore the **📈 Analytics** tab for data visualization and insights

## 📖 Usage Guide

### **Scraping Jobs**

1. **Configure Search Parameters**:
   - Enter search keyword (e.g., "software engineering")
   - Optionally specify location
   - Set maximum pages to scrape
   - Choose headless mode if desired

2. **Start Scraping**:
   - Click "🚀 Start Scraping"
   - Monitor progress in real-time
   - View detailed logs of the scraping process

3. **Monitor Progress**:
   - Progress bar shows completion status
   - Live log updates with timestamps
   - Status bar displays current operation

### **Analyzing Data**

1. **Load Data**:
   - Automatically loads latest scraped data
   - Browse and load any CSV file
   - View file statistics and metadata

2. **Search & Filter**:
   - Real-time search across all columns
   - Column-specific filtering
   - Clear filters to restore original view

3. **Export Results**:
   - Export filtered data only
   - Export complete dataset
   - Choose output format and location

### **Configuration**

1. **Settings Tab**:
   - Customize engineering fields
   - Save configuration preferences
   - View application information

2. **Auto-save**:
   - Scraped data automatically saved with timestamps
   - Configuration changes persist between sessions

## 🔧 Technical Details

### **Dependencies**
- **Python 3.8+**: Core runtime
- **Selenium**: Web scraping automation
- **Pandas**: Data manipulation and analysis
- **CustomTkinter**: Modern GUI framework with beautiful styling
- **WebDriver Manager**: Automatic Chrome driver management

### **Browser Requirements**
- **Google Chrome**: Required for Selenium automation
- **ChromeDriver**: Automatically managed by webdriver-manager

### **Performance Features**
- **Lazy Loading**: Shows first 1000 rows for performance
- **Background Processing**: Non-blocking scraping operations
- **Memory Management**: Efficient data handling for large datasets

## 🛠️ Customization

### **Modifying Scraping Logic**
Edit `simple_wuzzuf_scraper.py` to:
- Change CSS selectors for different websites
- Modify data extraction patterns
- Add new data fields

### **GUI Customization**
Edit `wuzzuf_gui.py` to:
- Change color schemes
- Add new tabs or sections
- Modify layout and styling

### **Configuration**
Edit `simple_config.py` to:
- Set default search parameters
- Configure output preferences
- Define engineering fields

## 🚨 Troubleshooting

### **Common Issues**

1. **Chrome Driver Errors**:
   ```bash
   # Reinstall webdriver-manager
   pip uninstall webdriver-manager
   pip install webdriver-manager
   ```

2. **Import Errors**:
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

3. **Scraping Fails**:
   - Check internet connection
   - Verify Wuzzuf.net is accessible
   - Try different search keywords
   - Check browser console for errors

### **Debug Mode**
- Enable detailed logging in the scraping tab
- Check the log output for specific error messages
- Use the debug methods in the scraper class

## 📝 File Structure

```
Wuzzuf_Scraping_mini-project/
├── wuzzuf_gui.py              # Main GUI application
├── simple_wuzzuf_scraper.py   # Core scraping engine
├── read_csv.py                # Launcher script
├── simple_config.py           # Configuration file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── *.csv                      # Scraped data files
└── *.json                     # Scraped data files (JSON format)
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with Python, Selenium, and CustomTkinter
- Inspired by the need for efficient job market analysis
- Designed for researchers, recruiters, and job seekers

---

**Happy Scraping! 🎉**

For support or questions, please check the troubleshooting section or create an issue in the repository.
