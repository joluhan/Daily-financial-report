# Daily Financial Report Generator

A Python script that automatically generates daily financial reports for trading pairs using OpenAI's ChatGPT API and exports them to Excel format.

## Features

- 📊 Generates structured financial analysis for 8 trading pairs
- 🤖 Uses ChatGPT API with web search capabilities for real-time market data
- 📈 Creates formatted Excel reports with proper styling
- 🇫🇷 French language analysis optimized for European trading hours (8h-15h Paris time)
- 💼 Professional trading insights with fundamental analysis

## Trading Pairs Analyzed

- BCOUSD (Brent Crude Oil)
- NATGASUSD (Natural Gas)
- EURUSD (Euro/US Dollar)
- GBPJPY (British Pound/Japanese Yen)
- XAUUSD (Gold/US Dollar)
- XAUEUR (Gold/Euro)
- NAS100USD (Nasdaq 100)
- SPX500USD (S&P 500)

## Prerequisites

- Python 3.7 or higher
- OpenAI API key
- Windows PowerShell (for Windows users)

## Installation & Setup

### 1. Clone or Download the Project

```powershell
# Navigate to your desired directory
cd C:\Users\YourUsername\Documents\GitHub\

# Create project directory
mkdir Daily-financial-report
cd Daily-financial-report
```

### 2. Create Python Virtual Environment

```powershell
# Create virtual environment
python -m venv env

# Bypass execution policy if needed (run as Administrator or use -Scope Process)
Set-ExecutionPolicy Bypass -Scope Process -Force

# Activate virtual environment
.\env\Scripts\Activate.ps1
```

You should see `(env)` prefix in your PowerShell prompt indicating the virtual environment is active.

### 3. Install Dependencies

```powershell
# Install required packages
pip install openai pandas openpyxl
```

Or install from requirements.txt:

```powershell
pip install -r requirements.txt
```

### 4. Set Up OpenAI API Key

#### Option A: Environment Variable (Recommended)
```powershell
# Set API key for current session
$env:OPENAI_API_KEY = "your_api_key_here"

# Or set permanently (requires restart)
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your_api_key_here", "User")
```

#### Option B: Modify Script Directly
Edit the script and replace:
```python
self.openai_api_key = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
```

### 5. Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in to your account
3. Click "Create new secret key"
4. Copy the key and use it in step 4 above

## Usage

### Run the Script

```powershell
# Make sure virtual environment is activated
# You should see (env) in your prompt

# Run the financial report generator
python financial_report.py
```

### Expected Output

```
🚀 Starting financial report generation...
📅 Date: 05/06/2025 14:30:15
📡 Calling OpenAI API...
✅ Report data generated successfully
✅ Excel file created successfully: Rapport_Marche_2025-06-05.xlsx
📊 Report contains 8 currency pairs
🎉 Process completed! File saved as: Rapport_Marche_2025-06-05.xlsx
```

## Output File Structure

The generated Excel file contains:

| Column | Description |
|--------|-------------|
| **Paire** | Trading pair symbol |
| **Biais_Quotidien** | Daily bias (Haussier/Baissier/Neutre) |
| **Resume_Executif** | One-line executive summary |
| **Explication_Approfondie** | Detailed fundamental analysis |

## Troubleshooting

### PowerShell Execution Policy Error

If you encounter execution policy errors:

```powershell
# Run PowerShell as Administrator and execute:
Set-ExecutionPolicy RemoteSigned

# Or for current session only:
Set-ExecutionPolicy Bypass -Scope Process -Force
```

### API Key Issues

1. Verify your API key is correct
2. Check your OpenAI account has sufficient credits
3. Ensure the API key has proper permissions

### Module Import Errors

```powershell
# Ensure virtual environment is activated
.\env\Scripts\Activate.ps1

# Reinstall packages if needed
pip install --upgrade openai pandas openpyxl
```

## Automation

### Schedule Daily Reports

#### Using Windows Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to Daily
4. Set action to "Start a program"
5. Program: `python`
6. Arguments: `financial_report.py`
7. Start in: `C:\Users\YourUsername\Documents\GitHub\Daily-financial-report`

#### Using PowerShell Script:

Create a batch file `run_report.bat`:

```batch
@echo off
cd /d "C:\Users\YourUsername\Documents\GitHub\Daily-financial-report"
call env\Scripts\activate.bat
python financial_report.py
pause
```

## Project Structure

```
Daily-financial-report/
├── env/                    # Virtual environment
├── financial_report.py     # Main script
├── requirements.txt        # Dependencies
├── README.md              # This file
└── Rapport_Marche_*.xlsx  # Generated reports
```

## API Information

The script uses two API approaches:
1. **Primary**: OpenAI's responses API with web search
2. **Fallback**: Standard Chat Completions API

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the script.

## License

This project is for educational and personal use. Please ensure compliance with OpenAI's usage policies.

---

**Note**: This script is designed for informational purposes only. Trading decisions should not be based solely on automated reports. Always conduct your own research and consider consulting with financial professionals.