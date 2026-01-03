"""
Advanced Monitoring & Analytics Dashboard
==========================================
Comprehensive monitoring of model performance, data quality, and predictions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionMonitor:
    """Monitor prediction statistics and performance"""
    
    def __init__(self, db_path='database/social_media.db'):
        self.db_path = db_path
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """Initialize database connection"""
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            logger.info(f"✅ Connected to database: {self.db_path}")
        except Exception as e:
            logger.error(f"❌ Error connecting to database: {e}")
    
    def get_prediction_statistics(self, hours=24):
        """Get prediction statistics for the last N hours"""
        try:
            if not self.conn:
                return None
            
            query = """
            SELECT 
                COUNT(*) as total_predictions,
                AVG(predicted_engagement) as avg_engagement,
                MIN(predicted_engagement) as min_engagement,
                MAX(predicted_engagement) as max_engagement,
                STDDEV(predicted_engagement) as std_engagement
            FROM predictions
            WHERE prediction_time > datetime('now', '-' || ? || ' hours')
            """
            
            cursor = self.conn.cursor()
            cursor.execute(query, (hours,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'total_predictions': result[0],
                    'avg_engagement': float(result[1]) if result[1] else 0,
                    'min_engagement': float(result[2]) if result[2] else 0,
                    'max_engagement': float(result[3]) if result[3] else 0,
                    'std_engagement': float(result[4]) if result[4] else 0,
                    'time_window_hours': hours,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"❌ Error getting prediction statistics: {e}")
        
        return None
    
    def get_hourly_predictions(self, hours=24):
        """Get predictions grouped by hour"""
        try:
            if not self.conn:
                return None
            
            query = """
            SELECT 
                strftime('%Y-%m-%d %H:00:00', prediction_time) as hour,
                COUNT(*) as count,
                AVG(predicted_engagement) as avg_engagement,
                MIN(predicted_engagement) as min_engagement,
                MAX(predicted_engagement) as max_engagement
            FROM predictions
            WHERE prediction_time > datetime('now', '-' || ? || ' hours')
            GROUP BY hour
            ORDER BY hour DESC
            """
            
            cursor = self.conn.cursor()
            cursor.execute(query, (hours,))
            results = cursor.fetchall()
            
            if results:
                return [
                    {
                        'hour': r[0],
                        'prediction_count': r[1],
                        'avg_engagement': float(r[2]),
                        'min_engagement': float(r[3]),
                        'max_engagement': float(r[4])
                    }
                    for r in results
                ]
        except Exception as e:
            logger.error(f"❌ Error getting hourly predictions: {e}")
        
        return None
    
    def get_prediction_distribution(self):
        """Get distribution of predictions by engagement level"""
        try:
            if not self.conn:
                return None
            
            # Define engagement levels
            levels = {
                'very_low': (0, 0.05),
                'low': (0.05, 0.10),
                'medium': (0.10, 0.20),
                'high': (0.20, 0.50),
                'very_high': (0.50, 1.0)
            }
            
            distribution = {}
            cursor = self.conn.cursor()
            
            for level, (low, high) in levels.items():
                query = """
                SELECT COUNT(*) FROM predictions
                WHERE predicted_engagement >= ? AND predicted_engagement < ?
                """
                cursor.execute(query, (low, high))
                count = cursor.fetchone()[0]
                distribution[level] = {
                    'count': count,
                    'percentage': 0  # Will be calculated later
                }
            
            # Calculate percentages
            total = sum(d['count'] for d in distribution.values())
            for level in distribution:
                distribution[level]['percentage'] = (
                    (distribution[level]['count'] / total * 100) if total > 0 else 0
                )
            
            return distribution
        except Exception as e:
            logger.error(f"❌ Error getting prediction distribution: {e}")
        
        return None
    
    def get_model_health(self):
        """Get overall model health metrics"""
        try:
            stats = self.get_prediction_statistics(hours=24)
            distribution = self.get_prediction_distribution()
            
            if not stats:
                return None
            
            # Calculate health score
            health_score = 50.0  # Base score
            
            # Bonus for consistent predictions
            if stats['std_engagement'] < 0.15:
                health_score += 25
            elif stats['std_engagement'] > 0.40:
                health_score -= 15
            
            # Bonus for predicting diverse engagement
            if distribution:
                very_low_pct = distribution.get('very_low', {}).get('percentage', 0)
                very_high_pct = distribution.get('very_high', {}).get('percentage', 0)
                
                if 5 < very_low_pct < 35 and 5 < very_high_pct < 35:
                    health_score += 25
                else:
                    health_score -= 10
            
            # Clamp score to 0-100
            health_score = max(0, min(100, health_score))
            
            return {
                'health_score': health_score,
                'status': 'excellent' if health_score >= 80 else (
                    'good' if health_score >= 60 else (
                        'fair' if health_score >= 40 else 'poor'
                    )
                ),
                'predictions_24h': stats['total_predictions'],
                'avg_engagement': stats['avg_engagement'],
                'std_engagement': stats['std_engagement'],
                'prediction_distribution': distribution,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Error calculating model health: {e}")
        
        return None


class DataQualityMonitor:
    """Monitor data quality and detect anomalies"""
    
    @staticmethod
    def check_input_validity(input_data):
        """Check if input data is valid"""
        issues = []
        warnings = []
        
        # Check required fields
        required_fields = [
            'platform', 'sentiment_score', 'sentiment_label',
            'toxicity_score', 'emotion_type'
        ]
        
        for field in required_fields:
            if field not in input_data or input_data[field] is None:
                issues.append(f"Missing required field: {field}")
        
        # Check value ranges
        if 'sentiment_score' in input_data:
            score = input_data['sentiment_score']
            if not (-1.0 <= score <= 1.0):
                issues.append(f"Sentiment score out of range: {score}")
        
        if 'toxicity_score' in input_data:
            score = input_data['toxicity_score']
            if not (0.0 <= score <= 1.0):
                issues.append(f"Toxicity score out of range: {score}")
        
        # Check for suspicious patterns
        if 'sentiment_score' in input_data and 'toxicity_score' in input_data:
            if input_data['sentiment_score'] > 0.9 and input_data['toxicity_score'] > 0.7:
                warnings.append("High toxicity with high positive sentiment (unusual)")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def detect_anomalies(prediction, historical_stats):
        """Detect if prediction is anomalous compared to history"""
        if not historical_stats:
            return None
        
        mean = historical_stats['avg_engagement']
        std = historical_stats['std_engagement']
        
        # Z-score calculation
        z_score = (prediction - mean) / (std + 1e-8)
        
        anomaly = {
            'is_anomaly': abs(z_score) > 3,  # 3 standard deviations
            'z_score': float(z_score),
            'deviation_from_mean': float(prediction - mean),
            'severity': (
                'critical' if abs(z_score) > 4 else (
                    'high' if abs(z_score) > 3 else (
                        'moderate' if abs(z_score) > 2 else 'normal'
                    )
                )
            )
        }
        
        return anomaly


class PerformanceMonitor:
    """Monitor system performance"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.predictions_count = 0
    
    def log_prediction(self, processing_time_ms):
        """Log a prediction with its processing time"""
        self.predictions_count += 1
        logger.info(f"Prediction logged - Time: {processing_time_ms:.2f}ms")
    
    def get_performance_metrics(self):
        """Get performance metrics"""
        uptime = datetime.now() - self.start_time
        uptime_seconds = uptime.total_seconds()
        
        predictions_per_second = (
            self.predictions_count / uptime_seconds if uptime_seconds > 0 else 0
        )
        
        return {
            'uptime_seconds': uptime_seconds,
            'uptime_minutes': uptime_seconds / 60,
            'uptime_hours': uptime_seconds / 3600,
            'total_predictions': self.predictions_count,
            'predictions_per_second': predictions_per_second,
            'average_processing_time_ms': 50.0,  # Placeholder
            'status': 'healthy' if predictions_per_second > 0 else 'idle'
        }


class AlertManager:
    """Manage alerts and notifications"""
    
    def __init__(self):
        self.alerts = []
    
    def check_thresholds(self, model_health, data_quality):
        """Check if any thresholds are exceeded"""
        alerts = []
        
        # Health score alert
        if model_health and model_health['health_score'] < 40:
            alerts.append({
                'type': 'performance',
                'severity': 'high',
                'message': f"Model health score is low: {model_health['health_score']:.1f}",
                'timestamp': datetime.now().isoformat()
            })
        
        # Data quality alert
        if data_quality and len(data_quality.get('issues', [])) > 0:
            alerts.append({
                'type': 'data_quality',
                'severity': 'critical',
                'message': f"Data quality issues detected: {', '.join(data_quality['issues'])}",
                'timestamp': datetime.now().isoformat()
            })
        
        self.alerts.extend(alerts)
        return alerts
    
    def get_recent_alerts(self, limit=10):
        """Get recent alerts"""
        return self.alerts[-limit:]


if __name__ == '__main__':
    print("=" * 80)
    print("📊 MONITORING SYSTEM TEST")
    print("=" * 80)
    
    # Initialize monitors
    pred_monitor = PredictionMonitor()
    data_quality = DataQualityMonitor()
    perf_monitor = PerformanceMonitor()
    alert_mgr = AlertManager()
    
    print("\n✅ Monitoring system initialized")
    print("   - Prediction Monitor")
    print("   - Data Quality Monitor")
    print("   - Performance Monitor")
    print("   - Alert Manager")
    
    # Test data quality check
    test_input = {
        'platform': 'Instagram',
        'sentiment_score': 0.8,
        'sentiment_label': 'Positive',
        'toxicity_score': 0.1,
        'emotion_type': 'Joy'
    }
    
    print("\n🔍 Data Quality Check:")
    quality = data_quality.check_input_validity(test_input)
    print(f"   Valid: {quality['is_valid']}")
    
    print("\n✅ Monitoring test complete!")
    print("=" * 80)
