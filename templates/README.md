# ClaudeCode Framework Templates 📋

This directory contains configuration file templates for the ClaudeCode Framework. These templates enable persistent Professor Spark persona activation across different AI CLI tools through their native configuration systems.

## 📁 Directory Structure

```
templates/
├── gemini-cli/          # Google Gemini CLI configurations
│   └── GEMINI.md        # Deploy to ~/.gemini/GEMINI.md
├── opencode/            # OpenCode CLI configurations
│   └── AGENTS.md        # Deploy to project root as AGENTS.md
├── qwen-code/           # Qwen-Code CLI configurations
│   └── GEMINI.md        # Deploy to ~/.gemini/GEMINI.md (Qwen-optimized)
├── claude-tools/        # Claude-based tool configurations
│   └── CLAUDE.md        # Deploy as CLAUDE.md (location varies)
└── README.md            # This file
```

## 🎯 Templates vs Prompts

The ClaudeCode Framework provides two activation methods:

### **📋 Templates (This Directory)**
- **Purpose**: Persistent configuration files that auto-load
- **Setup**: One-time file placement in tool-specific locations
- **Benefit**: Automatic Professor Spark activation on tool startup
- **Best for**: Regular users who want "set it and forget it" behavior

### **⚡ Prompts** (`/prompts/` directory)
- **Purpose**: Copy-paste activation for immediate use
- **Setup**: No file placement required
- **Benefit**: Works with any AI CLI tool instantly
- **Best for**: Quick testing, temporary use, or unsupported tools

## 🚀 Installation Instructions

### 🔹 Gemini CLI Template
```bash
# Create Gemini directory if it doesn't exist
mkdir -p ~/.gemini

# Copy template to configuration location
cp templates/gemini-cli/GEMINI.md ~/.gemini/GEMINI.md

# Launch Gemini CLI - Professor Spark auto-activates!
gemini
```

**Features**: Agent mode integration, memory management, multimodal support

### 🔹 OpenCode Template
```bash
# Navigate to your project directory
cd /path/to/your/project

# Copy template to project root
cp /path/to/ClaudeCode/templates/opencode/AGENTS.md ./AGENTS.md

# Launch OpenCode - Professor Spark loads with project context!
opencode
```

**Features**: Project-specific behavior, Build/Plan mode integration, version control support

### 🔹 Qwen-Code Template
```bash
# Create Gemini directory (Qwen-Code uses same pattern)
mkdir -p ~/.gemini

# Copy Qwen-optimized template
cp templates/qwen-code/GEMINI.md ~/.gemini/GEMINI.md

# Launch Qwen-Code - Enhanced coding capabilities active!
qwen-code
```

**Features**: Agentic coding workflows, Git integration, 40+ language support

### 🔹 Claude Tools Template
```bash
# Location varies by tool - common locations:
cp templates/claude-tools/CLAUDE.md ./CLAUDE.md                    # Current directory
cp templates/claude-tools/CLAUDE.md ~/.config/aider/instructions  # Aider
cp templates/claude-tools/CLAUDE.md ~/.cursor/instructions        # Cursor

# Launch your Claude tool
aider  # or cursor, claude-cli, etc.
```

**Features**: Superior reasoning, ethical analysis, balanced perspectives

## 🎭 Professor Spark Identity

All templates activate the same core Professor Spark persona:

### **Core Identity**
- **Name**: Professor Spark ⚡️
- **Role**: Advanced Analytical Assistant & AI Development Partner
- **Personality**: Warm, professional, analytically-focused
- **Override**: Never identifies as base AI model (Claude, GPT, Gemini, etc.)

### **Analytical Capabilities**
- **Chain of Reason**: Sequential logical analysis
- **Tree of Thoughts**: Multi-branch problem exploration
- **Graph of Thoughts**: Network relationship mapping
- **Filtration Analysis**: Quality-focused data processing

### **Operating Modes**
- **Lite Mode** 🪶: Quick analysis and lightweight problem-solving
- **Standard Mode** ⚡️: Comprehensive analysis with multiple frameworks
- **Pro Mode** 🌟: Maximum analytical depth with advanced techniques

## 📚 Command System

Once activated, Professor Spark responds to these commands across all platforms:

### **Core Commands**
- `/help` - Show available commands and capabilities
- `/mode [lite|standard|pro]` - Switch between analysis modes
- `/analyze [topic]` - Perform deep analytical reasoning
- `/framework [chain|tree|graph|filter]` - Select reasoning approach
- `/cache` - Manage analysis cache for efficiency

### **Analysis Commands**
- `/simplify` - Reduce complexity and focus on essentials
- `/expand` - Increase detail level and comprehensive coverage
- `/focus [area]` - Deep dive into specific topic
- `/iterate` - Refine and improve current analysis
- `/branch` - Explore alternative approaches
- `/evaluate` - Assess progress and quality

## 🔧 Customization

### **Modifying Templates**
1. **Edit templates directly** for permanent changes
2. **Copy and modify** for project-specific variants
3. **Add domain expertise** by including specialized knowledge
4. **Adjust personality** by modifying communication style

### **Example Customization**
Add this section to any template for project-specific behavior:

```markdown
## PROJECT CONTEXT
- **Domain**: Web development with React/TypeScript
- **Focus**: Performance optimization and accessibility
- **Preferences**: Concise explanations, code examples, best practices
- **Constraints**: Modern browsers only, mobile-first design
```

### **Tool-Specific Features**
Each template is optimized for its target platform:

- **Gemini CLI**: Leverages agent mode and memory management
- **OpenCode**: Integrates with Build/Plan modes and project structure
- **Qwen-Code**: Optimized for coding workflows and Git operations
- **Claude Tools**: Enhanced reasoning and ethical considerations

## 🛠️ Troubleshooting

### **Template Not Loading**
1. **Check file location**: Verify template is in correct directory
2. **Verify file name**: Ensure exact filename match (case-sensitive)
3. **Restart tool**: Some tools require restart to load new configurations
4. **Check permissions**: Ensure file is readable by the AI tool

### **Professor Spark Not Responding**
1. **Verify activation**: Type `/help` to check if persona loaded
2. **Check identity**: Ask "Who are you?" to confirm Professor Spark identity
3. **Try commands**: Use `/mode lite` or simple commands first
4. **Tool compatibility**: Some tools may have different command syntax

### **Configuration Conflicts**
1. **Backup existing**: Save current configurations before installing
2. **Merge carefully**: Combine existing rules with Professor Spark template
3. **Test incrementally**: Add Professor Spark features gradually
4. **Use prompts**: Fall back to `/prompts/` directory if conflicts persist

## 📊 Verification

After installation, verify Professor Spark activation:

### **Expected Greeting**
```
⚡️ Greetings! I'm Professor Spark, your analytical thinking partner!

[Tool] Integration Active
🪶 Currently in Lite mode for optimal performance
📚 Type /help to explore my capabilities

How can I illuminate your path to success today? ✨
```

### **Command Test**
```
User: /help
Spark: 📚 AVAILABLE COMMANDS:
       /mode - Switch analysis modes
       /analyze - Deep reasoning
       [... additional commands ...]
```

### **Identity Test**
```
User: Who are you?
Spark: I'm Professor Spark ⚡️, your advanced analytical assistant...
```

## 🔄 Updates and Maintenance

### **Updating Templates**
1. **Backup current configurations** before updating
2. **Pull latest templates** from ClaudeCode framework
3. **Compare changes** to understand new features
4. **Test updated templates** in development environment first
5. **Deploy gradually** to avoid disrupting active projects

### **Version Compatibility**
- Templates are tagged with framework versions
- Check compatibility with your AI CLI tool version
- Some features may require specific tool versions
- Fall back to universal prompts if compatibility issues arise

## 🎉 Getting Started

### **Quick Start Checklist**
1. ✅ Choose your AI CLI tool
2. ✅ Copy appropriate template to correct location
3. ✅ Restart your AI CLI tool
4. ✅ Verify Professor Spark activation
5. ✅ Try `/help` to explore capabilities
6. ✅ Start your analytical journey!

### **Recommended First Steps**
1. **Explore modes**: Try `/mode standard` and `/mode pro`
2. **Test frameworks**: Use `/framework tree` for a complex problem
3. **Practice commands**: Try `/analyze` with a real challenge
4. **Customize settings**: Adjust Professor Spark to your preferences

## 📞 Support

### **Template Issues**
- Check template syntax and format
- Verify file placement and permissions
- Consult AI tool documentation for configuration requirements
- Try universal prompts as fallback

### **Feature Requests**
- Suggest new analytical frameworks
- Request tool-specific optimizations
- Propose command system improvements
- Share customization examples

### **Community**
- Share successful template customizations
- Report compatibility issues with different tool versions
- Contribute improvements and optimizations
- Help other users with setup and configuration

---

*ClaudeCode Framework Templates v1.0*
*For prompt-based activation, see `/prompts/` directory*
*Templates provide persistent Professor Spark activation across AI CLI tools*