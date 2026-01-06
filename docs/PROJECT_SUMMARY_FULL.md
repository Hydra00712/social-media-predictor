# Social Media Engagement Predictor – Professor-Ready Summary

## 1) Problem Statement & Goals
- Predict post engagement (regression) before publishing; surface explainability; provide UI + monitoring + exportable logs.
- Deliverables: Streamlit app, ML model + explainability, Azure-backed storage/queue/monitoring, MLflow tracking/registry, Power BI–ready exports.

## 2) Data
- Source: cleaned CSV [cleaned_data/social_media_cleaned.csv](cleaned_data/social_media_cleaned.csv) (local; used for training and sampling).
- Shape: ~12k rows (≈9.6k train / 2.4k test referenced by metrics), 16 features; target is engagement (continuous).
- Feature mix: categoricals (platform, topic_category, language, location, etc.) + numerics (sentiment_score [-1,1], toxicity_score [0,1], user_engagement_growth %, buzz_change_rate %, etc.).
- Labels/classes: regression only (no classes).

## 3) Models & Performance (Machine Learning)
- Tried: RandomForest, ExtraTrees, HistGradientBoosting.
- Best model: HistGradientBoosting.
- Metrics (test set) from [models/experiment_results.json](models/experiment_results.json#L1-L25): R² ≈ -0.0410, MAE ≈ 0.3613, RMSE ≈ 1.1469.
- Artifacts: model [models/engagement_model.pkl](models/engagement_model.pkl), feature list [models/feature_columns.pkl](models/feature_columns.pkl), encoders [models/label_encoders.pkl](models/label_encoders.pkl), metrics JSON [models/experiment_results.json](models/experiment_results.json#L1-L25).

## 4) Explainability
- SHAP/LIME hooks via [model_explainability.py](model_explainability.py) (loaded in Streamlit).
- In-app: feature importance and per-prediction explanations displayed alongside predictions.

## 5) Application (UI) & Flow
- Main app: [streamlit_app.py](streamlit_app.py).
- Flow: user inputs → encode categoricals with saved encoders → predict with HistGradientBoosting → display score + explainability → log prediction.
- Persistence: predictions saved to SQLite [database/social_media.db](database/social_media.db) for counts/history.
- Model loading: prefers Azure Blob (`models` container) if connection string available; else local [models/](models).

## 6) Pipeline (End-to-End)
1. Data prepared in cleaned CSV.
2. Model artifacts saved to [models/](models).
3. MLflow used for tracking/registry (local server at 127.0.0.1:5000).
4. Streamlit app serves predictions and logs events.
5. Events optionally emitted to Azure Queue + App Insights.
6. Exports: Power BI CSV via generator script.

## 7) Services & Roles (Azure)
- Azure Blob Storage: stores model artifacts for remote app use.
- Azure Storage Queue: receives prediction events (streaming/Power BI ingestion).
- Application Insights + Log Analytics: telemetry/monitoring.
- Azure Key Vault (optional): secure secret retrieval.
- Azure ML workspace (optional): managed runs/registration (see [AZURE_ML_WORKSPACE.ipynb](AZURE_ML_WORKSPACE.ipynb)).

## 8) Deployment
- Local: `streamlit run streamlit_app.py`.
- Container: Dockerfile present for containerization.
- Cloud: Streamlit Cloud or container platforms; model pulled from Blob when connection string is set.

## 9) Experiment Tracking (MLflow)
- Start UI/server: `mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5000`.
- Point runs: set `MLFLOW_TRACKING_URI=http://127.0.0.1:5000` (PowerShell: `$Env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"`).
- Registry: model `social-media-engagement-model` (versions 1 and 2 logged with signature/input_example in run `register-local-model-v2`).

## 10) Generated Data for Power BI
- File: [predictions_powerbi.csv](predictions_powerbi.csv) (100 synthetic predictions with id, prediction value, timestamp, platform, topic_category, language, location).
- Created by: [generate_predictions.py](generate_predictions.py) (also streams queue events if Azure connection string set).

## 11) Monitoring & Logging
- AzureMonitoring in [azure_monitoring.py](azure_monitoring.py): sends prediction events to Storage Queue and Application Insights; uses `AZURE_STORAGE_CONNECTION_STRING` and queue `predictions-queue` from [azure_config.py](azure_config.py).
- Local DB logging via Streamlit app to SQLite for counts.

## 12) Configuration & Secrets
- Env file `.env` for storage connection string (and other secrets); ignored by git.
- Azure names in [azure_config.py](azure_config.py) (subscription, RG, workspace, storage account, queue, App Insights, Log Analytics, Key Vault).

## 13) Demonstration Steps (show each requirement works)
1. **MLflow UI**: start server (command above) → open http://127.0.0.1:5000 → verify experiment `social-media-engagement` and model `social-media-engagement-model` versions.
2. **Streamlit prediction**: `streamlit run streamlit_app.py` → fill form → see prediction + explainability → check SQLite count increases.
3. **Model load from Blob**: set `AZURE_STORAGE_CONNECTION_STRING` → restart app → verify load message shows Azure source (fallback to local otherwise).
4. **Queue/Monitoring**: ensure `AZURE_STORAGE_CONNECTION_STRING` set → make predictions or run `python generate_predictions.py` → confirm log lines “Prediction logged to queue/App Insights” and view queue messages in Azure portal.
5. **Power BI export**: open/import [predictions_powerbi.csv](predictions_powerbi.csv) into Power BI and build visuals (platform/topic vs prediction).
6. **Explainability**: in app, view feature importance/explanation output for a prediction (driven by `model_explainability.py`).
7. **Code artifacts**: inspect model files in [models/](models) and metrics JSON; confirm versions in MLflow registry.

## 14) Tech Stack (concise)
- Python, pandas, scikit-learn, imbalanced-learn, SHAP, LIME.
- Streamlit UI.
- MLflow for tracking/registry.
- Azure: Blob Storage, Storage Queue, Application Insights, Log Analytics, Key Vault (optional), Azure ML workspace (optional).
- SQLite for local persistence.

## 15) Files to Cite in Answers
- App: [streamlit_app.py](streamlit_app.py)
- Model artifacts: [models/](models)
- Metrics: [models/experiment_results.json](models/experiment_results.json#L1-L25)
- Explainability: [model_explainability.py](model_explainability.py)
- Monitoring: [azure_monitoring.py](azure_monitoring.py)
- Azure config: [azure_config.py](azure_config.py)
- ML workspace notebook: [AZURE_ML_WORKSPACE.ipynb](AZURE_ML_WORKSPACE.ipynb)
- Power BI data: [predictions_powerbi.csv](predictions_powerbi.csv)
- Generator: [generate_predictions.py](generate_predictions.py)

## 16) Quick FAQ (for professor)
- **What is predicted?** Engagement score (regression) for a post given metadata + sentiment/toxicity.
- **Best model?** HistGradientBoosting; see metrics above.
- **How is explainability done?** SHAP/LIME hooks, surfaced in Streamlit.
- **How is it monitored?** Azure Queue + App Insights + Log Analytics via `AzureMonitoring`.
- **How to reproduce runs?** Start MLflow UI, set tracking URI, run training/registration; artifacts and metrics logged/registered.
- **How to demo quickly?** Steps in section 13; open MLflow UI, run Streamlit, show queue/App Insights logs, load Power BI CSV.
