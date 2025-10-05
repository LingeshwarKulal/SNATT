"""
Connection Manager
Manages SSH connections to network devices
"""

import logging
from typing import Dict, Optional, List
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import time

from models.device import Device, DeviceStatus
from utils.credential_manager import CredentialManager


class ConnectionManager:
    """Manages connections to network devices"""
    
    # Device type mapping for Netmiko
    DEVICE_TYPE_MAP = {
        'Cisco': 'cisco_ios',
        'Juniper': 'juniper_junos',
        'HP': 'hp_procurve',
        'Huawei': 'huawei',
        'MikroTik': 'mikrotik_routeros',
        'Aruba': 'aruba_os'
    }
    
    def __init__(self, config: dict):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.credential_manager = CredentialManager()
        self.connections: Dict[str, ConnectHandler] = {}
        self.default_timeout = config.get('network', {}).get('default_timeout', 10)
        self.retry_attempts = config.get('network', {}).get('retry_attempts', 3)
        self.retry_delay = config.get('network', {}).get('retry_delay', 2)
    
    def connect(self, device: Device) -> bool:
        """
        Establish SSH connection to a device.
        
        Args:
            device: Device object to connect to
            
        Returns:
            bool: True if connection successful
        """
        if device.ip_address in self.connections:
            self.logger.info(f"Connection to {device.ip_address} already exists")
            return True
        
        if not device.credential_name:
            self.logger.error(f"No credentials specified for {device.ip_address}")
            return False
        
        # Get credentials
        credentials = self.credential_manager.get_credential(device.credential_name)
        if not credentials:
            self.logger.error(f"Credentials '{device.credential_name}' not found")
            return False
        
        # Determine device type for Netmiko
        device_type = self._get_netmiko_device_type(device.vendor)
        
        # Connection parameters
        connection_params = {
            'device_type': device_type,
            'host': device.ip_address,
            'username': credentials['username'],
            'password': credentials['password'],
            'port': device.ssh_port,
            'timeout': device.connection_timeout or self.default_timeout,
            'session_log': None,  # Can be enabled for debugging
            'global_delay_factor': 1,
        }
        
        # Add enable password if available
        if credentials.get('enable_password'):
            connection_params['secret'] = credentials['enable_password']
        
        # Attempt connection with retries
        for attempt in range(1, self.retry_attempts + 1):
            try:
                self.logger.info(f"Connecting to {device.ip_address} (attempt {attempt}/{self.retry_attempts})...")
                
                connection = ConnectHandler(**connection_params)
                
                # Enter enable mode if Cisco device
                if device.vendor == 'Cisco' and credentials.get('enable_password'):
                    connection.enable()
                
                self.connections[device.ip_address] = connection
                device.update_status(DeviceStatus.CONNECTED)
                
                self.logger.info(f"Successfully connected to {device.ip_address}")
                return True
            
            except NetmikoTimeoutException as e:
                self.logger.warning(f"Timeout connecting to {device.ip_address}: {e}")
                device.update_status(DeviceStatus.UNREACHABLE)
                
            except NetmikoAuthenticationException as e:
                self.logger.error(f"Authentication failed for {device.ip_address}: {e}")
                device.update_status(DeviceStatus.ERROR)
                return False  # Don't retry on auth errors
            
            except Exception as e:
                self.logger.error(f"Error connecting to {device.ip_address}: {e}")
                device.update_status(DeviceStatus.ERROR)
            
            # Wait before retry
            if attempt < self.retry_attempts:
                time.sleep(self.retry_delay)
        
        self.logger.error(f"Failed to connect to {device.ip_address} after {self.retry_attempts} attempts")
        return False
    
    def disconnect(self, device: Device) -> bool:
        """
        Disconnect from a device.
        
        Args:
            device: Device to disconnect from
            
        Returns:
            bool: True if successful
        """
        if device.ip_address not in self.connections:
            self.logger.warning(f"No active connection to {device.ip_address}")
            return False
        
        try:
            connection = self.connections[device.ip_address]
            connection.disconnect()
            del self.connections[device.ip_address]
            
            device.update_status(DeviceStatus.DISCONNECTED)
            self.logger.info(f"Disconnected from {device.ip_address}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error disconnecting from {device.ip_address}: {e}")
            return False
    
    def disconnect_all(self) -> None:
        """Disconnect from all devices"""
        self.logger.info("Disconnecting from all devices...")
        
        for ip in list(self.connections.keys()):
            try:
                self.connections[ip].disconnect()
                self.logger.info(f"Disconnected from {ip}")
            except Exception as e:
                self.logger.error(f"Error disconnecting from {ip}: {e}")
        
        self.connections.clear()
    
    def get_connection(self, device: Device) -> Optional[ConnectHandler]:
        """
        Get active connection for a device.
        
        Args:
            device: Device object
            
        Returns:
            ConnectHandler instance or None
        """
        connection = self.connections.get(device.ip_address)
        
        if connection and self._is_connection_alive(connection):
            return connection
        
        # Connection dead, remove it
        if device.ip_address in self.connections:
            del self.connections[device.ip_address]
        
        return None
    
    def is_connected(self, device: Device) -> bool:
        """
        Check if device has active connection.
        
        Args:
            device: Device to check
            
        Returns:
            bool: True if connected
        """
        return device.ip_address in self.connections
    
    def execute_command(
        self,
        device: Device,
        command: str,
        timeout: Optional[int] = None
    ) -> tuple[bool, str]:
        """
        Execute a command on a device.
        
        Args:
            device: Device to execute command on
            command: Command to execute
            timeout: Command timeout (uses default if None)
            
        Returns:
            Tuple of (success, output)
        """
        connection = self.get_connection(device)
        
        if not connection:
            self.logger.error(f"No active connection to {device.ip_address}")
            return False, "No active connection"
        
        try:
            self.logger.debug(f"Executing command on {device.ip_address}: {command}")
            
            output = connection.send_command(
                command,
                read_timeout=timeout or self.default_timeout
            )
            
            return True, output
        
        except Exception as e:
            self.logger.error(f"Error executing command on {device.ip_address}: {e}")
            return False, str(e)
    
    def execute_commands(
        self,
        device: Device,
        commands: List[str],
        timeout: Optional[int] = None
    ) -> List[tuple[str, bool, str]]:
        """
        Execute multiple commands on a device.
        
        Args:
            device: Device to execute commands on
            commands: List of commands
            timeout: Command timeout
            
        Returns:
            List of tuples (command, success, output)
        """
        results = []
        
        for command in commands:
            success, output = self.execute_command(device, command, timeout)
            results.append((command, success, output))
        
        return results
    
    def _get_netmiko_device_type(self, vendor: Optional[str]) -> str:
        """
        Map vendor name to Netmiko device type.
        
        Args:
            vendor: Vendor name
            
        Returns:
            Netmiko device type string
        """
        if not vendor:
            return 'cisco_ios'  # Default to Cisco IOS
        
        return self.DEVICE_TYPE_MAP.get(vendor, 'cisco_ios')
    
    def _is_connection_alive(self, connection: ConnectHandler) -> bool:
        """
        Check if a connection is still alive.
        
        Args:
            connection: Connection to check
            
        Returns:
            bool: True if alive
        """
        try:
            # Send a simple command to check connectivity
            connection.send_command("", read_timeout=2, expect_string=r"#|>")
            return True
        except:
            return False
    
    def get_active_connections_count(self) -> int:
        """Get number of active connections"""
        return len(self.connections)
    
    def get_connected_devices(self) -> List[str]:
        """Get list of connected device IPs"""
        return list(self.connections.keys())
