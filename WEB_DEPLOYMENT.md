# SNATT Web Application - Deployment Guide

This guide explains how to deploy the SNATT web application to Vercel.

## 🌐 Project Structure

```
automa/
├── web/                          # Next.js frontend application
│   ├── app/                      # Next.js app directory
│   │   ├── components/           # React components (5 panels)
│   │   ├── globals.css          # Global styles
│   │   ├── layout.js            # Root layout
│   │   └── page.js              # Main page
│   ├── api/                      # Python FastAPI backend
│   │   ├── main.py              # API endpoints
│   │   └── requirements.txt     # Python dependencies
│   ├── package.json             # Node.js dependencies
│   ├── next.config.js           # Next.js configuration
│   ├── tailwind.config.js       # Tailwind CSS config
│   └── postcss.config.js        # PostCSS config
├── vercel.json                   # Vercel deployment config
└── src/                          # Original Python backend (reused)
```

## 🚀 Deployment to Vercel

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Push to GitHub**:
   ```powershell
   cd e:\automa
   git add .
   git commit -m "Add web application for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account
   - Click "Add New Project"
   - Select your `SNATT` repository
   - Configure project:
     - **Framework Preset**: Next.js
     - **Root Directory**: `web`
     - **Build Command**: `npm run build`
     - **Output Directory**: `.next`
   - Click "Deploy"

3. **Done!** Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```powershell
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```powershell
   vercel login
   ```

3. **Deploy**:
   ```powershell
   cd e:\automa\web
   vercel
   ```

4. **Follow prompts**:
   - Set up and deploy? Yes
   - Which scope? (your account)
   - Link to existing project? No
   - Project name: snatt-web
   - Directory: `./`
   - Override settings? No

5. **Deploy to production**:
   ```powershell
   vercel --prod
   ```

## ⚙️ Configuration

### Environment Variables

If you need to configure API endpoints or other settings:

1. Go to your Vercel project dashboard
2. Settings → Environment Variables
3. Add variables:
   - `API_URL`: Your API endpoint (if using external API)
   - `NEXT_PUBLIC_API_URL`: Client-side API URL

### Custom Domain

1. Go to your project on Vercel
2. Settings → Domains
3. Add your custom domain
4. Update DNS records as instructed

## 🛠️ Local Development

### Setup

1. **Install Node.js dependencies**:
   ```powershell
   cd e:\automa\web
   npm install
   ```

2. **Install Python dependencies** (for local API):
   ```powershell
   cd api
   pip install -r requirements.txt
   ```

### Run Development Server

1. **Start Next.js frontend**:
   ```powershell
   cd e:\automa\web
   npm run dev
   ```
   Access at: http://localhost:3000

2. **Start Python API** (in separate terminal):
   ```powershell
   cd e:\automa\web\api
   python main.py
   ```
   API runs at: http://localhost:8000

## 📝 Key Differences from Desktop Version

### Web Application:
- ✅ Access from any browser
- ✅ No installation required
- ✅ Cross-platform (Windows/Mac/Linux)
- ✅ Mobile responsive
- ✅ Deployed on Vercel
- ✅ Automatic HTTPS
- ⚠️ Requires internet connection
- ⚠️ Backend API needed for SSH operations

### Desktop Application:
- ✅ Direct SSH access to devices
- ✅ Works offline
- ✅ Local file storage
- ✅ Full system access
- ⚠️ Requires Python installation
- ⚠️ Platform-specific (Windows .exe)

## 🔒 Important Security Notes

### For Production Deployment:

1. **Never expose SSH credentials in frontend code**
2. **Use proper authentication** (JWT tokens, OAuth)
3. **Implement rate limiting** on API endpoints
4. **Use environment variables** for sensitive data
5. **Enable CORS** only for your domain
6. **Use HTTPS** (Vercel provides this automatically)

### Network Device Access:

The web version requires special consideration for SSH:
- SSH connections must be handled by backend API
- Backend should be on a server with network access to devices
- Consider using a VPN or bastion host for security
- Never allow direct SSH from browser to devices

## 🚧 Limitations & Next Steps

### Current Implementation:
- Frontend is complete and functional
- API endpoints are defined
- Basic connectivity simulated

### To Make Fully Functional:

1. **Deploy Backend API Separately**:
   - Vercel serverless functions have 10-second timeout
   - SSH operations take longer
   - Solution: Deploy API on:
     - AWS EC2 / DigitalOcean Droplet
     - Google Cloud Run
     - Azure Container Instances
     - Render.com / Railway.app

2. **Add Authentication**:
   ```javascript
   // Add NextAuth.js for user authentication
   npm install next-auth
   ```

3. **Add Database**:
   ```javascript
   // Store devices, credentials, backups
   npm install prisma @prisma/client
   ```

4. **WebSocket for Real-time Updates**:
   ```javascript
   // Real-time device status updates
   npm install socket.io socket.io-client
   ```

## 📊 Architecture Overview

```
┌─────────────┐
│   Browser   │ ← User accesses via web browser
└──────┬──────┘
       │ HTTPS
       ↓
┌─────────────┐
│   Vercel    │ ← Hosts Next.js frontend
│  (Frontend) │
└──────┬──────┘
       │ API Calls
       ↓
┌─────────────┐
│  API Server │ ← FastAPI backend (separate hosting)
│  (Backend)  │
└──────┬──────┘
       │ SSH
       ↓
┌─────────────┐
│   Network   │ ← Your network devices
│   Devices   │
└─────────────┘
```

## 🎯 Recommended Deployment Strategy

### Phase 1: Frontend Only (Current)
- Deploy Next.js to Vercel
- Use mock data for testing
- Share with stakeholders for UI feedback

### Phase 2: Add Backend API
- Deploy FastAPI to Railway/Render
- Connect to real network devices
- Implement authentication

### Phase 3: Production Ready
- Add database (PostgreSQL)
- Implement WebSockets
- Add monitoring and logging
- Set up CI/CD pipeline

## 📚 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 🆘 Troubleshooting

### Build Fails on Vercel
- Check Node.js version (use 18.x or later)
- Verify all dependencies in package.json
- Check build logs in Vercel dashboard

### API Not Working
- Verify API_URL environment variable
- Check CORS settings
- Ensure backend is running and accessible

### Styling Issues
- Run `npm run build` locally first
- Check Tailwind CSS configuration
- Clear browser cache

---

**Need Help?** Check the main DEPLOYMENT.md for more options or create an issue on GitHub.
