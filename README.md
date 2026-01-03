# Social Media Engagement Predictor (cost-safe)

End-to-end ML pipeline for predicting social media engagement, using Azure storage + monitoring and a Streamlit UI. This repo is trimmed to essentials and avoids paid Azure services by default.

---

## Quick start (local, cost-safe)
1) Python env
```bash
pip install -r requirements.txt
```
2) Secrets (storage only; keep Event Hub unset to avoid cost)
Create `.env` at repo root:
```
AZURE_STORAGE_CONNECTION_STRING=<your_storage_connection_string>
# leave Event Hub unset/unused
```
3) Run Streamlit
```bash
streamlit run streamlit_app.py
```
The app will load model artifacts from the `models` container in `stsocialmediajkvqol` when the storage connection string is set; otherwise it falls back to local models/.

---

## Azure resources in place (free tiers)
- Resource group: rg-social-media-ml (francecentral)
- Storage: stsocialmediajkvqol with containers (models, data, logs, experiments, notebooks), queue `predictions-queue`, tables `socialmediaposts`, `interactions`.
- Monitoring: Application Insights `mlwsociainsightsf7431d22`, Log Analytics `mlwsocialogalytiea9b60fd` (5 GB/mo free).
- ML workspace: `mlw-social-media` (free tier).
- Key Vault: kv-social-ml-7487.
- Event Hub exists but is **not used** to avoid cost; prefer Storage Queue.

---

## How the grading criteria are met
- Data ingestion/storage: cleaned CSV in Blob; Storage Queue available; Table Storage tables exist.
- Processing: batch-prepared dataset; online scoring via Streamlit app.
- Streaming: use Storage Queue (free) instead of Event Hub.
- Data balancing: handled at training time (note SMOTE/oversampling if instructor asks).
- Model training: artifacts in `models/` and experiment_results.json.
- Experiment tracking: experiment_results.json (lightweight); ML workspace exists.
- Deployment/inference/UI: Streamlit app (`streamlit_app.py`).
- Monitoring/alerts: App Insights + Log Analytics present; add alert rules if required (free).
- Security: Key Vault exists; store secrets there or in local .env.
- Dashboard: Power BI to be delivered from `cleaned_data/social_media_cleaned.csv` with visuals below.
- CI/CD: manual for now; add a minimal GitHub Action if needed (optional).

Power BI visuals to include (.pbix):
- Sentiment Breakdown (donut) — by `sentiment_label`, values = avg `engagement_rate` (%).
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

