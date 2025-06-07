# 🤖 TermixAI

**AI-Powered Shell Assistant – Transform your terminal into an intelligent conversation!**

TermixAI is a terminal application that bridges the gap between natural language and Linux commands. Simply describe what you want to accomplish in plain English, and TermixAI will generate, explain, and execute the appropriate commands through an elegant, chat-style interface.

Combining the power of AI with an intuitive chat interface. Instead of memorizing complex command syntax, just tell TermixAI what you need – it understands context, suggests optimal solutions, and helps you learn along the way.

---


## 🚀 Key Features

### 💬 **Intuitive Chat Interface**
- Beautiful, scrollable TUI powered by [Textual](https://github.com/Textualize/textual)
- Syntax highlighting and proper formatting
- Persistent chat history within sessions
- In-Built textual command palette for quick access to certain features
- Drop-down Option to switch between different models


### 🧠 **AI-Powered Command Generation**
- Future Supports for more AI providers (OpenAI, Anthropic)
- Short term memory for context -  5 window size
- Short Descirption of each command

### 🛡️ **Safe Command Execution**
- **Command Preview**: See exactly what will be executed
- **Approval Required**: Confirm before running potentially destructive commands

### 📚 **Learning-Focused**
- Command explanations help you understand what each operation does
- Build your Linux knowledge while getting work done

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Linux/macOS terminal environment
- Required Credentials for supported AI services

### 🌟 Recommended Installation (Virtual Environment)

```bash
# Clone the repository
git clone https://github.com/rahul-08-11/termixai.git
cd termixai

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install TermixAI
pip install .
```

### 🔧 Alternative Installation Methods

**From PyPI (when available):**
```bash
pip install termixai
```

**Development Installation:**
```bash
git clone https://github.com/rahul-08-11/termixai.git
cd termixai
pip install -e .
```

---

## ⚙️ Configuration

### Initial Setup

Configure your AI provider credentials:
```bash
termixai config
```

This will guide you through setting up:
- API keys for your preferred AI service
- Default model preferences
- Safety and execution settings

### Supported AI Providers

| Provider | Status | Models |
|----------|--------|--------|
| Azure OpenAI | ✅ **Currently Supported** | GPT-4, GPT-3.5-turbo etc. |
| OpenAI | 🔄 **Coming Soon** | GPT-4, GPT-3.5-turbo |
| Anthropic Claude | 🔄 **Planned** | Claude-3, Claude-2 |
| Local Models | 🔄 **Planned** | Ollama, llama.cpp |

---

## 🎮 Usage

### Start the Chat Interface
```bash
termixai chat
```

### Example Workflow
1. **Launch TermixAI**: Run `termixai chat`
2. **Describe your task**: Type naturally, like "show me all running services"
3. **Review the command**: TermixAI will display the suggested command with explanation
4. **Approve & execute**: Confirm to run the command and see results
5. **Learn & iterate**: Ask follow-up questions or try related tasks

### Sample Commands to Try
```
"Find large files in my home directory"
"Check which process is using the most CPU"
"Create a backup of my project folder"
"Show me network connections"
"Install a package and check if it worked"
```

---

## 🔧 Advanced Usage

### Command Line Options
```bash
# Start with specific configuration
termixai chat --config /path/to/config.yaml

# Enable debug mode
termixai chat --debug

# Use specific AI model
termixai chat --model gpt-4

# Run in batch mode (non-interactive)
termixai execute "your command description"
```

### Configuration File
Create `~/.termixai/config.yaml` for persistent settings:
```yaml
ai_provider: azure_openai
model: gpt-4
auto_execute: false
max_history: 50
theme: dark
safety_checks: true
```

---

## 🛡️ Safety Features

TermixAI prioritizes safety with several built-in protections:
- **Command Preview**: Always shows commands before execution
- **Destructive Command Detection**: Extra warnings for potentially harmful operations
- **Execution Limits**: Prevents infinite loops and resource exhaustion
- **User Confirmation**: Manual approval required for all executions

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit**: `git commit -m 'Add amazing feature'`
5. **Push**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Setup
```bash
git clone https://github.com/rahul-08-11/termixai.git
cd termixai
python -m venv dev-env
source dev-env/bin/activate
pip install -e ".[dev]"
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/rahul-08-11/termixai/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/rahul-08-11/termixai/discussions)
- **Documentation**: [Wiki](https://github.com/rahul-08-11/termixai/wiki)

---

## 🎯 Roadmap

- [ ] **Multi-provider AI support** (OpenAI, Anthropic, local models)
- [ ] **Plugin system** for custom commands
- [ ] **Command history and favorites**
- [ ] **Batch processing mode**
- [ ] **Integration with popular dev tools**
- [ ] **Windows PowerShell support**
- [ ] **Mobile companion app**

---

## ⭐ Show Your Support

If TermixAI helps improve your terminal workflow, please consider:
- ⭐ **Starring this repository**
- 🐦 **Sharing on social media**
- 💡 **Contributing ideas and feedback**
- 🐛 **Reporting bugs and issues**

---

**Made with ❤️ for the Linux community**

*Transform your terminal experience – one conversation at a time.*