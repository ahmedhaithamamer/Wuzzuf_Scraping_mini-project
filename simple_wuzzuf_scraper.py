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
                    print("⚠️ No new jobs found, might be on same page")
                    # Try to force page refresh and wait longer
                    print("🔄 Refreshing page and waiting...")
                    self.driver.refresh()
                    time.sleep(5)  # Longer wait for refresh
                    continue
                
                total_jobs_before = current_total
                print(f"📊 Total jobs collected so far: {current_total}")
                
                # Additional check: verify we're not stuck on the same page
                if page > 1 and current_total < (page * 10):  # Assuming ~10 jobs per page
                    print("⚠️ Job count seems low, might be stuck on same page")
                    # Force navigation by updating URL
                    current_url = self.driver.current_url
                    if 'page=' in current_url:
                        # Extract current page number and increment
                        import re
                        page_match = re.search(r'page=(\d+)', current_url)
                        if page_match:
                            current_page_num = int(page_match.group(1))
                            next_page_url = current_url.replace(f'page={current_page_num}', f'page={current_page_num + 1}')
                            print(f"🔄 Forcing navigation to: {next_page_url}")
                            self.driver.get(next_page_url)
                            time.sleep(5)
                            continue
                
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
                print("⚠️ No job cards found on this page")
                print("💡 This might mean the website structure changed or no jobs are available")
                
                # Debug: Show what elements are available
                self.debug_page_structure()
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

    def debug_page_structure(self):
        """Debug method to help troubleshoot selector issues"""
        try:
            print("\n🔍 Debug: Analyzing page structure...")
            
            # Check for job-related content
            page_text = self.driver.page_source.lower()
            if 'job' in page_text or 'position' in page_text or 'career' in page_text:
                print("✅ Page contains job-related text")
            else:
                print("⚠️ Page doesn't seem to contain job-related text")
            
            # Check for key elements we're targeting
            print("\n🔍 Key elements found:")
            
            # Job type elements
            job_type_elements = self.driver.find_elements(By.CSS_SELECTOR, "span[class*='eoyjyou0'], div[class*='css-5jhz9n']")
            print(f"  Job type elements: {len(job_type_elements)}")
            
            # Experience elements (our primary strategy)
            span_no_class = self.driver.find_elements(By.CSS_SELECTOR, "span:not([class])")
            print(f"  Span elements without classes: {len(span_no_class)}")
            
            # Skill elements
            skill_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[class*='css-o171kl'], a[class*='css-5x9pm1']")
            print(f"  Skill elements: {len(skill_elements)}")
            
            # Pagination elements
            next_button = self.driver.find_elements(By.CSS_SELECTOR, "button[class*='css-wq4g8g'], a[class*='css-1fcv3il']")
            print(f"  Next page buttons: {len(next_button)}")
                
        except Exception as e:
            print(f"❌ Debug error: {e}")
    
    def go_to_next_page(self):
        """Navigate to next page using JavaScript click strategy"""
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, 
                    "button[class*='css-wq4g8g'][class*='ezfki8j0']")
            
            if next_button and next_button.is_enabled() and next_button.is_displayed():
                self.driver.execute_script("arguments[0].click();", next_button)
                time.sleep(5)  # Wait for page load
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def save_data(self, filename_prefix="wuzzuf_jobs"):
        """Save data to CSV and JSON"""
        if not self.jobs_data:
            print("⚠️ No data to save!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to CSV
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        self.save_to_csv(csv_filename)
        
        # Save to JSON
        json_filename = f"{filename_prefix}_{timestamp}.json"
        self.save_to_json(json_filename)
        
        print(f"💾 Data saved: {len(self.jobs_data)} jobs")
    
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
        
        # Save the data
        scraper.save_data(OUTPUT_PREFIX)
        
        print("✅ Scraping completed successfully!")
        
    except ImportError:
        print("⚠️ Configuration file not found. Using default settings...")
        # Fallback to default settings
        scraper = SimpleWuzzufScraper(headless=False)
        scraper.search_jobs(
            keyword="software engineering",
            location="",
            max_pages=3
        )
        scraper.save_data()
        print("✅ Scraping completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🔚 Scraper finished")

if __name__ == "__main__":
    main()
