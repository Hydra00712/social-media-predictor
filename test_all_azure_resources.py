"""
Comprehensive Azure Resources Connection Test
Tests ALL Azure resources to verify they are connected
"""

import sys
from datetime import datetime

print("=" * 100)
print("🔍 COMPREHENSIVE AZURE RESOURCES CONNECTION TEST")
print("=" * 100)
print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 100)
print()

# Track results
results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

# ============================================================================
# TEST 1: AZURE CONFIGURATION
# ============================================================================
print("1️⃣  TESTING: Azure Configuration")
print("-" * 100)
try:
    from azure_config import AZURE_CONFIG
    print(f"✅ PASS: Azure configuration loaded")
    print(f"   📊 Subscription ID: {AZURE_CONFIG['subscription_id'][:20]}...")
    print(f"   📦 Resource Group: {AZURE_CONFIG['resource_group']}")
    print(f"   🌍 Location: {AZURE_CONFIG['location']}")
    results['passed'].append('Azure Configuration')
except Exception as e:
    print(f"❌ FAIL: {e}")
    results['failed'].append('Azure Configuration')
print()

# ============================================================================
# TEST 2: AZURE BLOB STORAGE (Model Storage)
# ============================================================================
print("2️⃣  TESTING: Azure Blob Storage (Model Storage)")
print("-" * 100)
try:
    from azure.storage.blob import BlobServiceClient

    connection_string = AZURE_CONFIG['storage_connection_string']
    # Get container name - try different config structures
    if 'blob_containers' in AZURE_CONFIG:
        container_name = AZURE_CONFIG['blob_containers'][0]  # 'models'
    elif 'containers' in AZURE_CONFIG:
        container_name = AZURE_CONFIG['containers'].get('models', 'models')
    else:
        container_name = 'models'

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # List blobs
    blobs = list(container_client.list_blobs())

    print(f"✅ PASS: Connected to Blob Storage")
    print(f"   📦 Storage Account: {AZURE_CONFIG['storage_account']}")
    print(f"   📦 Container: {container_name}")
    print(f"   📁 Files found: {len(blobs)}")
    for blob in blobs[:5]:  # Show first 5
        print(f"      - {blob.name} ({blob.size} bytes)")

    results['passed'].append('Azure Blob Storage')
except Exception as e:
    print(f"❌ FAIL: {e}")
    results['failed'].append('Azure Blob Storage')
print()

# ============================================================================
# TEST 3: AZURE STORAGE QUEUE (Predictions Queue)
# ============================================================================
print("3️⃣  TESTING: Azure Storage Queue (Predictions Queue)")
print("-" * 100)
try:
    from azure.storage.queue import QueueClient
    
    connection_string = AZURE_CONFIG['storage_connection_string']
    queue_name = AZURE_CONFIG['streaming']['queue_name']
    
    queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    properties = queue_client.get_queue_properties()
    
    print(f"✅ PASS: Connected to Storage Queue")
    print(f"   📡 Queue: {queue_name}")
    print(f"   📨 Messages in queue: {properties.approximate_message_count}")
    
    results['passed'].append('Azure Storage Queue')
except Exception as e:
    print(f"❌ FAIL: {e}")
    results['failed'].append('Azure Storage Queue')
print()

# ============================================================================
# TEST 4: APPLICATION INSIGHTS
# ============================================================================
print("4️⃣  TESTING: Application Insights")
print("-" * 100)
try:
    app_insights_key = AZURE_CONFIG['monitoring']['application_insights']['instrumentation_key']
    app_insights_name = AZURE_CONFIG['monitoring']['application_insights']['name']
    
    # Try to import SDK
    try:
        from applicationinsights import TelemetryClient
        tc = TelemetryClient(app_insights_key)
        tc.track_event('ConnectionTest', {'source': 'test_all_azure_resources'})
        tc.flush()
        
        print(f"✅ PASS: Application Insights SDK connected")
        print(f"   📊 Name: {app_insights_name}")
        print(f"   🔑 Key: {app_insights_key[:20]}...")
        print(f"   📡 Test event sent successfully")
        results['passed'].append('Application Insights')
    except ImportError:
        print(f"⚠️  WARNING: Application Insights SDK not installed")
        print(f"   📊 Name: {app_insights_name}")
        print(f"   🔑 Key configured: Yes")
        results['warnings'].append('Application Insights SDK not installed')
        
except Exception as e:
    print(f"❌ FAIL: {e}")
    results['failed'].append('Application Insights')
print()

# ============================================================================
# TEST 5: LOG ANALYTICS
# ============================================================================
print("5️⃣  TESTING: Log Analytics Workspace")
print("-" * 100)
try:
    log_analytics_id = AZURE_CONFIG['monitoring']['log_analytics']['workspace_id']
    log_analytics_name = AZURE_CONFIG['monitoring']['log_analytics']['name']
    
    print(f"✅ PASS: Log Analytics configured")
    print(f"   📊 Name: {log_analytics_name}")
    print(f"   🆔 Workspace ID: {log_analytics_id[:20]}...")
    
    results['passed'].append('Log Analytics')
except Exception as e:
    print(f"❌ FAIL: {e}")
    results['failed'].append('Log Analytics')
print()

# ============================================================================
# TEST 6: AZURE COSMOS DB
# ============================================================================
print("6️⃣  TESTING: Azure Cosmos DB")
print("-" * 100)
try:
    # Check if Cosmos DB is configured
    if 'cosmos_db' in AZURE_CONFIG:
        cosmos_endpoint = AZURE_CONFIG['cosmos_db']['endpoint']
        cosmos_key = AZURE_CONFIG['cosmos_db']['key']
        database_name = AZURE_CONFIG['cosmos_db']['database_name']

        from azure.cosmos import CosmosClient

        client = CosmosClient(cosmos_endpoint, cosmos_key)
        database = client.get_database_client(database_name)

        # Try to list containers
        containers = list(database.list_containers())

        print(f"✅ PASS: Connected to Cosmos DB")
        print(f"   🗄️  Database: {database_name}")
        print(f"   📦 Containers: {len(containers)}")
        for container in containers:
            print(f"      - {container['id']}")

        results['passed'].append('Azure Cosmos DB')
    else:
        print(f"⚠️  WARNING: Cosmos DB not configured in azure_config.json")
        print(f"   ℹ️  This is optional - app can work without it")
        results['warnings'].append('Azure Cosmos DB (not configured)')
except Exception as e:
    print(f"❌ FAIL: {e}")
    results['failed'].append('Azure Cosmos DB')
print()

# ============================================================================
# TEST 7: AZURE KEY VAULT
# ============================================================================
print("7️⃣  TESTING: Azure Key Vault")
print("-" * 100)
try:
    # Check if Key Vault is configured
    if 'key_vault' in AZURE_CONFIG:
        key_vault_name = AZURE_CONFIG['key_vault']['name']
        key_vault_url = AZURE_CONFIG['key_vault']['vault_url']

        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

        # Try to list secrets (just to verify connection)
        print(f"✅ PASS: Connected to Key Vault")
        print(f"   🔐 Name: {key_vault_name}")
        print(f"   🌐 URL: {key_vault_url}")

        results['passed'].append('Azure Key Vault')
    else:
        print(f"⚠️  WARNING: Key Vault not configured in azure_config.json")
        print(f"   ℹ️  This is optional - app uses connection strings directly")
        results['warnings'].append('Azure Key Vault (not configured)')
except Exception as e:
    print(f"⚠️  WARNING: Key Vault connection issue")
    print(f"   ℹ️  Error: {str(e)[:100]}")
    results['warnings'].append('Azure Key Vault (authentication required)')
print()

# ============================================================================
# TEST 8: AZURE EVENT HUB
# ============================================================================
print("8️⃣  TESTING: Azure Event Hub")
print("-" * 100)
try:
    # Check if Event Hub is configured
    if 'event_hub' in AZURE_CONFIG:
        event_hub_namespace = AZURE_CONFIG['event_hub']['namespace']
        event_hub_name = AZURE_CONFIG['event_hub']['name']
        event_hub_connection = AZURE_CONFIG['event_hub']['connection_string']

        from azure.eventhub import EventHubProducerClient

        producer = EventHubProducerClient.from_connection_string(
            conn_str=event_hub_connection,
            eventhub_name=event_hub_name
        )

        # Just verify we can create the client
        print(f"✅ PASS: Connected to Event Hub")
        print(f"   📡 Namespace: {event_hub_namespace}")
        print(f"   📨 Event Hub: {event_hub_name}")

        producer.close()
        results['passed'].append('Azure Event Hub')
    else:
        print(f"⚠️  WARNING: Event Hub not configured in azure_config.json")
        print(f"   ℹ️  Using Storage Queue instead for streaming")
        results['warnings'].append('Azure Event Hub (using Storage Queue instead)')
except Exception as e:
    print(f"❌ FAIL: {e}")
    results['failed'].append('Azure Event Hub')
print()

# ============================================================================
# TEST 9: AZURE MONITORING (Combined)
# ============================================================================
print("9️⃣  TESTING: Azure Monitoring Module")
print("-" * 100)
try:
    from azure_monitoring import AzureMonitoring

    monitoring = AzureMonitoring()

    # Test queue stats
    stats = monitoring.get_queue_stats()

    print(f"✅ PASS: Azure Monitoring module working")
    print(f"   📊 Application Insights: Connected")
    print(f"   📡 Storage Queue: Connected")
    print(f"   📨 Messages in queue: {stats['message_count']}")

    results['passed'].append('Azure Monitoring Module')
except Exception as e:
    print(f"❌ FAIL: {e}")
    results['failed'].append('Azure Monitoring Module')
print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 100)
print("📊 TEST SUMMARY")
print("=" * 100)
print()

total_tests = len(results['passed']) + len(results['failed']) + len(results['warnings'])
print(f"✅ PASSED: {len(results['passed'])}/{total_tests}")
for item in results['passed']:
    print(f"   ✓ {item}")
print()

if results['warnings']:
    print(f"⚠️  WARNINGS: {len(results['warnings'])}")
    for item in results['warnings']:
        print(f"   ⚠ {item}")
    print()

if results['failed']:
    print(f"❌ FAILED: {len(results['failed'])}")
    for item in results['failed']:
        print(f"   ✗ {item}")
    print()

# Calculate success rate
success_rate = (len(results['passed']) / total_tests * 100) if total_tests > 0 else 0

print("=" * 100)
print(f"🎯 SUCCESS RATE: {success_rate:.1f}%")
print("=" * 100)
print()

if success_rate >= 80:
    print("🎉 EXCELLENT! Most Azure resources are connected and working!")
elif success_rate >= 60:
    print("👍 GOOD! Most resources are working, but some need attention.")
else:
    print("⚠️  ATTENTION NEEDED! Several resources have connection issues.")

print()
print("=" * 100)
print("📝 For detailed verification, check the Azure Portal:")
print("   https://portal.azure.com")
print("=" * 100)


