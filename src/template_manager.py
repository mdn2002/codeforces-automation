import os
from typing import Dict, Any, Optional
from utils.file_utils import FileUtils

class TemplateManager:
    """Handles template loading and customization with problem data"""
    
    def __init__(self, template_directory: str):
        self.template_directory = template_directory
        self.templates = {}
        self.load_templates()
    
    def load_templates(self) -> None:
        """Load all available templates from the template directory"""
        try:
            if not os.path.exists(self.template_directory):
                print(f"Template directory not found: {self.template_directory}")
                return
            
            for filename in os.listdir(self.template_directory):
                file_path = os.path.join(self.template_directory, filename)
                if os.path.isfile(file_path):
                    template_name = os.path.splitext(filename)[0]
                    content = FileUtils.read_file(file_path)
                    if content:
                        self.templates[template_name] = content
                        print(f"Loaded template: {template_name}")
        
        except Exception as e:
            print(f"Failed to load templates: {e}")
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get a template by name"""
        return self.templates.get(template_name)
    
    def list_templates(self) -> list:
        """List all available templates"""
        return list(self.templates.keys())
    
    def customize_template(self, template_name: str, variables: Dict[str, Any]) -> Optional[str]:
        """Customize a template with given variables"""
        template = self.get_template(template_name)
        if not template:
            print(f"Template not found: {template_name}")
            return None
        
        try:
            customized = template
            for key, value in variables.items():
                placeholder = f"{{{key}}}"
                customized = customized.replace(placeholder, str(value))
            
            return customized
        
        except Exception as e:
            print(f"Failed to customize template {template_name}: {e}")
            return None
    
    def create_solution_file(self, problem_data: Dict[str, Any], output_path: str) -> bool:
        """Create a solution file from template"""
        try:
            # Prepare variables for the template
            variables = self.prepare_solution_variables(problem_data)
            
            # Get the appropriate template based on language
            language = problem_data.get('language', 'cpp')
            template_name = f"{language}_template"
            
            # Customize the template
            content = self.customize_template(template_name, variables)
            if not content:
                return False
            
            # Write the file
            return FileUtils.write_file(output_path, content)
        
        except Exception as e:
            print(f"Failed to create solution file: {e}")
            return False
    
    def create_metadata_file(self, problem_data: Dict[str, Any], output_path: str) -> bool:
        """Create a metadata file from template"""
        try:
            # Prepare variables for the template
            variables = self.prepare_metadata_variables(problem_data)
            
            # Customize the metadata template
            content = self.customize_template("metadata_template", variables)
            if not content:
                return False
            
            # Write the file
            return FileUtils.write_file(output_path, content)
        
        except Exception as e:
            print(f"Failed to create metadata file: {e}")
            return False
    
    def prepare_solution_variables(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare variables for solution template"""
        return {
            'problem_name': problem_data.get('problem_name', 'Unknown Problem'),
            'problem_id': problem_data.get('problem_id', 'Unknown'),
            'problem_url': problem_data.get('url', ''),
            'date': problem_data.get('created_date', FileUtils.get_current_date())
        }
    
    def prepare_metadata_variables(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare variables for metadata template"""
        test_cases = problem_data.get('test_cases', [])
        test_case_files = []
        
        for i, test_case in enumerate(test_cases, 1):
            test_case_files.append({
                'input': f"in{i}",
                'output': f"out{i}"
            })
        
        return {
            'problem_id': problem_data.get('problem_id', 'Unknown'),
            'problem_name': problem_data.get('problem_name', 'Unknown Problem'),
            'problem_url': problem_data.get('url', ''),
            'date': problem_data.get('created_date', FileUtils.get_current_date()),
            'test_case_count': len(test_cases),
            'time_limit': problem_data.get('time_limit', 'Unknown'),
            'memory_limit': problem_data.get('memory_limit', 'Unknown')
        }
    
    def reload_templates(self) -> None:
        """Reload all templates from disk"""
        self.templates.clear()
        self.load_templates() 