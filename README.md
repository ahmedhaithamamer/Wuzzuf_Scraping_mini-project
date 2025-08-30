# 🚀 Wuzzuf Job Scraper Pro

**A simple and powerful tool to collect job listings from Wuzzuf.net with a beautiful, easy-to-use interface.**

## 🎯 What This Tool Does

This application helps you:
- **Find jobs** by searching keywords like "software engineer" or "data scientist"
- **Collect job details** automatically from Wuzzuf.net
- **View and analyze** all the jobs in a clean table format
- **Save your data** to CSV or JSON files for further analysis
- **Filter and search** through collected jobs easily

## 🚀 Getting Started (3 Simple Steps)

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed on your computer.

### Step 2: Download and Setup
```bash
# Download the project files
# Navigate to the project folder
cd Wuzzuf_Scraping_mini-project

# Install required packages
pip install -r requirements.txt
```

### Step 3: Run the App

You have **two ways** to run the project:

#### 🖥️ **Option 1: Beautiful GUI Interface (Recommended)**
```bash
python wuzzuf_gui.py
```
- **Best for**: Most users who want a visual interface
- **Features**: Full GUI with tabs, real-time progress, data viewer, and export options
- **What you get**: Modern interface with buttons, progress bars, and easy data management

#### 💻 **Option 2: Console Menu Interface**
```bash
python run_scraper.py
```
- **Best for**: Users who prefer command-line tools or want to automate scraping
- **Features**: Text-based menu with quick search options
- **What you get**: Simple menu to choose search type, run scraping, and view results

**Choose Option 1** if you want the full experience with a beautiful interface.
**Choose Option 2** if you prefer a simple console-based approach.

That's it! The app will open and you're ready to start.

## 📱 How to Use

### 🔍 **Step 1: Scrape Jobs**
1. Go to the **"🔍 Scraping"** tab
2. Type what you're looking for (e.g., "software engineering")
3. Optionally add a location (e.g., "Cairo")
4. Set how many pages to search (start with 5-10)
5. Click **"🚀 Start Scraping"**
6. Watch the progress bar and logs as it works

### 📊 **Step 2: View Your Data**
1. Go to the **"📊 Data Viewer"** tab
2. Your scraped jobs will appear in a table
3. Use the search box to find specific jobs
4. Scroll through all the collected data

### 💾 **Step 3: Save Your Data**
1. In the Data Viewer, click **"💾 Export Data"**
2. Choose CSV or JSON format
3. Pick where to save your file
4. Your data is now saved and ready to use!

## 🎨 What You'll See

### **GUI Interface (wuzzuf_gui.py)**
- **Dark, modern interface** that's easy on the eyes
- **Real-time progress** showing what the app is doing
- **Clean data table** with all job information
- **Search and filter** tools to find what you need
- **Automatic saving** so you never lose your data
- **Tabbed interface** for organized workflow

### **Console Interface (run_scraper.py)**
- **Simple text menu** with numbered options
- **Quick search presets** for common scenarios
- **Custom search input** for specific needs
- **Data file overview** showing what you've collected
- **Configuration display** of current settings
- **Lightweight** - perfect for servers or automation

## 📋 What Data You'll Get

For each job, you'll collect:
- **Job Title** (e.g., "Senior Software Engineer")
- **Company Name** (e.g., "TechCorp")
- **Location** (e.g., "Cairo, Egypt")
- **Job Type** (e.g., "Full-time", "Remote")
- **Experience Level** (e.g., "3-5 years")
- **Required Skills** (e.g., "Python, Django, SQL")
- **Posting Date** (when the job was posted)
- **Application Link** (direct link to apply)

## 🔧 If Something Goes Wrong

### **Common Issues & Solutions**

**Problem**: "Chrome driver not found"
**Solution**: The app will automatically download it for you. Just wait a moment.

**Problem**: "Can't connect to Wuzzuf"
**Solution**: Check your internet connection and try again.

**Problem**: "No jobs found"
**Solution**: Try different keywords or check if the website is working.

**Problem**: "App won't start"
**Solution**: Make sure you installed all requirements with `pip install -r requirements.txt`

## 📁 Your Files

After scraping, you'll find:
- **CSV files** with all job data (easy to open in Excel)
- **JSON files** with the same data (for developers)
- **Summary files** showing what was collected

All files are saved with timestamps so you can keep track of different scraping sessions.

## 💡 Tips for Best Results

1. **Start small**: Begin with 5-10 pages to test
2. **Use specific keywords**: "Python developer" works better than just "developer"
3. **Be patient**: Scraping takes time, especially for many pages
4. **Check the logs**: The app tells you exactly what it's doing
5. **Save regularly**: Export your data after each scraping session

## 🆘 Need Help?

- **Check the logs** in the app for error messages
- **Try different keywords** if no jobs are found
- **Restart the app** if something seems stuck
- **Check your internet** connection

## 🎉 You're All Set!

This tool makes it super easy to collect job market data from Wuzzuf.net. Whether you're:
- **Looking for a job** and want to see what's available
- **Researching the market** for your field
- **Analyzing trends** in job postings
- **Building a job database** for your company

...this tool has you covered!

**Happy job hunting! 🚀**

---

*Built with Python, Selenium, and CustomTkinter for a smooth, professional experience.*
