# SNATT - Smart Network Automation and Troubleshooting Tool

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![React](https://img.shields.io/badge/react-19-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Overview

SNATT is available as both a **desktop application** (Python + CustomTkinter) and a **web application** (React + Vite). Choose the version that fits your needs:

- **Desktop**: Direct SSH connections, local operations, full network device access
- **Web**: Browser-based, no installation, team collaboration, Vercel-deployable

Both versions share the same 5 core panels: Discovery, Diagnostics, Backup, Reports, and Settings.

## ✨ Key Features

- 🔍 **Automated Network Discovery** - Scan subnets and identify routers/switches automatically
- 🔐 **Secure Connection Management** - SSH-based connections with encrypted credential storage
- 🧰 **Intelligent Troubleshooting** - Execute diagnostic workflows and identify issues automatically
- 💾 **Configuration Backup** - Batch backup with version control and timestamping
- 📊 **Professional Reporting** - Generate Excel/PDF reports with health summaries
- 🖥️ **Modern GUI** - Intuitive interface with color-coded status indicators

## 🚀 Quick Start

### Desktop Application (Python)

**Prerequisites:**
- Python 3.8 or higher
- pip package manager
- Network access to devices you want to manage

**Installation:**

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/LingeshwarKulal/SNATT.git
   cd SNATT
   ```

2. **Create a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```powershell
   python src/main.py
   ```

### Web Application (React + Vite)

**Prerequisites:**
- Node.js 18+ and npm

**Local Development:**

1. **Navigate to React app:**
   ```powershell
   cd snatt-react
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Run development server:**
   ```powershell
   npm run dev
   ```
   Visit http://localhost:5173

4. **Build for production:**
   ```powershell
   npm run build
   ```

**Deploy to Vercel:**
1. Go to [vercel.com](https://vercel.com)
2. Import `LingeshwarKulal/SNATT`
3. Set Root Directory to `snatt-react`
4. Deploy!

See **REACT_DEPLOYMENT.md** for detailed instructions.

## 📁 Project Structure

```
automa/
├── src/                          # Source code
│   ├── main.py                   # Application entry point
│   ├── gui/                      # GUI components
│   │   ├── main_window.py
│   │   ├── discovery_panel.py
│   │   ├── diagnostics_panel.py
│   │   ├── backup_panel.py
│   │   ├── reports_panel.py
│   │   └── settings_panel.py
│   ├── engines/                  # Core business logic
│   │   ├── discovery_engine.py
│   │   ├── connection_manager.py
│   │   ├── troubleshooting_engine.py
│   │   ├── backup_manager.py
│   │   └── reporting_engine.py
│   ├── models/                   # Data models
│   │   ├── device.py
│   │   ├── diagnostic_result.py
│   │   └── backup_record.py
│   ├── utils/                    # Utility functions
│   │   ├── logger.py
│   │   ├── credential_manager.py
│   │   ├── config_manager.py
│   │   └── validators.py
│   └── resources/                # Static resources
│       ├── icons/
│       └── templates/
├── tests/                        # Test suite
│   ├── unit/
│   ├── integration/
│   └── test_data/
├── backups/                      # Device configuration backups
├── reports/                      # Generated reports
├── logs/                         # Application logs
├── docs/                         # Documentation
│   ├── user_guide.md
│   ├── api_reference.md
│   └── architecture.md
├── config/                       # Configuration files
│   └── default_config.json
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── PRD.md                        # Product Requirements Document
└── README.md                     # This file
```

## 🛠️ Technology Stack

- **GUI Framework:** CustomTkinter (modern themed UI)
- **Network Automation:** Netmiko, NAPALM, Paramiko
- **Network Discovery:** Scapy, PySNMP
- **Reporting:** Pandas, OpenPyXL, ReportLab
- **Data Storage:** SQLite, JSON
- **Security:** Keyring (credential encryption)
- **Testing:** Pytest
- **Code Quality:** Black, Flake8

## 📖 Usage Guide

### 1. Network Discovery

1. Launch SNATT and navigate to the **Discovery** tab
2. Enter your subnet (e.g., `192.168.1.0/24`)
3. Click **Scan Network**
4. Review discovered devices in the results table
5. Select devices and click **Connect**

### 2. Run Diagnostics

1. Navigate to the **Diagnostics** tab
2. Select one or more connected devices
3. Choose a diagnostic workflow (Interface Health, CPU Check, etc.)
4. Click **Run Diagnostics**
5. Review results with color-coded indicators

### 3. Backup Configurations

1. Navigate to the **Backup** tab
2. Select devices to backup
3. Choose configuration type (running/startup)
4. Click **Backup Now**
5. View backup history and compare versions

### 4. Generate Reports

1. Navigate to the **Reports** tab
2. Select report type and date range
3. Choose export format (Excel/PDF)
4. Click **Generate Report**
5. Report opens automatically

## 🔒 Security

- **Credential Storage:** Encrypted using OS keyring
- **Communication:** SSH only (no plaintext protocols)
- **Audit Logging:** All actions logged with timestamps
- **Input Validation:** All user inputs sanitized

## 🧪 Testing

Run the test suite:

```powershell
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage report
pytest --cov=src --cov-report=html
```

## 📊 Supported Devices

| Vendor | Status | Notes |
|--------|--------|-------|
| Cisco IOS | ✅ Full Support | All IOS versions |
| Cisco IOS-XE | ✅ Full Support | ISR, ASR series |
| Cisco NX-OS | ✅ Full Support | Nexus switches |
| Juniper Junos | 🟡 Tested | Basic operations |
| HP/Aruba | 🟡 Tested | ProCurve, ArubaOS |
| Huawei | 🟡 Community | VRP platform |
| MikroTik | 🟡 Community | RouterOS |

## 🐛 Troubleshooting

### Common Issues

**Problem:** Application won't start
- **Solution:** Ensure Python 3.8+ is installed, check `python --version`

**Problem:** Cannot discover devices
- **Solution:** Check network connectivity, firewall rules, ICMP enabled

**Problem:** SSH connection fails
- **Solution:** Verify credentials, ensure SSH enabled on devices, check port 22

**Problem:** Reports not generating
- **Solution:** Check write permissions in reports/ directory

### Logs

Application logs are stored in `logs/snatt.log`. Check this file for detailed error messages.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to all functions
- Write unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🗺️ Roadmap

### Phase 1 - MVP (v0.1) ✅ Current
- [x] Project structure
- [x] Basic network discovery
- [x] SSH connection to Cisco devices
- [x] Simple configuration backup
- [ ] Basic GUI

### Phase 2 - Core Features (v1.0)
- [ ] Multi-vendor support
- [ ] Complete troubleshooting workflows
- [ ] Batch operations
- [ ] Excel/PDF reporting
- [ ] Full GUI implementation

### Phase 3 - Advanced (v1.5)
- [ ] Configuration diff viewer
- [ ] Scheduled backups
- [ ] Custom workflows
- [ ] API integrations

### Phase 4 - Enterprise (v2.0)
- [ ] Multi-user support
- [ ] Web dashboard
- [ ] SNMP monitoring
- [ ] ML anomaly detection

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Issues:** Report bugs and feature requests in the Issues section
- **Email:** support@snatt.dev (placeholder)

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Network automation powered by [Netmiko](https://github.com/ktbyers/netmiko)
- Inspired by the network engineering community

---

**Made with ❤️ for Network Engineers**

*Last Updated: October 5, 2025*
