# 🚀 DEPLOY STREAMLIT APP TO CLOUD (Connected to Azure)

## 🎯 **HOW IT WORKS**

```
┌─────────────────────────────────────────────────────────┐
│         USER (Your Professor or Anyone)                  │
│                                                          │
│  Opens: https://your-app.streamlit.app                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              STREAMLIT CLOUD (FREE)                      │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  streamlit_app.py                              │    │
│  │                                                 │    │
│  │  1. User fills form                            │    │
│  │  2. App connects to Azure Blob Storage ────────┼────┼──┐
│  │  3. Downloads models from Azure                │    │  │
│  │  4. Makes prediction                           │    │  │
│  │  5. Shows result                               │    │  │
│  └────────────────────────────────────────────────┘    │  │
│                                                          │  │
│  Hosted on: Streamlit Cloud (FREE)                     │  │
└─────────────────────────────────────────────────────────┘  │
                                                              │
                    INTERNET (HTTPS)                          │
                                                              │
                                                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    MICROSOFT AZURE                            │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Azure Blob Storage                                │     │
│  │  Account: stsocialmediajkvqol                      │     │
│  │                                                     │     │
│  │  📦 models/                                        │     │
│  │     ├── engagement_model.pkl      ◄────────────────┼─────┘
│  │     ├── feature_columns.pkl                        │
│  │     ├── label_encoders.pkl                         │
│  │     └── experiment_results.json                    │
│  │                                                     │
│  │  📦 data/                                          │
│  │     └── social_media_cleaned.csv                   │
│  └────────────────────────────────────────────────────┘
│                                                               │
│  ✅ ALL YOUR DATA AND MODELS ARE IN AZURE                   │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔑 **THE CONNECTION: How Streamlit Cloud Talks to Azure**

### **Step 1: Azure Connection String**

Your app uses a **connection string** (like a password) to access Azure Blob Storage.

**Where it's stored:**
- In Streamlit Cloud: As a **secret** (encrypted, secure)
- Locally: In environment variable or `.streamlit/secrets.toml`

**What it looks like:**
```
DefaultEndpointsProtocol=https;
AccountName=stsocialmediajkvqol;
AccountKey=YOUR_SECRET_KEY;
EndpointSuffix=core.windows.net
```

---

### **Step 2: App Loads Models from Azure**

When someone visits your Streamlit app:

1. **User opens:** `https://your-app.streamlit.app`
2. **App connects to Azure** using connection string
3. **Downloads models** from Azure Blob Storage
4. **Caches models** in memory (fast!)
5. **Makes predictions** using Azure models
6. **Shows results** to user

---

## 📋 **DEPLOYMENT STEPS**

### **STEP 1: Get Azure Connection String**

**Option A: From Azure Portal (EASIEST)**

1. Go to: https://portal.azure.com
2. Search for: `stsocialmediajkvqol`
3. Click on your storage account
4. In the left menu, click **"Access keys"**
5. Click **"Show"** next to **key1**
6. Click **"Copy"** next to **"Connection string"**

**It will look like this:**
```
DefaultEndpointsProtocol=https;AccountName=stsocialmediajkvqol;AccountKey=XXXXX...;EndpointSuffix=core.windows.net
```

⚠️ **IMPORTANT:** This is like a password! Keep it secret!

---

### **STEP 2: Create GitHub Repository**

1. Go to: https://github.com
2. Click **"New repository"**
3. Name it: `social-media-predictor`
4. Make it **Public**
5. Click **"Create repository"**

---

### **STEP 3: Push Code to GitHub**

Open terminal in your project folder and run:

```bash
git init
git add streamlit_app.py requirements.txt
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/social-media-predictor.git
git push -u origin main
```

**Files to push:**
- ✅ `streamlit_app.py` (your app)
- ✅ `requirements.txt` (dependencies)
- ❌ `models/` folder (NO! Models are in Azure)
- ❌ `.streamlit/secrets.toml` (NO! Contains secrets)

---

### **STEP 4: Deploy to Streamlit Cloud**

1. Go to: https://share.streamlit.io
2. Click **"New app"**
3. Connect your GitHub account
4. Select:
   - **Repository:** `social-media-predictor`
   - **Branch:** `main`
   - **Main file:** `streamlit_app.py`
5. Click **"Advanced settings"**
6. In **"Secrets"**, paste:

```toml
AZURE_STORAGE_CONNECTION_STRING = "YOUR_CONNECTION_STRING_FROM_STEP_1"
```

7. Click **"Deploy"**
8. Wait 2-3 minutes ⏳

---

### **STEP 5: Test Your App**

1. Streamlit Cloud will give you a URL like:
   `https://YOUR_USERNAME-social-media-predictor.streamlit.app`

2. Open the URL
3. You should see: **"✅ Model loaded from Azure Blob Storage!"**
4. Fill in the form
5. Click **"Predict Engagement"**
6. See the result!

---

## ✅ **WHAT YOU'VE ACHIEVED**

```
┌──────────────────────────────────────────────────┐
│  PUBLIC URL (Anyone can access)                   │
│  https://your-app.streamlit.app                  │
└────────────────┬─────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│  STREAMLIT CLOUD (FREE)                          │
│  - Hosts your app                                │
│  - Runs streamlit_app.py                         │
│  - Connects to Azure using secrets              │
└────────────────┬─────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│  MICROSOFT AZURE                                 │
│  - Stores models (engagement_model.pkl)          │
│  - Stores data (social_media_cleaned.csv)        │
│  - Azure Blob Storage: stsocialmediajkvqol       │
└──────────────────────────────────────────────────┘
```

**YOU NOW HAVE:**
- ✅ Public URL anyone can access
- ✅ App hosted on Streamlit Cloud (FREE)
- ✅ Models stored in Azure Blob Storage
- ✅ Data stored in Azure
- ✅ Complete cloud deployment!

---

## 🎓 **FOR YOUR PROFESSOR**

**What to say:**

> "I deployed my Streamlit application to Streamlit Cloud, which connects to Microsoft Azure Blob Storage to load the trained models. All data and models are stored in Azure, and the application is accessible via a public URL. This demonstrates a complete cloud-based ML deployment using Azure services."

**What to show:**

1. **Public URL:** Show the live app
2. **Azure Portal:** Show storage account with models
3. **GitHub:** Show code repository
4. **Streamlit Cloud:** Show deployment dashboard

---

## 💰 **COST**

- **Streamlit Cloud:** FREE ✅
- **Azure Blob Storage:** ~$0.50/month ✅
- **Total:** Almost FREE ✅

---

## 🎯 **ADVANTAGES OF THIS APPROACH**

1. ✅ **100% Cloud-based:** Everything in the cloud
2. ✅ **Azure Integration:** Uses Azure Blob Storage
3. ✅ **Public URL:** Anyone can access
4. ✅ **FREE:** No additional costs
5. ✅ **Professional:** Industry-standard deployment
6. ✅ **Scalable:** Can handle many users
7. ✅ **Secure:** Secrets encrypted in Streamlit Cloud

---

## 📋 **QUICK CHECKLIST**

- [ ] Get Azure connection string from portal
- [ ] Create GitHub repository
- [ ] Push code to GitHub (streamlit_app.py + requirements.txt)
- [ ] Sign up for Streamlit Cloud
- [ ] Deploy app with Azure connection string in secrets
- [ ] Test the public URL
- [ ] Show to professor!

---

## 🚀 **READY TO START?**

**Tell me when you're ready and I'll guide you through each step!**

Or if you prefer, I can create a simpler local demo for your oral exam.

