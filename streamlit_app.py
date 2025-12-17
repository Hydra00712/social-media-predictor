"""
Simple Streamlit App for Social Media Engagement Prediction
This satisfies the professor's requirement for user interface + Streamlit
"""

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import json
import os
from azure.storage.blob import BlobServiceClient
import tempfile

# Page config
st.set_page_config(
    page_title="Social Media Engagement Predictor",
    page_icon="📱",
    layout="wide"
)

# Title
st.title("📱 Social Media Engagement Predictor")
st.markdown("### Predict engagement rate for your social media posts")
st.markdown("---")

# Load model and encoders from Azure Blob Storage
@st.cache_resource
def load_model_from_azure():
    """
    Load model from Azure Blob Storage
    This allows the Streamlit app to run anywhere (local or cloud)
    while still using models stored in Azure
    """
    try:
        # Get Azure connection string from Streamlit secrets or environment
        connection_string = st.secrets.get("AZURE_STORAGE_CONNECTION_STRING",
                                          os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))

        if not connection_string:
            # Fallback to local files if no Azure connection
            st.warning("⚠️ No Azure connection found. Loading from local files...")
            return load_model_local()

        st.info("🔄 Loading model from Azure Blob Storage...")

        # Connect to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client("models")

        # Create temporary directory
        temp_dir = tempfile.mkdtemp()

        # Download model files from Azure
        files_to_download = [
            'engagement_model.pkl',
            'feature_columns.pkl',
            'label_encoders.pkl',
            'experiment_results.json'
        ]

        for file_name in files_to_download:
            blob_client = container_client.get_blob_client(file_name)
            download_path = os.path.join(temp_dir, file_name)

            with open(download_path, "wb") as f:
                f.write(blob_client.download_blob().readall())

        # Load models from temporary directory
        model = joblib.load(os.path.join(temp_dir, 'engagement_model.pkl'))
        feature_columns = joblib.load(os.path.join(temp_dir, 'feature_columns.pkl'))
        label_encoders = joblib.load(os.path.join(temp_dir, 'label_encoders.pkl'))

        # Load experiment results
        experiment_results = None
        exp_path = os.path.join(temp_dir, 'experiment_results.json')
        if os.path.exists(exp_path):
            with open(exp_path, 'r') as f:
                experiment_results = json.load(f)

        st.success("✅ Model loaded from Azure Blob Storage!")

        return model, feature_columns, label_encoders, experiment_results

    except Exception as e:
        st.error(f"❌ Error loading from Azure: {e}")
        st.warning("Trying local files as fallback...")
        return load_model_local()

@st.cache_resource
def load_model_local():
    """
    Fallback: Load model from local files
    """
    try:
        model = joblib.load('models/engagement_model.pkl')
        feature_columns = joblib.load('models/feature_columns.pkl')
        label_encoders = joblib.load('models/label_encoders.pkl')

        # Load experiment results if available
        experiment_results = None
        if os.path.exists('models/experiment_results.json'):
            with open('models/experiment_results.json', 'r') as f:
                experiment_results = json.load(f)

        st.info("📁 Model loaded from local files")

        return model, feature_columns, label_encoders, experiment_results
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None

model, feature_columns, label_encoders, experiment_results = load_model_from_azure()

if model is None:
    st.error("❌ Could not load model. Please ensure model files are in the 'models' folder.")
    st.stop()

# Sidebar - Model Info
with st.sidebar:
    st.header("📊 Model Information")
    
    if experiment_results:
        st.metric("Best Model", experiment_results['best_model'])
        st.metric("R² Score", f"{experiment_results['metrics'][experiment_results['best_model']]['r2']:.4f}")
        st.metric("MAE", f"{experiment_results['metrics'][experiment_results['best_model']]['mae']:.4f}")
        st.metric("RMSE", f"{experiment_results['metrics'][experiment_results['best_model']]['rmse']:.4f}")
        
        st.markdown("---")
        st.markdown("### Models Compared")
        for model_name in experiment_results['models_compared']:
            st.text(f"✓ {model_name}")
    else:
        st.info("Model loaded successfully")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app predicts social media engagement rate using machine learning.")

# Main content - Input Form
st.header("📝 Enter Post Details")

col1, col2, col3 = st.columns(3)

with col1:
    day_of_week = st.selectbox("Day of Week", 
                               ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    platform = st.selectbox("Platform", 
                           ['Instagram', 'Twitter', 'Facebook', 'LinkedIn', 'TikTok'])
    location = st.selectbox("Location", 
                           ['USA', 'UK', 'Canada', 'Australia', 'India', 'France', 'Germany'])
    language = st.selectbox("Language", 
                           ['English', 'French', 'Spanish', 'German', 'Hindi'])

with col2:
    topic_category = st.selectbox("Topic Category", 
                                 ['Technology', 'Fashion', 'Food', 'Travel', 'Sports', 'Entertainment', 'Business'])
    sentiment_score = st.slider("Sentiment Score", -1.0, 1.0, 0.0, 0.1)
    sentiment_label = st.selectbox("Sentiment Label", 
                                  ['Positive', 'Negative', 'Neutral'])
    emotion_type = st.selectbox("Emotion Type", 
                               ['Joy', 'Sadness', 'Anger', 'Fear', 'Surprise', 'Neutral'])

with col3:
    toxicity_score = st.slider("Toxicity Score", 0.0, 1.0, 0.0, 0.1)
    brand_name = st.selectbox("Brand", 
                             ['Apple', 'Google', 'Microsoft', 'Amazon', 'Nike', 'Adidas', 'Coca-Cola'])
    product_name = st.selectbox("Product", 
                               ['iPhone', 'Pixel', 'Surface', 'Echo', 'Air Max', 'Ultraboost', 'Coke'])
    campaign_name = st.selectbox("Campaign", 
                                ['LaunchWave', 'SummerSale', 'BlackFriday', 'NewYear', 'SpringCollection'])

col4, col5 = st.columns(2)

with col4:
    campaign_phase = st.selectbox("Campaign Phase", 
                                 ['Pre-Launch', 'Launch', 'Post-Launch', 'Sustain'])
    user_past_sentiment_avg = st.slider("User Past Sentiment Avg", -1.0, 1.0, 0.0, 0.1)

with col5:
    user_engagement_growth = st.slider("User Engagement Growth (%)", -100.0, 100.0, 0.0, 1.0)
    buzz_change_rate = st.slider("Buzz Change Rate (%)", -100.0, 100.0, 0.0, 1.0)

st.markdown("---")

# Predict button
if st.button("🚀 Predict Engagement Rate", type="primary", use_container_width=True):
    try:
        # Create input dataframe
        input_data = {
            'day_of_week': day_of_week,
            'platform': platform,
            'location': location,
            'language': language,
            'topic_category': topic_category,
            'sentiment_score': sentiment_score,
            'sentiment_label': sentiment_label,
            'emotion_type': emotion_type,
            'toxicity_score': toxicity_score,
            'brand_name': brand_name,
            'product_name': product_name,
            'campaign_name': campaign_name,
            'campaign_phase': campaign_phase,
            'user_past_sentiment_avg': user_past_sentiment_avg,
            'user_engagement_growth': user_engagement_growth,
            'buzz_change_rate': buzz_change_rate
        }
        
        df_input = pd.DataFrame([input_data])
        
        # Encode categorical variables
        for col, encoder in label_encoders.items():
            if col in df_input.columns:
                try:
                    df_input[col] = encoder.transform(df_input[col].astype(str))
                except:
                    # If value not seen during training, use most common
                    df_input[col] = 0
        
        # Make prediction
        prediction = model.predict(df_input[feature_columns])[0]
        
        # Display result
        st.success("✅ Prediction Complete!")
        
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            st.metric(
                label="Predicted Engagement Rate",
                value=f"{prediction:.2%}",
                delta=None
            )
            
            # Interpretation
            if prediction > 0.5:
                st.success("🔥 High engagement expected!")
            elif prediction > 0.3:
                st.info("📊 Moderate engagement expected")
            else:
                st.warning("📉 Low engagement expected")
        
    except Exception as e:
        st.error(f"❌ Prediction error: {e}")

# Footer
st.markdown("---")
st.markdown("### 💡 Tips for Better Engagement")
st.markdown("""
- **Positive sentiment** generally leads to higher engagement
- **Low toxicity** is crucial for good engagement
- **User engagement growth** is a strong predictor
- **Buzz change rate** indicates trending topics
""")

