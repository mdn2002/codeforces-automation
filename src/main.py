#!/usr/bin/env python3
"""
Codeforces Problem Automation Tool
Main entry point for the application
"""

import sys
import argparse
import signal
from typing import Optional
from utils.config_parser import ConfigParser
from problem_creator import ProblemCreator

class CodeforcesAutomation:
    """Main application class"""
    
    def __init__(self):
        self.config = None
        self.problem_creator = None
        self.running = False
    
    def initialize(self) -> bool:
        """Initialize the application"""
        try:
            # Load configuration
            self.config = ConfigParser()
            print("Configuration loaded successfully")
            
            # Initialize problem creator
            self.problem_creator = ProblemCreator(self.config)
            print("Problem creator initialized")
            
            return True
            
        except Exception as e:
            print(f"Failed to initialize application: {e}")
            return False
    
    def run_interactive(self) -> None:
        """Run in interactive mode"""
        if not self.initialize():
            return
        
        print("Codeforces Problem Automation Tool")
        print("=" * 40)
        
        while True:
            try:
                print("\nOptions:")
                print("1. Create a new problem (manual input)")
                print("2. Create problem from browser tab")
                print("3. List created problems")
                print("4. Get problem info")
                print("5. Test configuration")
                print("6. Exit")
                
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == '1':
                    self.problem_creator.create_problem_interactive()
                elif choice == '2':
                    self.problem_creator.create_problem_from_browser()
                elif choice == '3':
                    problems = self.problem_creator.list_created_problems()
                    if problems:
                        print("\nCreated problems:")
                        for problem in problems:
                            print(f"  - {problem}")
                    else:
                        print("\nNo problems created yet")
                elif choice == '4':
                    problem_id = input("Enter problem ID: ").strip()
                    if problem_id:
                        info = self.problem_creator.get_problem_info(problem_id)
                        if info:
                            print(f"\nProblem: {info['problem_id']}")
                            print(f"Directory: {info['directory']}")
                            print(f"Files: {', '.join(info['files'])}")
                            if 'metadata' in info:
                                print(f"Status: {info['metadata'].get('status', 'Unknown')}")
                        else:
                            print(f"Problem {problem_id} not found")
                elif choice == '5':
                    self.test_configuration()
                elif choice == '6':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 1-6.")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def run_command_line(self, args: argparse.Namespace) -> None:
        """Run with command line arguments"""
        if not self.initialize():
            sys.exit(1)
        
        try:
            if args.browser:
                # Create problem from browser tab
                success = self.problem_creator.create_problem_from_browser()
                if not success:
                    sys.exit(1)
            elif args.problem:
                # Create problem from command line argument
                success = self.problem_creator.create_problem_from_input(args.problem)
                if not success:
                    sys.exit(1)
            
            elif args.list:
                # List created problems
                problems = self.problem_creator.list_created_problems()
                if problems:
                    print("Created problems:")
                    for problem in problems:
                        print(f"  - {problem}")
                else:
                    print("No problems created yet")
            
            elif args.info:
                # Get problem info
                info = self.problem_creator.get_problem_info(args.info)
                if info:
                    print(f"Problem: {info['problem_id']}")
                    print(f"Directory: {info['directory']}")
                    print(f"Files: {', '.join(info['files'])}")
                    if 'metadata' in info:
                        print(f"Status: {info['metadata'].get('status', 'Unknown')}")
                else:
                    print(f"Problem {args.info} not found")
                    sys.exit(1)
            
            elif args.test:
                # Test configuration
                self.test_configuration()
            
            else:
                # No arguments provided, run interactive mode
                self.run_interactive()
        
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def test_configuration(self) -> None:
        """Test the current configuration"""
        print("\nConfiguration Test")
        print("=" * 20)
        
        # Test configuration loading
        print(f"✓ Configuration loaded from: {self.config.config_path}")
        
        # Test output directory
        output_dir = self.config.get('output_directory')
        print(f"✓ Output directory: {output_dir}")
        
        # Test template directory
        template_dir = self.config.get('template_directory')
        print(f"✓ Template directory: {template_dir}")
        
        # Test editor configuration
        editor_config = self.config.get_editor_config()
        editor_cmd = editor_config.get('command', 'unknown')
        print(f"✓ Editor command: {editor_cmd}")
        
        # Test file opener
        if hasattr(self, 'problem_creator') and self.problem_creator:
            file_opener = self.problem_creator.file_opener
            if file_opener.test_editor_availability():
                print(f"✓ Editor '{editor_cmd}' is available")
            else:
                print(f"✗ Editor '{editor_cmd}' not found")
                available = file_opener.get_available_editors()
                if available:
                    print(f"  Available editors: {', '.join([name for cmd, name in available])}")
                    suggested = file_opener.suggest_editor()
                    print(f"  Suggested editor: {suggested}")
        
        # Test templates
        if hasattr(self, 'problem_creator') and self.problem_creator:
            templates = self.problem_creator.template_manager.list_templates()
            print(f"✓ Loaded templates: {', '.join(templates)}")
        
        print("\nConfiguration test completed!")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Codeforces Problem Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 1850A                    # Create problem 1850A
  %(prog)s "https://codeforces.com/contest/1850/problem/A"  # Create from URL
  %(prog)s --browser                # Create from active browser tab
  %(prog)s --list                   # List created problems
  %(prog)s --info 1850A             # Get info about problem 1850A
  %(prog)s --test                   # Test configuration
  %(prog)s                          # Interactive mode
        """
    )
    
    parser.add_argument(
        'problem',
        nargs='?',
        help='Problem ID, URL, or contest/problem format (e.g., 1850A, 1850/A)'
    )
    
    parser.add_argument(
        '--browser',
        action='store_true',
        help='Create problem from currently active browser tab'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all created problems'
    )
    
    parser.add_argument(
        '--info',
        metavar='PROBLEM_ID',
        help='Get information about a specific problem'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test the current configuration'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Codeforces Problem Automation Tool v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Create and run the application
    app = CodeforcesAutomation()
    app.run_command_line(args)

if __name__ == "__main__":
    main() 