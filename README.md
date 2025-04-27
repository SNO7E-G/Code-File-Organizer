# Code File Organizer

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/SNO7E-G/code-file-organizer/pulls)

**Intelligent file organization for developers**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation) • [Examples](#examples) • [License](#license)

</div>

---

## 🔍 Overview

Code File Organizer is a powerful Python tool that automatically organizes code files into directories based on file type, project structure, and content analysis. It uses intelligent algorithms to categorize files beyond just their extensions, making it perfect for cleaning up messy project directories or standardizing your development workspace.

## ✨ Features

- **Intelligent Content Analysis**
  - Detects file types based on content patterns and signatures
  - Identifies framework-specific files like React components
  - Recognizes configuration files regardless of extension

- **Project Structure Detection**
  - Automatically identifies Node.js, Python, and Git projects
  - Preserves important project structure with project mode
  - Adapts organization strategy based on detected project type

- **Advanced Organization**
  - Customizable mappings for complete control
  - Duplicate file detection using MD5 hashing
  - Smart categorization of scripts by shebang line detection

- **Developer Experience**
  - Dry run mode to preview changes
  - Detailed report generation
  - Performance metrics and statistics
  - Extensive configuration options

## 🚀 Installation

### Option 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/SNO7E-G/code-file-organizer.git

# Navigate to the directory
cd code-file-organizer

# Install the package
pip install -e .
```

### Option 2: Install from GitHub

```bash
pip install git+https://github.com/SNO7E-G/code-file-organizer.git
```

## 📋 Usage

### Basic Command

Organize the current directory:

```bash
code-organizer
```

Or use the Python script directly:

```bash
python file_organizer.py
```

### Command Line Arguments

```
usage: file_organizer.py [-h] [--target-dir TARGET_DIR] [--project-mode]
                        [--dry-run] [--save-config] [--load-config]
                        [--config-file CONFIG_FILE] [--report]
                        [--report-file REPORT_FILE] [--no-smart]
                        [--no-duplicates] [--exclude-dir EXCLUDE_DIR]
                        [--exclude-file EXCLUDE_FILE] [--version] [--verbose]
                        [source_dir]
```

### Common Commands

| Task | Command |
| --- | --- |
| Organize current directory | `code-organizer` |
| Preview changes without applying | `code-organizer --dry-run` |
| Preserve project structure | `code-organizer --project-mode` |
| Generate detailed report | `code-organizer --report` |
| Verbose output | `code-organizer --verbose` |
| Show version info | `code-organizer --version` |

### Advanced Examples

1. **Organize files with custom exclusions:**
   ```bash
   code-organizer --exclude-dir build --exclude-dir dist --exclude-file README.md
   ```

2. **Organize files from one directory to another:**
   ```bash
   code-organizer /source/directory --target-dir /target/directory
   ```

3. **Save and load configuration:**
   ```bash
   # Save current settings
   code-organizer --save-config --config-file my_config.json
   
   # Load saved settings
   code-organizer --load-config --config-file my_config.json
   ```

## 📊 How It Works

### Smart Detection Process

<div align="center">
<img src="https://via.placeholder.com/800x300.png?text=Smart+Detection+Process" alt="Smart Detection Process" width="700px" />
</div>

1. **Project Analysis**
   - Scans for project identifiers (package.json, requirements.txt, etc.)
   - Identifies repository type and structure
   - Determines optimal organization strategy

2. **File Processing**
   - Examines file content with pattern recognition
   - Analyzes file headers and signatures
   - Computes file hashes to detect duplicates
   - Identifies relationships between files

3. **Intelligent Organization**
   - Categorizes files based on combined analysis results
   - Creates logical directory structure
   - Maintains project integrity

## 🛠️ Custom Configuration

You can create a custom mapping file in JSON format:

```json
{
  "source_dir": "/path/to/source",
  "target_dir": "/path/to/target",
  "mappings": {
    "py": "Python",
    "js": "JavaScript",
    "html": "Web/HTML"
  },
  "project_mode": false,
  "exclude_dirs": [".git", "node_modules", "venv"],
  "exclude_files": ["file_organizer.py", "file_organizer_config.json"]
}
```

See [examples.md](examples.md) for more custom configuration examples.

## 📁 Default Mappings

The organizer includes comprehensive mappings for:

| Category | File Types |
| --- | --- |
| **Web Technologies** | HTML, CSS, JavaScript, TypeScript, PHP, React |
| **Programming Languages** | Python, Java, C/C++, C#, Go, Ruby, Rust, Swift, Kotlin |
| **Data Formats** | JSON, XML, YAML, CSV, Excel |
| **Documentation** | Markdown, Text, PDF, Word |
| **Configuration** | INI, CFG, ENV, TOML |
| **Media** | Images (JPG, PNG, SVG, etc.) |
| **Scripts** | Shell, Batch, PowerShell |
| **Database** | SQL |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📑 Documentation

For more detailed documentation and examples, see:

- [examples.md](examples.md) - Examples of intelligent file detection
- [custom_mappings_example.json](custom_mappings_example.json) - Example of custom mapping configurations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mahmoud Ashraf (SNO7E)**

[![GitHub](https://img.shields.io/badge/GitHub-SNO7E--G-blue?style=flat-square&logo=github)](https://github.com/SNO7E-G)

---

<div align="center">
<p>If you find this tool useful, please consider giving it a star! ⭐</p>
</div> 