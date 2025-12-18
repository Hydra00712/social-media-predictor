#!/bin/bash

# Azure Setup Script for Security & Streaming
# This script creates Azure resources for the project

set -e

# Configuration
RESOURCE_GROUP="rg-social-media-ml"
LOCATION="francecentral"
SUBSCRIPTION_ID="10ceef72-c9cd-4fb6-844b-ee8661d294fc"

# Resource names
KEY_VAULT_NAME="kv-socialmedia-ml"
EVENT_HUB_NAMESPACE="eh-socialmedia-ml"
EVENT_HUB_NAME="predictions-stream"
APP_INSIGHTS_NAME="appi-socialmedia-ml"

echo "🚀 Starting Azure Resource Deployment..."
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"
echo ""

# Set subscription
az account set --subscription $SUBSCRIPTION_ID

# 1. Create Azure Key Vault (FREE TIER)
echo "📦 Creating Azure Key Vault..."
az keyvault create \
  --name $KEY_VAULT_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku standard \
  --enable-rbac-authorization false \
  --enabled-for-deployment true \
  --enabled-for-template-deployment true

echo "✅ Key Vault created: $KEY_VAULT_NAME"

# 2. Store secrets in Key Vault
echo "🔐 Storing secrets in Key Vault..."

# Get storage account connection string
STORAGE_CONN_STRING=$(az storage account show-connection-string \
  --name stsocialmediajkvqol \
  --resource-group $RESOURCE_GROUP \
  --query connectionString -o tsv)

# Store in Key Vault
az keyvault secret set \
  --vault-name $KEY_VAULT_NAME \
  --name "azure-storage-connection-string" \
  --value "$STORAGE_CONN_STRING"

echo "✅ Secrets stored in Key Vault"

# 3. Create Event Hub Namespace (BASIC TIER - cheapest)
echo "📡 Creating Event Hub Namespace..."
az eventhubs namespace create \
  --name $EVENT_HUB_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Basic \
  --capacity 1

echo "✅ Event Hub Namespace created: $EVENT_HUB_NAMESPACE"

# 4. Create Event Hub
echo "📡 Creating Event Hub..."
az eventhubs eventhub create \
  --name $EVENT_HUB_NAME \
  --namespace-name $EVENT_HUB_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --partition-count 2 \
  --message-retention 1

echo "✅ Event Hub created: $EVENT_HUB_NAME"

# 5. Get Event Hub connection string
echo "🔑 Getting Event Hub connection string..."
EVENT_HUB_CONN_STRING=$(az eventhubs namespace authorization-rule keys list \
  --resource-group $RESOURCE_GROUP \
  --namespace-name $EVENT_HUB_NAMESPACE \
  --name RootManageSharedAccessKey \
  --query primaryConnectionString -o tsv)

# Store in Key Vault
az keyvault secret set \
  --vault-name $KEY_VAULT_NAME \
  --name "event-hub-connection-string" \
  --value "$EVENT_HUB_CONN_STRING"

echo "✅ Event Hub connection string stored in Key Vault"

# 6. Create Application Insights (FREE TIER)
echo "📊 Creating Application Insights..."
az monitor app-insights component create \
  --app $APP_INSIGHTS_NAME \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --application-type web

echo "✅ Application Insights created: $APP_INSIGHTS_NAME"

# 7. Get Application Insights instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app $APP_INSIGHTS_NAME \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Store in Key Vault
az keyvault secret set \
  --vault-name $KEY_VAULT_NAME \
  --name "app-insights-key" \
  --value "$INSTRUMENTATION_KEY"

echo "✅ Application Insights key stored in Key Vault"

# 8. Configure RBAC for current user
echo "🔐 Configuring RBAC..."
CURRENT_USER=$(az ad signed-in-user show --query id -o tsv)

az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee $CURRENT_USER \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT_NAME"

echo "✅ RBAC configured"

# 9. Update azure_config.json
echo "📝 Updating configuration..."
cat > azure_config_updated.json <<EOF
{
  "subscription_id": "$SUBSCRIPTION_ID",
  "subscription_name": "Azure for Students",
  "tenant_id": "78ddbe5d-b682-466c-bad0-6ffbaf7ceb2d",
  "resource_group": "$RESOURCE_GROUP",
  "location": "$LOCATION",
  "storage_account": "stsocialmediajkvqol",
  "key_vault": {
    "name": "$KEY_VAULT_NAME",
    "url": "https://$KEY_VAULT_NAME.vault.azure.net/"
  },
  "event_hub": {
    "namespace": "$EVENT_HUB_NAMESPACE",
    "name": "$EVENT_HUB_NAME"
  },
  "app_insights": {
    "name": "$APP_INSIGHTS_NAME",
    "instrumentation_key": "$INSTRUMENTATION_KEY"
  },
  "containers": {
    "models": "models",
    "data": "data",
    "logs": "logs",
    "experiments": "experiments"
  },
  "ml_workspace": {
    "workspace_name": "mlw-social-media",
    "compute_instance": "ci-social-media",
    "compute_cluster": "cpu-cluster",
    "workspace_id": "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/mlw-social-media",
    "location": "$LOCATION"
  }
}
EOF

echo ""
echo "✅ ✅ ✅ DEPLOYMENT COMPLETE! ✅ ✅ ✅"
echo ""
echo "📋 Resources Created:"
echo "  - Key Vault: $KEY_VAULT_NAME"
echo "  - Event Hub Namespace: $EVENT_HUB_NAMESPACE"
echo "  - Event Hub: $EVENT_HUB_NAME"
echo "  - Application Insights: $APP_INSIGHTS_NAME"
echo ""
echo "🔐 Security Features:"
echo "  ✅ Azure Key Vault for secrets management"
echo "  ✅ RBAC configured for access control"
echo "  ✅ Connection strings stored securely"
echo ""
echo "📡 Streaming Features:"
echo "  ✅ Event Hub for real-time data streaming"
echo "  ✅ Application Insights for monitoring"
echo ""
echo "📝 Configuration saved to: azure_config_updated.json"

