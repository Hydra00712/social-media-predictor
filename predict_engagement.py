"""
ENGAGEMENT RATE PREDICTION API
================================
Load the best model and make predictions
"""

import pandas as pd
import numpy as np
import pickle
from datetime import datetime

class EngagementPredictor:
    def __init__(self, model_dir='models_final'):
        """Load trained model and preprocessing objects"""
        print("🔄 Loading model...")
        
        with open(f'{model_dir}/extratrees_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        
        with open(f'{model_dir}/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        
        with open(f'{model_dir}/features.pkl', 'rb') as f:
            self.feature_names = pickle.load(f)
        
        with open(f'{model_dir}/encoders.pkl', 'rb') as f:
            self.encoders = pickle.load(f)
        
        print("✅ Model loaded successfully!")
    
    def prepare_features(self, data):
        """
        Prepare features from input data
        
        Expected input columns:
        - timestamp (datetime or string)
        - platform (str): Instagram, Twitter, Facebook, YouTube, Reddit
        - language (str): en, es, pt, ru, etc.
        - text_content (str)
        - hashtags (str): comma-separated or 'none'
        - mentions (str): comma-separated or 'none'
        - keywords (str): comma-separated or 'none'
        - topic_category (str)
        - sentiment_score (float): -1 to 1
        - sentiment_label (str): Positive, Negative, Neutral
        - emotion_type (str)
        - toxicity_score (float): 0 to 1
        - campaign_name (str)
        - campaign_phase (str)
        - user_past_sentiment_avg (float)
        - user_engagement_growth (float)
        - buzz_change_rate (float)
        """
        
        df = data.copy()
        
        # Temporal features
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day'] = df['timestamp'].dt.day
        df['month'] = df['timestamp'].dt.month
        df['dayofweek'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)
        df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 17)).astype(int)
        df['is_prime_time'] = ((df['hour'] >= 18) & (df['hour'] <= 22)).astype(int)
        
        # Text features
        df['hashtags_count'] = df['hashtags'].apply(lambda x: len(str(x).split(',')) if str(x) != 'none' else 0)
        df['mentions_count'] = df['mentions'].apply(lambda x: len(str(x).split(',')) if str(x) != 'none' else 0)
        df['keywords_count'] = df['keywords'].apply(lambda x: len(str(x).split(',')) if str(x) != 'none' else 0)
        df['text_length'] = df['text_content'].apply(lambda x: len(str(x)))
        df['word_count'] = df['text_content'].apply(lambda x: len(str(x).split()))
        df['avg_word_length'] = df.apply(lambda row: row['text_length'] / max(row['word_count'], 1), axis=1)
        
        # Sentiment & toxicity
        df['sentiment_toxicity_ratio'] = df['sentiment_score'] / (df['toxicity_score'] + 0.01)
        df['is_positive'] = (df['sentiment_score'] > 0).astype(int)
        df['is_negative'] = (df['sentiment_score'] < 0).astype(int)
        df['is_toxic'] = (df['toxicity_score'] > 0.5).astype(int)
        df['sentiment_abs'] = df['sentiment_score'].abs()
        
        # Engagement indicators
        df['has_hashtags'] = (df['hashtags_count'] > 0).astype(int)
        df['has_mentions'] = (df['mentions_count'] > 0).astype(int)
        df['has_keywords'] = (df['keywords_count'] > 0).astype(int)
        df['total_engagement_features'] = df['has_hashtags'] + df['has_mentions'] + df['has_keywords']
        
        # Encode categoricals (handle unknown values)
        def safe_encode(encoder, values):
            """Encode values, using 0 for unknown categories"""
            result = []
            for val in values:
                if pd.isna(val):
                    result.append(0)
                elif val in encoder.classes_:
                    result.append(encoder.transform([val])[0])
                else:
                    result.append(0)  # Unknown category
            return result

        df['topic_encoded'] = safe_encode(self.encoders['topic'], df['topic_category'])
        df['campaign_encoded'] = safe_encode(self.encoders['campaign'], df['campaign_name'])
        df['phase_encoded'] = safe_encode(self.encoders['phase'], df['campaign_phase'])
        df['emotion_encoded'] = safe_encode(self.encoders['emotion'], df['emotion_type'])
        df['sentiment_label_encoded'] = safe_encode(self.encoders['sentiment_label'], df['sentiment_label'])
        
        # Platform one-hot
        for platform in ['Instagram', 'Twitter', 'Facebook', 'YouTube', 'Reddit']:
            df[f'platform_{platform}'] = (df['platform'] == platform).astype(int)

        # Language one-hot (must match training)
        for lang in ['ja', 'ru', 'es', 'ar', 'zh']:
            df[f'lang_{lang}'] = (df['language'] == lang).astype(int)
        
        # Select features in correct order
        X = df[self.feature_names].fillna(0)
        
        return X
    
    def predict(self, data):
        """
        Predict engagement rate
        
        Args:
            data: DataFrame with required columns
        
        Returns:
            numpy array of predicted engagement rates
        """
        X = self.prepare_features(data)
        X_scaled = self.scaler.transform(X)
        
        # Predict on log scale
        y_pred_log = self.model.predict(X_scaled)
        
        # Transform back to original scale
        y_pred = np.expm1(y_pred_log)
        
        return y_pred
    
    def predict_single(self, **kwargs):
        """
        Predict for a single post
        
        Example:
            predictor.predict_single(
                timestamp='2024-12-17 14:30:00',
                platform='Instagram',
                language='en',
                text_content='Check out our new product!',
                hashtags='#NewProduct,#Launch',
                mentions='@BrandSupport',
                keywords='new,product,launch',
                topic_category='Product',
                sentiment_score=0.8,
                sentiment_label='Positive',
                emotion_type='Happy',
                toxicity_score=0.1,
                campaign_name='ProductLaunch',
                campaign_phase='Launch',
                user_past_sentiment_avg=0.5,
                user_engagement_growth=0.2,
                buzz_change_rate=15.0
            )
        """
        df = pd.DataFrame([kwargs])
        return self.predict(df)[0]


if __name__ == '__main__':
    # Test the predictor
    print("=" * 80)
    print("🧪 TESTING ENGAGEMENT PREDICTOR")
    print("=" * 80)
    
    predictor = EngagementPredictor()
    
    # Test with sample data
    print("\n📝 Test Case 1: High engagement post")
    pred1 = predictor.predict_single(
        timestamp='2024-12-17 19:00:00',  # Prime time
        platform='Instagram',
        language='en',
        text_content='Amazing new product launch! Check it out! #MustHave #Trending',
        hashtags='#MustHave,#Trending',
        mentions='@BrandCEO',
        keywords='amazing,new,product,launch',
        topic_category='Product',
        sentiment_score=0.9,
        sentiment_label='Positive',
        emotion_type='Happy',
        toxicity_score=0.05,
        campaign_name='ProductLaunch',
        campaign_phase='Launch',
        user_past_sentiment_avg=0.7,
        user_engagement_growth=0.5,
        buzz_change_rate=25.0
    )
    print(f"   Predicted engagement rate: {pred1:.4f}")
    
    print("\n📝 Test Case 2: Low engagement post")
    pred2 = predictor.predict_single(
        timestamp='2024-12-17 03:00:00',  # Off-peak
        platform='Reddit',
        language='en',
        text_content='Product update.',
        hashtags='none',
        mentions='none',
        keywords='update',
        topic_category='Product',
        sentiment_score=-0.2,
        sentiment_label='Negative',
        emotion_type='Neutral',
        toxicity_score=0.3,
        campaign_name='Update',
        campaign_phase='Post-Launch',
        user_past_sentiment_avg=-0.1,
        user_engagement_growth=-0.2,
        buzz_change_rate=-5.0
    )
    print(f"   Predicted engagement rate: {pred2:.4f}")
    
    print("\n✅ Predictor working correctly!")
    print("=" * 80)

