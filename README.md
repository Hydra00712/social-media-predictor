# 📱 Social Media Engagement Predictor

A comprehensive machine learning project for predicting social media engagement rates using Azure Blob Storage, MLflow, and Streamlit.

[![Status](https://img.shields.io/badge/Status-Live-success)]()
[![Python](https://img.shields.io/badge/Python-3.12-blue)]()
[![ML](https://img.shields.io/badge/ML-HistGradientBoosting-orange)]()
[![Cloud](https://img.shields.io/badge/Cloud-Azure-blue)]()
[![UI](https://img.shields.io/badge/UI-Streamlit-red)]()

---

## 🌐 Live Demo

**Access the app:** https://social-media-engagement-predictor-hydra00712.streamlit.app/

---

## 🎯 Project Overview

This project implements an **end-to-end machine learning solution** that:
- ✅ Predicts engagement rates for social media posts
- ✅ Tracks experiments using MLflow
- ✅ Deploys models to Azure Blob Storage
- ✅ Provides a user-friendly Streamlit interface
- ✅ **NEW: Azure Monitoring (100% FREE!)**
  - 📊 Application Insights for performance tracking
  - 📊 Log Analytics for centralized logging
  - 📡 Storage Queue for real-time streaming
- ✅ Integrates with SQLite database

**Objective**: Predict social media post engagement BEFORE posting to optimize content strategy.

**💰 Cost**: $0.00 - All Azure resources use FREE tier!

---

## 📊 Model Performance

**Best Model:** HistGradientBoostingRegressor

| Metric | Value |
|--------|-------|
| R² Score | -0.0410 |
| MAE | 0.3613 |
| RMSE | 1.1469 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Azure account (for cloud features)
- Git

### Local Installation

1. **Clone the repository:**
```bash
git clone https://github.com/hydra00712/social-media-predictor.git
cd CL
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Test Azure setup (optional):**
```bash
py test_azure_setup.py
```

4. **Run the Streamlit app locally:**
```bash
streamlit run streamlit_app.py
```

**📖 See [QUICK_START.md](QUICK_START.md) for detailed instructions**

---

## 📁 Project Structure

```
CL/
├── streamlit_app.py                      # Main Streamlit application
├── predict_engagement.py                 # Prediction logic and model loading
├── azure_config.py                       # Azure Blob Storage configuration
├── azure_config.json                     # 🆕 Azure credentials & config
├── azure_monitoring.py                   # 🆕 Azure monitoring class
├── test_azure_setup.py                   # 🆕 Test Azure resources
├── requirements.txt                      # Python dependencies
├── Social Media Engagement Dataset.csv   # Original dataset
├── Social_Media_ML_Notebook.ipynb       # Jupyter notebook for analysis
├── cleaned_data/
│   └── social_media_cleaned.csv         # Processed dataset
├── models/
│   ├── engagement_model.pkl             # Trained model
│   ├── label_encoders.pkl               # Encoders for categorical features
│   ├── feature_columns.pkl              # Feature column names
│   └── experiment_results.json          # Model comparison results
├── database/
│   ├── db_setup.py                      # Database initialization
│   └── social_media.db                  # SQLite database
├── mlflow_tracking/
│   └── track_experiments.py             # MLflow experiment tracking
├── monitoring/
│   └── dashboard.py                     # Monitoring dashboard
└── docs/
    ├── AZURE_SETUP_COMPLETE.md          # 🆕 Complete Azure setup guide
    ├── QUICK_START.md                   # 🆕 Quick start guide
    └── CHANGES_SUMMARY.md               # 🆕 What was changed
```

---

## ✨ Features

### 🔹 Data Processing
- Automated data cleaning and validation
- Feature engineering (sentiment, toxicity, engagement metrics)
- Label encoding for categorical variables
- Data normalization and scaling

### 🔹 Model Training
- Multiple algorithms tested:
  - Random Forest
  - Gradient Boosting
  - **HistGradientBoostingRegressor** (Best Model)
  - Extra Trees
- Hyperparameter tuning
- Cross-validation
- Model comparison and selection

### 🔹 Cloud Deployment
- **Azure Blob Storage** for model storage
- **Streamlit Cloud** for web hosting
- Secure connection string management
- Automated model loading from cloud

### 🔹 Monitoring & Analytics (🆕 100% FREE!)
- **Application Insights** - Performance tracking & telemetry
- **Log Analytics** - Centralized logging & queries
- **Storage Queue** - Real-time prediction streaming
- Session uptime monitoring
- Model status indicators
- Prediction counter
- Queue statistics display

### 🔹 User Interface
- Interactive Streamlit web app
- 16 input features for predictions
- Real-time engagement rate predictions
- Model information sidebar
- Monitoring dashboard

---

## 🎓 Academic Requirements Fulfilled

| # | Requirement | Status | Implementation |
|---|-------------|--------|----------------|
| 1 | Data Preprocessing | ✅ | `cleaned_data/` + feature engineering |
| 2 | Multiple ML Algorithms | ✅ | 3+ algorithms tested |
| 3 | Model Evaluation | ✅ | R², MAE, RMSE metrics |
| 4 | Cloud Deployment | ✅ | Azure Blob + Streamlit Cloud |
| 5 | Database Integration | ✅ | SQLite database |
| 6 | Web Interface | ✅ | Streamlit app |
| 7 | Experiment Tracking | ✅ | MLflow + experiment_results.json |
| 8 | Monitoring | ✅ | **Azure Monitoring (App Insights + Log Analytics + Queue)** |
| 9 | Security | ✅ | Azure secure connections |
| 10 | Real-time Streaming | ✅ | **Storage Queue (FREE!)** |

---

## 🎯 How to Use the Live App

1. **Access:** https://social-media-engagement-predictor-hydra00712.streamlit.app/
2. **Fill in post details:**
   - Day of Week
   - Platform (Instagram, Twitter, Facebook, etc.)
   - Location, Language, Topic
   - Sentiment & Toxicity scores
   - Brand, Product, Campaign info
   - User engagement metrics
3. **Click "🎯 Predict Engagement"**
4. **View prediction results**
5. **Check monitoring metrics** in sidebar

---

## 🔧 Technology Stack

- **Language**: Python 3.12
- **ML Framework**: scikit-learn
- **Cloud**: Azure Blob Storage
- **UI**: Streamlit
- **Visualization**: Plotly
- **Database**: SQLite
- **Experiment Tracking**: MLflow
- **Data Processing**: Pandas, NumPy, Joblib

---

## 🔐 Configuration

### Azure Setup
The app connects to Azure Blob Storage to load models. Configuration is in `azure_config.py`:

```python
AZURE_STORAGE_CONNECTION_STRING = "your-connection-string"
AZURE_CONTAINER_NAME = "models"
```

### Streamlit Secrets
For deployment, add to `.streamlit/secrets.toml`:
```toml
AZURE_STORAGE_CONNECTION_STRING = "your-connection-string"
```

---

## 📝 Key Files

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Main application with UI and prediction logic |
| `predict_engagement.py` | Model loading and prediction functions |
| `azure_config.py` | Azure Blob Storage configuration |
| `azure_config.json` | 🆕 Azure credentials & resource names |
| `azure_monitoring.py` | 🆕 Azure monitoring integration |
| `test_azure_setup.py` | 🆕 Test Azure resources |
| `requirements.txt` | All Python dependencies |
| `models/engagement_model.pkl` | Trained ML model |
| `models/experiment_results.json` | Model comparison results |
| `database/social_media.db` | SQLite database |
| `mlflow_tracking/track_experiments.py` | Experiment tracking |

### 📚 Documentation

| File | Purpose |
|------|---------|
| `AZURE_SETUP_COMPLETE.md` | Complete Azure setup guide |
| `QUICK_START.md` | Quick start guide (3 steps) |
| `CHANGES_SUMMARY.md` | What was changed for monitoring |

---

## ✅ Status

**🟢 LIVE AND WORKING**

- ✅ App deployed to Streamlit Cloud
- ✅ Models stored in Azure Blob Storage
- ✅ **Azure Monitoring active (100% FREE!)**
  - ✅ Application Insights
  - ✅ Log Analytics
  - ✅ Storage Queue
- ✅ All requirements implemented
- ✅ Ready for demonstration

**💰 Total Cost: $0.00 - All FREE resources!**

---

## 🙏 Acknowledgments

- **Azure** for cloud infrastructure
- **Streamlit** for web framework
- **MLflow** for experiment tracking
- **Scikit-learn** for ML algorithms

---

**🎉 Social Media Engagement Predictor - Live and Ready! 🎉**

