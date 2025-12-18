"""
Real-time Prediction Processor
Processes streaming predictions and sends to Event Hub
"""

import logging
from datetime import datetime
import json
from streaming.event_hub_client import get_event_hub_streamer

logger = logging.getLogger(__name__)

class RealtimeProcessor:
    """
    Processes predictions in real-time and streams to Event Hub
    """
    
    def __init__(self):
        self.event_hub = get_event_hub_streamer()
        self.prediction_count = 0
        self.start_time = datetime.now()
    
    def process_prediction(self, input_data, prediction, model_info=None):
        """
        Process a prediction in real-time
        
        Args:
            input_data: Input features used for prediction
            prediction: Model prediction result
            model_info: Optional model metadata
            
        Returns:
            Processing result dictionary
        """
        self.prediction_count += 1
        
        # Create prediction event
        prediction_event = {
            "prediction_id": f"pred_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "prediction": float(prediction),
            "model": model_info or {"name": "engagement_model"},
            "processing_time_ms": 0  # Can be calculated if needed
        }
        
        # Stream to Event Hub
        if self.event_hub.enabled:
            success = self.event_hub.send_prediction_event(prediction_event)
            if success:
                logger.info(f"✅ Prediction #{self.prediction_count} streamed to Event Hub")
        
        # Check for anomalies or alerts
        self._check_for_alerts(prediction_event)
        
        return {
            "status": "processed",
            "prediction_id": prediction_event["prediction_id"],
            "streamed": self.event_hub.enabled,
            "count": self.prediction_count
        }
    
    def _check_for_alerts(self, prediction_event):
        """
        Check prediction for anomalies and send alerts
        
        Args:
            prediction_event: Prediction event data
        """
        prediction_value = prediction_event["prediction"]
        
        # Alert if prediction is unusually high
        if prediction_value > 0.9:
            alert_data = {
                "severity": "info",
                "message": "High engagement prediction detected",
                "prediction_id": prediction_event["prediction_id"],
                "value": prediction_value
            }
            self.event_hub.send_alert_event(alert_data)
            logger.info(f"📢 Alert sent: High engagement ({prediction_value:.2f})")
        
        # Alert if prediction is unusually low
        elif prediction_value < 0.1:
            alert_data = {
                "severity": "warning",
                "message": "Low engagement prediction detected",
                "prediction_id": prediction_event["prediction_id"],
                "value": prediction_value
            }
            self.event_hub.send_alert_event(alert_data)
            logger.warning(f"⚠️ Alert sent: Low engagement ({prediction_value:.2f})")
    
    def get_stats(self):
        """
        Get real-time processing statistics
        
        Returns:
            Dictionary with processing stats
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "total_predictions": self.prediction_count,
            "uptime_seconds": uptime,
            "predictions_per_minute": (self.prediction_count / uptime * 60) if uptime > 0 else 0,
            "streaming_enabled": self.event_hub.enabled,
            "start_time": self.start_time.isoformat()
        }
    
    def send_model_update(self, model_name, metrics):
        """
        Send model update event when model is retrained
        
        Args:
            model_name: Name of the updated model
            metrics: Model performance metrics
        """
        model_info = {
            "model_name": model_name,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "version": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        if self.event_hub.enabled:
            success = self.event_hub.send_model_update_event(model_info)
            if success:
                logger.info(f"✅ Model update event sent: {model_name}")
        
        return model_info

# Global instance
_realtime_processor = None

def get_realtime_processor():
    """Get singleton realtime processor instance"""
    global _realtime_processor
    if _realtime_processor is None:
        _realtime_processor = RealtimeProcessor()
    return _realtime_processor

