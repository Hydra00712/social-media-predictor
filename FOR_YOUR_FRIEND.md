# 📊 QUICK START - POWER BI PACKAGE

**Hi! This is the data package for the Power BI dashboard.**

---

## 📦 **WHAT YOU'RE GETTING**

### **3 Data Files:**

1. **`database/social_media.db`** - SQLite database with live predictions
2. **`cleaned_data/social_media_cleaned.csv`** - 12,000 historical posts
3. **`powerbi_data/` folder** - Exported CSV files (after running script)

---

## 🚀 **QUICK START (3 STEPS)**

### **Step 1: Run Export Script**
```bash
python export_for_powerbi.py
```
This creates a `powerbi_data/` folder with CSV files ready for Power BI.

### **Step 2: Open Power BI Desktop**
- Click **Get Data** → **Text/CSV**
- Load: `powerbi_data/combined_data.csv`

### **Step 3: Start Building**
- Create visualizations
- Add slicers (Platform, Topic, Date)
- Make it look awesome!

---

## 📊 **DATA COLUMNS EXPLAINED**

| Column | What It Means | Example |
|--------|---------------|---------|
| `engagement_rate` | How many people engaged (0-1) | 0.45 = 45% |
| `platform` | Social media platform | Instagram, Twitter |
| `sentiment_score` | How positive the post is (-1 to 1) | 0.8 = very positive |
| `toxicity_score` | How toxic the post is (0-1) | 0.1 = low toxicity |
| `day_of_week` | Day posted | Monday, Tuesday |
| `topic_category` | What it's about | Technology, Fashion |
| `brand_name` | Brand mentioned | Apple, Nike |
| `campaign_phase` | Campaign stage | Pre-Launch, Launch |

---

## 💡 **DASHBOARD IDEAS**

### **Must-Have Charts:**
1. **Engagement by Platform** (Bar Chart)
2. **Engagement Over Time** (Line Chart)
3. **Sentiment vs Engagement** (Scatter Plot)
4. **Platform Distribution** (Pie Chart)
5. **Top Topics** (Bar Chart)

### **Cool Additions:**
- Map showing engagement by location
- Heatmap of Day vs Platform
- Gauge showing average engagement
- Cards with key metrics

---

## 🎨 **COLOR SCHEME**

Use these colors for consistency:
- 🟢 High Engagement (>50%): Green
- 🟡 Medium Engagement (30-50%): Yellow
- 🔴 Low Engagement (<30%): Red

---

## 📞 **NEED HELP?**

**Questions about the data?** Ask your friend (the ML guy)

**Questions about Power BI?** Google is your friend 😊

---

## ✅ **CHECKLIST**

- [ ] Received all files
- [ ] Ran `export_for_powerbi.py`
- [ ] Opened Power BI Desktop
- [ ] Loaded the data
- [ ] Created at least 5 visualizations
- [ ] Added slicers for filtering
- [ ] Made it look professional
- [ ] Ready to present!

---

**🎯 YOU GOT THIS! MAKE AN AWESOME DASHBOARD! 🎯**

**P.S.** Read `POWER_BI_PACKAGE_README.md` for detailed instructions.

