"""
Model Explainability & Interpretability
========================================
Explains what features matter most in predictions and why
"""

import numpy as np
import pandas as pd
import pickle
import shap
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelExplainer:
    """Explain model predictions using SHAP and feature importance"""
    
    def __init__(self, model, feature_names, sample_data=None):
        """
        Initialize explainer
        
        Args:
            model: Trained sklearn model
            feature_names: List of feature names
            sample_data: Sample data for SHAP background (optional)
        """
        self.model = model
        self.feature_names = feature_names
        self.sample_data = sample_data
        self.explainer = None
        self.shap_values = None
        
        logger.info("✅ Model Explainer initialized")
    
    def get_feature_importance(self):
        """
        Get feature importance from the model
        
        Returns:
            dict: Feature importance scores
        """
        try:
            # For tree-based models (Random Forest, Gradient Boosting, etc.)
            if hasattr(self.model, 'feature_importances_'):
                importances = self.model.feature_importances_
                
                # Create dictionary
                feature_importance_dict = dict(zip(self.feature_names, importances))
                
                # Sort by importance
                sorted_features = sorted(
                    feature_importance_dict.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                
                logger.info("✅ Feature importance extracted from model")
                return {
                    'method': 'model_built_in',
                    'features': dict(sorted_features),
                    'top_5': dict(sorted_features[:5]),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.warning("⚠️ Model does not have built-in feature importance")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error getting feature importance: {e}")
            return None
    
    def explain_prediction(self, sample_input, top_k=5):
        """
        Explain a single prediction
        
        Args:
            sample_input: Feature vector or DataFrame
            top_k: Top K features to show
        
        Returns:
            dict: Explanation with feature contributions
        """
        try:
            # Get prediction
            prediction = self.model.predict(sample_input.reshape(1, -1))[0]
            
            # Get feature importance
            importance = self.get_feature_importance()
            
            if importance is None:
                return {
                    'prediction': float(prediction),
                    'explanation': 'Feature importance not available for this model',
                    'top_features': None
                }
            
            # Get top features for this prediction
            top_features = list(importance['top_5'].items())
            
            explanation = {
                'prediction': float(prediction),
                'model_type': type(self.model).__name__,
                'top_features': {
                    'name': [f[0] for f in top_features],
                    'importance': [float(f[1]) for f in top_features],
                    'normalized_importance': [
                        float(f[1]) / sum([x[1] for x in top_features])
                        for f in top_features
                    ]
                },
                'explanation_text': self._generate_explanation_text(top_features, prediction),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Prediction explained: {prediction:.4f}")
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Error explaining prediction: {e}")
            return {
                'error': str(e),
                'prediction': float(prediction) if 'prediction' in locals() else None
            }
    
    def _generate_explanation_text(self, top_features, prediction):
        """Generate human-readable explanation"""
        
        explanation = f"Engagement rate predicted: {prediction:.2%}\n\n"
        explanation += "Key factors driving this prediction:\n"
        
        for i, (feature_name, importance) in enumerate(top_features[:3], 1):
            importance_pct = (importance / sum([f[1] for f in top_features])) * 100
            explanation += f"{i}. {feature_name} ({importance_pct:.1f}%)\n"
        
        return explanation
    
    def get_prediction_contributions(self, sample_input, feature_names=None):
        """
        Get how much each feature contributes to the prediction
        
        Args:
            sample_input: Input features
            feature_names: Feature names (if different)
        
        Returns:
            dict: Feature contributions
        """
        if feature_names is None:
            feature_names = self.feature_names
        
        try:
            # Get base prediction
            prediction = self.model.predict(sample_input.reshape(1, -1))[0]
            
            # Get feature importance
            importance = self.get_feature_importance()
            
            if importance is None:
                return None
            
            # Normalize importance to sum to 1
            total_importance = sum(importance['features'].values())
            
            contributions = {}
            for feature in feature_names:
                if feature in importance['features']:
                    contribution = importance['features'][feature] / total_importance
                    contributions[feature] = {
                        'importance': float(importance['features'][feature]),
                        'contribution_to_prediction': float(contribution),
                        'value': float(sample_input[0, feature_names.index(feature)])
                    }
            
            return {
                'prediction': float(prediction),
                'contributions': contributions,
                'total_features': len(feature_names)
            }
            
        except Exception as e:
            logger.error(f"❌ Error calculating contributions: {e}")
            return None


class PredictionExplainer:
    """Simple explainer for predictions with interpretable rules"""
    
    def __init__(self):
        self.rules = {}
        logger.info("✅ Prediction Explainer initialized")
    
    def explain_engagement_prediction(self, prediction_value, input_features):
        """
        Explain engagement prediction using simple rules
        
        Args:
            prediction_value: Predicted engagement rate (0-1)
            input_features: Input feature dictionary
        
        Returns:
            dict: Human-readable explanation
        """
        
        explanation = {
            'predicted_engagement': float(prediction_value),
            'engagement_level': self._get_engagement_level(prediction_value),
            'key_factors': self._identify_key_factors(input_features),
            'recommendations': self._generate_recommendations(prediction_value, input_features),
            'interpretation': self._get_interpretation(prediction_value)
        }
        
        return explanation
    
    def _get_engagement_level(self, prediction):
        """Categorize engagement level"""
        if prediction > 0.15:
            return "🔥 Very High Engagement"
        elif prediction > 0.10:
            return "📈 High Engagement"
        elif prediction > 0.05:
            return "📊 Moderate Engagement"
        elif prediction > 0.02:
            return "📉 Low Engagement"
        else:
            return "❌ Very Low Engagement"
    
    def _identify_key_factors(self, features):
        """Identify which features helped this prediction"""
        key_factors = []
        
        # Sentiment analysis
        if features.get('sentiment_score', 0) > 0.5:
            key_factors.append({
                'factor': 'Very Positive Sentiment',
                'impact': 'Positive ✅',
                'description': f"Score: {features.get('sentiment_score', 0):.2f}"
            })
        elif features.get('sentiment_score', 0) < -0.5:
            key_factors.append({
                'factor': 'Very Negative Sentiment',
                'impact': 'Negative ❌',
                'description': f"Score: {features.get('sentiment_score', 0):.2f}"
            })
        
        # Toxicity
        if features.get('toxicity_score', 0) > 0.5:
            key_factors.append({
                'factor': 'High Toxicity',
                'impact': 'Negative ❌',
                'description': f"Score: {features.get('toxicity_score', 0):.2f}"
            })
        else:
            key_factors.append({
                'factor': 'Low Toxicity',
                'impact': 'Positive ✅',
                'description': 'Clean, friendly content'
            })
        
        # User engagement growth
        if features.get('user_engagement_growth', 0) > 0.2:
            key_factors.append({
                'factor': 'Strong Engagement Growth',
                'impact': 'Positive ✅',
                'description': f"Growth rate: {features.get('user_engagement_growth', 0):.1%}"
            })
        
        # Buzz
        if features.get('buzz_change_rate', 0) > 10:
            key_factors.append({
                'factor': 'Trending Topic',
                'impact': 'Positive ✅',
                'description': f"Buzz increasing: {features.get('buzz_change_rate', 0):.1f}%"
            })
        
        return key_factors
    
    def _generate_recommendations(self, prediction, features):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Sentiment recommendations
        if features.get('sentiment_score', 0) < 0:
            recommendations.append("😊 Make it more positive - highlight benefits and happiness")
        
        # Toxicity recommendations
        if features.get('toxicity_score', 0) > 0.3:
            recommendations.append("🛡️ Reduce negative language - stay constructive and friendly")
        
        # Growth recommendations
        if features.get('user_engagement_growth', 0) < 0:
            recommendations.append("📈 Boost user engagement - try more interactive content")
        
        # Timing recommendations
        platform = features.get('platform', '')
        day = features.get('day_of_week', '')
        
        if day in ['Saturday', 'Sunday']:
            recommendations.append(f"⏰ Weekend post on {platform} - good choice for leisure users")
        
        # General recommendations
        if prediction < 0.05:
            recommendations.append("🎯 This content may underperform - consider major revisions")
        elif prediction < 0.10:
            recommendations.append("💡 Consider adding more engaging elements like hashtags or mentions")
        
        if not recommendations:
            recommendations.append("✨ Your content looks great! Keep it up!")
        
        return recommendations
    
    def _get_interpretation(self, prediction):
        """Get detailed interpretation"""
        interpretations = {
            'high': "This post has strong potential! Multiple factors align for good engagement.",
            'moderate': "This post has decent potential. A few tweaks could improve it significantly.",
            'low': "This post may struggle. Consider revising the sentiment, tone, or timing.",
            'very_low': "This post is at risk of poor engagement. Major changes recommended."
        }
        
        if prediction > 0.10:
            return interpretations['high']
        elif prediction > 0.05:
            return interpretations['moderate']
        elif prediction > 0.02:
            return interpretations['low']
        else:
            return interpretations['very_low']


def load_and_explain_model(model_path, features_path):
    """Load model and create explainer"""
    try:
        model = pickle.load(open(model_path, 'rb'))
        features = pickle.load(open(features_path, 'rb'))
        
        explainer = ModelExplainer(model, features)
        pred_explainer = PredictionExplainer()
        
        return explainer, pred_explainer
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None


if __name__ == '__main__':
    print("=" * 80)
    print("🔍 MODEL EXPLAINABILITY TEST")
    print("=" * 80)
    
    # Load model
    try:
        explainer, pred_explainer = load_and_explain_model(
            'models/engagement_model.pkl',
            'models/feature_columns.pkl'
        )
        
        if explainer:
            print("\n📊 Feature Importance:")
            importance = explainer.get_feature_importance()
            if importance:
                print(json.dumps(importance, indent=2))
        
        # Test explanation
        sample_input = np.random.randn(1, len(explainer.feature_names))
        explanation = explainer.explain_prediction(sample_input)
        
        print("\n💡 Prediction Explanation:")
        print(json.dumps(explanation, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n✅ Explainability module working!")
    print("=" * 80)
