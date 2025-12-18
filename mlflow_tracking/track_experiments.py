"""
MLFLOW EXPERIMENT TRACKING
==========================
Track model training experiments and compare performance
"""

import mlflow
import mlflow.sklearn
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set MLflow tracking URI
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("social_media_engagement_prediction")

def load_and_prepare_data():
    """Load and prepare data for training"""
    print("📥 Loading data...")
    df = pd.read_csv('cleaned_data/social_media_cleaned.csv')
    
    # Feature engineering (simplified version)
    from clean_dataset import SocialMediaCleaner
    cleaner = SocialMediaCleaner()
    df = cleaner.engineer_features(df)
    
    # Prepare features
    X = df.drop(['engagement_rate'], axis=1)
    y = df['engagement_rate']
    
    # Log transform target
    y = np.log1p(y)
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_and_log_model(model_name, model, X_train, X_test, y_train, y_test):
    """Train model and log to MLflow"""
    
    with mlflow.start_run(run_name=model_name):
        print(f"\n🔄 Training {model_name}...")
        
        # Log parameters
        mlflow.log_param("model_type", model_name)
        mlflow.log_param("n_samples_train", len(X_train))
        mlflow.log_param("n_samples_test", len(X_test))
        mlflow.log_param("n_features", X_train.shape[1])
        
        # Log model-specific parameters
        if hasattr(model, 'get_params'):
            for param, value in model.get_params().items():
                mlflow.log_param(f"model_{param}", value)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        import time
        start_time = time.time()
        model.fit(X_train_scaled, y_train)
        training_time = time.time() - start_time
        
        # Make predictions
        y_train_pred = model.predict(X_train_scaled)
        y_test_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        train_mae = mean_absolute_error(y_train, y_train_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        
        # Log metrics
        mlflow.log_metric("train_mae", train_mae)
        mlflow.log_metric("test_mae", test_mae)
        mlflow.log_metric("train_rmse", train_rmse)
        mlflow.log_metric("test_rmse", test_rmse)
        mlflow.log_metric("train_r2", train_r2)
        mlflow.log_metric("test_r2", test_r2)
        mlflow.log_metric("training_time_seconds", training_time)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        # Print results
        print(f"✅ {model_name} trained")
        print(f"   Test MAE: {test_mae:.4f}")
        print(f"   Test R²: {test_r2:.4f}")
        print(f"   Training time: {training_time:.2f}s")
        
        return {
            'model_name': model_name,
            'test_mae': test_mae,
            'test_r2': test_r2,
            'training_time': training_time
        }

def main():
    """Main experiment tracking function"""
    print("=" * 80)
    print("🧪 MLFLOW EXPERIMENT TRACKING")
    print("=" * 80)
    
    # Load data
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    print(f"✅ Data loaded: {len(X_train)} train, {len(X_test)} test samples")
    
    # Define models to test
    models = {
        'ExtraTrees': ExtraTreesRegressor(n_estimators=300, max_depth=25, random_state=42, n_jobs=-1),
        'RandomForest': RandomForestRegressor(n_estimators=300, max_depth=25, random_state=42, n_jobs=-1),
        'GradientBoosting': GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42)
    }
    
    # Train and log all models
    results = []
    for model_name, model in models.items():
        result = train_and_log_model(model_name, model, X_train, X_test, y_train, y_test)
        results.append(result)
    
    # Print comparison
    print("\n" + "=" * 80)
    print("📊 MODEL COMPARISON")
    print("=" * 80)
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('test_mae')
    
    print(results_df.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("✅ EXPERIMENT TRACKING COMPLETE")
    print("=" * 80)
    print("\nView results:")
    print("  mlflow ui")
    print("  Then open: http://localhost:5000")
    print("=" * 80)

if __name__ == '__main__':
    main()

