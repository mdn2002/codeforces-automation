# Codeforces Problem Automation

A Python tool to automate the creation of Codeforces problem files with templates, test cases, and metadata.

## Features

- **Browser Integration**: Extract problem data directly from active Codeforces browser tabs
- **Template System**: Customizable C++ templates with variables
- **Test Case Management**: Creates clean input/output files for testing
- **Auto File Opening**: Opens solution file in your preferred editor
- **Metadata Tracking**: Stores problem information in JSON format
- **Fallback System**: Works even when web scraping is blocked

## Project Structure

```
codeforces-automation/
├── src/                    # Source code
├── templates/              # Template files
├── config/                 # Configuration files
├── problems/               # Generated problem files
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install ChromeDriver** (for browser integration):
   ```bash
   ./install_chromedriver.sh
   ```

3. **Configure Settings**:
   Edit `config/settings.json` to set your preferences:
   - Output directory
   - Editor preferences
   - File naming conventions

4. **Set Up Templates**:
   Customize `templates/cpp_template.cpp` with your preferred C++ template

5. **Run the Application**:
   ```bash
   python3 run.py
   ```

## Usage

### Browser Integration (Recommended)
1. **Start the Python server:**
   ```bash
   python3 cf_receiver.py
   ```
2. **Open a Codeforces problem in your browser**
3. **Press your extension shortcut** (e.g., Ctrl+Alt+C)
4. The tool will:
   - Receive the problem HTML from your browser
   - Extract problem information and test cases
   - Create the problem directory and files
   - Open the solution file in your editor

## Configuration

### Settings (`config/settings.json`)
- `output_directory`: Where to create problem files
- `editor`: Your preferred code editor
- `auto_open_files`: Whether to open files after creation
- `file_naming`: Customize file names and structure

### Templates
- `cpp_template.cpp`: Your C++ solution template
- `metadata_template.json`: Metadata file structure

## File Structure Example

```
problems/1850A/
├── solution.cpp    # Your solution file
├── in1            # Test case 1 input
├── in2            # Test case 2 input
├── out1           # Expected output for test case 1
├── out2           # Expected output for test case 2
└── metadata.json  # Problem metadata
```

## Testing Your Solutions

```bash
# Compile your solution
g++ -o main solution.cpp

# Test with input files
./main < in1
./main < in2

# Compare with expected output
./main < in1 > my_output
diff my_output out1
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License 