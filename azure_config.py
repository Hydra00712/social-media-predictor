"""
Azure Configuration
This file stores Azure resource names and settings
"""

import os

# Azure Resource Configuration
AZURE_CONFIG = {
    # Subscription & Resource Group
    'subscription_id': '10ceef72-c9cd-4fb6-844b-ee8661d294fc',
    'subscription_name': 'Azure for Students',
    'tenant_id': '78ddbe5d-b682-466c-bad0-6ffbaf7ceb2d',
    'resource_group': 'rg-social-media-ml',
    'location': 'francecentral',

    # Azure ML Workspace
    'workspace_name': 'mlw-social-media',

    # Storage Account
    'storage_account': 'stsocialmediajkvqol',
    'storage_connection_string': os.getenv('AZURE_STORAGE_CONNECTION_STRING', 'YOUR_STORAGE_CONNECTION_STRING_HERE'),

    # Streaming (FREE - Storage Queue)
    'streaming': {
        'queue_name': 'predictions-queue',
        'enabled': True,
        'type': 'storage_queue'
    },

    # Event Hub
    'event_hub': {
        'namespace': 'evhnssocialml669',
        'name': 'predictions-hub',
        'connection_string': os.getenv('AZURE_EVENTHUB_CONNECTION_STRING', 'YOUR_EVENTHUB_CONNECTION_STRING_HERE')
    },

    # Monitoring (FREE)
    'monitoring': {
        'application_insights': {
            'name': 'mlwsocialnsightsf7431d22',
            'instrumentation_key': '07a147a2-326a-4751-b3ce-e59bdc2318b3'
        },
        'log_analytics': {
            'name': 'mlwsocialogalytjea9b61fd',
            'workspace_id': '9da1901d-7676-40e8-a9b0-e13f71169b7d'
        }
    },

    # Key Vault (for secrets)
    'key_vault': {
        'name': 'kv-social-ml-7487',
        'vault_url': 'https://kv-social-ml-7487.vault.azure.net/'
    },

    # Blob Storage Containers
    'blob_containers': [
        'models',
        'data',
        'logs',
        'experiments'
    ],

    # Tags
    'tags': {
        'Project': 'SocialMediaML',
        'Environment': 'Production',
        'ManagedBy': 'AzureCLI'
    }
}

# Subscription ID (will be set after login)
SUBSCRIPTION_ID = '10ceef72-c9cd-4fb6-844b-ee8661d294fc'

def get_unique_name(base_name, suffix=''):
    """Generate a unique name for Azure resources"""
    import random
    import string
    if suffix:
        return f"{base_name}{suffix}"
    else:
        # Add random suffix for uniqueness
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{base_name}{random_suffix}"

def update_storage_account_name():
    """Update storage account name to ensure uniqueness"""
    AZURE_CONFIG['storage_account'] = get_unique_name('stsocialmedia')
    AZURE_CONFIG['container_registry'] = get_unique_name('acrsocialmedia')
    AZURE_CONFIG['cosmos_account'] = get_unique_name('cosmossocialmedia')
    AZURE_CONFIG['web_app_api'] = get_unique_name('appsocialmediaapi')
    AZURE_CONFIG['web_app_ui'] = get_unique_name('appsocialmediaui')
    return AZURE_CONFIG

