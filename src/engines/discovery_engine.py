"""
Discovery Engine
Network device discovery and identification
"""

import logging
import ipaddress
import concurrent.futures
from typing import List, Optional, Set
from datetime import datetime
import subprocess
import platform

from models.device import Device, DeviceStatus, DeviceType


class DiscoveryEngine:
    """Handles network device discovery"""
    
    def __init__(self, config: dict):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.max_threads = config.get('discovery', {}).get('max_threads', 100)
        self.ping_timeout = config.get('network', {}).get('ping_timeout', 1)
    
    def discover_subnet(self, subnet: str, progress_callback=None) -> List[Device]:
        """
        Discover devices in a subnet using ICMP ping.
        
        Args:
            subnet: Subnet in CIDR notation (e.g., '192.168.1.0/24')
            progress_callback: Optional callback function for progress updates
            
        Returns:
            List of discovered Device objects
        """
        self.logger.info(f"Starting discovery for subnet: {subnet}")
        
        try:
            network = ipaddress.ip_network(subnet, strict=False)
            hosts = list(network.hosts())
            total_hosts = len(hosts)
            
            self.logger.info(f"Scanning {total_hosts} hosts...")
            
            discovered_devices = []
            
            # Ping sweep with thread pool
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                future_to_ip = {
                    executor.submit(self._ping_host, str(ip)): str(ip) 
                    for ip in hosts
                }
                
                completed = 0
                for future in concurrent.futures.as_completed(future_to_ip):
                    completed += 1
                    ip = future_to_ip[future]
                    
                    try:
                        is_reachable = future.result()
                        if is_reachable:
                            device = Device(
                                ip_address=ip,
                                status=DeviceStatus.REACHABLE,
                                last_seen=datetime.now()
                            )
                            discovered_devices.append(device)
                            self.logger.debug(f"Device found: {ip}")
                    
                    except Exception as e:
                        self.logger.error(f"Error checking {ip}: {e}")
                    
                    # Progress callback
                    if progress_callback:
                        progress_callback(completed, total_hosts)
            
            self.logger.info(f"Discovery complete. Found {len(discovered_devices)} devices.")
            return discovered_devices
        
        except Exception as e:
            self.logger.error(f"Error during subnet discovery: {e}")
            return []
    
    def discover_ip_range(self, start_ip: str, end_ip: str, progress_callback=None) -> List[Device]:
        """
        Discover devices in an IP range.
        
        Args:
            start_ip: Starting IP address
            end_ip: Ending IP address
            progress_callback: Optional callback function for progress updates
            
        Returns:
            List of discovered Device objects
        """
        self.logger.info(f"Starting discovery for IP range: {start_ip} - {end_ip}")
        
        try:
            start = ipaddress.ip_address(start_ip)
            end = ipaddress.ip_address(end_ip)
            
            # Generate IP list
            ips = []
            current = start
            while current <= end:
                ips.append(str(current))
                current += 1
            
            total_hosts = len(ips)
            self.logger.info(f"Scanning {total_hosts} hosts...")
            
            discovered_devices = []
            
            # Ping sweep with thread pool
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                future_to_ip = {
                    executor.submit(self._ping_host, ip): ip 
                    for ip in ips
                }
                
                completed = 0
                for future in concurrent.futures.as_completed(future_to_ip):
                    completed += 1
                    ip = future_to_ip[future]
                    
                    try:
                        is_reachable = future.result()
                        if is_reachable:
                            device = Device(
                                ip_address=ip,
                                status=DeviceStatus.REACHABLE,
                                last_seen=datetime.now()
                            )
                            discovered_devices.append(device)
                            self.logger.debug(f"Device found: {ip}")
                    
                    except Exception as e:
                        self.logger.error(f"Error checking {ip}: {e}")
                    
                    # Progress callback
                    if progress_callback:
                        progress_callback(completed, total_hosts)
            
            self.logger.info(f"Discovery complete. Found {len(discovered_devices)} devices.")
            return discovered_devices
        
        except Exception as e:
            self.logger.error(f"Error during IP range discovery: {e}")
            return []
    
    def _ping_host(self, ip: str) -> bool:
        """
        Ping a single host to check if it's reachable.
        
        Args:
            ip: IP address to ping
            
        Returns:
            bool: True if host is reachable
        """
        try:
            # Determine ping command based on OS
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
            
            command = ['ping', param, '1', timeout_param, str(self.ping_timeout * 1000 if platform.system().lower() == 'windows' else self.ping_timeout), ip]
            
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.ping_timeout + 1
            )
            
            return result.returncode == 0
        
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            self.logger.debug(f"Ping error for {ip}: {e}")
            return False
    
    def identify_device_vendor(self, device: Device, connection) -> Device:
        """
        Identify device vendor and type through SSH banner or command output.
        
        Args:
            device: Device object
            connection: Active connection to device
            
        Returns:
            Updated Device object with vendor information
        """
        try:
            # Try to get device information through show version or similar
            output = connection.send_command("show version", read_timeout=10)
            
            # Vendor identification patterns
            vendor_patterns = {
                'Cisco': ['Cisco', 'IOS', 'NX-OS', 'IOS-XE', 'IOS-XR'],
                'Juniper': ['Juniper', 'JUNOS', 'JunOS'],
                'HP': ['HP ', 'HPE ', 'ProCurve', 'Aruba'],
                'Huawei': ['Huawei', 'VRP'],
                'MikroTik': ['MikroTik', 'RouterOS'],
                'Ubiquiti': ['Ubiquiti', 'EdgeOS']
            }
            
            # Check output for vendor patterns
            output_lower = output.lower()
            for vendor, patterns in vendor_patterns.items():
                if any(pattern.lower() in output_lower for pattern in patterns):
                    device.vendor = vendor
                    self.logger.info(f"Identified {device.ip_address} as {vendor}")
                    break
            
            # Try to extract model and OS version (Cisco example)
            if device.vendor == 'Cisco':
                # Extract model
                if 'cisco' in output_lower:
                    lines = output.split('\n')
                    for line in lines:
                        if 'cisco' in line.lower() and ('bytes' in line.lower() or 'processor' in line.lower()):
                            parts = line.split()
                            if len(parts) > 1:
                                device.model = parts[1]
                            break
                
                # Extract IOS version
                for line in output.split('\n'):
                    if 'version' in line.lower() and ('ios' in line.lower() or 'nx-os' in line.lower()):
                        device.os_version = line.strip()
                        break
            
            return device
        
        except Exception as e:
            self.logger.error(f"Error identifying device {device.ip_address}: {e}")
            return device
    
    def enrich_device_info(self, device: Device, connection) -> Device:
        """
        Enrich device information with hostname, uptime, etc.
        
        Args:
            device: Device object
            connection: Active connection to device
            
        Returns:
            Updated Device object
        """
        try:
            # Get hostname
            if device.vendor == 'Cisco':
                hostname_output = connection.send_command("show running-config | include hostname")
                if hostname_output:
                    parts = hostname_output.split()
                    if len(parts) >= 2:
                        device.hostname = parts[1]
            
            # Get uptime (basic implementation)
            version_output = connection.send_command("show version")
            for line in version_output.split('\n'):
                if 'uptime' in line.lower():
                    device.uptime = line.strip()
                    break
            
            self.logger.info(f"Enriched device info for {device.ip_address}")
            return device
        
        except Exception as e:
            self.logger.error(f"Error enriching device info for {device.ip_address}: {e}")
            return device
