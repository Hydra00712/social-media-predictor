"""
Export database to CSV for Power BI
This script exports the predictions table from SQLite to CSV format
for easy import into Power BI
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime

def export_predictions_to_csv():
    """
    Export predictions from SQLite database to CSV for Power BI
    """
    try:
        # Connect to database
        db_path = 'database/social_media.db'
        
        if not os.path.exists(db_path):
            print(f"❌ Database not found at {db_path}")
            return
        
        conn = sqlite3.connect(db_path)
        
        # Read predictions table
        query = "SELECT * FROM predictions"
        df = pd.read_sql_query(query, conn)
        
        # Close connection
        conn.close()
        
        # Create output directory
        output_dir = 'powerbi_data'
        os.makedirs(output_dir, exist_ok=True)
        
        # Export to CSV
        output_file = f'{output_dir}/predictions_export.csv'
        df.to_csv(output_file, index=False)
        
        print(f"✅ Successfully exported {len(df)} predictions to {output_file}")
        print(f"\n📊 Data Summary:")
        print(f"   - Total Predictions: {len(df)}")
        print(f"   - Columns: {len(df.columns)}")
        print(f"   - Date Range: {df['created_at'].min()} to {df['created_at'].max()}")
        print(f"\n📁 File ready for Power BI: {output_file}")
        
        # Also create a summary statistics file
        summary_file = f'{output_dir}/predictions_summary.csv'
        summary = df.describe()
        summary.to_csv(summary_file)
        print(f"📊 Summary statistics saved to: {summary_file}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return None

def export_combined_dataset():
    """
    Combine historical data with predictions for comprehensive analysis
    """
    try:
        # Load historical data
        historical_df = pd.read_csv('cleaned_data/social_media_cleaned.csv')
        historical_df['data_source'] = 'historical'
        
        # Load predictions
        conn = sqlite3.connect('database/social_media.db')
        predictions_df = pd.read_sql_query("SELECT * FROM predictions", conn)
        conn.close()
        
        # Rename prediction_value to engagement_rate for consistency
        if 'prediction_value' in predictions_df.columns:
            predictions_df['engagement_rate'] = predictions_df['prediction_value']
            predictions_df.drop('prediction_value', axis=1, inplace=True)
        
        predictions_df['data_source'] = 'live_prediction'
        
        # Align columns (keep only common columns)
        common_columns = list(set(historical_df.columns) & set(predictions_df.columns))
        
        historical_subset = historical_df[common_columns]
        predictions_subset = predictions_df[common_columns]
        
        # Combine
        combined_df = pd.concat([historical_subset, predictions_subset], ignore_index=True)
        
        # Export
        output_dir = 'powerbi_data'
        os.makedirs(output_dir, exist_ok=True)
        output_file = f'{output_dir}/combined_data.csv'
        
        combined_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Combined dataset created!")
        print(f"   - Historical records: {len(historical_subset)}")
        print(f"   - Live predictions: {len(predictions_subset)}")
        print(f"   - Total records: {len(combined_df)}")
        print(f"   - File: {output_file}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error creating combined dataset: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("📊 POWER BI DATA EXPORT TOOL")
    print("=" * 60)
    print()
    
    # Export predictions
    print("1️⃣ Exporting predictions from database...")
    export_predictions_to_csv()
    
    print("\n" + "=" * 60)
    
    # Export combined dataset
    print("\n2️⃣ Creating combined dataset (historical + predictions)...")
    export_combined_dataset()
    
    print("\n" + "=" * 60)
    print("\n✅ ALL EXPORTS COMPLETE!")
    print("\n📦 Files ready for Power BI:")
    print("   1. powerbi_data/predictions_export.csv")
    print("   2. powerbi_data/combined_data.csv")
    print("   3. powerbi_data/predictions_summary.csv")
    print("\n🎯 Share the 'powerbi_data' folder with your friend!")
    print("=" * 60)

