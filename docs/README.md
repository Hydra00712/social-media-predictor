# Social Media Engagement Predictor

**Predict social media engagement with AI/ML on Azure** — built with Python, scikit-learn, Streamlit, and Azure cloud services (free tier).

### Core Features
- 🤖 **ML Model** — HistGradientBoosting classifier predicting engagement levels
- 📊 **Data Balancing** — SMOTE/ADASYN handling class imbalance
- 🔍 **Explainability** — Feature importance + prediction explanations (SHAP/LIME)
- 📈 **Monitoring** — Azure App Insights + Log Analytics + live dashboard
- 🎨 **UI** — Streamlit web app for predictions & analytics
- ☁️ **Cloud Ready** — Fully integrated with Azure Storage, monitoring, & Key Vault

---

## Quick Start

### 1. Install dependencies
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Azure connection (optional)
Create `.env` file:
```env
AZURE_STORAGE_CONNECTION_STRING=<your_storage_connection_string>
```
*Without this, the app uses local models in `models/`*

### 3. Run the app
```bash
streamlit run streamlit_app.py
```
Opens at `http://localhost:8501`

---

## Architecture

```
┌─────────────────┐
│  Streamlit App  │
│   (UI + Pred)   │
└────────┬────────┘
         │
    ┌────┴──────────┬──────────┬──────────┐
    │               │          │          │
┌───▼─────┐  ┌─────▼──┐  ┌──▼─────┐  ┌─▼──────┐
│  Model  │  │Monitor │  │ Azure  │  │ Data   │
│  Files  │  │ & Log  │  │Storage │  │Balance │
└────────┘  └────────┘  └────────┘  └────────┘
```

**Data Flow:**
1. User inputs → Streamlit form
2. Data balancing/validation
3. Model prediction (HistGradientBoosting)
4. Feature importance + explanations
5. Azure monitoring (App Insights, Log Analytics)
6. Results displayed in UI

---

## Project Structure

```
├── streamlit_app.py              # Main UI application
├── azure_monitoring.py           # Monitoring & logging
├── azure_config.py               # Azure configuration
├── model_explainability.py       # SHAP/LIME explanations
├── data_balancing.py             # SMOTE/ADASYN balancing
├── monitoring_dashboard.py       # Performance tracking
├── requirements.txt              # Python dependencies
├── .env                          # Azure credentials (ignored)
│
├── models/
│   ├── engagement_model.pkl      # Trained ML model
│   ├── feature_columns.pkl       # Feature list
│   ├── label_encoders.pkl        # Encoder mappings
│   └── experiment_results.json   # Model metrics
│
├── database/
│   └── social_media.db           # SQLite cache
│
├── cleaned_data/
│   └── social_media_cleaned.csv  # Training dataset
│
├── README.md                      # This file
├── PROJECT_SUMMARY.md            # Presentation guide
├── COMPLETION_CHECKLIST.md       # Feature checklist
└── PROJECT_ARCHITECTURE.md       # Technical details
```

---

## Azure Resources (Free Tier)

| Resource | Type | Status |
|----------|------|--------|
| Storage Account | `stsocialmediajkvqol` | ✅ Active |
| App Insights | `mlwsociainsightsf7431d22` | ✅ Active |
| Log Analytics | `mlwsocialogalytjea9b61fd` | ✅ Active |
| Storage Queue | `predictions-queue` | ✅ Active |
| Key Vault | `kv-social-ml-7487` | ✅ Configured |

**Cost:** 100% free tier — no charges for development/testing.

---

## Model Performance

Tested on 3 algorithms. **Best:** HistGradientBoosting
- **R² Score:** -0.041 (high variance in engagement)
- **MAE:** 0.36 engagement level
- **RMSE:** 1.15 engagement level

---

## Features

### 1. Data Balancing
- Detects class imbalance in dataset
- Applies SMOTE (synthetic oversampling) or ADASYN
- Ensures fair model training

### 2. Model Explainability
- Feature importance ranking
- Per-prediction explanations
- Rule-based engagement recommendations
- Shows which factors drive predictions

### 3. Monitoring & Alerts
- Live prediction stats (last 24h)
- Data quality checks
- System uptime tracking
- Automatic alerts on thresholds

### 4. Streamlit UI
- Real-time prediction form
- Engagement level output (0-5 scale)
- Feature importance visualization
- Model health dashboard

---

## How Grading Criteria Are Met

✅ **Data Ingestion & Storage**
  - CSV dataset in `cleaned_data/`
  - Azure Blob Storage containers
  - Storage Queue for async processing

✅ **Data Processing**
  - Cleaned & preprocessed dataset
  - Feature scaling & encoding

✅ **Streaming** (Optional)
  - Storage Queue implementation
  - Real-time prediction logging

✅ **Data Balancing**
  - SMOTE & ADASYN algorithms
  - Stratified train/test split

✅ **Model Training**
  - RandomForest, HistGradientBoosting, ExtraTrees tested
  - Hyperparameter tuning
  - Cross-validation

✅ **Experiment Tracking**
  - `experiment_results.json` with metrics
  - ML workspace integration

✅ **Deployment & Inference**
  - Streamlit web app
  - Local + cloud model loading

✅ **Monitoring & Alerts**
  - App Insights + Log Analytics
  - Custom alert thresholds
  - Health score tracking

✅ **Security**
  - Key Vault for credentials
  - Environment variables in `.env`
  - Secrets redaction in logs

✅ **Explainability**
  - Feature importance analysis
  - SHAP/LIME integration
  - Human-readable explanations

---

## Dependencies

Core:
- `scikit-learn` — ML algorithms
- `pandas` — Data processing
- `numpy` — Numerical computing
- `streamlit` — Web UI

Advanced:
- `shap` — Model explanations
- `lime` — Local interpretability
- `imbalanced-learn` — Data balancing
- `azure-*` — Azure SDK clients

See `requirements.txt` for full list.
- Avg Engagement by Platform (bar) — `platform` vs avg `engagement_rate`.
- Avg Engagement by Topic Category (treemap) — `topic_category` vs avg `engagement_rate`.
- Engagement Trend by Campaign Phase (line/area) — `campaign_phase` vs avg `engagement_rate`.
- Engagement Rate Distribution (histogram) — bins of `engagement_rate`.
- Details table — brand_name, product_name, topic_category, platform, sentiment_label, engagement_rate.
- Slicers — platform; topic_category or sentiment_label.

---

## Running with monitoring (still free)
- Set `AZURE_STORAGE_CONNECTION_STRING` (from Key Vault or portal). Leave Event Hub unset to avoid charges.
- `azure_monitoring.py` uses Application Insights + Storage Queue; no paid services required.
- If you need alerts, create them in App Insights/Log Analytics; free tier covers basic alerts.

---

## Minimal file map (current)
- streamlit_app.py — UI + inference; falls back to local models if Azure unavailable.
- predict_engagement.py — feature prep + prediction.
- azure_config.{py,json} — resource names; secrets are placeholders.
- azure_monitoring.py — telemetry to App Insights + Storage Queue.
- cleaned_data/social_media_cleaned.csv — dataset for Power BI.
- models/ — engagement_model.pkl, feature_columns.pkl, label_encoders.pkl, experiment_results.json.
- database/ — SQLite used by the app (created on first run).
- requirements.txt — dependencies.

---

## Cost notes
- Using only Storage + App Insights + Log Analytics free tiers is $0.
- Event Hub is the only notable cost; it is unused by default. If you keep it, disable its use in any deployment configs.

