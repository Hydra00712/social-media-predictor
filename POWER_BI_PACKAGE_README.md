# 📊 POWER BI INTEGRATION PACKAGE

**For:** Power BI Dashboard Development  
**Date:** December 18, 2025  
**Project:** Social Media Engagement Predictor

---

## 📦 **FILES TO USE FOR POWER BI**

### **1. PRIMARY DATA SOURCE (RECOMMENDED)** ⭐

**File:** `database/social_media.db`  
**Type:** SQLite Database  
**Size:** ~50 KB  
**Contains:**
- ✅ **predictions** table - All predictions made by users
- ✅ **alerts** table - System alerts and monitoring data
- ✅ **Real-time data** - Updates as users make predictions

**Columns in `predictions` table:**
- `id` - Unique prediction ID
- `prediction_value` - Predicted engagement rate (0.0 to 1.0)
- `day_of_week` - Day of the week
- `platform` - Social media platform
- `location` - Geographic location
- `language` - Content language
- `topic_category` - Content topic
- `sentiment_score` - Sentiment score (-1 to 1)
- `sentiment_label` - Positive/Negative/Neutral
- `emotion_type` - Joy/Sadness/Anger/Fear/Surprise/Neutral
- `toxicity_score` - Toxicity level (0 to 1)
- `brand_name` - Brand name
- `product_name` - Product name
- `campaign_name` - Campaign name
- `campaign_phase` - Pre-Launch/Launch/Post-Launch/Sustain
- `user_past_sentiment_avg` - User's past sentiment average
- `user_engagement_growth` - User engagement growth rate
- `buzz_change_rate` - Buzz change rate
- `created_at` - Timestamp of prediction

**Why use this:**
- ✅ Real-time data from live app
- ✅ Shows actual user predictions
- ✅ Demonstrates live integration
- ✅ Professional approach

---

### **2. TRAINING DATA (ALTERNATIVE)**

**File:** `cleaned_data/social_media_cleaned.csv`  
**Type:** CSV File  
**Size:** ~2 MB  
**Rows:** 12,000+ records  
**Contains:** Historical social media posts with actual engagement rates

**Columns:**
- All the same columns as predictions table PLUS:
- `timestamp` - When the post was made
- `text_content` - Actual post text
- `hashtags` - Hashtags used
- `mentions` - User mentions
- `keywords` - Extracted keywords
- `engagement_rate` - **ACTUAL engagement rate** (ground truth)

**Why use this:**
- ✅ Large dataset (12,000 rows)
- ✅ Rich historical data
- ✅ Good for trend analysis
- ✅ Shows model training data

---

### **3. ORIGINAL DATASET (BACKUP)**

**File:** `Social Media Engagement Dataset.csv`  
**Type:** CSV File  
**Size:** ~2.5 MB  
**Contains:** Raw, unprocessed data

**Use this if:** You want to show data cleaning process

---

## 🎯 **RECOMMENDED APPROACH**

### **Option 1: Use BOTH (BEST)** ⭐⭐⭐

**Combine:**
1. **Historical Data:** `cleaned_data/social_media_cleaned.csv`
2. **Live Predictions:** `database/social_media.db`

**Benefits:**
- ✅ Show historical trends
- ✅ Show live predictions
- ✅ Compare predicted vs actual
- ✅ Most impressive for presentation

---

## 📊 **POWER BI DASHBOARD IDEAS**

### **Page 1: Overview Dashboard**
- Total predictions made
- Average predicted engagement rate
- Predictions by platform
- Predictions by day of week
- Predictions over time (timeline)

### **Page 2: Platform Analysis**
- Engagement by platform (Instagram, Twitter, Facebook, etc.)
- Best performing platforms
- Platform comparison charts
- Platform trends over time

### **Page 3: Content Analysis**
- Engagement by topic category
- Sentiment vs Engagement correlation
- Toxicity impact on engagement
- Emotion type distribution

### **Page 4: Campaign Performance**
- Engagement by campaign phase
- Brand performance comparison
- Product performance
- Campaign effectiveness

### **Page 5: Geographic Analysis**
- Engagement by location
- Map visualization
- Language impact on engagement
- Regional trends

### **Page 6: Predictive Insights**
- Predicted vs Actual engagement (if using both datasets)
- Model accuracy visualization
- Prediction confidence levels
- Recommendations

---

## 🔧 **HOW TO CONNECT TO POWER BI**

### **For SQLite Database:**

1. **Open Power BI Desktop**
2. Click **Get Data** → **More**
3. Search for **"ODBC"** or **"Database"** → **"SQLite"**
4. Browse to: `database/social_media.db`
5. Select table: **predictions**
6. Click **Load**

**Alternative (if SQLite connector not available):**
1. Export database to CSV first
2. Use CSV connector

### **For CSV Files:**

1. **Open Power BI Desktop**
2. Click **Get Data** → **Text/CSV**
3. Browse to: `cleaned_data/social_media_cleaned.csv`
4. Click **Load**
5. Power BI will auto-detect columns

---

## 📈 **KEY METRICS TO VISUALIZE**

### **Primary KPIs:**
- Average Engagement Rate
- Total Predictions
- Most Popular Platform
- Best Performing Topic
- Sentiment Distribution

### **Trends:**
- Engagement over time
- Platform popularity trends
- Sentiment trends
- Campaign phase effectiveness

### **Comparisons:**
- Platform vs Engagement
- Sentiment vs Engagement
- Toxicity vs Engagement
- Day of Week vs Engagement

### **Correlations:**
- Sentiment Score vs Engagement Rate
- Toxicity Score vs Engagement Rate
- User Growth vs Engagement
- Buzz Rate vs Engagement

---

## 🎨 **VISUALIZATION SUGGESTIONS**

### **Charts to Use:**

1. **Line Chart:** Engagement trends over time
2. **Bar Chart:** Engagement by platform/topic
3. **Pie Chart:** Platform distribution
4. **Scatter Plot:** Sentiment vs Engagement correlation
5. **Map:** Geographic distribution
6. **Gauge:** Average engagement rate
7. **Card:** Total predictions, avg engagement
8. **Table:** Top performing posts/predictions
9. **Heatmap:** Day of week vs Platform performance
10. **Funnel:** Campaign phase progression

---

## 📁 **FILES TO SHARE**

### **Essential Files:**
```
📦 Power BI Package/
├── 📊 database/social_media.db          (Live predictions)
├── 📊 cleaned_data/social_media_cleaned.csv  (Historical data)
├── 📄 POWER_BI_PACKAGE_README.md        (This file)
└── 📄 models/experiment_results.json    (Model metrics)
```

### **Optional Files:**
```
├── 📊 Social Media Engagement Dataset.csv  (Original data)
├── 📓 Social_Media_ML_Notebook.ipynb      (Analysis notebook)
└── 📄 README.md                           (Project overview)
```

---

## 🔗 **INTEGRATION WITH STREAMLIT APP**

### **Live Data Connection:**

Your friend can set up **automatic refresh** in Power BI to pull latest predictions:

1. **Publish to Power BI Service**
2. **Set up Scheduled Refresh**
3. **Connect to SQLite database**
4. **Refresh every hour/day**

**Result:** Dashboard updates automatically as users make predictions!

---

## 💡 **TIPS FOR YOUR FRIEND**

### **Data Preparation:**
- ✅ Data is already cleaned (no missing values)
- ✅ Columns are properly named
- ✅ Data types are correct
- ✅ Ready to use immediately

### **Best Practices:**
- Use **slicers** for Platform, Topic, Date Range
- Add **drill-through** pages for detailed analysis
- Use **bookmarks** for different views
- Add **tooltips** for additional context
- Use **conditional formatting** for engagement levels

### **Color Scheme:**
- 🟢 High Engagement: Green (#4CAF50)
- 🟡 Medium Engagement: Yellow (#FFC107)
- 🔴 Low Engagement: Red (#F44336)
- 🔵 Neutral: Blue (#2196F3)

---

## 📞 **SUPPORT INFORMATION**

### **If Your Friend Has Questions:**

**About the Data:**
- 12,000+ social media posts
- 22 features/columns
- Engagement rate: 0% to 100%
- Time period: 2024 data

**About the Model:**
- Algorithm: HistGradientBoosting
- R² Score: -0.0410
- MAE: 0.3613
- RMSE: 1.1469

**About the App:**
- Live URL: https://social-media-engagement-predictor-hydra00712.streamlit.app/
- Database updates in real-time
- Predictions persist across sessions

---

## ✅ **CHECKLIST FOR YOUR FRIEND**

- [ ] Received `database/social_media.db`
- [ ] Received `cleaned_data/social_media_cleaned.csv`
- [ ] Received this README file
- [ ] Installed Power BI Desktop
- [ ] Connected to data source
- [ ] Created at least 3 visualizations
- [ ] Added slicers for filtering
- [ ] Tested dashboard functionality
- [ ] Ready for presentation

---

## 🎯 **DELIVERABLES EXPECTED**

Your friend should create:

1. **Power BI Dashboard (.pbix file)**
2. **PDF Export** of the dashboard
3. **Screenshots** of key visualizations
4. **Brief documentation** of insights found

---

**📊 EVERYTHING YOUR FRIEND NEEDS IS READY! 📊**

**Good luck with the Power BI dashboard!** 🚀

