"""
Input Validators
Validation functions for user inputs
"""

import re
import ipaddress
from typing import Tuple, Optional


def validate_ip_address(ip: str) -> Tuple[bool, Optional[str]]:
    """
    Validate IP address format.
    
    Args:
        ip: IP address string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        ipaddress.ip_address(ip)
        return True, None
    except ValueError as e:
        return False, f"Invalid IP address: {str(e)}"


def validate_subnet(subnet: str) -> Tuple[bool, Optional[str]]:
    """
    Validate subnet in CIDR notation.
    
    Args:
        subnet: Subnet string (e.g., '192.168.1.0/24')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        ipaddress.ip_network(subnet, strict=False)
        return True, None
    except ValueError as e:
        return False, f"Invalid subnet: {str(e)}"


def validate_ip_range(ip_range: str) -> Tuple[bool, Optional[str]]:
    """
    Validate IP range format (e.g., '192.168.1.1-192.168.1.50').
    
    Args:
        ip_range: IP range string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if '-' not in ip_range:
            return False, "IP range must contain '-' separator"
        
        start_ip, end_ip = ip_range.split('-')
        start_ip = start_ip.strip()
        end_ip = end_ip.strip()
        
        # Validate both IPs
        start_valid, start_err = validate_ip_address(start_ip)
        if not start_valid:
            return False, f"Invalid start IP: {start_err}"
        
        end_valid, end_err = validate_ip_address(end_ip)
        if not end_valid:
            return False, f"Invalid end IP: {end_err}"
        
        # Check if start < end
        if ipaddress.ip_address(start_ip) >= ipaddress.ip_address(end_ip):
            return False, "Start IP must be less than end IP"
        
        return True, None
        
    except Exception as e:
        return False, f"Invalid IP range: {str(e)}"


def validate_port(port: str) -> Tuple[bool, Optional[str]]:
    """
    Validate port number.
    
    Args:
        port: Port number as string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        port_num = int(port)
        if 1 <= port_num <= 65535:
            return True, None
        else:
            return False, "Port must be between 1 and 65535"
    except ValueError:
        return False, "Port must be a number"


def validate_hostname(hostname: str) -> Tuple[bool, Optional[str]]:
    """
    Validate hostname format.
    
    Args:
        hostname: Hostname string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not hostname:
        return False, "Hostname cannot be empty"
    
    if len(hostname) > 253:
        return False, "Hostname too long (max 253 characters)"
    
    # RFC 1123 hostname validation
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    
    if re.match(pattern, hostname):
        return True, None
    else:
        return False, "Invalid hostname format"


def validate_credential_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate credential name.
    
    Args:
        name: Credential name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Credential name cannot be empty"
    
    if len(name) > 50:
        return False, "Credential name too long (max 50 characters)"
    
    # Allow alphanumeric, underscore, hyphen
    if re.match(r'^[a-zA-Z0-9_-]+$', name):
        return True, None
    else:
        return False, "Credential name can only contain letters, numbers, underscore, and hyphen"


def validate_timeout(timeout: str) -> Tuple[bool, Optional[str]]:
    """
    Validate timeout value.
    
    Args:
        timeout: Timeout in seconds as string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        timeout_val = int(timeout)
        if 1 <= timeout_val <= 300:
            return True, None
        else:
            return False, "Timeout must be between 1 and 300 seconds"
    except ValueError:
        return False, "Timeout must be a number"
