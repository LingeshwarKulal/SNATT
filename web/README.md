# SNATT Web Application - Quick Setup

## 🚀 Quick Start

### 1. Install Dependencies
```powershell
cd e:\automa\web
npm install
```

### 2. Run Development Server
```powershell
npm run dev
```

Visit: http://localhost:3000

## 📦 What's Included

- ✅ Modern React UI with Next.js 14
- ✅ Tailwind CSS for styling
- ✅ 5 Functional Panels:
  - Discovery
  - Diagnostics
  - Backup
  - Reports
  - Settings
- ✅ Responsive design
- ✅ Ready for Vercel deployment

## 🌐 Deploy to Vercel

### Method 1: GitHub Integration (Recommended)
1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your SNATT repository
4. Set root directory to `web`
5. Deploy!

### Method 2: Vercel CLI
```powershell
npm install -g vercel
cd e:\automa\web
vercel login
vercel --prod
```

## 🎨 Features

- **No Installation Required**: Runs in any modern browser
- **Cross-Platform**: Works on Windows, Mac, Linux, mobile
- **Modern UI**: Clean, intuitive interface
- **Real-time Updates**: (Backend integration required)
- **Secure**: HTTPS by default on Vercel

## ⚡ Next Steps

1. **Deploy Frontend**: Push to Vercel (done in 2 minutes)
2. **Backend API**: For full functionality, deploy API separately
3. **Authentication**: Add user login (NextAuth.js)
4. **Database**: Store data persistently (Prisma + PostgreSQL)

## 📝 Note

This web version provides the same interface as the desktop app but runs in a browser. For full SSH functionality to network devices, you'll need to deploy the backend API on a server with network access to your devices.

See **WEB_DEPLOYMENT.md** for complete deployment instructions.
