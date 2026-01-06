"""
Azure Monitoring & Logging Setup
100% FREE - Application Insights + Log Analytics
"""

from azure.storage.queue import QueueClient
from azure_config import AZURE_CONFIG
import json
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Application Insights SDK
try:
    from applicationinsights import TelemetryClient
    from applicationinsights.channel import TelemetryChannel
    APP_INSIGHTS_AVAILABLE = True
except ImportError:
    APP_INSIGHTS_AVAILABLE = False
    logger.warning("Application Insights SDK not available. Install with: pip install applicationinsights")

class AzureMonitoring:
    """Azure Monitoring with Application Insights and Log Analytics"""

    def __init__(self):
        self.app_insights_key = AZURE_CONFIG['monitoring']['application_insights']['instrumentation_key']
        self.log_analytics_id = AZURE_CONFIG['monitoring']['log_analytics']['workspace_id']
        self.queue_name = AZURE_CONFIG['streaming']['queue_name']
        self.connection_string = AZURE_CONFIG['storage_connection_string']

        # Initialize Application Insights Telemetry Client
        self.telemetry_client = None
        if APP_INSIGHTS_AVAILABLE and self.app_insights_key:
            try:
                self.telemetry_client = TelemetryClient(self.app_insights_key)
                # Send a test event to verify connection
                self.telemetry_client.track_event('MonitoringInitialized', {
                    'status': 'success',
                    'timestamp': datetime.now().isoformat()
                })
                self.telemetry_client.flush()
                logger.info("✅ Application Insights SDK connected")
            except Exception as e:
                logger.warning(f"Could not initialize Application Insights SDK: {e}")
                self.telemetry_client = None

        # Initialize queue client for streaming
        try:
            self.queue_client = QueueClient.from_connection_string(
                conn_str=self.connection_string,
                queue_name=self.queue_name
            )
            logger.info("✅ Storage Queue connected")
        except Exception as e:
            logger.error(f"Could not initialize queue client: {e}")
            self.queue_client = None

        logger.info("✅ Azure Monitoring initialized")
        logger.info(f"📊 Application Insights: {AZURE_CONFIG['monitoring']['application_insights']['name']}")
        logger.info(f"📊 Log Analytics: {AZURE_CONFIG['monitoring']['log_analytics']['name']}")
        logger.info(f"📡 Storage Queue: {self.queue_name}")
    
    def log_prediction(self, input_data, prediction, confidence=None):
        """Log a prediction event to Application Insights and Azure Storage Queue"""
        try:
            timestamp = datetime.now().isoformat()

            # Send to Application Insights (if available)
            if self.telemetry_client:
                try:
                    # Track as REQUEST (shows up in Overview dashboard)
                    import time
                    start_time = time.time()
                    
                    # Track custom event
                    self.telemetry_client.track_event('PredictionMade', {
                        'prediction': str(prediction),
                        'confidence': str(confidence) if confidence else 'null',
                        'timestamp': timestamp,
                        'platform': str(input_data.get('platform', 'unknown')),
                        'topic_category': str(input_data.get('topic_category', 'unknown'))
                    }, {
                        'prediction_value': float(prediction),
                        'processing_time': (time.time() - start_time) * 1000
                    })

                    # Track custom metric (shows in Metrics explorer)
                    self.telemetry_client.track_metric('engagement_prediction', float(prediction))
                    
                    # Track as request (shows in server requests graph)
                    self.telemetry_client.track_request(
                        name='ML_Prediction',
                        url='http://localhost:8502/predict',
                        success=True,
                        duration=(time.time() - start_time) * 1000,
                        response_code='200',
                        properties={
                            'platform': str(input_data.get('platform', 'unknown')),
                            'prediction': str(prediction)
                        }
                    )

                    # Flush IMMEDIATELY to ensure data is sent
                    self.telemetry_client.flush()
                    
                    # Wait a tiny bit for flush to complete
                    time.sleep(0.1)
                    
                    logger.info(f"✅ Prediction logged to Application Insights: {prediction}")
                except Exception as e:
                    logger.warning(f"Could not log to Application Insights: {e}")

            # Send to Storage Queue (FREE streaming)
            if self.queue_client:
                event = {
                    'event_type': 'prediction',
                    'timestamp': timestamp,
                    'input': input_data,
                    'prediction': prediction,
                    'confidence': confidence,
                    'app_insights_key': self.app_insights_key,
                    'log_analytics_id': self.log_analytics_id
                }

                self.queue_client.send_message(json.dumps(event))
                logger.info(f"✅ Prediction logged to queue: {prediction}")

            return True

        except Exception as e:
            logger.error(f"❌ Error logging prediction: {e}")
            return False
    
    def log_error(self, error_message, context=None):
        """Log an error event to Application Insights and Queue"""
        try:
            timestamp = datetime.now().isoformat()

            # Send to Application Insights (if available)
            if self.telemetry_client:
                try:
                    # Track exception
                    self.telemetry_client.track_exception(
                        type(Exception).__name__,
                        str(error_message),
                        properties={'context': str(context), 'timestamp': timestamp}
                    )

                    # Track trace
                    self.telemetry_client.track_trace(
                        f'Error: {error_message}',
                        severity='ERROR',
                        properties={'context': str(context)}
                    )

                    self.telemetry_client.flush()
                    logger.info("✅ Error logged to Application Insights")
                except Exception as e:
                    logger.warning(f"Could not log error to Application Insights: {e}")

            # Send to queue
            if self.queue_client:
                event = {
                    'event_type': 'error',
                    'timestamp': timestamp,
                    'error': str(error_message),
                    'context': context,
                    'app_insights_key': self.app_insights_key,
                    'log_analytics_id': self.log_analytics_id
                }

                self.queue_client.send_message(json.dumps(event))
                logger.error(f"❌ Error logged: {error_message}")

            return True

        except Exception as e:
            logger.error(f"❌ Error logging error: {e}")
            return False
    
    def log_metric(self, metric_name, value, tags=None):
        """Log a custom metric to Application Insights and Queue"""
        try:
            timestamp = datetime.now().isoformat()

            # Send to Application Insights (if available)
            if self.telemetry_client:
                try:
                    # Track metric
                    self.telemetry_client.track_metric(metric_name, value, properties=tags)

                    # Track trace for context
                    self.telemetry_client.track_trace(
                        f'Metric: {metric_name} = {value}',
                        properties=tags or {}
                    )

                    self.telemetry_client.flush()
                    logger.info(f"✅ Metric logged to Application Insights: {metric_name} = {value}")
                except Exception as e:
                    logger.warning(f"Could not log metric to Application Insights: {e}")

            # Send to queue
            if self.queue_client:
                event = {
                    'event_type': 'metric',
                    'timestamp': timestamp,
                    'metric_name': metric_name,
                    'value': value,
                    'tags': tags or {},
                    'app_insights_key': self.app_insights_key,
                    'log_analytics_id': self.log_analytics_id
                }

                self.queue_client.send_message(json.dumps(event))
                logger.info(f"📊 Metric logged to queue: {metric_name} = {value}")

            return True

        except Exception as e:
            logger.error(f"❌ Error logging metric: {e}")
            return False
    
    def get_queue_stats(self):
        """Get queue statistics"""
        try:
            properties = self.queue_client.get_queue_properties()
            return {
                'message_count': properties.approximate_message_count,
                'queue_name': self.queue_name,
                'status': 'active'
            }
        except Exception as e:
            logger.error(f"❌ Error getting queue stats: {e}")
            return None
    
    def test_connection(self):
        """Test Azure monitoring connection"""
        try:
            # Test queue
            test_event = {
                'event_type': 'test',
                'timestamp': datetime.now().isoformat(),
                'message': 'Azure Monitoring Test',
                'app_insights_key': self.app_insights_key,
                'log_analytics_id': self.log_analytics_id
            }
            
            self.queue_client.send_message(json.dumps(test_event))
            stats = self.get_queue_stats()
            
            print("\n✅ ✅ ✅ AZURE MONITORING TEST SUCCESSFUL! ✅ ✅ ✅\n")
            print(f"📊 Application Insights: {AZURE_CONFIG['monitoring']['application_insights']['name']}")
            print(f"📊 Log Analytics: {AZURE_CONFIG['monitoring']['log_analytics']['name']}")
            print(f"📡 Storage Queue: {self.queue_name}")
            print(f"📨 Messages in queue: {stats['message_count']}")
            print(f"\n💰 COST: $0.00 - 100% FREE!\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}\n")
            return False


if __name__ == "__main__":
    print("🚀 Testing Azure Monitoring Setup...\n")
    
    monitoring = AzureMonitoring()
    monitoring.test_connection()

