import subprocess
import platform
import os
from typing import Dict, Any

class FileOpener:
    """Handles opening files in the user's preferred editor"""
    
    def __init__(self, editor_config: Dict[str, Any]):
        self.editor_config = editor_config
        self.editor_command = editor_config.get('command', 'code')
        self.editor_args = editor_config.get('args', [])
    
    def open_file(self, file_path: str) -> bool:
        """Open a file with the configured editor"""
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return False
            
            # Build the command
            cmd = [self.editor_command] + self.editor_args + [file_path]
            
            # Open the file
            subprocess.Popen(cmd, start_new_session=True)
            print(f"Opened file: {file_path}")
            return True
            
        except FileNotFoundError:
            print(f"Editor command not found: {self.editor_command}")
            print("Please check your editor configuration in settings.json")
            return False
        except Exception as e:
            print(f"Failed to open file {file_path}: {e}")
            return False
    
    def open_problem_files(self, problem_dir: str, problem_id: str, file_naming: Dict[str, str]) -> None:
        """Open relevant files after problem creation"""
        try:
            # Open solution file if configured
            if self.editor_config.get('open_solution', True):
                solution_file = os.path.join(problem_dir, file_naming.get('solution_file', 'solution.cpp'))
                if os.path.exists(solution_file):
                    self.open_file(solution_file)
                else:
                    print(f"Solution file not found: {solution_file}")
            
            # Optionally open first test case
            if self.editor_config.get('open_testcase', False):
                testcase_file = os.path.join(problem_dir, 'in1')
                if os.path.exists(testcase_file):
                    self.open_file(testcase_file)
            
            # Optionally open metadata
            if self.editor_config.get('open_metadata', False):
                metadata_file = os.path.join(problem_dir, file_naming.get('metadata_file', 'metadata.json'))
                if os.path.exists(metadata_file):
                    self.open_file(metadata_file)
        
        except Exception as e:
            print(f"Failed to open problem files: {e}")
    
    def test_editor_availability(self) -> bool:
        """Test if the configured editor is available"""
        try:
            # Try to run the editor command with --version or --help
            test_cmd = [self.editor_command]
            
            # Add common version flags
            if self.editor_command == 'code':
                test_cmd.append('--version')
            elif self.editor_command in ['vim', 'nvim']:
                test_cmd.append('--version')
            elif self.editor_command == 'subl':
                test_cmd.append('--version')
            else:
                test_cmd.append('--help')
            
            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=5)
            return result.returncode == 0
            
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False
    
    def get_available_editors(self) -> list:
        """Get a list of available editors on the system"""
        available_editors = []
        
        # Common editors to check
        editors = [
            ('code', 'Visual Studio Code'),
            ('subl', 'Sublime Text'),
            ('nvim', 'Neovim'),
            ('vim', 'Vim'),
            ('nano', 'Nano'),
            ('gedit', 'Gedit'),
            ('geany', 'Geany'),
            ('kate', 'Kate'),
            ('mousepad', 'Mousepad')
        ]
        
        for command, name in editors:
            try:
                result = subprocess.run([command, '--version'], 
                                      capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    available_editors.append((command, name))
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        return available_editors
    
    def suggest_editor(self) -> str:
        """Suggest an available editor if current one is not found"""
        available = self.get_available_editors()
        if available:
            return available[0][0]  # Return the first available editor
        return 'nano'  # Fallback to nano which is usually available 