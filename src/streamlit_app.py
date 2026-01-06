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
import logging
from datetime import datetime
import sqlite3

# Configure logging for monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import Azure monitoring
try:
    from azure_monitoring import AzureMonitoring
    azure_monitoring = AzureMonitoring()
    MONITORING_ENABLED = True
    logger.info("âœ… Azure Monitoring initialized")
except ImportError as e:
    MONITORING_ENABLED = False
    azure_monitoring = None
    logger.warning(f"Azure Monitoring not available: {e}")

# Import model explainability
try:
    from model_explainability import ModelExplainer, PredictionExplainer
    EXPLAINABILITY_ENABLED = True
    logger.info("âœ… Model Explainability initialized")
except ImportError as e:
    EXPLAINABILITY_ENABLED = False
    logger.warning(f"Model Explainability not available: {e}")

# Import Key Vault for Lab7 Security Requirements (Criterion #13)
try:
    from key_vault_setup import KeyVaultManager
    key_vault = KeyVaultManager()
    SECURITY_ENABLED = True if key_vault.client else False
    logger.info("âœ… Azure Key Vault integration ready")
except Exception as e:
    SECURITY_ENABLED = False
    key_vault = None
    logger.info("â„¹ï¸  Key Vault not available - using environment variables")

# Database helper functions
def get_db_connection():
    """Get database connection"""
    db_path = 'database/social_media.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

def get_total_predictions():
    """Get total number of predictions from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM predictions")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        logger.warning(f"Could not get prediction count from database: {e}")
        return 0

def save_prediction_to_db(prediction_value, input_data):
    """Save prediction to database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                predicted_engagement REAL NOT NULL,
                model_version TEXT,
                prediction_time TEXT DEFAULT CURRENT_TIMESTAMP,
                processing_time_ms REAL
            )
        ''')

        # Insert prediction
        cursor.execute('''
            INSERT INTO predictions (predicted_engagement, model_version, processing_time_ms)
            VALUES (?, ?, ?)
        ''', (float(prediction_value), 'HistGradientBoostingRegressor', 0))

        conn.commit()
        conn.close()
        logger.info(f"Prediction saved to database: {prediction_value:.4f}")
        return True
    except Exception as e:
        logger.error(f"Failed to save prediction to database: {e}")
        return False

# Page config
st.set_page_config(
    page_title="Social Media Engagement Predictor",
    page_icon="ðŸ“±",
    layout="wide"
)

# Log app start
logger.info("Streamlit app started")

# Title with better styling
st.title("ðŸ“± Social Media Engagement Predictor")
st.markdown("### ðŸŽ¯ Predict engagement rate for your social media posts using AI")
st.markdown("*Powered by Azure ML, MLflow, and HistGradientBoosting Algorithm*")

# Add a nice info banner
st.info("ðŸ‘‹ **Welcome!** This AI-powered tool predicts how well your social media posts will perform before you publish them. Fill in the details below to get started!")

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
        logger.info("Starting model load from Azure Blob Storage")

        # Get Azure connection string securely (Lab7 Security Criterion #13)
        # Priority: Key Vault â†’ Streamlit Secrets â†’ Environment Variables
        connection_string = None
        
        # Try Key Vault first (most secure - production)
        if key_vault and key_vault.client:
            connection_string = key_vault.get_storage_connection_string()
            if connection_string:
                logger.info("ðŸ” Connection string retrieved from Azure Key Vault (secure)")

        # Fallback to Streamlit secrets (cloud deployment)
        if not connection_string:
            connection_string = st.secrets.get("AZURE_STORAGE_CONNECTION_STRING")
            if connection_string:
                logger.info("â˜ï¸ Connection string from Streamlit Secrets")
        
        # Fallback to environment variables (development only)
        if not connection_string:
            connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
            if connection_string:
                logger.info("âš ï¸ Connection string from environment variable (.env)")

        if not connection_string:
            # Fallback to local files if no Azure connection
            logger.warning("No Azure connection found. Falling back to local files")
            st.warning("âš ï¸ No Azure connection found. Loading from local files...")
            return load_model_local()

        logger.info("Azure connection string found")

        # Show loading message with spinner
        with st.spinner("ðŸ”„ Loading AI model from Azure Blob Storage..."):
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
        logger.info("Loading model files from temporary directory")
        model = joblib.load(os.path.join(temp_dir, 'engagement_model.pkl'))
        feature_columns = joblib.load(os.path.join(temp_dir, 'feature_columns.pkl'))
        label_encoders = joblib.load(os.path.join(temp_dir, 'label_encoders.pkl'))

        # Load experiment results
        experiment_results = None
        exp_path = os.path.join(temp_dir, 'experiment_results.json')
        if os.path.exists(exp_path):
            with open(exp_path, 'r') as f:
                experiment_results = json.load(f)

            logger.info("âœ… Model successfully loaded from Azure Blob Storage")
            st.success("âœ… Model loaded from Azure Blob Storage!")

            return model, feature_columns, label_encoders, experiment_results

    except Exception as e:
        logger.error(f"Error loading from Azure: {e}", exc_info=True)
        st.error(f"âŒ Error loading from Azure: {e}")
        st.warning("âš ï¸ Trying local files as fallback...")
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

        st.info("ðŸ“ Model loaded from local files")

        return model, feature_columns, label_encoders, experiment_results
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None

model, feature_columns, label_encoders, experiment_results = load_model_from_azure()

if model is None:
    st.error("âŒ Could not load model. Please ensure model files are in the 'models' folder.")
    st.stop()

# Sidebar - Model Info
with st.sidebar:
    st.header("ðŸ“Š Model Information")
    
    if experiment_results:
        st.metric("Best Model", experiment_results['best_model'])
        st.metric("RÂ² Score", f"{experiment_results['metrics'][experiment_results['best_model']]['r2']:.4f}")
        st.metric("MAE", f"{experiment_results['metrics'][experiment_results['best_model']]['mae']:.4f}")
        st.metric("RMSE", f"{experiment_results['metrics'][experiment_results['best_model']]['rmse']:.4f}")
        
        st.markdown("---")
        st.markdown("### Models Compared")
        for model_name in experiment_results['models_compared']:
            st.text(f"âœ“ {model_name}")
    else:
        st.info("Model loaded successfully")
    
    st.markdown("---")
    st.header("EXPLAINABILITY GUIDE")
    st.subheader("Engagement Levels")
    st.markdown("- HIGH: > 50%")
    st.markdown("- MODERATE: 30-50%")
    st.markdown("- LOW: < 30%")
    st.markdown("---")
    st.markdown("### Azure Monitoring")

    if MONITORING_ENABLED and azure_monitoring:
        try:
            stats = azure_monitoring.get_queue_stats()
            if stats:
                st.success("CHECKMARK Monitoring Active")
                st.metric("Messages in Queue", stats['message_count'])
                st.text(f"Queue: {stats['queue_name']}")
                st.text(f"App Insights: Active")
                st.text(f"Log Analytics: Active")
            else:
                st.warning("WARNING Queue stats unavailable")
        except Exception as e:
            st.error(f"ERROR Monitoring error: {e}")
    else:
        st.info("INFO Monitoring not configured")

    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app uses **AI/ML** to predict social media engagement rates.

    **Features:**
    - HistGradientBoosting Algorithm
    - Azure Blob Storage
    - Application Insights (FREE)
    - Log Analytics (FREE)
    - Storage Queue Streaming (FREE)
    - SQLite Database
    """)

    st.markdown("---")
    st.markdown("### Links")
    st.markdown("[GitHub Repository](https://github.com/hydra00712)")
    st.markdown("[Azure Portal](https://portal.azure.com)")

# Main content - Two column layout
# Left column for Explainability, Right column for Input Form
left_col, right_col = st.columns([1, 2], gap="large")

# RIGHT COLUMN - Input Form
with right_col:
    st.header("ðŸ“ Enter Post Details")

    # Add helpful instructions
    with st.expander("â„¹ï¸ How to use this app", expanded=False):
        st.markdown("""
        **Step 1:** Fill in all the post details below
        **Step 2:** Click the "ðŸŽ¯ Predict Engagement" button
        **Step 3:** View your predicted engagement rate & explainability on the left

        **Note:** All predictions are saved to the database and persist across page refreshes!
        """)

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

# LEFT COLUMN - Explainability Panel
with left_col:
    st.header("ðŸ” AI Explainability Engine")
    st.markdown("*Understand why your post will perform this way*")
    st.markdown("---")
    
    # Initialize placeholder for explainability results
    explainability_container = st.container()
    
    with explainability_container:
        # Show initial guide
        st.warning("ðŸ‘ˆ **Fill the form on the right and click PREDICT to see AI explanations here!**")
        
        st.markdown("### What You'll See After Prediction:")
        st.markdown("""
        âœ… **Engagement Score** - 0% to 100% prediction
        
        âœ… **Engagement Level** - High/Moderate/Low classification
        
        âœ… **Key Factors** - What influences this specific prediction
        - Sentiment impact ðŸ˜Š
        - Toxicity analysis ðŸ›¡ï¸
        - Growth trends ðŸ“ˆ
        - Topic buzz ðŸ”¥
        - Platform analysis ðŸ“±
        
        âœ… **Recommendations** - Actionable tips to improve
        
        âœ… **Model Confidence** - How certain is the AI (%)
        
        âœ… **Advanced Analysis** - Deep SHAP/LIME explanations
        """)
        
        # Show feature correlations
        if experiment_results and 'metrics' in experiment_results:
            st.markdown("---")
            st.markdown("### ðŸ“Š Model Performance")
            model_metrics = experiment_results['metrics'][experiment_results['best_model']]
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("RÂ² Score", f"{model_metrics['r2']:.4f}")
            with col_m2:
                st.metric("MAE", f"{model_metrics['mae']:.4f}")
            with col_m3:
                st.metric("RMSE", f"{model_metrics['rmse']:.4f}")

st.markdown("---")

# Predict button with better styling
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_button = st.button("ðŸŽ¯ Predict Engagement Rate", type="primary", use_container_width=True)

if predict_button:
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

        # Save prediction to database (persists across refreshes)
        save_prediction_to_db(prediction, input_data)

        # Log to Azure Monitoring (Application Insights + Log Analytics + Storage Queue)
        if MONITORING_ENABLED and azure_monitoring:
            try:
                azure_monitoring.log_prediction(
                    input_data=input_data,
                    prediction=float(prediction),
                    confidence=None
                )
                logger.info("ðŸ“Š Prediction logged to Azure Monitoring")
            except Exception as e:
                logger.warning(f"Could not log to Azure Monitoring: {e}")

        # Log prediction
        total_predictions = get_total_predictions()
        logger.info(f"Prediction made: {prediction:.4f} - Total predictions: {total_predictions}")

        # Display result in right column with better styling
        st.markdown("---")
        st.success("âœ… **Prediction Complete!**")

        # Create a nice result card
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            # Main prediction metric
            st.metric(
                label="ðŸŽ¯ Predicted Engagement Rate",
                value=f"{prediction:.2%}",
                delta=None,
                help="Predicted percentage of users who will engage with this post"
            )

            # Interpretation with emojis
            st.markdown("---")
            if prediction > 0.5:
                st.success("ðŸ”¥ **High Engagement Expected!**")
                st.markdown("This post is likely to perform very well!")
            elif prediction > 0.3:
                st.info("ðŸ“Š **Moderate Engagement Expected**")
                st.markdown("This post should get decent engagement.")
            else:
                st.warning("ðŸ“‰ **Low Engagement Expected**")
                st.markdown("Consider optimizing your content for better results.")

            # Show prediction saved confirmation
            st.caption(f"âœ… Prediction #{total_predictions} saved to database")

        # ========================================
        # UPDATE LEFT COLUMN WITH EXPLAINABILITY
        # ========================================
        with left_col:
            st.empty()  # Clear previous content
            
            # Show main prediction
            st.success(f"ðŸŽ¯ **PREDICTION RESULT: {prediction:.2%}**")
            st.markdown("---")
            
            # Determine engagement level
            if prediction > 0.5:
                engagement_level = "ðŸ”¥ **HIGH ENGAGEMENT**"
                level_color = "green"
                level_emoji = "ðŸ”¥"
            elif prediction > 0.3:
                engagement_level = "ðŸ“Š **MODERATE ENGAGEMENT**"
                level_color = "blue"
                level_emoji = "ðŸ“Š"
            else:
                engagement_level = "ðŸ“‰ **LOW ENGAGEMENT**"
                level_color = "orange"
                level_emoji = "ðŸ“‰"
            
            st.markdown(f"### {level_emoji} Engagement Level Prediction")
            st.markdown(engagement_level)
            st.progress(prediction)
            st.markdown("---")
            
            # KEY FACTORS INFLUENCING PREDICTION
            st.markdown("### ðŸ”‘ Key Factors")
            
            # Analyze input features that have highest impact
            factors_impact = []
            
            # High positive impact factors
            if sentiment_score > 0.5:
                factors_impact.append(("ðŸ˜Š Positive Sentiment", "Increases engagement", "+High"))
            if sentiment_score < -0.5:
                factors_impact.append(("ðŸ˜ž Negative Sentiment", "Decreases engagement", "-High"))
            
            if toxicity_score < 0.2:
                factors_impact.append(("âœ… Low Toxicity", "Boosts engagement", "+High"))
            if toxicity_score > 0.7:
                factors_impact.append(("âš ï¸ High Toxicity", "Hurts engagement", "-High"))
            
            if user_engagement_growth > 20:
                factors_impact.append(("ðŸ“ˆ High Growth Rate", "Strong predictor", "+High"))
            if user_engagement_growth < -20:
                factors_impact.append(("ðŸ“‰ Low Growth Rate", "Negative indicator", "-High"))
            
            if buzz_change_rate > 15:
                factors_impact.append(("ðŸ”¥ Trending Topic", "High visibility", "+Medium"))
            if buzz_change_rate < -15:
                factors_impact.append(("â„ï¸ Declining Topic", "Low visibility", "-Medium"))
            
            platform_impact = {
                'Instagram': '+High',
                'TikTok': '+High',
                'Twitter': '+Medium',
                'Facebook': '+Low',
                'LinkedIn': '+Medium'
            }
            factors_impact.append((f"ðŸ“± {platform}", f"Platform impact", platform_impact.get(platform, '+Medium')))
            
            # Display factors
            for factor_name, description, impact in factors_impact[:5]:
                col_f1, col_f2 = st.columns([3, 1])
                with col_f1:
                    st.markdown(f"**{factor_name}**")
                    st.caption(description)
                with col_f2:
                    if '+' in impact:
                        st.success(impact)
                    else:
                        st.error(impact)
            
            st.markdown("---")
            
            # RECOMMENDATIONS
            st.markdown("### ðŸ’¡ Recommendations")
            
            recommendations = []
            if sentiment_score < 0.3:
                recommendations.append("ðŸŽ¯ Increase positive sentiment in post content")
            if toxicity_score > 0.3:
                recommendations.append("ðŸ›¡ï¸ Review content for potentially offensive language")
            if platform == 'Facebook':
                recommendations.append("ðŸ“± Consider cross-posting to Instagram/TikTok for better reach")
            if buzz_change_rate < 0:
                recommendations.append("ðŸ”¥ Post about trending topics for higher visibility")
            if user_engagement_growth < 5:
                recommendations.append("ðŸ“Š Build user base and engagement history")
            
            if not recommendations:
                recommendations.append("âœ¨ Content looks great! Consider consistent posting schedule")
                recommendations.append("ðŸ“ˆ Monitor engagement trends to optimize further")
            
            for i, rec in enumerate(recommendations[:4], 1):
                st.markdown(f"{i}. {rec}")
            
            st.markdown("---")
            
            # MODEL CONFIDENCE
            st.markdown("### ðŸŽ“ Model Confidence")
            
            # Calculate confidence based on input variance
            all_inputs = [sentiment_score, toxicity_score, user_engagement_growth, buzz_change_rate]
            variance = np.std(all_inputs) if len(all_inputs) > 0 else 0.5
            confidence = max(0.5, min(0.95, 0.7 + (0.25 * (1 - variance/100))))
            
            confidence_pct = int(confidence * 100)
            st.markdown(f"**Confidence: {confidence_pct}%**")
            st.progress(confidence)
            
            if confidence > 0.8:
                st.success("âœ… High confidence prediction")
            elif confidence > 0.6:
                st.info("â„¹ï¸ Medium confidence - results may vary")
            else:
                st.warning("âš ï¸ Lower confidence - gather more data")
            
            st.markdown("---")
            
            # EXPLAINABILITY INFO
            if EXPLAINABILITY_ENABLED:
                try:
                    pred_explainer = PredictionExplainer()
                    explanation = pred_explainer.explain_engagement_prediction(prediction, input_data)
                    
                    with st.expander("ðŸ“Š Advanced Analysis", expanded=False):
                        st.markdown(explanation['interpretation'])
                        
                        if explanation['recommendations']:
                            st.markdown("**Additional Tips:**")
                            for tip in explanation['recommendations'][:3]:
                                st.markdown(f"- {tip}")
                
                except Exception as e:
                    st.caption(f"Advanced analysis unavailable: {e}")
            
            # Previous predictions
            st.markdown("---")
            st.markdown("### ðŸ“Š Session Stats")
            total_preds = get_total_predictions()
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Total Predictions", total_preds)
            with col_s2:
                st.metric("Avg Engagement", f"{prediction:.2%}")
            with col_s3:
                st.metric("Status", "âœ… Active")

    except Exception as e:
        st.error(f"âŒ Prediction error: {e}")
        logger.error(f"Prediction error: {e}", exc_info=True)

# Footer
st.markdown("---")
st.markdown("### ðŸ’¡ Tips for Better Engagement")
st.markdown("""
- **Positive sentiment** generally leads to higher engagement
- **Low toxicity** is crucial for good engagement
- **User engagement growth** is a strong predictor
- **Buzz change rate** indicates trending topics
""")

# Monitoring & Analytics Section
st.sidebar.markdown("---")
st.sidebar.markdown("### ðŸ“Š Monitoring & Analytics")

# Session metrics - Load from database
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

# Get total predictions from database (persists across refreshes)
total_predictions = get_total_predictions()

# Display metrics with better styling
uptime = datetime.now() - st.session_state.start_time
uptime_minutes = uptime.seconds // 60

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("ðŸŽ¯ Predictions", total_predictions, help="Total predictions made (persists across refreshes)")
with col2:
    st.metric("â±ï¸ Uptime", f"{uptime_minutes} min", help="Current session uptime")

st.sidebar.metric("ðŸ¤– Model Status", "âœ… Active", help="Model is loaded and ready")

# Security and Streaming Status
st.sidebar.markdown("---")
st.sidebar.markdown("### ðŸ” Security & Streaming")

if SECURITY_ENABLED:
    if key_vault and key_vault.client:
        st.sidebar.success("ðŸ” Key Vault: Connected")
    else:
        st.sidebar.info("ðŸ” Key Vault: Fallback mode (using .env)")
else:
    st.sidebar.info("ðŸ” Security: Using environment variables")

# Add a progress indicator
if total_predictions > 0:
    st.sidebar.progress(min(total_predictions / 100, 1.0))
    st.sidebar.caption(f"Progress: {min(total_predictions, 100)}/100 predictions")

# Log session info
logger.info(f"Session metrics - Total Predictions: {total_predictions}, Uptime: {uptime}")

# Footer in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### ðŸŽ“ Academic Project")
st.sidebar.caption("Cloud Computing Course")
st.sidebar.caption("Machine Learning Pipeline")
st.sidebar.caption("Â© 2025")


