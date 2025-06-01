<div align="center">

# 🚀 FluxPilot

### A powerful development environment launcher with intuitive profile management

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey.svg)](https://github.com/Tamer7/fluxpilot)
[![CI](https://github.com/Tamer7/fluxpilot/actions/workflows/ci.yml/badge.svg)](https://github.com/Tamer7/fluxpilot/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[📖 Documentation](#-documentation) • [🚀 Installation](#-installation) • [✨ Features](#-features) • [🤝 Contributing](#-contributing)

---

</div>

## 📖 Overview

FluxPilot transforms the way you manage development environments. With its sleek interface and powerful automation capabilities, you can orchestrate complex development workflows with a single click. Built for developers who value efficiency and elegance.

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 **Core Features**
- 📁 **Profile Management** - Create, edit, and organize development profiles
- ⚡ **Multi-step Execution** - Sequential command execution with real-time feedback  
- 📊 **Live Console Output** - See exactly what's happening as it happens
- 🖥️ **Tabbed Interface** - Run multiple profiles simultaneously
- 🔄 **Process Control** - Start, stop, and monitor with precision

</td>
<td width="50%">

### 🛠️ **Advanced Features**
- 🌐 **Port Monitoring** - Built-in port checker and process manager
- 📂 **Working Directory Support** - Custom paths for each command
- 🌙 **Dark Theme** - Modern interface that's easy on the eyes
- 🔧 **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux
- 💾 **Smart Config** - Automatic profile persistence and backup

</td>
</tr>
</table>

## 📸 Screenshots

<div align="center">

### Main Interface
![FluxPilot Main Interface](https://via.placeholder.com/800x500/2D3748/FFFFFF?text=FluxPilot+Main+Interface)
*Clean, intuitive design with profile management and real-time console output*

### Profile Management
![Profile Management](https://via.placeholder.com/600x400/4A5568/FFFFFF?text=Profile+Management+Dialog)
*Easy-to-use profile creation with multi-step command support*

</div>

## 🚀 Installation

### Prerequisites
- 🐍 **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- 📦 **pip** (comes with Python)

### Quick Start

```bash
# 📥 Clone the repository
git clone https://github.com/Tamer7/fluxpilot.git
cd fluxpilot

# 🔧 Install dependencies
pip install -r requirements.txt

# 🚀 Launch FluxPilot
python main.py
```

### 📦 Alternative Installation Methods

<details>
<summary>🔽 Using Virtual Environment (Recommended)</summary>

```bash
# Create virtual environment
python -m venv fluxpilot-env

# Activate it
# Windows:
fluxpilot-env\Scripts\activate
# macOS/Linux:
source fluxpilot-env/bin/activate

# Install and run
pip install -r requirements.txt
python main.py
```

</details>

<details>
<summary>🔽 Development Setup</summary>

```bash
# Clone and setup for development
git clone https://github.com/Tamer7/fluxpilot.git
cd fluxpilot

# Install with development dependencies
pip install -r requirements.txt
pip install pre-commit

# Setup pre-commit hooks
pre-commit install

# You're ready to contribute! 🎉
```

</details>

## 🎮 Usage

### 🆕 Creating Your First Profile

1. **Launch FluxPilot** and click the **"Add"** button
2. **Enter a profile name** (e.g., "Full Stack Dev")
3. **Add your commands:**
   - **Label**: "Start Database"
   - **Command**: `docker-compose up -d postgres`
   - **Working Dir**: `/path/to/your/project`
4. **Save and run!** 🎉

### 💡 Example Profiles

<details>
<summary>🌐 Full Stack Web Development</summary>

```yaml
Profile: "Full Stack Development"
Steps:
  1. Label: "Start Database"
     Command: docker-compose up -d postgres
     Working Dir: /path/to/project

  2. Label: "Start Backend API"  
     Command: npm run dev
     Working Dir: /path/to/project/backend

  3. Label: "Start Frontend"
     Command: npm start
     Working Dir: /path/to/project/frontend
```

</details>

<details>
<summary>🐍 Python Development</summary>

```yaml
Profile: "Python Development"
Steps:
  1. Label: "Activate Virtual Environment"
     Command: venv\Scripts\activate
     Working Dir: /path/to/project

  2. Label: "Start Django Server"
     Command: python manage.py runserver
     Working Dir: /path/to/project

  3. Label: "Start Celery Worker"
     Command: celery -A myproject worker -l info
     Working Dir: /path/to/project
```

</details>

## ⚙️ Configuration

FluxPilot automatically stores your profiles in the appropriate system directory:

| OS | Configuration Path |
|---|---|
| 🪟 **Windows** | `%APPDATA%\FluxPilot\profiles.json` |
| 🍎 **macOS** | `~/Library/Application Support/FluxPilot/profiles.json` |
| 🐧 **Linux** | `~/.config/FluxPilot/profiles.json` |

> 💡 **Tip**: While you can manually edit the JSON file, we recommend using the GUI for the best experience!

## 🛠️ Development

### 📁 Project Structure

```
FluxPilot/
├── 🚀 main.py                    # Application entry point
├── 📦 modules/                   # Core modules
│   ├── 📄 __init__.py           # Package initialization
│   ├── 👤 profile_manager.py    # Profile management
│   ├── 🔄 process_runner.py     # Process execution
│   └── 🌐 ports_checker.py      # Port monitoring
├── ⚙️ config/                   # Configuration files  
├── 📚 docs/                     # Documentation
├── 🧪 .github/                  # GitHub workflows & templates
└── 📄 requirements.txt         # Dependencies
```

### 🏗️ Tech Stack

- **🖼️ GUI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern, dark-themed UI
- **🔍 System Monitoring**: [psutil](https://github.com/giampaolo/psutil) - Cross-platform process utilities
- **🐍 Language**: Python 3.8+ - Reliable, cross-platform development
- **🎨 Code Formatting**: Black - Consistent, readable code style

## 🤝 Contributing

We love contributions! FluxPilot is a community-driven project that thrives on collaboration.

### 🌟 Contributors

Thanks to these amazing people who have contributed to FluxPilot:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Tamer7"><img src="https://avatars.githubusercontent.com/u/28959383?v=4?s=100" width="100px;" alt="Tamer7"/><br /><sub><b>Tamer7</b></sub></a><br /><a href="https://github.com/Tamer7/fluxpilot/commits?author=Tamer7" title="Code">💻</a> <a href="#design-Tamer7" title="Design">🎨</a> <a href="https://github.com/Tamer7/fluxpilot/commits?author=Tamer7" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

**Want to contribute?** Check out our [Contributing Guide](CONTRIBUTING.md) for detailed information on how to get started!

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🎨 **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - For the beautiful, modern UI framework
- 🔍 **[psutil](https://github.com/giampaolo/psutil)** - For robust cross-platform system monitoring
- 💝 **Our Contributors** - For making FluxPilot better every day
- 🌍 **The Open Source Community** - For inspiration and continuous learning

## 🔮 Roadmap

<details>
<summary>🗺️ What's Coming Next</summary>

### 🚧 In Development
- [ ] 📱 **System Tray Integration** - Run FluxPilot in the background
- [ ] 🔒 **Environment Variables** - Secure credential management
- [ ] 📊 **Enhanced Logging** - Detailed execution logs and export

### 🎯 Planned Features
- [ ] 🎭 **Profile Templates** - Pre-built profiles for common stacks
- [ ] 🌐 **Cloud Sync** - Sync profiles across devices
- [ ] 🤖 **Smart Suggestions** - AI-powered profile recommendations
- [ ] 📱 **Mobile Companion** - Monitor your environments on the go

### 💭 Ideas & Research
- [ ] 🐳 **Docker Integration** - Native container management
- [ ] 🔌 **Plugin System** - Extensible architecture
- [ ] 📈 **Analytics Dashboard** - Performance insights
- [ ] 🎮 **CLI Interface** - Command-line power users

</details>

---

<div align="center">

### 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Tamer7/fluxpilot&type=Date)](https://star-history.com/#Tamer7/fluxpilot&Date)

**Made with ❤️ by the FluxPilot community**

[⬆️ Back to Top](#-fluxpilot)

</div> 