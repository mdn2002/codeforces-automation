import os
import shutil
from typing import List, Optional
from datetime import datetime

class FileUtils:
    """Utility class for file and directory operations"""
    
    @staticmethod
    def ensure_directory(path: str) -> str:
        """Ensure a directory exists, create if it doesn't"""
        os.makedirs(path, exist_ok=True)
        return path
    
    @staticmethod
    def create_problem_directory(base_path: str, problem_id: str) -> str:
        """Create a directory for a specific problem"""
        problem_dir = os.path.join(base_path, problem_id)
        return FileUtils.ensure_directory(problem_dir)
    
    @staticmethod
    def write_file(file_path: str, content: str) -> bool:
        """Write content to a file"""
        try:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Failed to write file {file_path}: {e}")
            return False
    
    @staticmethod
    def read_file(file_path: str) -> Optional[str]:
        """Read content from a file"""
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Failed to read file {file_path}: {e}")
            return None
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists"""
        return os.path.exists(file_path)
    
    @staticmethod
    def directory_exists(dir_path: str) -> bool:
        """Check if a directory exists"""
        return os.path.exists(dir_path) and os.path.isdir(dir_path)
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """List files in a directory matching a pattern"""
        try:
            if not os.path.exists(directory):
                return []
            
            files = []
            for file in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, file)):
                    if pattern == "*" or file.endswith(pattern):
                        files.append(file)
            return sorted(files)
        except Exception as e:
            print(f"Failed to list files in {directory}: {e}")
            return []
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get the file extension"""
        return os.path.splitext(file_path)[1]
    
    @staticmethod
    def get_filename_without_extension(file_path: str) -> str:
        """Get filename without extension"""
        return os.path.splitext(os.path.basename(file_path))[0]
    
    @staticmethod
    def copy_file(src: str, dst: str) -> bool:
        """Copy a file from src to dst"""
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            print(f"Failed to copy file from {src} to {dst}: {e}")
            return False
    
    @staticmethod
    def get_current_date() -> str:
        """Get current date in YYYY-MM-DD format"""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_current_datetime() -> str:
        """Get current date and time in ISO format"""
        return datetime.now().isoformat()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize a filename by removing invalid characters"""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove leading/trailing spaces and dots
        filename = filename.strip('. ')
        
        return filename 