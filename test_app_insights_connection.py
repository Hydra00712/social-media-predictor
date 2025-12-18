"""
Test Application Insights Connection
This script sends test data to Application Insights to verify it's working
"""

from azure_monitoring import AzureMonitoring
import time

print("=" * 80)
print("🧪 TESTING APPLICATION INSIGHTS CONNECTION")
print("=" * 80)
print()

# Initialize monitoring
print("1️⃣ Initializing Azure Monitoring...")
monitoring = AzureMonitoring()
print()

# Test 1: Send a custom event
print("2️⃣ Sending custom event to Application Insights...")
try:
    monitoring.telemetry_client.track_event('TestEvent', {
        'test_type': 'connection_test',
        'status': 'testing',
        'source': 'test_script'
    })
    monitoring.telemetry_client.flush()
    print("✅ Custom event sent!")
except Exception as e:
    print(f"❌ Failed to send event: {e}")
print()

# Test 2: Send a custom metric
print("3️⃣ Sending custom metric to Application Insights...")
try:
    monitoring.telemetry_client.track_metric('test_metric', 42.5)
    monitoring.telemetry_client.flush()
    print("✅ Custom metric sent!")
except Exception as e:
    print(f"❌ Failed to send metric: {e}")
print()

# Test 3: Send a trace
print("4️⃣ Sending trace to Application Insights...")
try:
    monitoring.telemetry_client.track_trace('This is a test trace message', properties={
        'test_id': '12345',
        'environment': 'test'
    })
    monitoring.telemetry_client.flush()
    print("✅ Trace sent!")
except Exception as e:
    print(f"❌ Failed to send trace: {e}")
print()

# Test 4: Log a prediction (using the monitoring method)
print("5️⃣ Logging a test prediction...")
try:
    test_input = {
        'platform': 'Instagram',
        'topic_category': 'Technology',
        'sentiment_score': 0.8
    }
    
    monitoring.log_prediction(
        input_data=test_input,
        prediction=3.5,
        confidence=0.85
    )
    print("✅ Prediction logged!")
except Exception as e:
    print(f"❌ Failed to log prediction: {e}")
print()

# Test 5: Log a metric
print("6️⃣ Logging a test metric...")
try:
    monitoring.log_metric('test_engagement_score', 4.2, tags={'platform': 'Twitter'})
    print("✅ Metric logged!")
except Exception as e:
    print(f"❌ Failed to log metric: {e}")
print()

# Test 6: Log an error
print("7️⃣ Logging a test error...")
try:
    monitoring.log_error('This is a test error', context={'test': True})
    print("✅ Error logged!")
except Exception as e:
    print(f"❌ Failed to log error: {e}")
print()

# Wait for data to be sent
print("⏳ Waiting 5 seconds for data to be sent to Application Insights...")
time.sleep(5)
print()

print("=" * 80)
print("✅ TEST COMPLETE!")
print("=" * 80)
print()
print("📊 Now check Application Insights in Azure Portal:")
print()
print("1. Go to: https://portal.azure.com")
print("2. Search for: mlwsociainsightsf7431d22")
print("3. Click on 'Journaux' (Logs)")
print("4. Run this query:")
print()
print("   traces")
print("   | where timestamp > ago(10m)")
print("   | order by timestamp desc")
print()
print("5. You should see the test data!")
print()
print("Alternative queries:")
print()
print("   # See custom events")
print("   customEvents")
print("   | where timestamp > ago(10m)")
print("   | order by timestamp desc")
print()
print("   # See custom metrics")
print("   customMetrics")
print("   | where timestamp > ago(10m)")
print("   | order by timestamp desc")
print()
print("=" * 80)

