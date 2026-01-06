"""
Generate ~100 synthetic predictions and optionally push them to Azure Storage Queue
for Power BI ingestion. Outputs a local CSV: predictions_powerbi.csv

Behavior:
- Loads local model artifacts from models/
- Samples up to 100 rows from cleaned_data/social_media_cleaned.csv
- Encodes using saved label_encoders, predicts, writes CSV
- If Azure Monitoring is configured (connection string + queue), also logs each
  prediction via AzureMonitoring.log_prediction (App Insights + Queue)

Usage:
    $env:AZURE_STORAGE_CONNECTION_STRING="<conn>"  # optional, for queue
    python generate_predictions.py

The CSV is safe to import directly into Power BI.
"""
import os
import json
import uuid
from datetime import datetime
import pandas as pd
import joblib

# Optional Azure monitoring import
try:
    from azure_monitoring import AzureMonitoring
    MONITORING_AVAILABLE = True
except Exception:
    AzureMonitoring = None  # type: ignore
    MONITORING_AVAILABLE = False

PREDICTION_COUNT = 100
DATA_PATH = "cleaned_data/social_media_cleaned.csv"
OUTPUT_CSV = "predictions_powerbi.csv"


def load_artifacts():
    model = joblib.load("models/engagement_model.pkl")
    feature_columns = joblib.load("models/feature_columns.pkl")
    label_encoders = joblib.load("models/label_encoders.pkl")
    with open("models/experiment_results.json", "r", encoding="utf-8") as f:
        exp = json.load(f)
    return model, feature_columns, label_encoders, exp


def prepare_sample(df, label_encoders, feature_columns):
    sample_df = df.sample(min(PREDICTION_COUNT, len(df)), random_state=42).copy()
    # Encode categoricals with saved encoders
    for col, encoder in label_encoders.items():
        if col in sample_df.columns:
            try:
                sample_df[col] = encoder.transform(sample_df[col].astype(str))
            except Exception:
                fallback = encoder.classes_[0]
                sample_df[col] = (
                    sample_df[col]
                    .astype(str)
                    .where(sample_df[col].astype(str).isin(encoder.classes_), fallback)
                )
                sample_df[col] = encoder.transform(sample_df[col])
    return sample_df[feature_columns]


def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    model, feature_columns, label_encoders, _ = load_artifacts()

    X = prepare_sample(df, label_encoders, feature_columns)
    preds = model.predict(X)

    records = []
    now_iso = datetime.utcnow().isoformat()
    for idx, (pred, raw_row) in enumerate(zip(preds, df.sample(len(X), random_state=42).to_dict(orient="records"))):
        record = {
            "prediction_id": str(uuid.uuid4()),
            "prediction": float(pred),
            "prediction_time": now_iso,
            "platform": raw_row.get("platform"),
            "topic_category": raw_row.get("topic_category"),
            "language": raw_row.get("language"),
            "location": raw_row.get("location"),
        }
        records.append(record)

    # Write CSV for Power BI
    out_df = pd.DataFrame(records)
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Wrote {len(out_df)} predictions to {OUTPUT_CSV}")

    # Optional: push to Azure Queue via AzureMonitoring
    if MONITORING_AVAILABLE and AzureMonitoring:
        try:
            monitor = AzureMonitoring()
            sent = 0
            for rec in records:
                ok = monitor.log_prediction(
                    input_data={"platform": rec["platform"], "topic_category": rec["topic_category"], "language": rec["language"], "location": rec["location"]},
                    prediction=rec["prediction"],
                    confidence=None,
                )
                if ok:
                    sent += 1
            print(f"📡 Sent {sent} prediction events to queue/App Insights (if configured)")
        except Exception as e:
            print(f"⚠️ Queue/App Insights not sent: {e}")
    else:
        print("ℹ️ Azure monitoring not configured; skipped queue send. Set AZURE_STORAGE_CONNECTION_STRING to enable.")


if __name__ == "__main__":
    main()
