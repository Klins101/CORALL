# LLM Setup Guide

## 🔑 Setting Up LLM API Keys (OpenAI & Claude)

### **Method 1: .env File (Recommended)**

1. **Create .env file** in the project root:
```bash
# Copy the template
cp .env.example .env

# Edit with your actual API key
nano .env
```

2. **Add your API keys**:
```
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Claude Configuration  
CLAUDE_API_KEY=sk-ant-your-actual-claude-key-here

# Choose default provider
LLM_PROVIDER=openai
# Options: openai, claude
```

3. **Run simulation**:
```bash
source simEnv/bin/activate

# Use default provider from .env
python main.py --llm 1 --case_number 1

# Or specify provider explicitly
python main.py --llm 1 --llm_provider claude --case_number 1
python main.py --llm 1 --llm_provider openai --case_number 1
```

### **Method 2: Environment Variable**

#### Temporary (current session):
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
source simEnv/bin/activate
python main.py --llm 1 --case_number 1
```

#### Permanent:
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export OPENAI_API_KEY="sk-your-actual-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### **Method 3: Configuration File**

1. **Edit config/api_keys.json**:
```json
{
  "openai": {
    "api_key": "sk-your-actual-api-key-here",
    "model": "gpt-4.0",
    "temperature": 0.1,
    "max_tokens": 200
  }
}
```

2. **Load in code** (advanced users can modify the LLM module to read from this file)

## 🔐 Security Best Practices

### **DO:**
- ✅ Use .env file for local development
- ✅ Keep API keys in environment variables for production
- ✅ Add .env to .gitignore (already done)
- ✅ Use different keys for development/production
- ✅ Rotate keys regularly

### **DON'T:**
- ❌ Never commit API keys to git
- ❌ Don't share keys in plain text
- ❌ Don't use production keys for testing
- ❌ Don't hardcode keys in source code

## 🚀 Quick Start

1. **Get your API key** from https://platform.openai.com/api-keys
2. **Choose your method** (we recommend .env file)
3. **Set the key**:
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```
4. **Test it**:
```bash
source simEnv/bin/activate
python main.py --llm 1 --case_number 1 --sim_time 60
```

## 🔧 Configuration Options

### **Model Settings**
You can customize the LLM behavior by setting these environment variables:

```bash
# In .env file
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4          
OPENAI_TEMPERATURE=0.1              # 0.0 to 1.0
OPENAI_MAX_TOKENS=200               # Response length
```

