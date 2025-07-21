import os
from typing import Dict, Any, Optional
from src.utils.config_parser import ConfigParser
from src.utils.file_utils import FileUtils
from src.template_manager import TemplateManager
from src.file_opener import FileOpener

class ProblemCreator:
    """Main class that coordinates problem creation"""
    
    def __init__(self, config: ConfigParser):
        self.config = config
        self.template_manager = TemplateManager(config.get('template_directory'))
        self.file_opener = FileOpener(config.get_editor_config())
        self.file_naming = config.get_file_naming()
    
    def create_problem(self, problem_id: str, problem_data: Dict[str, Any]) -> bool:
        """Create a complete problem setup from browser extension/server workflow"""
        try:
            print(f"Creating problem: {problem_id}")
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
            self.create_test_case_files(problem_dir, problem_data.get('test_cases', []))
            # Create metadata file
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