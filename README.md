# 🗺️ SupaMap

```
 ███████╗██╗   ██╗██████╗  █████╗ ███╗   ███╗ █████╗ ██████╗ 
 ██╔════╝██║   ██║██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔══██╗
 ███████╗██║   ██║██████╔╝███████║██╔████╔██║███████║██████╔╝
 ╚════██║██║   ██║██╔═══╝ ██╔══██║██║╚██╔╝██║██╔══██║██╔═══╝
 ███████║╚██████╔╝██║     ██║  ██║██║ ╚═╝ ██║██║  ██║██║     
 ╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     
```

> **Supabase Data Extraction & Manipulation Framework**  
> A powerful toolkit for authorized security testing and bug bounty hunting on Supabase instances.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen.svg)](https://github.com/yourusername/supamap)

---

## 🎯 Features

- 🔍 **Table Enumeration** - Discover all accessible tables in the database
- 📊 **Data Extraction** - Pull records with advanced filtering and pagination
- 🔎 **Query Engine** - Execute complex queries with multiple filters
- ✏️ **Record Manipulation** - Insert, update, and delete records
- 💾 **Bulk Export** - Export entire tables to JSON format
- 🔐 **Auth Support** - Works with API keys and bearer tokens
- ⚡ **Fast & Efficient** - Optimized for large datasets with batch processing

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/supamap.git
cd supamap

# Install dependencies
pip install -r requirements.txt

# Make it executable
chmod +x supamap.py
```

### Basic Usage

```bash
# List all tables
python supamap.py -u https://xxx.supabase.co -k YOUR_API_KEY list-tables

# Extract data from a table
python supamap.py -u https://xxx.supabase.co -k YOUR_API_KEY list -t users -l 50
```

---

## 📖 Usage Guide

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list-tables` | List all available tables | `supamap.py -u URL -k KEY list-tables` |
| `list` | List records from a table | `supamap.py -u URL -k KEY list -t users` |
| `query` | Query with specific filters | `supamap.py -u URL -k KEY query -t users -f '{"email":"test@test.com"}'` |
| `insert` | Insert new record | `supamap.py -u URL -k KEY insert -t users -d '{"name":"John"}'` |
| `update` | Update existing records | `supamap.py -u URL -k KEY update -t users -f '{"id":"1"}' -d '{"name":"Jane"}'` |
| `delete` | Delete records | `supamap.py -u URL -k KEY delete -t users -f '{"id":"1"}'` |
| `export` | Export entire table | `supamap.py -u URL -k KEY export -t users -o output.json` |

### Arguments

```
Required:
  -u, --url         Supabase project URL
  -k, --apikey      Supabase API key (anon/service key)

Optional:
  -a, --auth        Authorization bearer token
  -t, --table       Target table name
  -f, --filters     JSON filters (ex: {"column":"value"})
  -d, --data        JSON data for insert/update
  -l, --limit       Record limit (default: 100)
  -o, --output      Output file path
  --offset          Pagination offset
  --order           Sort order (ex: created_at.desc)
```

---

## 💡 Examples

### 1. Reconnaissance Phase

```bash
# Discover all tables
python supamap.py -u https://target.supabase.co -k eyJhbGc... list-tables

# List records with pagination
python supamap.py -u https://target.supabase.co -k eyJhbGc... list -t users -l 100 --offset 0
```

### 2. Data Extraction

```bash
# Query specific users
python supamap.py -u https://target.supabase.co -k eyJhbGc... \
  query -t users -f '{"role":"admin"}' -l 50

# Export entire table
python supamap.py -u https://target.supabase.co -k eyJhbGc... \
  export -t sensitive_data -o dump.json -l 10000
```

### 3. Data Manipulation

```bash
# Insert test record
python supamap.py -u https://target.supabase.co -k eyJhbGc... \
  insert -t users -d '{"name":"Test User","email":"test@example.com"}'

# Update record
python supamap.py -u https://target.supabase.co -k eyJhbGc... \
  update -t users -f '{"email":"test@example.com"}' -d '{"verified":true}'

# Delete record (requires confirmation)
python supamap.py -u https://target.supabase.co -k eyJhbGc... \
  delete -t users -f '{"email":"test@example.com"}'
```

### 4. Advanced Queries

```bash
# Multiple filters
python supamap.py -u https://target.supabase.co -k eyJhbGc... \
  query -t orders -f '{"status":"pending","amount":"100"}' -l 200

# With authentication token
python supamap.py -u https://target.supabase.co -k eyJhbGc... \
  -a eyJhbGc... list -t private_data
```

---

## 🛡️ Security & Ethics

### ⚠️ Important Notice

This tool is designed for **authorized security testing only**. Unauthorized access to computer systems is illegal.

### Legal Use Cases

- ✅ Bug bounty programs with explicit authorization
- ✅ Penetration testing with written permission
- ✅ Security audits of your own applications
- ✅ Red team exercises with proper scope

### Illegal Use Cases

- ❌ Unauthorized access to systems
- ❌ Data theft or exfiltration
- ❌ Attacking systems without permission
- ❌ Any activity violating local laws

**By using this tool, you agree to use it responsibly and legally.**

---

## 🔧 Advanced Features

### Batch Processing

SupaMap automatically handles large datasets with batch processing:

```python
# Exports in batches of 1000 records
python supamap.py -u URL -k KEY export -t large_table -o output.json -l 50000
```

### Error Handling

All operations include comprehensive error handling:
- Network timeouts
- Invalid JSON parsing
- Authentication failures
- Permission denied scenarios

### Output Formatting

All data is output in clean, readable JSON format:

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

## 🐛 Bug Bounty Tips

### Finding Vulnerable Instances

1. **Look for exposed API keys** in:
   - JavaScript files
   - Mobile app code
   - GitHub repositories
   - Browser developer tools

2. **Test RLS (Row Level Security)**:
   - Try accessing tables without authentication
   - Test with different user contexts
   - Look for privilege escalation vectors

3. **Common Misconfigurations**:
   - Anonymous key with write access
   - Missing RLS policies
   - Overly permissive policies
   - Exposed service role keys

### Reporting Format

When reporting vulnerabilities:

```markdown
**Title**: Unauthorized Data Access in Supabase Instance

**Severity**: High/Critical

**Description**: 
The application exposes a Supabase API key that allows unauthorized 
access to sensitive user data without authentication.

**Steps to Reproduce**:
1. Extract API key from [source]
2. Use SupaMap to enumerate tables
3. Access sensitive data without authentication

**Impact**:
- Full database read access
- Potential data exfiltration
- PII exposure

**Proof of Concept**:
[Attach screenshots/logs from SupaMap]

**Remediation**:
- Implement proper RLS policies
- Rotate exposed API keys
- Enable authentication requirements
```

---

## 📚 Resources

### Supabase Security

- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth/row-level-security)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [API Authentication](https://supabase.com/docs/guides/api)

### Bug Bounty Platforms

- [HackerOne](https://hackerone.com)
- [Bugcrowd](https://bugcrowd.com)
- [Intigriti](https://intigriti.com)
- [YesWeHack](https://yeswehack.com)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/supamap.git
cd supamap

# Install dev dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**dnlalb.exe**

- 🐦 Twitter: [@yourusername](https://twitter.com/yourusername)
- 🌐 Website: [yourwebsite.com](https://yourwebsite.com)
- 📧 Email: your.email@example.com

---

## ⭐ Star History

If you find this tool useful, please consider giving it a star!

---

## 🙏 Acknowledgments

- Thanks to the Supabase team for building an awesome platform
- Inspired by the security research community
- Built for ethical hackers and security professionals

---

## 📊 Statistics

- **Lines of Code**: ~400
- **Dependencies**: 1 (requests)
- **Python Version**: 3.7+
- **Platforms**: Linux, macOS, Windows

---

## 🔄 Changelog

### v1.0.0 (2024)
- Initial release
- Basic CRUD operations
- Table enumeration
- Bulk export functionality
- Authentication support

---

<div align="center">

**Made with ❤️ by dnlalb.exe**

*For authorized security testing only*

[⬆ Back to Top](#-supamap)

</div>