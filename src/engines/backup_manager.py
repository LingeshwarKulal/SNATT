"""
Backup Manager
Handles device configuration backups
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import concurrent.futures

from models.device import Device
from models.backup_record import BackupRecord
from engines.connection_manager import ConnectionManager


class BackupManager:
    """Manages device configuration backups"""
    
    # Vendor-specific config retrieval commands
    CONFIG_COMMANDS = {
        'Cisco': {
            'running-config': 'show running-config',
            'startup-config': 'show startup-config'
        },
        'Juniper': {
            'running-config': 'show configuration',
            'startup-config': 'show configuration'
        },
        'HP': {
            'running-config': 'display current-configuration',
            'startup-config': 'display saved-configuration'
        },
        'Huawei': {
            'running-config': 'display current-configuration',
            'startup-config': 'display saved-configuration'
        }
    }
    
    def __init__(self, config: dict, connection_manager: ConnectionManager):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.connection_manager = connection_manager
        
        # Get backup directory from config
        backup_dir = config.get('backup', {}).get('directory', 'backups')
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True, parents=True)
        
        self.naming_format = config.get('backup', {}).get('naming_format', '{hostname}_{timestamp}.cfg')
    
    def backup_device(
        self,
        device: Device,
        config_types: List[str] = None
    ) -> List[BackupRecord]:
        """
        Backup configuration(s) from a single device.
        
        Args:
            device: Device to backup
            config_types: List of config types ('running-config', 'startup-config').
                         If None, backs up based on config settings.
            
        Returns:
            List of BackupRecord objects
        """
        if config_types is None:
            config_types = []
            if self.config.get('backup', {}).get('include_running_config', True):
                config_types.append('running-config')
            if self.config.get('backup', {}).get('include_startup_config', False):
                config_types.append('startup-config')
        
        self.logger.info(f"Backing up {device.ip_address} - Config types: {config_types}")
        
        records = []
        
        for config_type in config_types:
            record = self._backup_single_config(device, config_type)
            records.append(record)
        
        return records
    
    def backup_multiple_devices(
        self,
        devices: List[Device],
        config_types: List[str] = None,
        progress_callback=None
    ) -> List[BackupRecord]:
        """
        Backup configurations from multiple devices in parallel.
        
        Args:
            devices: List of devices to backup
            config_types: Config types to backup
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of all BackupRecord objects
        """
        self.logger.info(f"Starting batch backup for {len(devices)} devices")
        
        all_records = []
        completed = 0
        
        for device in devices:
            records = self.backup_device(device, config_types)
            all_records.extend(records)
            
            completed += 1
            if progress_callback:
                progress_callback(completed, len(devices))
        
        success_count = sum(1 for r in all_records if r.backup_successful)
        self.logger.info(f"Batch backup complete: {success_count}/{len(all_records)} successful")
        
        return all_records
    
    def _backup_single_config(self, device: Device, config_type: str) -> BackupRecord:
        """Backup a single configuration type from a device"""
        
        try:
            # Check connection
            if not self.connection_manager.is_connected(device):
                return BackupRecord.create_failed(
                    device.ip_address,
                    device.hostname,
                    config_type,
                    "Device not connected"
                )
            
            # Get appropriate command for vendor
            command = self._get_config_command(device.vendor, config_type)
            if not command:
                return BackupRecord.create_failed(
                    device.ip_address,
                    device.hostname,
                    config_type,
                    f"No config command defined for vendor: {device.vendor}"
                )
            
            # Execute command
            self.logger.debug(f"Executing: {command} on {device.ip_address}")
            success, output = self.connection_manager.execute_command(
                device,
                command,
                timeout=30  # Longer timeout for config retrieval
            )
            
            if not success:
                return BackupRecord.create_failed(
                    device.ip_address,
                    device.hostname,
                    config_type,
                    f"Command execution failed: {output}"
                )
            
            # Generate filename
            filename = self._generate_filename(device, config_type)
            filepath = self.backup_dir / filename
            
            # Create backup record (this also saves the file)
            record = BackupRecord.create(
                device_ip=device.ip_address,
                device_hostname=device.hostname,
                config_type=config_type,
                file_path=filepath,
                config_content=output
            )
            
            self.logger.info(f"Backup successful: {filepath}")
            return record
        
        except Exception as e:
            self.logger.error(f"Error backing up {device.ip_address}: {e}")
            return BackupRecord.create_failed(
                device.ip_address,
                device.hostname,
                config_type,
                str(e)
            )
    
    def _get_config_command(self, vendor: Optional[str], config_type: str) -> Optional[str]:
        """Get the appropriate command for retrieving configuration"""
        
        if not vendor:
            vendor = 'Cisco'  # Default
        
        commands = self.CONFIG_COMMANDS.get(vendor, self.CONFIG_COMMANDS['Cisco'])
        return commands.get(config_type)
    
    def _generate_filename(self, device: Device, config_type: str) -> str:
        """Generate backup filename"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        hostname = device.hostname or device.ip_address.replace('.', '_')
        
        # Clean hostname (remove invalid characters)
        hostname = "".join(c for c in hostname if c.isalnum() or c in ('_', '-'))
        
        config_suffix = 'running' if 'running' in config_type else 'startup'
        
        return f"{hostname}_{config_suffix}_{timestamp}.cfg"
    
    def list_backups(self, device_ip: Optional[str] = None) -> List[Path]:
        """
        List backup files.
        
        Args:
            device_ip: If provided, list only backups for this device
            
        Returns:
            List of backup file paths
        """
        if device_ip:
            # Filter by IP (in filename)
            ip_pattern = device_ip.replace('.', '_')
            backups = [f for f in self.backup_dir.glob('*.cfg') if ip_pattern in f.name]
        else:
            backups = list(self.backup_dir.glob('*.cfg'))
        
        # Sort by modification time (newest first)
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        return backups
    
    def delete_backup(self, filepath: Path) -> bool:
        """Delete a backup file"""
        try:
            if filepath.exists():
                filepath.unlink()
                self.logger.info(f"Deleted backup: {filepath}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting backup {filepath}: {e}")
            return False
    
    def cleanup_old_backups(self, retention_days: Optional[int] = None) -> int:
        """
        Delete backups older than retention period.
        
        Args:
            retention_days: Days to retain backups (from config if None)
            
        Returns:
            Number of files deleted
        """
        if retention_days is None:
            retention_days = self.config.get('backup', {}).get('retention_days', 90)
        
        self.logger.info(f"Cleaning up backups older than {retention_days} days")
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        deleted_count = 0
        for backup_file in self.backup_dir.glob('*.cfg'):
            mod_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
            if mod_time < cutoff_date:
                if self.delete_backup(backup_file):
                    deleted_count += 1
        
        self.logger.info(f"Deleted {deleted_count} old backup files")
        return deleted_count
