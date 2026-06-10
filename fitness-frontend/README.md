# FitHydrate — React Frontend

A React + Vite frontend for the fitness MCP server deployed on Render.

## Features
- Register / Login (JWT auth)
- Tool 1: Daily Water Intake calculator
- Tool 2: Sweat Loss Estimator (v1 basic + v2 with food tips)
- Tool 3: Weather-Adjusted Hydration (live Open-Meteo data)

---

## Step-by-Step: Run locally

### 1. Install Node.js
Download from https://nodejs.org — get the LTS version.

### 2. Clone or copy this folder into your repo
Put the `fitness-frontend/` folder inside your existing `takatokoro/fitness-mcp` repo, or as a separate repo.

### 3. Install dependencies
```bash
cd fitness-frontend
npm install
```

### 4. Run the dev server
```bash
npm run dev
```
Open http://localhost:5173 in your browser.

---

## Step-by-Step: Deploy to Vercel (free)

### 1. Push to GitHub
If you added this folder inside your existing repo, just commit and push:
```bash
git add fitness-frontend/
git commit -m "Add React frontend"
git push
```

### 2. Sign up at vercel.com
Use your GitHub account — it's free.

### 3. Click "Add New Project"
- Select your `fitness-mcp` repository
- Set **Root Directory** to `fitness-frontend`
- Framework Preset: Vite (Vercel auto-detects this)
- Click **Deploy**

That's it! Vercel gives you a live URL like `https://fitness-mcp-frontend.vercel.app`.

### 4. Every future deploy is automatic
Push to GitHub → Vercel rebuilds automatically.

---

## File structure explained

```
fitness-frontend/
  src/
    api.js              ← All fetch() calls to your Render server
    App.jsx             ← Main app: handles auth state + tab switching
    index.css           ← All styles
    main.jsx            ← Entry point (don't edit)
    components/
      ResultBox.jsx     ← Shows API response as formatted JSON
    pages/
      AuthPage.jsx      ← Login + Register form
      WaterIntakePage.jsx
      SweatLossPage.jsx
      WeatherHydrationPage.jsx
  index.html
  package.json
  vite.config.js
  vercel.json           ← Tells Vercel to handle client-side routing
```

## Changing the backend URL
Edit the first line of `src/api.js`:
```js
const BASE_URL = 'https://fitness-mcp-6vuf.onrender.com'
```
