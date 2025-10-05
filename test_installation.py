# Quick Test Script for SNATT
# Run this to verify installation and basic functionality

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*60)
print("SNATT - Installation & Syntax Check")
print("="*60)
print()

# Test 1: Check Python version
print("1. Checking Python version...")
if sys.version_info < (3, 8):
    print("   ❌ FAILED: Python 3.8+ required")
    print(f"   Current version: {sys.version}")
    sys.exit(1)
else:
    print(f"   ✅ PASSED: Python {sys.version_info.major}.{sys.version_info.minor}")
print()

# Test 2: Check if requirements are met
print("2. Checking dependencies...")
required_packages = [
    'customtkinter',
    'netmiko',
    'napalm',
    'paramiko',
    'scapy',
    'pandas',
    'openpyxl',
    'keyring',
    'cryptography',
    'colorlog'
]

missing = []
for package in required_packages:
    try:
        __import__(package)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NOT INSTALLED")
        missing.append(package)

if missing:
    print()
    print("   Missing packages detected!")
    print("   Run: pip install -r requirements.txt")
    print()
else:
    print()
    print("   All dependencies installed!")
    print()

# Test 3: Check directory structure
print("3. Checking directory structure...")
required_dirs = [
    'src',
    'src/engines',
    'src/models',
    'src/utils',
    'src/gui',
    'config',
    'docs',
    'tests',
]

for directory in required_dirs:
    if os.path.exists(directory):
        print(f"   ✅ {directory}/")
    else:
        print(f"   ❌ {directory}/ - MISSING")
print()

# Test 4: Check key files
print("4. Checking key files...")
required_files = [
    'src/main.py',
    'src/engines/discovery_engine.py',
    'src/engines/connection_manager.py',
    'src/engines/troubleshooting_engine.py',
    'src/engines/backup_manager.py',
    'src/engines/reporting_engine.py',
    'src/gui/main_window.py',
    'src/gui/discovery_panel.py',
    'src/gui/diagnostics_panel.py',
    'src/gui/backup_panel.py',
    'src/gui/reports_panel.py',
    'src/gui/settings_panel.py',
    'config/default_config.json',
    'requirements.txt',
]

for filepath in required_files:
    if os.path.exists(filepath):
        print(f"   ✅ {filepath}")
    else:
        print(f"   ❌ {filepath} - MISSING")
print()

# Test 5: Syntax check Python files (if no imports needed)
print("5. Checking Python syntax...")
try:
    import py_compile
    
    python_files = [
        'src/main.py',
        'src/utils/logger.py',
        'src/utils/config_manager.py',
        'src/utils/credential_manager.py',
        'src/utils/validators.py',
        'src/models/device.py',
        'src/models/diagnostic_result.py',
        'src/models/backup_record.py',
    ]
    
    syntax_ok = True
    for pyfile in python_files:
        if os.path.exists(pyfile):
            try:
                py_compile.compile(pyfile, doraise=True)
                print(f"   ✅ {pyfile}")
            except py_compile.PyCompileError as e:
                print(f"   ❌ {pyfile} - SYNTAX ERROR")
                print(f"      {e}")
                syntax_ok = False
    
    if syntax_ok:
        print()
        print("   All checked files have valid syntax!")
    else:
        print()
        print("   Some files have syntax errors!")
    print()

except Exception as e:
    print(f"   ⚠️  Could not perform syntax check: {e}")
    print()

# Summary
print("="*60)
print("SUMMARY")
print("="*60)

if not missing and sys.version_info >= (3, 8):
    print("✅ SNATT is ready to run!")
    print()
    print("To start the application:")
    print("   python src/main.py")
    print()
    print("For first-time setup:")
    print("   1. Click 'Settings' in the GUI")
    print("   2. Go to 'Credentials' tab")
    print("   3. Add your device credentials")
    print("   4. Start discovering devices!")
    print()
else:
    print("⚠️  SNATT needs setup!")
    print()
    if sys.version_info < (3, 8):
        print("   - Upgrade Python to 3.8 or higher")
    if missing:
        print("   - Install missing dependencies:")
        print("     pip install -r requirements.txt")
    print()

print("="*60)
