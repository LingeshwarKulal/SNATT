"""
Build script to create a standalone Windows executable for SNATT.
Uses PyInstaller to package the application.
"""

import PyInstaller.__main__
import os

# Get the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# PyInstaller configuration
PyInstaller.__main__.run([
    'src/main.py',
    '--name=SNATT',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    f'--add-data={os.path.join(project_root, "config")}{os.pathsep}config',
    f'--add-data={os.path.join(project_root, "docs")}{os.pathsep}docs',
    '--hidden-import=customtkinter',
    '--hidden-import=netmiko',
    '--hidden-import=napalm',
    '--hidden-import=paramiko',
    '--hidden-import=openpyxl',
    '--hidden-import=reportlab',
    '--collect-all=customtkinter',
    '--noconsole',
])

print("\n" + "="*60)
print("Build complete!")
print(f"Executable location: {os.path.join(project_root, 'dist', 'SNATT.exe')}")
print("="*60)
