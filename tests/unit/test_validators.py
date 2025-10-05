"""
Unit tests for validators
"""

import pytest
from utils.validators import (
    validate_ip_address,
    validate_subnet,
    validate_ip_range,
    validate_port,
    validate_hostname,
    validate_credential_name,
    validate_timeout
)


class TestValidators:
    """Test validation functions"""
    
    def test_validate_ip_address_valid(self):
        """Test valid IP addresses"""
        valid, error = validate_ip_address("192.168.1.1")
        assert valid is True
        assert error is None
        
        valid, error = validate_ip_address("10.0.0.1")
        assert valid is True
    
    def test_validate_ip_address_invalid(self):
        """Test invalid IP addresses"""
        valid, error = validate_ip_address("256.1.1.1")
        assert valid is False
        assert error is not None
        
        valid, error = validate_ip_address("not.an.ip")
        assert valid is False
    
    def test_validate_subnet_valid(self):
        """Test valid subnets"""
        valid, error = validate_subnet("192.168.1.0/24")
        assert valid is True
        
        valid, error = validate_subnet("10.0.0.0/8")
        assert valid is True
    
    def test_validate_subnet_invalid(self):
        """Test invalid subnets"""
        valid, error = validate_subnet("192.168.1.0/33")
        assert valid is False
        
        valid, error = validate_subnet("not-a-subnet")
        assert valid is False
    
    def test_validate_ip_range_valid(self):
        """Test valid IP ranges"""
        valid, error = validate_ip_range("192.168.1.1-192.168.1.50")
        assert valid is True
    
    def test_validate_ip_range_invalid(self):
        """Test invalid IP ranges"""
        valid, error = validate_ip_range("192.168.1.50-192.168.1.1")
        assert valid is False  # Start > End
        
        valid, error = validate_ip_range("not-a-range")
        assert valid is False
    
    def test_validate_port_valid(self):
        """Test valid ports"""
        valid, error = validate_port("22")
        assert valid is True
        
        valid, error = validate_port("8080")
        assert valid is True
    
    def test_validate_port_invalid(self):
        """Test invalid ports"""
        valid, error = validate_port("0")
        assert valid is False
        
        valid, error = validate_port("99999")
        assert valid is False
        
        valid, error = validate_port("not-a-port")
        assert valid is False
    
    def test_validate_hostname_valid(self):
        """Test valid hostnames"""
        valid, error = validate_hostname("router-01")
        assert valid is True
        
        valid, error = validate_hostname("switch.example.com")
        assert valid is True
    
    def test_validate_hostname_invalid(self):
        """Test invalid hostnames"""
        valid, error = validate_hostname("")
        assert valid is False
        
        valid, error = validate_hostname("invalid_hostname!")
        assert valid is False
    
    def test_validate_credential_name_valid(self):
        """Test valid credential names"""
        valid, error = validate_credential_name("cisco_lab")
        assert valid is True
        
        valid, error = validate_credential_name("prod-routers")
        assert valid is True
    
    def test_validate_credential_name_invalid(self):
        """Test invalid credential names"""
        valid, error = validate_credential_name("")
        assert valid is False
        
        valid, error = validate_credential_name("invalid name!")
        assert valid is False
    
    def test_validate_timeout_valid(self):
        """Test valid timeouts"""
        valid, error = validate_timeout("10")
        assert valid is True
        
        valid, error = validate_timeout("60")
        assert valid is True
    
    def test_validate_timeout_invalid(self):
        """Test invalid timeouts"""
        valid, error = validate_timeout("0")
        assert valid is False
        
        valid, error = validate_timeout("500")
        assert valid is False
        
        valid, error = validate_timeout("not-a-number")
        assert valid is False
