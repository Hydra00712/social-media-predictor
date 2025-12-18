# Azure Setup Script for Security & Streaming (PowerShell)
# This script creates Azure resources for the project

$ErrorActionPreference = "Stop"

# Configuration
$RESOURCE_GROUP = "rg-social-media-ml"
$LOCATION = "francecentral"
$SUBSCRIPTION_ID = "10ceef72-c9cd-4fb6-844b-ee8661d294fc"

# Resource names
$KEY_VAULT_NAME = "kv-socialmedia-ml"
$EVENT_HUB_NAMESPACE = "eh-socialmedia-ml"
$EVENT_HUB_NAME = "predictions-stream"
$APP_INSIGHTS_NAME = "appi-socialmedia-ml"

Write-Host "🚀 Starting Azure Resource Deployment..." -ForegroundColor Green
Write-Host "Resource Group: $RESOURCE_GROUP"
Write-Host "Location: $LOCATION"
Write-Host ""

# Check if Azure CLI is installed
try {
    az --version | Out-Null
} catch {
    Write-Host "❌ Azure CLI not installed!" -ForegroundColor Red
    Write-Host "Install from: https://aka.ms/installazurecliwindows"
    exit 1
}

# Login and set subscription
Write-Host "🔐 Logging in to Azure..."
az login --tenant 78ddbe5d-b682-466c-bad0-6ffbaf7ceb2d
az account set --subscription $SUBSCRIPTION_ID

# 1. Create Azure Key Vault (FREE TIER)
Write-Host "📦 Creating Azure Key Vault..." -ForegroundColor Cyan
az keyvault create `
  --name $KEY_VAULT_NAME `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku standard `
  --enable-rbac-authorization false `
  --enabled-for-deployment true `
  --enabled-for-template-deployment true

Write-Host "✅ Key Vault created: $KEY_VAULT_NAME" -ForegroundColor Green

# 2. Store secrets in Key Vault
Write-Host "🔐 Storing secrets in Key Vault..." -ForegroundColor Cyan

# Get storage account connection string
$STORAGE_CONN_STRING = az storage account show-connection-string `
  --name stsocialmediajkvqol `
  --resource-group $RESOURCE_GROUP `
  --query connectionString -o tsv

# Store in Key Vault
az keyvault secret set `
  --vault-name $KEY_VAULT_NAME `
  --name "azure-storage-connection-string" `
  --value "$STORAGE_CONN_STRING"

Write-Host "✅ Secrets stored in Key Vault" -ForegroundColor Green

# 3. Create Event Hub Namespace (BASIC TIER - cheapest)
Write-Host "📡 Creating Event Hub Namespace..." -ForegroundColor Cyan
az eventhubs namespace create `
  --name $EVENT_HUB_NAMESPACE `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku Basic `
  --capacity 1

Write-Host "✅ Event Hub Namespace created: $EVENT_HUB_NAMESPACE" -ForegroundColor Green

# 4. Create Event Hub
Write-Host "📡 Creating Event Hub..." -ForegroundColor Cyan
az eventhubs eventhub create `
  --name $EVENT_HUB_NAME `
  --namespace-name $EVENT_HUB_NAMESPACE `
  --resource-group $RESOURCE_GROUP `
  --partition-count 2 `
  --message-retention 1

Write-Host "✅ Event Hub created: $EVENT_HUB_NAME" -ForegroundColor Green

# 5. Get Event Hub connection string
Write-Host "🔑 Getting Event Hub connection string..." -ForegroundColor Cyan
$EVENT_HUB_CONN_STRING = az eventhubs namespace authorization-rule keys list `
  --resource-group $RESOURCE_GROUP `
  --namespace-name $EVENT_HUB_NAMESPACE `
  --name RootManageSharedAccessKey `
  --query primaryConnectionString -o tsv

# Store in Key Vault
az keyvault secret set `
  --vault-name $KEY_VAULT_NAME `
  --name "event-hub-connection-string" `
  --value "$EVENT_HUB_CONN_STRING"

Write-Host "✅ Event Hub connection string stored in Key Vault" -ForegroundColor Green

# 6. Create Application Insights (FREE TIER)
Write-Host "📊 Creating Application Insights..." -ForegroundColor Cyan
az monitor app-insights component create `
  --app $APP_INSIGHTS_NAME `
  --location $LOCATION `
  --resource-group $RESOURCE_GROUP `
  --application-type web

Write-Host "✅ Application Insights created: $APP_INSIGHTS_NAME" -ForegroundColor Green

# 7. Get Application Insights instrumentation key
$INSTRUMENTATION_KEY = az monitor app-insights component show `
  --app $APP_INSIGHTS_NAME `
  --resource-group $RESOURCE_GROUP `
  --query instrumentationKey -o tsv

# Store in Key Vault
az keyvault secret set `
  --vault-name $KEY_VAULT_NAME `
  --name "app-insights-key" `
  --value "$INSTRUMENTATION_KEY"

Write-Host "✅ Application Insights key stored in Key Vault" -ForegroundColor Green

# 8. Configure RBAC for current user
Write-Host "🔐 Configuring RBAC..." -ForegroundColor Cyan
$CURRENT_USER = az ad signed-in-user show --query id -o tsv

az role assignment create `
  --role "Key Vault Secrets User" `
  --assignee $CURRENT_USER `
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT_NAME"

Write-Host "✅ RBAC configured" -ForegroundColor Green

# 9. Update azure_config.json
Write-Host "📝 Updating configuration..." -ForegroundColor Cyan

$config = @{
    subscription_id = $SUBSCRIPTION_ID
    subscription_name = "Azure for Students"
    tenant_id = "78ddbe5d-b682-466c-bad0-6ffbaf7ceb2d"
    resource_group = $RESOURCE_GROUP
    location = $LOCATION
    storage_account = "stsocialmediajkvqol"
    key_vault = @{
        name = $KEY_VAULT_NAME
        url = "https://$KEY_VAULT_NAME.vault.azure.net/"
    }
    event_hub = @{
        namespace = $EVENT_HUB_NAMESPACE
        name = $EVENT_HUB_NAME
    }
    app_insights = @{
        name = $APP_INSIGHTS_NAME
        instrumentation_key = $INSTRUMENTATION_KEY
    }
    containers = @{
        models = "models"
        data = "data"
        logs = "logs"
        experiments = "experiments"
    }
    ml_workspace = @{
        workspace_name = "mlw-social-media"
        compute_instance = "ci-social-media"
        compute_cluster = "cpu-cluster"
        workspace_id = "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/mlw-social-media"
        location = $LOCATION
    }
}

$config | ConvertTo-Json -Depth 10 | Out-File -FilePath "azure_config.json" -Encoding UTF8

Write-Host ""
Write-Host "✅ ✅ ✅ DEPLOYMENT COMPLETE! ✅ ✅ ✅" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Resources Created:" -ForegroundColor Yellow
Write-Host "  - Key Vault: $KEY_VAULT_NAME"
Write-Host "  - Event Hub Namespace: $EVENT_HUB_NAMESPACE"
Write-Host "  - Event Hub: $EVENT_HUB_NAME"
Write-Host "  - Application Insights: $APP_INSIGHTS_NAME"
Write-Host ""
Write-Host "🔐 Security Features:" -ForegroundColor Yellow
Write-Host "  ✅ Azure Key Vault for secrets management"
Write-Host "  ✅ RBAC configured for access control"
Write-Host "  ✅ Connection strings stored securely"
Write-Host ""
Write-Host "📡 Streaming Features:" -ForegroundColor Yellow
Write-Host "  ✅ Event Hub for real-time data streaming"
Write-Host "  ✅ Application Insights for monitoring"
Write-Host ""
Write-Host "📝 Configuration updated in: azure_config.json" -ForegroundColor Green

