# SNATT Web - Vercel Deployment Configuration

## ⚙️ Vercel Project Settings

When importing your project to Vercel, use these exact settings:

### General Settings:
- **Framework Preset**: `Next.js`
- **Root Directory**: `web`  ⚠️ **IMPORTANT - Must set this!**
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### Build & Development Settings:
- **Node.js Version**: `18.x` (or latest)

## 📋 Step-by-Step Deployment

### 1. Delete Existing Project (if any)
- Go to Vercel Dashboard
- Settings → General → Delete Project

### 2. Import Fresh from GitHub
1. Click **"Add New Project"**
2. Select **"Import Git Repository"**
3. Choose: `LingeshwarKulal/SNATT`
4. Click **"Import"**

### 3. ⚠️ CRITICAL: Set Root Directory
**Before clicking Deploy:**
- Find **"Root Directory"** setting
- Click **"Edit"** 
- Enter: `web`
- Click **"Continue"**

### 4. Verify Settings
Make sure you see:
```
Framework Preset: Next.js
Root Directory: web ← Must be set!
Build Command: npm run build
Install Command: npm install
Output Directory: .next
```

### 5. Deploy!
Click **"Deploy"** and wait ~2 minutes

## ✅ Local Testing (Confirmed Working)

The application has been tested locally and works perfectly:

```powershell
cd e:\automa\web
npm install          # ✅ Installs successfully
npm run dev          # ✅ Runs on localhost:3000
npm run build        # ✅ Builds successfully
```

**Build Output:**
```
✓ Creating an optimized production build
✓ Compiled successfully
✓ Generating static pages (4/4)
✓ Finalizing page optimization

Route (app)                              Size     First Load JS
┌ ○ /                                    23.5 kB         111 kB
```

## 🐛 Common Vercel Errors & Solutions

### Error: "No Next.js version detected"
**Cause**: Root Directory not set to `web`
**Solution**: Set Root Directory to `web` in project settings

### Error: "Could not read package.json"
**Cause**: Vercel looking in wrong directory
**Solution**: Set Root Directory to `web`

### Error: "npm install failed"
**Cause**: Dependency issues
**Solution**: Already fixed - TypeScript removed from package.json

## 📸 What Settings Should Look Like

```
┌─────────────────────────────────────┐
│ Import Git Repository               │
├─────────────────────────────────────┤
│ Repository: LingeshwarKulal/SNATT   │
│ Branch: main                         │
│                                      │
│ Build and Output Settings            │
│ ┌─────────────────────────────────┐ │
│ │ Framework Preset: Next.js       │ │
│ │ Root Directory: web          ✓ │ │  ← MUST SET THIS!
│ │ Build Command: npm run build    │ │
│ │ Output Directory: .next         │ │
│ │ Install Command: npm install    │ │
│ └─────────────────────────────────┘ │
│                                      │
│          [Deploy] ←  Click here      │
└─────────────────────────────────────┘
```

## 🎯 Quick Fix Checklist

- [ ] Root Directory set to `web`
- [ ] Framework Preset is `Next.js`
- [ ] Latest code pushed to GitHub (commit: 74d4365)
- [ ] Old failed deployments deleted
- [ ] Fresh import from GitHub

## 🔗 After Successful Deployment

Your app will be available at:
- `https://snatt-[random].vercel.app`
- Or your custom domain

## 📞 Still Having Issues?

If deployment still fails after setting Root Directory to `web`:

1. **Check Vercel Build Logs** for specific errors
2. **Verify package.json exists** in `web/` directory
3. **Try Vercel CLI**:
   ```powershell
   cd e:\automa\web
   npm install -g vercel
   vercel login
   vercel --prod
   ```

## ✨ Expected Result

After deployment:
- URL: `https://your-project.vercel.app`
- Status: ✅ Ready
- Build Time: ~2 minutes
- All 5 panels functional
- Mobile responsive
- HTTPS enabled

---

**The app works perfectly locally - just need to set Root Directory to `web` on Vercel!**
