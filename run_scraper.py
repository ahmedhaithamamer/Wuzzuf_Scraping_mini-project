#!/usr/bin/env python3
"""
Simple Launcher for Wuzzuf Job Scraper
Easy way to run the scraper with different settings
"""

import os
import sys
from simple_wuzzuf_scraper import SimpleWuzzufScraper

def show_menu():
    """Show the main menu"""
    print("🚀 Wuzzuf Job Scraper - Simple Launcher")
    print("=" * 50)
    print("Choose an option:")
    print("1. 🎯 Quick Search (software engineering)")
    print("2. 🏢 Location Search (Cairo)")
    print("3. 🔧 Custom Search")
    print("4. 📊 Show Current Data")
    print("5. ⚙️  Show Current Config")
    print("6. 🚪 Exit")
    print("=" * 50)

def quick_search():
    """Run a quick software engineering search"""
    print("\n🔍 Quick Search: Software Engineering")
    print("-" * 40)
    
    scraper = SimpleWuzzufScraper(headless=False)
    
    try:
        scraper.search_jobs(
            keyword="software engineering",
            location="",
            max_pages=2
        )
        scraper.save_data("quick_search")
        print("✅ Quick search completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def location_search():
    """Run a location-specific search"""
    print("\n🏢 Location Search: Cairo")
    print("-" * 40)
    
    scraper = SimpleWuzzufScraper(headless=False)
    
    try:
        scraper.search_jobs(
            keyword="engineering",
            location="Cairo",
            max_pages=2
        )
        scraper.save_data("cairo_search")
        print("✅ Cairo search completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def custom_search():
    """Run a custom search with user input"""
    print("\n🔧 Custom Search")
    print("-" * 40)
    
    # Get user input
    keyword = input("Enter search keyword (e.g., 'mechanical engineering'): ").strip()
    if not keyword:
        keyword = "engineering"
    
    location = input("Enter location (leave empty for all): ").strip()
    
    try:
        max_pages = int(input("Enter number of pages (1-10): ").strip())
        if max_pages < 1 or max_pages > 10:
            max_pages = 3
    except ValueError:
        max_pages = 3
    
    headless = input("Run in background? (y/n): ").strip().lower() == 'y'
    
    print(f"\n🔍 Searching: {keyword} in {location or 'All locations'} ({max_pages} pages)")
    
    scraper = SimpleWuzzufScraper(headless=headless)
    
    try:
        scraper.search_jobs(
            keyword=keyword,
            location=location,
            max_pages=max_pages
        )
        scraper.save_data("custom_search")
        print("✅ Custom search completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_config():
    """Show current configuration"""
    print("\n⚙️  Current Configuration")
    print("-" * 40)
    
    try:
        from simple_config import SEARCH_KEYWORD, LOCATION, MAX_PAGES, HEADLESS_MODE
        
        print(f"Search Keyword: {SEARCH_KEYWORD}")
        print(f"Location: {LOCATION or 'All locations'}")
        print(f"Max Pages: {MAX_PAGES}")
        print(f"Headless Mode: {HEADLESS_MODE}")
        
    except ImportError:
        print("⚠️ Configuration file not found")
        print("Using default settings:")
        print("Search Keyword: software engineering")
        print("Location: All locations")
        print("Max Pages: 3")
        print("Headless Mode: False")

def show_current_data():
    """Show current data files in the directory"""
    print("\n📊 Current Data Files")
    print("-" * 40)
    
    try:
        # Check for CSV and JSON files
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        json_files = [f for f in os.listdir('.') if f.endswith('.json')]
        
        if csv_files:
            print("📄 CSV Files:")
            for file in sorted(csv_files, reverse=True)[:5]:  # Show last 5
                file_size = os.path.getsize(file) / 1024  # KB
                print(f"  • {file} ({file_size:.1f} KB)")
        else:
            print("📄 No CSV files found")
            
        if json_files:
            print("\n📋 JSON Files:")
            for file in sorted(json_files, reverse=True)[:5]:  # Show last 5
                file_size = os.path.getsize(file) / 1024  # KB
                print(f"  • {file} ({file_size:.1f} KB)")
        else:
            print("📋 No JSON files found")
            
    except Exception as e:
        print(f"❌ Error checking data files: {e}")

def main():
    """Main launcher function"""
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                quick_search()
            elif choice == "2":
                location_search()
            elif choice == "3":
                custom_search()
            elif choice == "4":
                show_current_data()
            elif choice == "5":
                show_config()
            elif choice == "6":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
            
            if choice in ["1", "2", "3", "4"]:
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
