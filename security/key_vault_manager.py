"""
Azure Key Vault Manager
Secure secrets management using Azure Key Vault
"""

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import logging

logger = logging.getLogger(__name__)

class KeyVaultManager:
    """
    Manages secrets using Azure Key Vault
    Provides secure access to connection strings and API keys
    """
    
    def __init__(self, vault_url=None):
        """
        Initialize Key Vault client
        
        Args:
            vault_url: Azure Key Vault URL (e.g., https://kv-social-media-ml.vault.azure.net/)
        """
        self.vault_url = vault_url or os.getenv("AZURE_KEY_VAULT_URL")
        
        if not self.vault_url:
            logger.warning("No Key Vault URL provided. Using environment variables as fallback.")
            self.client = None
        else:
            try:
                credential = DefaultAzureCredential()
                self.client = SecretClient(vault_url=self.vault_url, credential=credential)
                logger.info(f"✅ Connected to Key Vault: {self.vault_url}")
            except Exception as e:
                logger.error(f"❌ Failed to connect to Key Vault: {e}")
                self.client = None
    
    def get_secret(self, secret_name, fallback_env_var=None):
        """
        Get secret from Key Vault or environment variable
        
        Args:
            secret_name: Name of the secret in Key Vault
            fallback_env_var: Environment variable to use if Key Vault fails
            
        Returns:
            Secret value or None
        """
        # Try Key Vault first
        if self.client:
            try:
                secret = self.client.get_secret(secret_name)
                logger.info(f"✅ Retrieved secret '{secret_name}' from Key Vault")
                return secret.value
            except Exception as e:
                logger.warning(f"⚠️ Could not get secret from Key Vault: {e}")
        
        # Fallback to environment variable
        if fallback_env_var:
            value = os.getenv(fallback_env_var)
            if value:
                logger.info(f"✅ Retrieved secret from environment variable: {fallback_env_var}")
                return value
        
        logger.error(f"❌ Could not retrieve secret: {secret_name}")
        return None
    
    def set_secret(self, secret_name, secret_value):
        """
        Store secret in Key Vault
        
        Args:
            secret_name: Name of the secret
            secret_value: Value to store
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("❌ Key Vault client not initialized")
            return False
        
        try:
            self.client.set_secret(secret_name, secret_value)
            logger.info(f"✅ Secret '{secret_name}' stored in Key Vault")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to store secret: {e}")
            return False
    
    def get_storage_connection_string(self):
        """Get Azure Storage connection string"""
        return self.get_secret(
            "azure-storage-connection-string",
            fallback_env_var="AZURE_STORAGE_CONNECTION_STRING"
        )
    
    def get_cosmos_connection_string(self):
        """Get Cosmos DB connection string"""
        return self.get_secret(
            "cosmos-connection-string",
            fallback_env_var="COSMOS_CONNECTION_STRING"
        )
    
    def get_api_key(self):
        """Get API authentication key"""
        return self.get_secret(
            "api-key",
            fallback_env_var="API_KEY"
        )


# Global instance
_key_vault_manager = None

def get_key_vault_manager():
    """Get singleton Key Vault manager instance"""
    global _key_vault_manager
    if _key_vault_manager is None:
        _key_vault_manager = KeyVaultManager()
    return _key_vault_manager

