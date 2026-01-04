"""
Azure Key Vault Integration for Lab7 Security Requirements
Stores and retrieves secrets securely using Azure Key Vault
"""

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv

load_dotenv()

# Key Vault configuration
KEY_VAULT_NAME = "kv-social-ml-7487"
KEY_VAULT_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

class KeyVaultManager:
    """Manages secrets in Azure Key Vault"""
    
    def __init__(self):
        """Initialize Key Vault client with Azure credentials"""
        try:
            # Use DefaultAzureCredential (works with Azure CLI, Managed Identity, etc.)
            credential = DefaultAzureCredential()
            self.client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
            print(f"✅ Connected to Key Vault: {KEY_VAULT_NAME}")
        except Exception as e:
            print(f"⚠️ Could not connect to Key Vault: {e}")
            print("💡 Make sure you're logged in with: az login")
            self.client = None
    
    def get_secret(self, secret_name):
        """Retrieve a secret from Key Vault"""
        if not self.client:
            return None
        
        try:
            secret = self.client.get_secret(secret_name)
            print(f"✅ Retrieved secret: {secret_name}")
            return secret.value
        except Exception as e:
            print(f"⚠️ Could not retrieve secret '{secret_name}': {e}")
            return None
    
    def set_secret(self, secret_name, secret_value):
        """Store a secret in Key Vault"""
        if not self.client:
            return False
        
        try:
            self.client.set_secret(secret_name, secret_value)
            print(f"✅ Stored secret: {secret_name}")
            return True
        except Exception as e:
            print(f"❌ Could not store secret '{secret_name}': {e}")
            return False
    
    def get_storage_connection_string(self):
        """Get Azure Storage connection string from Key Vault"""
        # Try Key Vault first
        connection_string = self.get_secret("AZURE-STORAGE-CONNECTION-STRING")
        
        # Fallback to environment variable
        if not connection_string:
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if connection_string:
                print("⚠️ Using connection string from environment variable")
        
        return connection_string


def setup_key_vault_secrets():
    """
    Setup script to store secrets in Key Vault
    Run this once to migrate secrets from .env to Key Vault
    """
    print("\n🔐 Azure Key Vault Setup for Lab7 Security")
    print("=" * 50)
    
    # Load from .env file
    load_dotenv()
    
    manager = KeyVaultManager()
    
    if not manager.client:
        print("\n❌ Cannot proceed without Key Vault access")
        print("💡 Run: az login")
        print("💡 Then run this script again")
        return False
    
    # Get connection string from .env
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    
    if not connection_string:
        print("\n⚠️ No AZURE_STORAGE_CONNECTION_STRING found in .env file")
        print("💡 Add it to .env first, then run this script")
        return False
    
    print(f"\n📤 Uploading secrets to Key Vault: {KEY_VAULT_NAME}")
    
    # Store in Key Vault (note: Key Vault secret names use hyphens, not underscores)
    success = manager.set_secret("AZURE-STORAGE-CONNECTION-STRING", connection_string)
    
    if success:
        print("\n✅ Secrets successfully stored in Key Vault!")
        print("\n🎯 Security Criteria Met:")
        print("   ✅ Secrets encrypted with Azure Key Vault")
        print("   ✅ No hardcoded credentials in code")
        print("   ✅ Secure secret retrieval with Azure Identity")
        print("\n💡 You can now remove secrets from .env file")
        print("💡 The app will fetch them from Key Vault automatically")
        return True
    else:
        print("\n❌ Failed to store secrets in Key Vault")
        return False


if __name__ == "__main__":
    # Run setup
    setup_key_vault_secrets()
