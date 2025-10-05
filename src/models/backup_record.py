"""
Backup Record Model
Represents a configuration backup
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import hashlib


@dataclass
class BackupRecord:
    """Configuration backup record"""
    
    device_ip: str
    device_hostname: Optional[str]
    timestamp: datetime
    config_type: str  # 'running-config' or 'startup-config'
    file_path: Path
    size_bytes: int
    checksum: str
    backup_successful: bool = True
    error_message: Optional[str] = None
    
    @classmethod
    def create(
        cls,
        device_ip: str,
        device_hostname: Optional[str],
        config_type: str,
        file_path: Path,
        config_content: str
    ) -> 'BackupRecord':
        """
        Create a backup record and save the configuration file.
        
        Args:
            device_ip: Device IP address
            device_hostname: Device hostname
            config_type: Type of configuration
            file_path: Path to save the configuration
            config_content: Configuration content
            
        Returns:
            BackupRecord instance
        """
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write configuration to file
        file_path.write_text(config_content, encoding='utf-8')
        
        # Calculate checksum
        checksum = hashlib.sha256(config_content.encode()).hexdigest()
        
        # Get file size
        size_bytes = file_path.stat().st_size
        
        return cls(
            device_ip=device_ip,
            device_hostname=device_hostname,
            timestamp=datetime.now(),
            config_type=config_type,
            file_path=file_path,
            size_bytes=size_bytes,
            checksum=checksum,
            backup_successful=True
        )
    
    @classmethod
    def create_failed(
        cls,
        device_ip: str,
        device_hostname: Optional[str],
        config_type: str,
        error_message: str
    ) -> 'BackupRecord':
        """
        Create a failed backup record.
        
        Args:
            device_ip: Device IP address
            device_hostname: Device hostname
            config_type: Type of configuration
            error_message: Error description
            
        Returns:
            BackupRecord instance
        """
        return cls(
            device_ip=device_ip,
            device_hostname=device_hostname,
            timestamp=datetime.now(),
            config_type=config_type,
            file_path=Path(""),
            size_bytes=0,
            checksum="",
            backup_successful=False,
            error_message=error_message
        )
    
    def verify_integrity(self) -> bool:
        """
        Verify backup file integrity using checksum.
        
        Returns:
            bool: True if file integrity is valid
        """
        if not self.backup_successful or not self.file_path.exists():
            return False
        
        try:
            content = self.file_path.read_text(encoding='utf-8')
            current_checksum = hashlib.sha256(content.encode()).hexdigest()
            return current_checksum == self.checksum
        except Exception:
            return False
    
    def get_config_content(self) -> Optional[str]:
        """
        Read and return configuration content.
        
        Returns:
            Configuration content or None if error
        """
        if not self.backup_successful or not self.file_path.exists():
            return None
        
        try:
            return self.file_path.read_text(encoding='utf-8')
        except Exception:
            return None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'device_ip': self.device_ip,
            'device_hostname': self.device_hostname,
            'timestamp': self.timestamp.isoformat(),
            'config_type': self.config_type,
            'file_path': str(self.file_path),
            'size_bytes': self.size_bytes,
            'checksum': self.checksum,
            'backup_successful': self.backup_successful,
            'error_message': self.error_message
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BackupRecord':
        """Create from dictionary"""
        if isinstance(data.get('timestamp'), str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        if isinstance(data.get('file_path'), str):
            data['file_path'] = Path(data['file_path'])
        
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation"""
        status = "Success" if self.backup_successful else "Failed"
        return f"BackupRecord(device={self.device_ip}, type={self.config_type}, status={status})"
