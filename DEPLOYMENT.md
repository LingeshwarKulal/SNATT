# SNATT Deployment Guide

## Understanding SNATT's Architecture

SNATT is a **desktop application** built with:
- Python + CustomTkinter (Desktop GUI)
- Direct SSH connections to network devices
- Local file system access (logs, backups, reports)

**Important**: This is NOT a web application and cannot be deployed to web hosting platforms like Vercel, Netlify, or Heroku.

## Deployment Options

### Option 1: Local Installation (Recommended)

**Best for**: Personal use, small teams, secure environments

**Steps**:
1. Users clone the repository:
   ```bash
   git clone https://github.com/LingeshwarKulal/SNATT.git
   cd SNATT
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/main.py
   ```

**Pros**:
- Simple setup
- Direct network access
- Secure (no internet exposure)
- Full control

**Cons**:
- Requires Python installation
- Each user installs separately

---

### Option 2: Windows Executable Distribution

**Best for**: Users without Python knowledge, easy distribution

**Steps to Build**:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_executable.py
   ```

3. Distribute the executable:
   - Location: `dist/SNATT.exe`
   - Users double-click to run
   - No Python installation needed

**Pros**:
- Single .exe file
- No Python needed
- Easy for non-technical users
- Can distribute via USB/email/download

**Cons**:
- Large file size (~100-200 MB)
- Windows only
- Need to rebuild for updates

---

### Option 3: Network Share Deployment

**Best for**: Corporate environments, centralized management

**Setup**:
1. Install SNATT on a shared network location:
   ```
   \\fileserver\apps\SNATT\
   ```

2. Create a batch file for users:
   ```batch
   @echo off
   cd /d \\fileserver\apps\SNATT
   python src/main.py
   pause
   ```

3. Users run the batch file from their desktop shortcut

**Pros**:
- Centralized updates
- Single installation point
- Easy to maintain

**Cons**:
- Requires network share
- Users need Python installed
- Network dependency

---

### Option 4: Convert to Web Application (Advanced)

**Best for**: Remote access, multi-user environments, cloud deployment

**Requirements** (Complete Rewrite):

1. **Backend** (Python):
   - Flask/FastAPI for API
   - WebSocket for real-time updates
   - JWT authentication
   - Database for user management
   - Background workers for SSH tasks

2. **Frontend** (JavaScript):
   - React/Vue.js
   - Modern UI components
   - Real-time updates
   - Responsive design

3. **Infrastructure**:
   - VPS/Cloud server (not Vercel)
   - SSH bastion host
   - Secure credential storage
   - Network access to devices

**Estimated Effort**: 2-3 months full-time development

**Example Stack**:
```
Frontend: React + Tailwind CSS
Backend: FastAPI + Celery
Database: PostgreSQL
Cache: Redis
Hosting: AWS/DigitalOcean/Azure
```

**Pros**:
- Access from anywhere
- Multi-user support
- Modern web interface
- Centralized management

**Cons**:
- Complete rewrite needed
- Complex infrastructure
- Security challenges
- Higher hosting costs
- Requires different hosting (VPS, not Vercel)

---

## Why Vercel Won't Work

**Vercel is designed for**:
- Static websites (HTML/CSS/JS)
- Next.js applications
- Serverless functions (short-lived)
- Frontend frameworks

**Vercel CANNOT run**:
- Desktop GUI applications (CustomTkinter)
- Long-running SSH connections
- Applications requiring Tkinter/GTK/Qt
- Direct system access applications

**Error explanation**:
The "404: NOT_FOUND" error occurs because Vercel looks for a web application entry point (like `index.html` or `pages/`) but finds a Python desktop app instead.

---

## Recommended Path Forward

### For Current Desktop Version:
1. **Immediate**: Use Option 1 (Local Installation)
2. **Better UX**: Build Option 2 (Windows Executable)
3. **Team Use**: Setup Option 3 (Network Share)

### For Web Version:
If you need web access, consider hiring a developer to rebuild as a web application, or learn web development to convert it yourself.

---

## Quick Distribution Method

**Create a release on GitHub**:

1. Build the executable:
   ```bash
   python build_executable.py
   ```

2. Create a release on GitHub:
   - Go to: https://github.com/LingeshwarKulal/SNATT/releases
   - Click "Create a new release"
   - Tag version: v1.0.0
   - Upload `dist/SNATT.exe`
   - Add release notes

3. Users download and run:
   - Download SNATT.exe
   - Double-click to run
   - No installation needed

---

## Security Notes

⚠️ **Important for Web Version**:
- Never expose SSH credentials to the internet without proper encryption
- Use VPN for remote network device access
- Implement proper authentication
- Regular security audits

✅ **Current Desktop Version**:
- Credentials stored locally
- Direct SSH connections
- No internet exposure
- Secure by design

---

## Need Help?

- **Desktop version issues**: Check docs/user_guide.md
- **Building executable**: Use build_executable.py
- **Web conversion**: Consider hiring a web developer
- **GitHub**: https://github.com/LingeshwarKulal/SNATT

---

**Summary**: SNATT is a desktop application. Run it locally with `python src/main.py` or build an executable for easy distribution. It cannot be deployed to Vercel.
