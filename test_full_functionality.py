"""
COMPREHENSIVE FUNCTIONALITY TEST
Tests all Azure resources with actual operations
"""

import sys
import os
from datetime import datetime

# Fix encoding for Windows
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

print("=" * 100)
print("COMPREHENSIVE FUNCTIONALITY TEST")
print("=" * 100)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 100)
print()

results = {'passed': [], 'failed': []}

# ============================================================================
# TEST 1: BLOB STORAGE - READ/WRITE
# ============================================================================
print("1. TESTING: Blob Storage Read/Write Operations")
print("-" * 100)
try:
    from azure.storage.blob import BlobServiceClient
    from azure_config import AZURE_CONFIG
    import json
    
    connection_string = AZURE_CONFIG['storage_connection_string']
    blob_service = BlobServiceClient.from_connection_string(connection_string)
    
    # Test 1: Read model file
    container_client = blob_service.get_container_client('models')
    blob_client = container_client.get_blob_client('engagement_model.pkl')
    
    properties = blob_client.get_blob_properties()
    print(f"   [OK] READ: engagement_model.pkl ({properties.size} bytes)")

    # Test 2: Read structured data
    data_container = blob_service.get_container_client('data')
    data_blob = data_container.get_blob_client('social_media_cleaned.csv')
    data_props = data_blob.get_blob_properties()
    print(f"   [OK] READ: social_media_cleaned.csv ({data_props.size} bytes)")

    # Test 3: Write test file
    test_data = {
        "test": "functionality_test",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

    logs_container = blob_service.get_container_client('logs')
    test_blob = logs_container.get_blob_client('test_functionality.json')
    test_blob.upload_blob(json.dumps(test_data), overwrite=True)
    print(f"   [OK] WRITE: test_functionality.json uploaded")

    results['passed'].append('Blob Storage Read/Write')
    print("   [PASS] Blob Storage fully functional")
except Exception as e:
    print(f"   [FAIL] {e}")
    results['failed'].append('Blob Storage Read/Write')
print()

# ============================================================================
# TEST 2: STORAGE QUEUE - SEND/RECEIVE
# ============================================================================
print("2. TESTING: Storage Queue Send/Receive Operations")
print("-" * 100)
try:
    from azure.storage.queue import QueueClient
    
    connection_string = AZURE_CONFIG['storage_connection_string']
    queue_name = AZURE_CONFIG['streaming']['queue_name']
    
    queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    
    # Send test message
    test_message = {
        "test": "functionality_test",
        "timestamp": datetime.now().isoformat(),
        "prediction": 3.5
    }
    
    queue_client.send_message(json.dumps(test_message))
    print(f"   [OK] SEND: Test message sent to queue")

    # Peek messages
    messages = queue_client.peek_messages(max_messages=5)
    print(f"   [OK] PEEK: {len(list(messages))} messages in queue")

    results['passed'].append('Storage Queue Send/Receive')
    print("   [PASS] Storage Queue fully functional")
except Exception as e:
    print(f"   [FAIL] {e}")
    results['failed'].append('Storage Queue Send/Receive')
print()

# ============================================================================
# TEST 3: APPLICATION INSIGHTS - TELEMETRY
# ============================================================================
print("3. TESTING: Application Insights Telemetry")
print("-" * 100)
try:
    from applicationinsights import TelemetryClient
    
    instrumentation_key = AZURE_CONFIG['monitoring']['application_insights']['instrumentation_key']
    tc = TelemetryClient(instrumentation_key)
    
    # Send custom event
    tc.track_event('FunctionalityTest', {
        'test_type': 'comprehensive',
        'timestamp': datetime.now().isoformat()
    })
    
    # Send custom metric
    tc.track_metric('test_metric', 100)
    
    # Send trace
    tc.track_trace('Functionality test executed successfully')
    
    tc.flush()

    print(f"   [OK] EVENT: Custom event sent")
    print(f"   [OK] METRIC: Custom metric sent")
    print(f"   [OK] TRACE: Trace log sent")

    results['passed'].append('Application Insights Telemetry')
    print("   [PASS] Application Insights fully functional")
except Exception as e:
    print(f"   [FAIL] {e}")
    results['failed'].append('Application Insights Telemetry')
print()

# ============================================================================
# TEST 4: KEY VAULT - READ SECRETS
# ============================================================================
print("4. TESTING: Key Vault Secret Retrieval")
print("-" * 100)
try:
    from azure.keyvault.secrets import SecretClient
    from azure.identity import DefaultAzureCredential
    
    vault_url = AZURE_CONFIG['key_vault']['vault_url']
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    # Retrieve secret
    secret = client.get_secret("storage-connection-string")
    print(f"   [OK] READ: storage-connection-string retrieved")
    print(f"   [OK] Secret length: {len(secret.value)} characters")

    results['passed'].append('Key Vault Secret Retrieval')
    print("   [PASS] Key Vault fully functional")
except Exception as e:
    print(f"   [FAIL] {e}")
    results['failed'].append('Key Vault Secret Retrieval')
print()

# ============================================================================
# TEST 5: EVENT HUB - SEND EVENT
# ============================================================================
print("5. TESTING: Event Hub Send Event")
print("-" * 100)
try:
    from azure.eventhub import EventHubProducerClient, EventData
    
    connection_string = AZURE_CONFIG['event_hub']['connection_string']
    eventhub_name = AZURE_CONFIG['event_hub']['name']
    
    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_string,
        eventhub_name=eventhub_name
    )
    
    # Send test event
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(json.dumps({
        "test": "functionality_test",
        "timestamp": datetime.now().isoformat(),
        "event_type": "test_event"
    })))
    
    producer.send_batch(event_data_batch)
    producer.close()

    print(f"   [OK] SEND: Test event sent to Event Hub")

    results['passed'].append('Event Hub Send Event')
    print("   [PASS] Event Hub fully functional")
except Exception as e:
    print(f"   [FAIL] {e}")
    results['failed'].append('Event Hub Send Event')
print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 100)
print("FUNCTIONALITY TEST SUMMARY")
print("=" * 100)
print()

total = len(results['passed']) + len(results['failed'])
success_rate = (len(results['passed']) / total * 100) if total > 0 else 0

print(f"PASSED: {len(results['passed'])}/{total}")
for item in results['passed']:
    print(f"   [OK] {item}")
print()

if results['failed']:
    print(f"FAILED: {len(results['failed'])}/{total}")
    for item in results['failed']:
        print(f"   [X] {item}")
    print()

print("=" * 100)
print(f"SUCCESS RATE: {success_rate:.1f}%")
print("=" * 100)
print()

if success_rate == 100:
    print("PERFECT! All Azure resources are fully functional!")
elif success_rate >= 80:
    print("EXCELLENT! Most resources are working correctly!")
else:
    print("WARNING: Some resources need attention!")

print()
print("=" * 100)

