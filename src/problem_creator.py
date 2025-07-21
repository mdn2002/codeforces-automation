import os
from typing import Dict, Any, Optional
from utils.config_parser import ConfigParser
from utils.file_utils import FileUtils
from template_manager import TemplateManager
from file_opener import FileOpener
from browser_automation import BrowserAutomation

class ProblemCreator:
    """Main class that coordinates problem creation"""
    
    def __init__(self, config: ConfigParser):
        self.config = config
        self.template_manager = TemplateManager(config.get('template_directory'))
        self.file_opener = FileOpener(config.get_editor_config())
        self.browser_automation = BrowserAutomation()
        self.file_naming = config.get_file_naming()
    
    def create_problem(self, problem_id: str, problem_data: Optional[Dict[str, Any]] = None) -> bool:
        """Create a complete problem setup"""
        try:
            print(f"Creating problem: {problem_id}")
            
            # Get problem data if not provided
            if not problem_data:
                problem_data = self.browser_automation.get_problem_data(problem_id)
                if not problem_data:
                    print(f"Failed to get problem data for {problem_id}")
                    print("Creating basic problem structure with minimal data...")
                    # Create basic problem data as fallback
                    problem_data = self.create_basic_problem_data(problem_id)
            
            # Add problem ID to data
            problem_data['problem_id'] = problem_id
            problem_data['language'] = self.config.get('default_language', 'cpp')
            
            # Create problem directory
            output_dir = self.config.get('output_directory')
            problem_dir = FileUtils.create_problem_directory(output_dir, problem_id)
            
            print(f"Created problem directory: {problem_dir}")
            
            # Create solution file
            solution_file = os.path.join(problem_dir, self.file_naming.get('solution_file', 'solution.cpp'))
            if not self.template_manager.create_solution_file(problem_data, solution_file):
                print("Failed to create solution file")
                return False
            
            print(f"Created solution file: {solution_file}")
            
            # Create test case files
            if self.config.get('auto_download_testcases', True):
                self.create_test_case_files(problem_dir, problem_data.get('test_cases', []))
            
            # Create metadata file
            if self.config.get('create_metadata', True):
                metadata_file = os.path.join(problem_dir, self.file_naming.get('metadata_file', 'metadata.json'))
                if not self.template_manager.create_metadata_file(problem_data, metadata_file):
                    print("Failed to create metadata file")
                    return False
                
                print(f"Created metadata file: {metadata_file}")
            
            # Open files if configured
            if self.config.get('auto_open_files', True):
                self.file_opener.open_problem_files(problem_dir, problem_id, self.file_naming)
            
            print(f"Successfully created problem: {problem_id}")
            return True
            
        except Exception as e:
            print(f"Failed to create problem {problem_id}: {e}")
            return False
    
    def create_test_case_files(self, problem_dir: str, test_cases: list) -> None:
        """Create test case input and output files"""
        try:
            input_prefix = self.file_naming.get('input_prefix', 'in')
            output_prefix = self.file_naming.get('output_prefix', 'out')
            start_number = self.config.get('test_cases.start_number', 1)
            
            for i, test_case in enumerate(test_cases, start_number):
                # Create input file
                input_file = os.path.join(problem_dir, f"{input_prefix}{i}")
                if FileUtils.write_file(input_file, test_case.get('input', '')):
                    print(f"Created input file: {input_file}")
                
                # Create output file
                output_file = os.path.join(problem_dir, f"{output_prefix}{i}")
                if FileUtils.write_file(output_file, test_case.get('output', '')):
                    print(f"Created output file: {output_file}")
        
        except Exception as e:
            print(f"Failed to create test case files: {e}")
    
    def create_problem_from_input(self, user_input: str) -> bool:
        """Create problem from user input (problem ID, URL, etc.)"""
        try:
            # Parse the input to get problem ID
            problem_id = self.browser_automation.parse_problem_id_input(user_input)
            if not problem_id:
                print(f"Could not parse problem ID from input: {user_input}")
                return False
            
            return self.create_problem(problem_id)
            
        except Exception as e:
            print(f"Failed to create problem from input: {e}")
            return False
    
    def create_problem_interactive(self) -> bool:
        """Interactive mode to create a problem"""
        try:
            print("Codeforces Problem Creator")
            print("=" * 30)
            
            # Get problem ID from user
            problem_input = input("Enter problem ID, URL, or contest/problem (e.g., 1850A, https://codeforces.com/contest/1850/problem/A, 1850/A): ").strip()
            
            if not problem_input:
                print("No input provided")
                return False
            
            return self.create_problem_from_input(problem_input)
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return False
        except Exception as e:
            print(f"Failed in interactive mode: {e}")
            return False
    
    def list_created_problems(self) -> list:
        """List all created problems"""
        try:
            output_dir = self.config.get('output_directory')
            if not os.path.exists(output_dir):
                return []
            
            problems = []
            for item in os.listdir(output_dir):
                item_path = os.path.join(output_dir, item)
                if os.path.isdir(item_path):
                    problems.append(item)
            
            return sorted(problems)
            
        except Exception as e:
            print(f"Failed to list problems: {e}")
            return []
    
    def get_problem_info(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a created problem"""
        try:
            output_dir = self.config.get('output_directory')
            problem_dir = os.path.join(output_dir, problem_id)
            
            if not os.path.exists(problem_dir):
                return None
            
            info = {
                'problem_id': problem_id,
                'directory': problem_dir,
                'files': []
            }
            
            # List files in the problem directory
            for file in os.listdir(problem_dir):
                file_path = os.path.join(problem_dir, file)
                if os.path.isfile(file_path):
                    info['files'].append(file)
            
            # Try to read metadata
            metadata_file = os.path.join(problem_dir, self.file_naming.get('metadata_file', 'metadata.json'))
            if os.path.exists(metadata_file):
                metadata_content = FileUtils.read_file(metadata_file)
                if metadata_content:
                    import json
                    try:
                        info['metadata'] = json.loads(metadata_content)
                    except:
                        pass
            
            return info
            
        except Exception as e:
            print(f"Failed to get problem info: {e}")
            return None
    
    def create_basic_problem_data(self, problem_id: str) -> Dict[str, Any]:
        """Create basic problem data when web scraping fails"""
        from datetime import datetime
        return {
            'problem_id': problem_id,
            'problem_name': f'Problem {problem_id}',
            'url': f'https://codeforces.com/problemset/problem/{problem_id[:-1]}/{problem_id[-1]}',
            'time_limit': '2 seconds',
            'memory_limit': '256 megabytes',
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'test_cases': [
                {
                    'input': '3\n4 4 5\n3 3 3\n1 1 1',
                    'output': 'YES\nNO\nNO'
                },
                {
                    'input': '2\n5 5 5\n2 2 2',
                    'output': 'YES\nNO'
                }
            ]
        }
    
    def create_problem_from_browser(self) -> bool:
        """Create problem from the currently active browser tab"""
        try:
            # Get the active Codeforces tab
            url = self.browser_automation.get_active_browser_url()
            if not url:
                print("No active Codeforces problem tab found")
                print("Please open a Codeforces problem in your browser")
                return False
            
            # Extract problem ID from URL
            problem_id = self.browser_automation.extract_problem_id_from_url(url)
            if not problem_id:
                print(f"Could not extract problem ID from URL: {url}")
                return False
            
            # Extract problem data from browser
            problem_data = self.browser_automation.extract_problem_data_from_browser()
            if not problem_data:
                print("Failed to extract problem data from browser")
                print("Falling back to basic problem structure...")
                problem_data = self.create_basic_problem_data(problem_id)
            
            return self.create_problem(problem_id, problem_data)
            
        except Exception as e:
            print(f"Failed to create problem from browser: {e}")
            return False 