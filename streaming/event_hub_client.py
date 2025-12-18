"""
Azure Event Hub Client
Real-time streaming of predictions and events
"""

from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub.exceptions import EventHubError
import json
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class EventHubStreamer:
    """
    Streams events to Azure Event Hub for real-time processing
    """
    
    def __init__(self, connection_string=None, event_hub_name=None):
        """
        Initialize Event Hub client
        
        Args:
            connection_string: Event Hub connection string
            event_hub_name: Name of the Event Hub
        """
        self.connection_string = connection_string or os.getenv("EVENT_HUB_CONNECTION_STRING")
        self.event_hub_name = event_hub_name or os.getenv("EVENT_HUB_NAME", "predictions-stream")
        
        self.client = None
        self.enabled = False
        
        if self.connection_string:
            try:
                self.client = EventHubProducerClient.from_connection_string(
                    conn_str=self.connection_string,
                    eventhub_name=self.event_hub_name
                )
                self.enabled = True
                logger.info(f"✅ Event Hub client initialized: {self.event_hub_name}")
            except Exception as e:
                logger.warning(f"⚠️ Event Hub not available: {e}")
                self.enabled = False
        else:
            logger.info("ℹ️ Event Hub streaming disabled (no connection string)")
    
    def send_prediction_event(self, prediction_data):
        """
        Send prediction event to Event Hub
        
        Args:
            prediction_data: Dictionary containing prediction details
        """
        if not self.enabled:
            logger.debug("Event Hub streaming disabled, skipping event")
            return False
        
        try:
            event_data = {
                "event_type": "prediction",
                "timestamp": datetime.now().isoformat(),
                "data": prediction_data
            }
            
            event = EventData(json.dumps(event_data))
            
            with self.client:
                event_batch = self.client.create_batch()
                event_batch.add(event)
                self.client.send_batch(event_batch)
            
            logger.info(f"📤 Prediction event sent to Event Hub")
            return True
            
        except EventHubError as e:
            logger.error(f"❌ Failed to send event to Event Hub: {e}")
            return False
    
    def send_model_update_event(self, model_info):
        """
        Send model update event
        
        Args:
            model_info: Dictionary containing model update details
        """
        if not self.enabled:
            return False
        
        try:
            event_data = {
                "event_type": "model_update",
                "timestamp": datetime.now().isoformat(),
                "data": model_info
            }
            
            event = EventData(json.dumps(event_data))
            
            with self.client:
                event_batch = self.client.create_batch()
                event_batch.add(event)
                self.client.send_batch(event_batch)
            
            logger.info(f"📤 Model update event sent to Event Hub")
            return True
            
        except EventHubError as e:
            logger.error(f"❌ Failed to send model update event: {e}")
            return False
    
    def send_alert_event(self, alert_data):
        """
        Send alert event for monitoring
        
        Args:
            alert_data: Dictionary containing alert details
        """
        if not self.enabled:
            return False
        
        try:
            event_data = {
                "event_type": "alert",
                "timestamp": datetime.now().isoformat(),
                "severity": alert_data.get("severity", "info"),
                "data": alert_data
            }
            
            event = EventData(json.dumps(event_data))
            
            with self.client:
                event_batch = self.client.create_batch()
                event_batch.add(event)
                self.client.send_batch(event_batch)
            
            logger.info(f"📤 Alert event sent to Event Hub: {alert_data.get('severity')}")
            return True
            
        except EventHubError as e:
            logger.error(f"❌ Failed to send alert event: {e}")
            return False
    
    def close(self):
        """Close Event Hub client"""
        if self.client:
            self.client.close()
            logger.info("Event Hub client closed")

# Global instance
_event_hub_streamer = None

def get_event_hub_streamer():
    """Get singleton Event Hub streamer instance"""
    global _event_hub_streamer
    if _event_hub_streamer is None:
        _event_hub_streamer = EventHubStreamer()
    return _event_hub_streamer

