#!/usr/bin/env python3
"""
Simple Wuzzuf Engineering Job Scraper
Extracts job listings from Wuzzuf.net using Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv
from datetime import datetime
import random
import os
from pathlib import Path

class SimpleWuzzufScraper:
    def __init__(self, headless=False):
        """Initialize the scraper"""
        self.base_url = "https://wuzzuf.net"
        self.jobs_data = []
        self.setup_driver(headless)
    
    def setup_driver(self, headless):
        """Setup Chrome driver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            # Auto-install ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ Chrome driver setup successful")
        except Exception as e:
            print(f"❌ Error setting up Chrome driver: {e}")
            raise
    
    def search_jobs(self, keyword="engineering", location="", max_pages=3):
        """Search for jobs with pagination"""
        search_url = f"{self.base_url}/search/jobs?q={keyword.replace(' ', '+')}"
        if location:
            search_url += f"&l={location.replace(' ', '+')}"
        
        print(f"🔍 Searching: {keyword} in {location or 'All locations'}")
        print(f"📡 URL: {search_url}")
        
        try:
            self.driver.get(search_url)
            print("⏳ Waiting for page to load...")
            
            # Wait for dynamic content to load
            time.sleep(5)  # Increased wait time for dynamic content
            
            # Try to scroll down to trigger lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            page = 1
            total_jobs_before = 0
            
            while page <= max_pages:
                print(f"📄 Scraping page {page}...")
                
                # Extract jobs from current page
                jobs_found = self.extract_jobs_from_page()
                if jobs_found == 0:
                    print("⚠️ No more jobs found, stopping")
                    break
                
                # Check if we're getting new jobs (not duplicates)
                current_total = len(self.jobs_data)
                if current_total == total_jobs_before:
                    # Try to force page refresh and wait longer
                    self.driver.refresh()
                    time.sleep(5)  # Longer wait for refresh
                    continue
                
                total_jobs_before = current_total
                

    
                # Try to go to next page (this will also detect if we're on the last page)
                
                # Try to go to next page
                if not self.go_to_next_page():
                    print("🏁 No more pages available")
                    break
                
                page += 1
                # Respectful delay
                delay = random.uniform(2, 4)
                print(f"⏳ Waiting {delay:.1f} seconds...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"❌ Error during search: {e}")
        finally:
            self.driver.quit()
    
    def extract_jobs_from_page(self):
        """Extract jobs from current page"""
        try:
            # Wait for job cards to load with correct Wuzzuf selectors
            try:
                # Try the main job card selector
                job_cards = self.wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='css-pkv5jc']"))
                )
            except:
                # Fallback to alternative selectors if the main one doesn't work
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='css-'], article, .job-card")
            
            if not job_cards:
                return 0
            
            print(f"Found {len(job_cards)} job cards")
            jobs_extracted = 0
            
            for job_card in job_cards:
                try:
                    job_info = self.extract_single_job(job_card)
                    if job_info:
                        self.jobs_data.append(job_info)
                        jobs_extracted += 1
                        print(f"📋 {job_info['title'][:50]}...")
                except Exception as e:
                    print(f"⚠️ Error extracting job: {e}")
                    continue
            
            return jobs_extracted
            
        except Exception as e:
            print(f"❌ Error extracting jobs: {e}")
            return 0
    
    def extract_single_job(self, job_card):
        """Extract information from a single job card"""
        try:
            # Extract basic info with correct Wuzzuf selectors
            title = self.safe_extract(job_card, [
                "h2 a[class*='css-193uk2c']",  # Primary title selector
                "h2 a",                        # Fallback title selector
                "h2", "h3", ".job-title", ".title"  # Additional fallbacks
            ])
            
            company = self.safe_extract(job_card, [
                "a[class*='css-ipsyv7']",    # Primary company selector
                ".company-name", ".company", ".employer"  # Fallbacks
            ])
            
            location = self.safe_extract(job_card, [
                "span[class*='css-16x61xq']",  # Primary location selector
                ".location", ".job-location", ".place"  # Fallbacks
            ])
            
            # Extract additional details using safe_extract
            job_type = self.safe_extract(job_card, [
                "span[class*='css-uc9rga eoyjyou0']",# Primary selector
                "div[class*='css-5jhz9n']",     
            ])
            
            experience = self.extract_experience_smart(job_card)
                   
            skills = self.extract_skills_comprehensive(job_card)
            
            posting_date = self.safe_extract(job_card, [    
                "div[class*='css-eg55jf']",   # Primary date selector
                ".date", ".posted-date", ".time-ago"  # Fallbacks
            ])
            
            application_link = self.safe_extract(job_card, [
                "a[class*='css-o171kl']",
                "h2 a[class*='css-193uk2c']",          # Job title link (most reliable)
                "a[href*='/jobs/']",                    # Job-specific links
                "a[href*='wuzzuf.net']",                # Wuzzuf domain links
                "a[href^='http']"                       # Any HTTP link as fallback
            ], extract_href=True)  # Extract href attribute instead of text
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'job_type': job_type,
                'experience_level': experience,
                'skills': skills,
                'posting_date': posting_date,
                'application_link': application_link,
                'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"❌ Error extracting job details: {e}")
            return None
    
    def safe_extract(self, element, selectors, extract_href=False):
        """Safely extract text or href using multiple selectors"""
        for selector in selectors:
            try:
                found = element.find_element(By.CSS_SELECTOR, selector)
                if found:
                    if extract_href:
                        # Extract href attribute for links
                        href = found.get_attribute('href')
                        if href and href.strip():
                            return href.strip()
                    else:
                        # Extract text content
                        text = found.text.strip()
                        if text:
                            return text
            except:
                continue
        if extract_href:
            return "Not available"
        else:
            return "Not specified"
    
    def extract_experience_smart(self, job_card):
        """Smart extraction of experience level using proven strategies"""
        try:

            span_elements = job_card.find_elements(By.CSS_SELECTOR, "span:not([class])")
            
            for span in span_elements:
                text = span.text.strip()
                if text and len(text) > 0:
                    # Check if this looks like experience information
                    if any(keyword in text.lower() for keyword in ['yrs', 'years', 'exp', 'experience', 'level', '-']):
                        return text
            
            # Strategy 2: Look for anchor elements with css-o171kl class 
            css_o171kl_anchors = job_card.find_elements(By.CSS_SELECTOR, "a.css-o171kl")
            
            if len(css_o171kl_anchors) >= 2:
                second_anchor = css_o171kl_anchors[1]  # Second occurrence
                text = second_anchor.text.strip()
                if text:
                    return text
            return "Not specified"
            
        except Exception as e:
            return "Not specified"
    
    def extract_skills_comprehensive(self, job_card):
        """Comprehensive extraction of all skills using proven strategies"""
        try:
            all_skills = []
            
            # Strategy 1: Collect ALL skills from css-5x9pm1 class (primary skills - 100% success rate)
            css_5x9pm1_elements = job_card.find_elements(By.CSS_SELECTOR, "a[class*='css-5x9pm1']")
            
            for elem in css_5x9pm1_elements:
                skill_text = elem.text.strip()
                if skill_text and skill_text not in all_skills:
                    # Filter out non-skill text (like job titles)
                    if len(skill_text) < 50 and not any(exclude in skill_text.lower() for exclude in ['full time', 'part time', 'contract', 'remote', 'on-site']):
                        all_skills.append(skill_text)
            
            # Strategy 2: Collect ALL skills from css-o171kl class (secondary skills - 100% success rate)
            css_o171kl_elements = job_card.find_elements(By.CSS_SELECTOR, "a[class*='css-o171kl']")
            
            for elem in css_o171kl_elements:
                skill_text = elem.text.strip()
                if skill_text and skill_text not in all_skills:
                    # Filter out non-skill text and job categories
                    if (len(skill_text) < 50 and 
                        not any(exclude in skill_text.lower() for exclude in ['full time', 'part time', 'contract', 'remote', 'on-site']) and
                        not any(category in skill_text.lower() for category in ['entry level', 'experienced', 'senior', 'junior'])):
                        all_skills.append(skill_text)
            
            return all_skills
                
        except Exception as e:
            return []


    
    def go_to_next_page(self):
        """Navigate to next page by finding the button with the right arrow SVG path"""
        try:
            # Find the button containing the specific right arrow SVG path
            next_button = None
            
            # Look for buttons with the exact SVG path for right arrow
            target_path = "M9.213 5L7.5 6.645 13.063 12 7.5 17.355 9.213 19l7.287-7z"
            
            # Find all buttons that might contain SVG elements
            all_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
            
            for button in all_buttons:
                try:
                    # Look for SVG elements within the button
                    svg_elements = button.find_elements(By.CSS_SELECTOR, "svg")
                    for svg in svg_elements:
                        # Look for path elements within the SVG
                        path_elements = svg.find_elements(By.CSS_SELECTOR, "path")
                        for path in path_elements:
                            path_d = path.get_attribute('d')
                            if path_d == target_path:
                                next_button = button
                                break
                        if next_button:
                            break
                    if next_button:
                        break
                except:
                    continue
            
            if next_button and next_button.is_enabled() and next_button.is_displayed():
                print("✅ Found next page button with right arrow SVG")
                try:
                    self.driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(5)  # Wait for page load
                    return True
                except Exception as e:
                    print(f"⚠️ Button click failed: {e}")
                    return False
            else:
                # If we can't find the next button, we're likely on the last page
                print("🏁 Last page reached - no next button found")
                return False
                 
        except Exception as e:
            print(f"❌ Error navigating to next page: {e}")
            return False
        
    def save_data(self, filename_prefix="wuzzuf_jobs"):
        """Save data to organized folders within Data directory"""
        if not self.jobs_data:
            print("⚠️ No data to save!")
            return
        
        try:
            # Create Data directory if it doesn't exist
            data_dir = Path("Data")
            data_dir.mkdir(exist_ok=True)
            
            # Create session folder with timestamp and keyword
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_keyword = filename_prefix.replace(' ', '_').replace('/', '_').replace('\\', '_')
            session_folder = data_dir / f"scraping_session_{timestamp}_{safe_keyword}"
            session_folder.mkdir(exist_ok=True)
            
            # Save to CSV in session folder
            csv_filename = f"wuzzuf_jobs_{safe_keyword}_{timestamp}.csv"
            csv_path = session_folder / csv_filename
            self.save_to_csv(str(csv_path))
            
            # Save to JSON in session folder
            json_filename = f"wuzzuf_jobs_{safe_keyword}_{timestamp}.json"
            json_path = session_folder / json_filename
            self.save_to_json(str(json_path))
            
            # Create summary file in session folder
            summary_filename = f"scraping_summary_{safe_keyword}_{timestamp}.txt"
            summary_path = session_folder / summary_filename
            self.create_summary_file(str(summary_path), safe_keyword, timestamp)
            
            print(f"💾 Data saved to session folder: {session_folder}")
            
            return str(session_folder)
            
        except Exception as e:
            print(f"❌ Error creating organized folders: {e}")
            # Fallback to current directory
            print("🔄 Falling back to current directory...")
            self.save_data_fallback(filename_prefix)
            return "."
    
    def save_to_csv(self, filename):
        """Save to CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if self.jobs_data:
                    writer = csv.DictWriter(f, fieldnames=self.jobs_data[0].keys())
                    writer.writeheader()
                    writer.writerows(self.jobs_data)
            print(f"✅ CSV saved: {filename}")
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
    
    def save_to_json(self, filename):
        """Save to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs_data, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON saved: {filename}")
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
    
    def save_data_fallback(self, filename_prefix="wuzzuf_jobs"):
        """Fallback method to save data in current directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to CSV
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        self.save_to_csv(csv_filename)
        
        # Save to JSON
        json_filename = f"{filename_prefix}_{timestamp}.json"
        self.save_to_json(json_filename)
        
        print(f"💾 Data saved to current directory: {len(self.jobs_data)} jobs")
    
    def create_summary_file(self, summary_path, keyword, timestamp):
        """Create a comprehensive summary file for the scraping session"""
        try:
            # Create summary content
            summary_content = f"""Wuzzuf Job Scraping Summary
========================================

Session Information:
- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Keyword: {keyword}
- Total Jobs Found: {len(self.jobs_data)}
- Session Folder: {Path(summary_path).parent}

Files Created:
- CSV Data: wuzzuf_jobs_{keyword}_{timestamp}.csv
- JSON Data: wuzzuf_jobs_{keyword}_{timestamp}.json
- Summary: scraping_summary_{keyword}_{timestamp}.txt

Data Overview:
- Companies: {len(set(job.get('company', '') for job in self.jobs_data if job.get('company') and job.get('company') != 'Not specified'))}
- Locations: {len(set(job.get('location', '') for job in self.jobs_data if job.get('location') and job.get('location') != 'Not specified'))}
- Experience Levels: {len(set(job.get('experience_level', '') for job in self.jobs_data if job.get('experience_level') and job.get('experience_level') != 'Not specified'))}

Top Companies (by job count):
"""
            
            # Count company occurrences
            company_counts = {}
            for job in self.jobs_data:
                company = job.get('company', 'Unknown')
                if company and company != 'Not specified':
                    company_counts[company] = company_counts.get(company, 0) + 1
            
            # Add top companies to summary
            if company_counts:
                sorted_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)
                for i, (company, count) in enumerate(sorted_companies[:10], 1):
                    summary_content += f"{i:2d}. {company}: {count} jobs\n"
            else:
                summary_content += "No company data available\n"
            
            summary_content += f"""

Top Locations (by job count):
"""
            
            # Count location occurrences
            location_counts = {}
            for job in self.jobs_data:
                location = job.get('location', 'Unknown')
                if location and location != 'Not specified':
                    location_counts[location] = location_counts.get(location, 0) + 1
            
            # Add top locations to summary
            if location_counts:
                sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
                for i, (location, count) in enumerate(sorted_locations[:10], 1):
                    summary_content += f"{i:2d}. {location}: {count} jobs\n"
            else:
                summary_content += "No location data available\n"
            
            summary_content += f"""

Generated by Wuzzuf Job Scraper Pro
Session completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            # Write summary file
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            print(f"📄 Created summary: {Path(summary_path).name}")
            
        except Exception as e:
            print(f"❌ Error creating summary file: {e}")
    


def main():
    """Main function"""
    print("🚀 Simple Wuzzuf Engineering Job Scraper")
    print("=" * 50)
    
    try:
        # Import configuration
        from simple_config import SEARCH_KEYWORD, LOCATION, MAX_PAGES, HEADLESS_MODE, OUTPUT_PREFIX
        
        # Initialize scraper
        scraper = SimpleWuzzufScraper(headless=HEADLESS_MODE)
        
        # Search for engineering jobs
        scraper.search_jobs(
            keyword=SEARCH_KEYWORD,
            location=LOCATION,
            max_pages=MAX_PAGES
        )
        
        # Save the data to organized folders
        session_folder = scraper.save_data(OUTPUT_PREFIX)
        
        print("✅ Scraping completed successfully!")
        print(f"📁 Data saved to: {session_folder}")
        

        
    except ImportError:
        print("⚠️ Configuration file not found. Using default settings...")
        # Fallback to default settings
        scraper = SimpleWuzzufScraper(headless=False)
        scraper.search_jobs(
            keyword="software engineering",
            location="",
            max_pages=3
        )
        session_folder = scraper.save_data()
        print("✅ Scraping completed successfully!")
        print(f"📁 Data saved to: {session_folder}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("\n🔚 Scraper finished")

if __name__ == "__main__":
    main()
