import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional, Tuple
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class BrowserAutomation:
    """Handles browser automation and problem data extraction"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.driver = None
    
    def setup_webdriver(self) -> bool:
        """Setup Chrome WebDriver for browser automation"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            # Uncomment the line below if you want to run headless
            # chrome_options.add_argument("--headless")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"Failed to setup WebDriver: {e}")
            print("Make sure Chrome and ChromeDriver are installed")
            return False
    
    def get_active_codeforces_tab(self) -> Optional[str]:
        """Get the URL of the active Codeforces tab"""
        try:
            if not self.driver:
                if not self.setup_webdriver():
                    return None
            
            # Get current URL
            current_url = self.driver.current_url
            
            # Check if it's a Codeforces problem page
            if self.is_codeforces_problem_url(current_url):
                return current_url
            
            # If not, try to find a Codeforces tab
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                url = self.driver.current_url
                if self.is_codeforces_problem_url(url):
                    return url
            
            return None
            
        except Exception as e:
            print(f"Failed to get active Codeforces tab: {e}")
            return None
    
    def is_codeforces_problem_url(self, url: str) -> bool:
        """Check if URL is a Codeforces problem page"""
        patterns = [
            r'codeforces\.com/problemset/problem/\d+/[A-Z]',
            r'codeforces\.com/contest/\d+/problem/[A-Z]',
            r'codeforces\.com/gym/\d+/problem/[A-Z]'
        ]
        
        for pattern in patterns:
            if re.search(pattern, url):
                return True
        return False
    
    def extract_problem_data_from_browser(self) -> Optional[Dict[str, Any]]:
        """Extract problem data from the currently active browser tab"""
        try:
            if not self.driver:
                if not self.setup_webdriver():
                    return None
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract problem information
            problem_data = {}
            
            # Problem title
            try:
                title_elem = self.driver.find_element(By.CSS_SELECTOR, "div.title")
                problem_data['problem_name'] = title_elem.text.strip()
            except:
                problem_data['problem_name'] = "Unknown Problem"
            
            # Contest name
            try:
                contest_elem = self.driver.find_element(By.CSS_SELECTOR, "a[href*='/contest/']")
                problem_data['contest_name'] = contest_elem.text.strip()
            except:
                problem_data['contest_name'] = "Unknown Contest"
            
            # Difficulty
            try:
                difficulty_elem = self.driver.find_element(By.CSS_SELECTOR, "span.difficulty")
                problem_data['difficulty'] = difficulty_elem.text.strip()
            except:
                problem_data['difficulty'] = "Unknown"
            
            # Time and memory limits
            try:
                limits_elem = self.driver.find_element(By.CSS_SELECTOR, "div.time-limit")
                limits_text = limits_elem.text
                time_match = re.search(r'(\d+)\s*second', limits_text)
                if time_match:
                    problem_data['time_limit'] = f"{time_match.group(1)} second"
            except:
                problem_data['time_limit'] = "2 seconds"
            
            try:
                memory_elem = self.driver.find_element(By.CSS_SELECTOR, "div.memory-limit")
                memory_text = memory_elem.text
                memory_match = re.search(r'(\d+)\s*megabytes', memory_text)
                if memory_match:
                    problem_data['memory_limit'] = f"{memory_match.group(1)} megabytes"
            except:
                problem_data['memory_limit'] = "256 megabytes"
            
            # Extract test cases
            test_cases = self.extract_test_cases_from_browser()
            problem_data['test_cases'] = test_cases
            
            # URL
            problem_data['url'] = self.driver.current_url
            
            return problem_data
            
        except Exception as e:
            print(f"Failed to extract problem data from browser: {e}")
            return None
    
    def extract_test_cases_from_browser(self) -> list:
        """Extract test cases from the browser page"""
        test_cases = []
        
        try:
            # Find input and output sections
            input_sections = self.driver.find_elements(By.CSS_SELECTOR, "div.input")
            output_sections = self.driver.find_elements(By.CSS_SELECTOR, "div.output")
            
            for i, (input_section, output_section) in enumerate(zip(input_sections, output_sections)):
                # Extract input
                try:
                    input_pre = input_section.find_element(By.TAG_NAME, "pre")
                    input_data = input_pre.text
                except:
                    input_data = ""
                
                # Extract output
                try:
                    output_pre = output_section.find_element(By.TAG_NAME, "pre")
                    output_data = output_pre.text
                except:
                    output_data = ""
                
                test_cases.append({
                    'input': input_data.strip(),
                    'output': output_data.strip()
                })
        
        except Exception as e:
            print(f"Failed to extract test cases from browser: {e}")
        
        return test_cases
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def extract_problem_id_from_url(self, url: str) -> Optional[str]:
        """Extract problem ID from a Codeforces URL"""
        try:
            # Handle different URL formats
            patterns = [
                r'codeforces\.com/problemset/problem/(\d+)/([A-Z])',
                r'codeforces\.com/contest/(\d+)/problem/([A-Z])',
                r'codeforces\.com/gym/(\d+)/problem/([A-Z])'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    contest_id = match.group(1)
                    problem_letter = match.group(2)
                    return f"{contest_id}{problem_letter}"
            
            return None
            
        except Exception as e:
            print(f"Failed to extract problem ID from URL: {e}")
            return None
    
    def get_problem_data(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """Get problem data from Codeforces (fallback method)"""
        try:
            # Determine if it's a contest problem or practice problem
            if len(problem_id) >= 2:
                contest_id = problem_id[:-1]
                problem_letter = problem_id[-1]
                
                # Try contest URL first
                url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_letter}"
                data = self.fetch_problem_page(url)
                
                if data:
                    data['contest_type'] = 'contest'
                    return data
                
                # Try problemset URL
                url = f"https://codeforces.com/problemset/problem/{contest_id}/{problem_letter}"
                data = self.fetch_problem_page(url)
                
                if data:
                    data['contest_type'] = 'practice'
                    return data
            
            return None
            
        except Exception as e:
            print(f"Failed to get problem data: {e}")
            return None
    
    def fetch_problem_page(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch and parse a problem page (fallback method)"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract problem information
            problem_data = {}
            
            # Problem title
            title_elem = soup.find('div', class_='title')
            if title_elem:
                problem_data['problem_name'] = title_elem.get_text().strip()
            
            # Contest name
            contest_elem = soup.find('a', href=re.compile(r'/contest/\d+'))
            if contest_elem:
                problem_data['contest_name'] = contest_elem.get_text().strip()
            
            # Difficulty
            difficulty_elem = soup.find('span', class_='difficulty')
            if difficulty_elem:
                difficulty_text = difficulty_elem.get_text().strip()
                problem_data['difficulty'] = difficulty_text
            
            # Time and memory limits
            limits_elem = soup.find('div', class_='time-limit')
            if limits_elem:
                limits_text = limits_elem.get_text()
                time_match = re.search(r'(\d+)\s*second', limits_text)
                if time_match:
                    problem_data['time_limit'] = f"{time_match.group(1)} second"
            
            memory_elem = soup.find('div', class_='memory-limit')
            if memory_elem:
                memory_text = memory_elem.get_text()
                memory_match = re.search(r'(\d+)\s*megabytes', memory_text)
                if memory_match:
                    problem_data['memory_limit'] = f"{memory_match.group(1)} megabytes"
            
            # Extract test cases
            test_cases = self.extract_test_cases(soup)
            problem_data['test_cases'] = test_cases
            
            # URL
            problem_data['url'] = url
            
            return problem_data
            
        except Exception as e:
            print(f"Failed to fetch problem page {url}: {e}")
            return None
    
    def extract_test_cases(self, soup: BeautifulSoup) -> list:
        """Extract test cases from the problem page (fallback method)"""
        test_cases = []
        
        try:
            # Find input and output sections
            input_sections = soup.find_all('div', class_='input')
            output_sections = soup.find_all('div', class_='output')
            
            for i, (input_section, output_section) in enumerate(zip(input_sections, output_sections)):
                # Extract input
                input_pre = input_section.find('pre')
                input_data = input_pre.get_text() if input_pre else ""
                
                # Extract output
                output_pre = output_section.find('pre')
                output_data = output_pre.get_text() if output_pre else ""
                
                test_cases.append({
                    'input': input_data.strip(),
                    'output': output_data.strip()
                })
        
        except Exception as e:
            print(f"Failed to extract test cases: {e}")
        
        return test_cases
    
    def get_active_browser_url(self) -> Optional[str]:
        """Get the URL from the active browser tab"""
        return self.get_active_codeforces_tab()
    
    def parse_problem_id_input(self, user_input: str) -> Optional[str]:
        """Parse problem ID from various input formats"""
        try:
            # If it's already a problem ID (e.g., "1850A")
            if re.match(r'^\d+[A-Z]$', user_input):
                return user_input
            
            # If it's a URL
            if user_input.startswith('http'):
                return self.extract_problem_id_from_url(user_input)
            
            # If it's contest_id/problem_letter format
            if '/' in user_input:
                parts = user_input.split('/')
                if len(parts) == 2 and parts[0].isdigit() and len(parts[1]) == 1:
                    return f"{parts[0]}{parts[1]}"
            
            return None
            
        except Exception as e:
            print(f"Failed to parse problem ID input: {e}")
            return None 