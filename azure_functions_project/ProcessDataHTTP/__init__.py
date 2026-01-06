"""
Azure Function: Process data with SMOTE/ADASYN balancing
HTTP triggered - POST /api/ProcessDataHTTP
"""

import azure.functions as func
import json
import pandas as pd
import numpy as np
from io import BytesIO
from azure.storage.blob import BlobServiceClient
import os
import logging

logger = logging.getLogger("ProcessDataHTTP")

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP triggered function to process and balance data
    Loads CSV from Blob Storage, applies SMOTE/ADASYN, saves result
    """
    try:
        logger.info("📨 Processing data request received")
        
        # Load connection string from environment
        connection_string = os.environ.get("AzureWebJobsStorage")
        if not connection_string:
            return func.HttpResponse(
                json.dumps({"error": "Storage connection string not configured"}),
                status_code=500
            )
        
        # Load CSV from blob
        logger.info("📥 Loading data from Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client("data")
        blob_client = container_client.get_blob_client("social_media_cleaned.csv")
        
        download_stream = blob_client.download_blob()
        df = pd.read_csv(BytesIO(download_stream.readall()))
        logger.info(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Apply data balancing
        logger.info("🔄 Applying SMOTE/ADASYN balancing...")
        balanced_df = apply_smote_adasyn(df)
        logger.info(f"✅ Balanced to {len(balanced_df)} rows")
        
        # Save balanced data to blob
        logger.info("💾 Saving balanced data...")
        csv_buffer = BytesIO()
        balanced_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        blob_client_out = container_client.get_blob_client("social_media_balanced.csv")
        blob_client_out.upload_blob(csv_buffer.getvalue(), overwrite=True)
        logger.info("✅ Saved to social_media_balanced.csv")
        
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "message": "Data processing completed",
                "original_rows": int(len(df)),
                "balanced_rows": int(len(balanced_df)),
                "output_file": "data/social_media_balanced.csv"
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

def apply_smote_adasyn(df: pd.DataFrame) -> pd.DataFrame:
    """Apply SMOTE and ADASYN balancing"""
    try:
        from imblearn.over_sampling import SMOTE, ADASYN
        from imblearn.pipeline import Pipeline as ImbPipeline
        
        # Assume last column is target
        target_col = df.columns[-1]
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Create pipeline
        balancer = ImbPipeline([
            ('smote', SMOTE(random_state=42, k_neighbors=3)),
            ('adasyn', ADASYN(random_state=42, n_neighbors=3))
        ])
        
        # Apply balancing
        X_balanced, y_balanced = balancer.fit_resample(X, y)
        
        # Recombine
        result = pd.concat([
            pd.DataFrame(X_balanced, columns=X.columns),
            pd.Series(y_balanced, name=target_col, index=X_balanced.index)
        ], axis=1)
        
        logger.info(f"✅ SMOTE/ADASYN: {len(y)} → {len(y_balanced)} samples")
        return result
        
    except ImportError:
        logger.warning("⚠️ SMOTE/ADASYN not available, returning original data")
        return df
    except Exception as e:
        logger.warning(f"⚠️ Balancing failed: {e}, returning original data")
        return df
