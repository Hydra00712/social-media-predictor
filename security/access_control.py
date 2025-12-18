"""
Access Control and Logging
Implements RBAC and audit logging for security compliance
"""

import logging
import json
from datetime import datetime
from enum import Enum
import sqlite3
import os

logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    DATA_SCIENTIST = "data_scientist"
    VIEWER = "viewer"
    API_USER = "api_user"

class Permission(Enum):
    """Permissions"""
    READ_DATA = "read_data"
    WRITE_DATA = "write_data"
    TRAIN_MODEL = "train_model"
    DEPLOY_MODEL = "deploy_model"
    VIEW_PREDICTIONS = "view_predictions"
    MAKE_PREDICTIONS = "make_predictions"
    ADMIN_ACCESS = "admin_access"

# Role-Permission mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [p for p in Permission],  # All permissions
    UserRole.DATA_SCIENTIST: [
        Permission.READ_DATA,
        Permission.WRITE_DATA,
        Permission.TRAIN_MODEL,
        Permission.VIEW_PREDICTIONS,
        Permission.MAKE_PREDICTIONS
    ],
    UserRole.VIEWER: [
        Permission.READ_DATA,
        Permission.VIEW_PREDICTIONS
    ],
    UserRole.API_USER: [
        Permission.MAKE_PREDICTIONS,
        Permission.VIEW_PREDICTIONS
    ]
}

class AccessLogger:
    """
    Logs all access attempts for security auditing
    """
    
    def __init__(self, db_path='database/social_media.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize access log table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    status TEXT NOT NULL,
                    details TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Access log table initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize access log: {e}")
    
    def log_access(self, user_id, action, resource, status, ip_address=None, user_agent=None, details=None):
        """
        Log an access attempt
        
        Args:
            user_id: User identifier
            action: Action performed (e.g., 'read', 'write', 'predict')
            resource: Resource accessed (e.g., 'model', 'data', 'api')
            status: 'success' or 'denied'
            ip_address: Client IP address
            user_agent: Client user agent
            details: Additional details (dict or string)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            details_str = json.dumps(details) if isinstance(details, dict) else str(details)
            
            cursor.execute('''
                INSERT INTO access_logs 
                (timestamp, user_id, action, resource, ip_address, user_agent, status, details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                user_id,
                action,
                resource,
                ip_address,
                user_agent,
                status,
                details_str
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"📝 Access logged: {user_id} - {action} - {resource} - {status}")
        except Exception as e:
            logger.error(f"❌ Failed to log access: {e}")
    
    def get_recent_logs(self, limit=100):
        """Get recent access logs"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM access_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            logs = cursor.fetchall()
            conn.close()
            
            return logs
        except Exception as e:
            logger.error(f"❌ Failed to retrieve logs: {e}")
            return []

class RBACManager:
    """
    Role-Based Access Control Manager
    """
    
    def __init__(self):
        self.access_logger = AccessLogger()
    
    def check_permission(self, user_role, required_permission):
        """
        Check if user role has required permission
        
        Args:
            user_role: UserRole enum
            required_permission: Permission enum
            
        Returns:
            True if permitted, False otherwise
        """
        if user_role not in ROLE_PERMISSIONS:
            return False
        
        return required_permission in ROLE_PERMISSIONS[user_role]
    
    def authorize(self, user_id, user_role, action, resource):
        """
        Authorize user action and log it
        
        Args:
            user_id: User identifier
            user_role: UserRole enum
            action: Permission enum
            resource: Resource being accessed
            
        Returns:
            True if authorized, False otherwise
        """
        authorized = self.check_permission(user_role, action)
        
        status = "success" if authorized else "denied"
        self.access_logger.log_access(
            user_id=user_id,
            action=action.value,
            resource=resource,
            status=status
        )
        
        if not authorized:
            logger.warning(f"⚠️ Access denied: {user_id} - {action.value} - {resource}")
        
        return authorized

# Global instance
_rbac_manager = None

def get_rbac_manager():
    """Get singleton RBAC manager instance"""
    global _rbac_manager
    if _rbac_manager is None:
        _rbac_manager = RBACManager()
    return _rbac_manager

