"""
Credential Manager
Secure storage and retrieval of device credentials
"""

import keyring
import logging
import json
from typing import Optional, Dict, List
from cryptography.fernet import Fernet
from pathlib import Path


class CredentialManager:
    """Manages secure storage of device credentials"""
    
    SERVICE_NAME = 'SNATT'
    CREDENTIALS_FILE = Path(__file__).parent.parent.parent / 'config' / 'credentials_meta.json'
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._encryption_key = self._get_or_create_key()
        self._cipher = Fernet(self._encryption_key)
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key for local encryption"""
        key_file = Path(__file__).parent.parent.parent / 'config' / '.key'
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            key_file.parent.mkdir(exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            self.logger.info("New encryption key generated")
            return key
    
    def save_credential(
        self,
        credential_name: str,
        username: str,
        password: str,
        enable_password: Optional[str] = None,
        description: str = ""
    ) -> bool:
        """
        Save device credential securely.
        
        Args:
            credential_name: Unique name for this credential set
            username: Device username
            password: Device password
            enable_password: Enable/privileged password (optional)
            description: Description of credential usage
            
        Returns:
            bool: True if successful
        """
        try:
            # Store in system keyring
            keyring.set_password(self.SERVICE_NAME, f"{credential_name}_user", username)
            keyring.set_password(self.SERVICE_NAME, f"{credential_name}_pass", password)
            
            if enable_password:
                keyring.set_password(self.SERVICE_NAME, f"{credential_name}_enable", enable_password)
            
            # Store metadata
            self._save_credential_metadata(credential_name, username, description, bool(enable_password))
            
            self.logger.info(f"Credential '{credential_name}' saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving credential: {e}")
            return False
    
    def get_credential(self, credential_name: str) -> Optional[Dict[str, str]]:
        """
        Retrieve credential by name.
        
        Args:
            credential_name: Name of credential set
            
        Returns:
            Dict with 'username', 'password', 'enable_password' keys, or None if not found
        """
        try:
            username = keyring.get_password(self.SERVICE_NAME, f"{credential_name}_user")
            password = keyring.get_password(self.SERVICE_NAME, f"{credential_name}_pass")
            enable_password = keyring.get_password(self.SERVICE_NAME, f"{credential_name}_enable")
            
            if username and password:
                return {
                    'username': username,
                    'password': password,
                    'enable_password': enable_password
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error retrieving credential: {e}")
            return None
    
    def delete_credential(self, credential_name: str) -> bool:
        """
        Delete a credential set.
        
        Args:
            credential_name: Name of credential to delete
            
        Returns:
            bool: True if successful
        """
        try:
            keyring.delete_password(self.SERVICE_NAME, f"{credential_name}_user")
            keyring.delete_password(self.SERVICE_NAME, f"{credential_name}_pass")
            
            try:
                keyring.delete_password(self.SERVICE_NAME, f"{credential_name}_enable")
            except:
                pass  # Enable password might not exist
            
            self._remove_credential_metadata(credential_name)
            
            self.logger.info(f"Credential '{credential_name}' deleted successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting credential: {e}")
            return False
    
    def list_credentials(self) -> List[Dict[str, str]]:
        """
        List all saved credentials (metadata only, no passwords).
        
        Returns:
            List of credential metadata dictionaries
        """
        try:
            if not self.CREDENTIALS_FILE.exists():
                return []
            
            with open(self.CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            return metadata.get('credentials', [])
            
        except Exception as e:
            self.logger.error(f"Error listing credentials: {e}")
            return []
    
    def _save_credential_metadata(
        self,
        name: str,
        username: str,
        description: str,
        has_enable: bool
    ) -> None:
        """Save credential metadata to file"""
        metadata = {'credentials': []}
        
        if self.CREDENTIALS_FILE.exists():
            with open(self.CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        # Remove existing entry if present
        metadata['credentials'] = [
            c for c in metadata['credentials'] if c['name'] != name
        ]
        
        # Add new entry
        metadata['credentials'].append({
            'name': name,
            'username': username,
            'description': description,
            'has_enable_password': has_enable
        })
        
        self.CREDENTIALS_FILE.parent.mkdir(exist_ok=True)
        with open(self.CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def _remove_credential_metadata(self, name: str) -> None:
        """Remove credential metadata from file"""
        if not self.CREDENTIALS_FILE.exists():
            return
        
        with open(self.CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        metadata['credentials'] = [
            c for c in metadata['credentials'] if c['name'] != name
        ]
        
        with open(self.CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
