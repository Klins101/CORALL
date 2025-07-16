# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for development)

## Quick Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Klins101/CORALL
cd CORALL
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test Installation
```bash
python main.py --case_number 1 --sim_time 260 --no_animation
```

## Development Installation

For development with editable installation:
```bash
pip install -e .
```

This allows you to modify the code and see changes without reinstalling.

## Optional Dependencies

### LLM Features
If you want to use LLM-based decision making:
```bash
pip install langchain_openai langchain
```

### Enhanced Visualization
For better plots and analysis:
```bash
pip install seaborn pandas scipy
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you're in the correct directory and virtual environment is activated
2. **Animation Not Working**: Check if matplotlib backend supports your display system
3. **Memory Issues**: Reduce simulation time or disable animation for large simulations

### Platform-Specific Notes

#### Linux
```bash
# Install system dependencies if needed
sudo apt-get install python3-dev python3-pip
```

#### macOS
```bash
# Install via Homebrew
brew install python3
```

#### Windows
- Use PowerShell or Command Prompt
- Ensure Python is added to PATH
- Use `python` instead of `python3`

## Verification

After installation, verify everything works:

```bash
python main.py --case_number 1 --sim_time 30
```

You should see:
- Simulation plots generated
- Output files in `img/` directory