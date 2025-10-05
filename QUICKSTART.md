# SNATT Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Installation (2 minutes)

Open PowerShell and navigate to the project directory:

```powershell
cd e:\automa
```

Create and activate virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### Step 2: First Launch (1 minute)

Start SNATT:

```powershell
python src/main.py
```

The GUI will launch with a welcome screen.

### Step 3: Configure Credentials (1 minute)

1. Click **⚙️ Settings** in the left sidebar
2. Navigate to Credentials section
3. Click **Add Credential**
4. Enter:
   - **Name:** `my_devices` (or any name you prefer)
   - **Username:** Your network device username
   - **Password:** Your device password
   - **Enable Password:** (Optional) Your enable/privileged mode password
5. Click **Save**

### Step 4: Discover Devices (1 minute)

1. Click **🔍 Discovery** in the left sidebar
2. Enter your network subnet:
   - Example: `192.168.1.0/24`
   - Or range: `192.168.1.1-192.168.1.50`
3. Click **Scan Network**
4. Wait for scan to complete (typically 10-30 seconds)
5. View discovered devices in the table

### Step 5: Connect and Test (Optional)

1. Select a device from the discovery results
2. Assign the credential you created earlier
3. Click **Connect**
4. Once connected, go to **🧰 Diagnostics**
5. Select the device
6. Choose **Interface Health Check**
7. Click **Run Diagnostics**
8. Review results!

## 📋 Common Commands

### Running the Application
```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Run SNATT
python src/main.py
```

### Running Tests
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_device.py
```

### Checking Logs
```powershell
# View today's log file
Get-Content logs\snatt_*.log -Tail 50

# Follow log in real-time (while app is running)
Get-Content logs\snatt_*.log -Wait -Tail 10
```

## 🎯 Quick Tips

### Discovery
- **Use CIDR notation** for full subnets: `192.168.1.0/24`
- **Use IP ranges** for partial ranges: `192.168.1.1-192.168.1.50`
- **Scanning speed**: ~254 IPs scanned in 10-30 seconds

### Diagnostics
- Always **connect devices first** before running diagnostics
- Start with **Interface Health Check** - it's the fastest
- **CPU & Memory Check** shows resource utilization
- Results are color-coded: 🟢 Green = OK, 🟡 Yellow = Warning, 🔴 Red = Critical

### Backups
- Backups are stored in `backups/` directory
- Files are named: `{hostname}_{type}_{timestamp}.cfg`
- Use **batch backup** to backup multiple devices at once
- Set up **scheduled backups** in Settings for automation

### Reports
- **Excel format** is best for detailed analysis
- **PDF format** is best for sharing with management
- Reports are saved in `reports/` directory
- Include **charts** for visual representation (enable in Settings)

## 🔧 Troubleshooting Quick Fixes

### Problem: Can't discover devices
```powershell
# Test if you can ping manually
ping 192.168.1.1

# Check if you're on the right network
ipconfig
```

### Problem: Can't connect to device
```powershell
# Test SSH manually
ssh username@192.168.1.1

# If that works, check your credentials in SNATT
```

### Problem: Application errors
```powershell
# Check logs for details
Get-Content logs\snatt_*.log -Tail 50

# Ensure all dependencies are installed
pip install -r requirements.txt
```

## 📚 Next Steps

Once you're comfortable with the basics:

1. **Read the full User Guide**: `docs/user_guide.md`
2. **Review the PRD**: `PRD.md` - Complete project specifications
3. **Customize workflows**: Edit `config/default_config.json`
4. **Explore advanced features**: API integrations, scheduled tasks, custom reports

## 💡 Pro Tips

1. **Start small**: Test with 1-2 devices before scanning entire networks
2. **Save your inventory**: Export discovered devices to CSV for future reference
3. **Regular backups**: Schedule nightly backups for critical devices
4. **Monitor health**: Generate weekly health reports to track trends
5. **Use tags**: Organize devices with tags like "production", "lab", "critical"

## 🆘 Need Help?

- Check `docs/user_guide.md` for detailed documentation
- Review `PRD.md` for technical specifications
- Check application logs in `logs/` directory
- Common issues are documented in the User Guide

---

**Remember**: Always test on non-production devices first!

**Happy Automating! 🎉**
