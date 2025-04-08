# Cybersecurity Tools Collection

This repository contains a collection of specialized tools for cybersecurity operations, including OSINT gathering, sensitive file detection, and technical translation for cybersecurity content.

## 📚 Table of Contents

- [Overview](#overview)
- [Tools](#tools)
  - [Dork - Google Dork Search Tool](#dork---google-dork-search-tool)
  - [Find-SensitiveFiles - Sensitive File Detection](#find-sensitivefiles---sensitive-file-detection)
  - [DeepSeek Translator - Technical Translation](#deepseek-translator---technical-translation)
  - [Merge - JSON Merger](#merge---json-merger)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Dependencies](#dependencies)
- [License](#license)

## Overview

This toolkit provides various utilities for security professionals conducting assessments, threat intelligence, and forensic analysis. The tools can be used independently or as part of an integrated workflow.

## Tools

### DAMN - Digital Asset Mapping and Network Analyzer

A network scanning tool for identifying and analyzing digital assets across networks, helping security professionals map infrastructure and discover potential vulnerabilities.

#### Features:

- IP and port scanning with multithreaded execution
- Support for various target formats (IP addresses, ranges, CIDR notation)
- Service detection and version identification
- Optional Nmap integration for enhanced scanning
- Vulnerability detection for common exposed services
- Comprehensive JSON reporting
- Terminal output with color-coded results

#### Usage:

```bash
# Basic scan of a specific target
python damn.py -t 192.168.1.1 -o scan_results.json

# Scan multiple targets on specific ports
python damn.py -t 192.168.1.1,192.168.1.2,example.com -p 22,80,443 -o network_scan.json

# Scan a network range
python damn.py -t 192.168.1.0/24 -p 22-25,80,443,3389 --timeout 2 --threads 50
```

### Dork - Google Dork Search Tool

A command-line utility for automating Google dork searches, which are specialized search queries that can reveal sensitive information exposed on websites.

#### Features:

- Execute Google dork queries from the command line
- Specify the number of results to retrieve
- Save results to a text file
- Automatic logging of search results in JSON format
- Colorized terminal output

#### Usage:

```bash
python dork.py -d "site:example.com filetype:pdf" -n 100 -o results.txt
```

### Find-SensitiveFiles - Sensitive File Detection

A PowerShell script that scans systems for potentially sensitive files based on various detection patterns, helping identify security risks or data exposures.

#### Features:

- Comprehensive file detection for 30+ sensitive file types
- Detection based on file name, extension, and content patterns
- Content scanning with support for common configuration files
- Recursive directory scanning
- Detailed reporting with file metadata
- CSV export functionality
- Hidden file detection
- Quick mode for rapid assessments

#### Usage:

```powershell
# Basic scan of C: drive
.\Find-SensitiveFiles.ps1 -Paths "C:\" -OutputFile "SensitiveFiles.csv"

# Quick scan without content inspection
.\Find-SensitiveFiles.ps1 -Paths "C:\Users", "D:\Data" -IncludeContent:$false

# Full scan including hidden files with detailed output
.\Find-SensitiveFiles.ps1 -Paths "C:\Users\Administrator" -CheckHidden -OutputFile "AdminScan.csv"
```

### DeepSeek Translator - Technical Translation

An advanced tool for translating and analyzing cybersecurity content using the DeepSeek API, with features for emotion analysis, technical term extraction, and context analysis.

#### Features:

- Multi-language technical translation
- Emotion and sentiment analysis
- Technical term extraction and definition
- Tag categorization for messages
- Context-aware message analysis
- Handling of truncated messages
- Multithreaded processing for performance
- Detailed metrics and statistics

#### Usage:

```bash
# Basic usage
python ds.py -j messages.json -a "your-api-key" -o translated_output.json

# Advanced usage with turbo mode
python ds.py -j messages.json -a "your-api-key" -m turbo -w 8 -b 20 -c 10 -o translated_output.json
```

### Merge - JSON Merger

A utility script for merging JSON outputs from DeepSeek Translator and other tools.

#### Features:

- Merges two JSON files based on object IDs
- Generates statistical reports about the merge operation
- Preserves all data from both sources
- Handles duplicate entries

#### Usage:

```bash
python merge.py deepseek_output.json ultraflower_colored.json merged_output.json
```

## Installation

### Prerequisites

- Python 3.6+
- PowerShell 5.1+ (for Find-SensitiveFiles)
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cybersecurity-tools.git
   cd cybersecurity-tools
   ```

2. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

### Integrated Workflow Example

1. **Gather potential targets using Dork:**
   ```bash
   python dork.py -d "inurl:admin filetype:php" -n 200 -o potential_targets.txt
   ```

2. **Scan a system for sensitive files:**
   ```powershell
   .\Find-SensitiveFiles.ps1 -Paths "C:\webroot" -OutputFile "sensitive_scan.csv"
   ```

3. **Translate and analyze technical conversations:**
   ```bash
   python ds.py -j chat_logs.json -a "your-api-key" -o translated_logs.json
   ```

4. **Merge analysis results:**
   ```bash
   python merge.py translated_logs.json additional_analysis.json final_report.json
   ```

## Dependencies

### Python Packages

- `googlesearch-python`: For Google dork searches
- `python-nmap`: For enhanced network scanning (optional for DAMN)
- `requests`: For API communication
- `colorama`: For terminal color output
- `tqdm`: For progress bars
- `jinja2`: For templating
- `concurrent.futures`: For multithreading (standard library)
- `tabulate`: For formatted table output
- `icecream`: For debugging

### PowerShell Modules

- No external modules required; uses built-in PowerShell functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

These tools are provided for legitimate security research and assessment purposes only. Usage of these tools against systems without explicit permission is illegal and unethical. Always ensure you have proper authorization before conducting security assessments.
