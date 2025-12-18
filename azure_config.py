"""
Azure Configuration
This file stores Azure resource names and settings
"""

# Azure Resource Configuration
AZURE_CONFIG = {
    # Resource Group
    'resource_group': 'rg-social-media-ml',
    'location': 'eastus',  # Change if needed: westeurope, westus2, etc.
    
    # Azure ML Workspace
    'workspace_name': 'mlw-social-media',
    
    # Storage Account
    'storage_account': 'stsocialmediaml',  # Must be globally unique, lowercase, no hyphens
    
    # Container Registry (for Docker images)
    'container_registry': 'acrsocialmediaml',  # Must be globally unique, lowercase, no hyphens
    
    # App Insights (for monitoring)
    'app_insights': 'appi-social-media-ml',
    
    # Key Vault (for secrets)
    'key_vault': 'kv-social-media-ml',  # Must be globally unique
    
    # Cosmos DB (database)
    'cosmos_account': 'cosmos-social-media-ml',  # Must be globally unique
    'cosmos_database': 'social_media_db',
    
    # App Service (for API)
    'app_service_plan': 'asp-social-media-ml',
    'web_app_api': 'app-social-media-api',  # Must be globally unique
    'web_app_ui': 'app-social-media-ui',  # Must be globally unique
    
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
SUBSCRIPTION_ID = None

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

