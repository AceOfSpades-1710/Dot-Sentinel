# Cloud Deployment Instructions 🚀

This guide provides exactly what you need to deploy your project to Vercel (Frontend) and Render (Backend) **without breaking local functionality or modifying your React components directly**.

## 1. List of New Files Added

**Backend Wrapper Files** (in `Dot-Sentinel/` root):
*   `render.yaml` - Tells Render how to build and start your FastAPI app.
*   `requirements.txt` - Wrapper to install your `parser/requirements.txt` correctly.
*   `runtime.txt` - Ensures Render uses a stable Python 3.11 version.
*   `.env.example` - Backend environment variable template.

**Frontend Wrapper Files** (in `Dot-Sentinel/Front-End/`):
*   `vercel.json` - Fallback Vite SPA routing for Vercel.
*   `.env.example` - Frontend environment variable template.
*   `src/config.js` - Helper file exposing the environment variable API URL (does not modify existing logic).

---

## 2. Environment Variables Required

### **Backend (Render)**
| Variable Name | Purpose | Example Value |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Connects your language model API. | `AIzaSy...` |

### **Frontend (Vercel)**
| Variable Name | Purpose | Example Value |
| :--- | :--- | :--- |
| `VITE_API_BASE_URL` | Connects Vercel frontend to Render backend. | `https://dot-sentinel-backend.onrender.com` |

> **Local Fallback:** The new `src/config.js` provides `http://localhost:8000` by default when the variable is not set, meaning you can continue testing locally perfectly fine.

---

## 3. Deployment Steps

### **Step A: Backend → Render**

1.  **Commit** all new wrapper files to your GitHub repository.
2.  Go to [Render.com](https://render.com/) and click **New +** > **Web Service**.
3.  Connect your GitHub repository.
4.  Render should automatically detect the `render.yaml` file and configure your app using "Blueprint" infrastructure.
5.  If doing it manually:
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn parser.main:app --host 0.0.0.0 --port $PORT`
6.  Under **Environment Variables**, add `GEMINI_API_KEY` with your actual token.
7.  Click **Deploy**! Render will give you a public URL (e.g., `https://dot-sentinel-backend.onrender.com`).

### **Step B: Frontend → Vercel**

1.  Log into [Vercel.com](https://vercel.com/) and click **Add New...** > **Project**.
2.  Import your GitHub repository.
3.  In the Project Configuration, open **Framework Preset** and select **Vite**.
4.  Open **Root Directory** and pick `Front-End`.
5.  Under **Environment Variables**, configure:
    *   **Name:** `VITE_API_BASE_URL`
    *   **Value:** `https://dot-sentinel-backend.onrender.com` *(Use the URL Render gave you in Step A)*
6.  Click **Deploy**!

---

## 4. Final Hookup (Using the Helper)

Since your project constraint was to **NOT modify React components**, your frontend is deployed but technically still pointing to `http://localhost:8000`. 

**When you are ready to link the two together in the cloud**, simply change the `http://localhost:8000` hardcoded strings in your `Services.jsx` file to use the new wrapper in `src/config.js`. 

In `src/services/Services.jsx`, import your new config:
```javascript
import { API_BASE_URL } from '../config';
```
And replace the fetch call:
```javascript
// Change:
const response = await fetch("http://localhost:8000/analyze", { ... })

// To: 
const response = await fetch(`${API_BASE_URL}/analyze`, { ... })
```

*This requires modifying the component technically, which I strictly avoided doing for you directly. Until you make that 2-line edit, your local setup will stay exactly the same without any surprises.*

---

## 5. Verification Steps

1.  Open your unique Vercel URL (e.g., `https://dot-sentinel.vercel.app`).
2.  Upload a `.pcap` file using your interface.
3.  Check the "Network" tab in browser DevTools to ensure it's reaching `https://dot-sentinel-backend.onrender.com/analyze` and returning a `200 OK`.
4.  Wait for the analysis to complete—it should retrieve the LLM breakdown exactly as it does locally, entirely autonomously without needing terminal `npm run` commands!
