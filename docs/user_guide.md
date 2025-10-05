# SNATT User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features](#features)
5. [Troubleshooting](#troubleshooting)

## Introduction

SNATT (Smart Network Automation and Troubleshooting Tool) is designed to simplify network management tasks through automation. This guide will help you get started and make the most of SNATT's features.

## Installation

### Requirements
- Python 3.8 or higher
- Windows 10/11, Linux, or macOS
- Network access to devices you want to manage

### Installation Steps

1. **Extract or clone the project:**
   ```powershell
   cd e:\automa
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

## Getting Started

### First Launch

1. **Start the application:**
   ```powershell
   python src/main.py
   ```

2. **Configure Credentials:**
   - Navigate to Settings → Credentials
   - Click "Add Credential"
   - Enter:
     - Name: e.g., "cisco_lab"
     - Username: Your device username
     - Password: Your device password
     - Enable Password: (optional) Privileged mode password

### Network Discovery

1. Navigate to the **Discovery** tab
2. Enter your network range:
   - Subnet format: `192.168.1.0/24`
   - Range format: `192.168.1.1-192.168.1.50`
3. Click **Scan Network**
4. Wait for scan to complete
5. Review discovered devices in the table
6. Select devices and assign credentials
7. Click **Connect** to establish SSH connections

### Running Diagnostics

1. Navigate to the **Diagnostics** tab
2. Select one or more connected devices
3. Choose a diagnostic workflow:
   - **Interface Health Check** - Checks interface status
   - **CPU & Memory Check** - Monitors resource usage
   - **Connectivity Check** - Verifies routing and reachability
   - **Log Analysis** - Scans logs for errors
4. Click **Run Diagnostics**
5. Review results with color-coded indicators:
   - 🟢 Green = Normal
   - 🟡 Yellow = Warning
   - 🔴 Red = Critical

### Configuration Backup

1. Navigate to the **Backup** tab
2. Select devices to backup
3. Choose configuration type:
   - Running configuration (current)
   - Startup configuration (saved)
   - Both
4. Click **Backup Now**
5. Monitor progress
6. View backup history and compare configurations

### Generating Reports

1. Navigate to the **Reports** tab
2. Select report type:
   - Network Health Report
   - Backup Report
   - Custom Report
3. Choose date range (if applicable)
4. Select export format:
   - Excel (.xlsx) - Recommended for detailed analysis
   - PDF - For sharing with stakeholders
   - CSV - For data import/processing
5. Click **Generate Report**
6. Report will automatically open when ready

## Features

### Device Management

**Supported Vendors:**
- Cisco IOS/IOS-XE/NX-OS
- Juniper Junos
- HP/Aruba
- Huawei VRP
- MikroTik RouterOS

**Connection Methods:**
- SSH (Primary)
- API (For supported platforms)

### Automation Workflows

**Pre-configured Workflows:**

1. **Interface Health Check**
   - Detects down interfaces
   - Identifies error-disabled ports
   - Shows interface statistics

2. **CPU & Memory Check**
   - Monitors CPU usage
   - Checks memory utilization
   - Alerts on high usage (configurable thresholds)

3. **Connectivity Check**
   - Verifies routing tables
   - Checks default gateway
   - Tests reachability

4. **Log Analysis**
   - Scans for critical errors
   - Identifies warnings
   - Provides recommendations

### Report Types

**Network Health Report:**
- Executive summary with health score
- Device inventory
- Health status per device
- Critical issues list
- Warnings and recommendations

**Backup Report:**
- Backup success/failure status
- File sizes and locations
- Timestamps
- Error messages (if any)

## Configuration

### Application Settings

Located in `config/default_config.json`:

**Network Settings:**
- `default_timeout`: Connection timeout (seconds)
- `max_concurrent_connections`: Maximum simultaneous connections
- `retry_attempts`: Number of connection retries

**Discovery Settings:**
- `max_threads`: Parallel scan threads
- `ping_timeout`: Ping timeout (seconds)

**Backup Settings:**
- `retention_days`: Days to keep backups
- `auto_backup_enabled`: Enable scheduled backups
- `directory`: Backup storage location

**Reporting Settings:**
- `company_name`: Your organization name
- `default_format`: Preferred export format

### Custom Workflows

You can create custom diagnostic workflows by editing the configuration file:

```json
"diagnostics": {
  "workflows": {
    "my_custom_check": {
      "name": "My Custom Check",
      "commands": [
        "show version",
        "show interfaces status"
      ],
      "enabled": true
    }
  }
}
```

## Troubleshooting

### Common Issues

**Problem: Application won't start**
- Solution: Verify Python 3.8+ is installed: `python --version`
- Check all dependencies are installed: `pip install -r requirements.txt`

**Problem: Cannot discover devices**
- Solution: 
  - Verify network connectivity
  - Check firewall allows ICMP (ping)
  - Ensure you're on the correct network segment

**Problem: SSH connection fails**
- Solution:
  - Verify credentials are correct
  - Check SSH is enabled on devices
  - Confirm port 22 is accessible
  - Try connecting manually with SSH client first

**Problem: Diagnostics show errors**
- Solution:
  - Check device is properly connected
  - Verify user has sufficient privileges
  - Review command output in detail
  - Check device-specific command syntax

**Problem: Reports not generating**
- Solution:
  - Check write permissions in `reports/` directory
  - Verify sufficient disk space
  - Review logs in `logs/snatt_YYYYMMDD.log`

### Logging

Application logs are stored in the `logs/` directory with daily rotation.

**Log Levels:**
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

**Viewing Logs:**
```powershell
# View today's log
Get-Content logs\snatt_20251005.log -Tail 50
```

### Support

For additional help:
1. Check the logs directory for detailed error messages
2. Review the PRD.md for detailed feature specifications
3. Consult device vendor documentation for command syntax

## Best Practices

1. **Start Small**: Begin with a small subnet to test functionality
2. **Test Credentials**: Verify credentials on one device before batch operations
3. **Regular Backups**: Schedule automated backups for critical devices
4. **Monitor Reports**: Review health reports regularly
5. **Update Regularly**: Keep SNATT and dependencies up to date

## Keyboard Shortcuts

- `Ctrl+1` - Discovery panel
- `Ctrl+2` - Diagnostics panel
- `Ctrl+3` - Backup panel
- `Ctrl+4` - Reports panel
- `Ctrl+5` - Settings panel
- `F5` - Refresh current view
- `Ctrl+Q` - Quit application

---

**Last Updated:** October 5, 2025  
**Version:** 0.1.0
