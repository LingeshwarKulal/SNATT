"""
Unit tests for Device model
"""

import pytest
from datetime import datetime
from models.device import Device, DeviceStatus, DeviceType


class TestDevice:
    """Test Device model"""
    
    def test_device_creation(self):
        """Test basic device creation"""
        device = Device(
            ip_address="192.168.1.1",
            hostname="router-01",
            vendor="Cisco"
        )
        
        assert device.ip_address == "192.168.1.1"
        assert device.hostname == "router-01"
        assert device.vendor == "Cisco"
        assert device.status == DeviceStatus.UNKNOWN
        assert device.device_type == DeviceType.UNKNOWN
    
    def test_device_with_status(self):
        """Test device with specific status"""
        device = Device(
            ip_address="192.168.1.1",
            status=DeviceStatus.REACHABLE
        )
        
        assert device.status == DeviceStatus.REACHABLE
        assert device.is_reachable() is True
    
    def test_device_to_dict(self):
        """Test device serialization to dictionary"""
        device = Device(
            ip_address="192.168.1.1",
            hostname="router-01",
            vendor="Cisco",
            device_type=DeviceType.ROUTER
        )
        
        device_dict = device.to_dict()
        
        assert device_dict['ip_address'] == "192.168.1.1"
        assert device_dict['hostname'] == "router-01"
        assert device_dict['vendor'] == "Cisco"
        assert device_dict['device_type'] == "router"
    
    def test_device_from_dict(self):
        """Test device creation from dictionary"""
        device_data = {
            'ip_address': "192.168.1.1",
            'hostname': "router-01",
            'vendor': "Cisco",
            'device_type': "router",
            'status': "reachable"
        }
        
        device = Device.from_dict(device_data)
        
        assert device.ip_address == "192.168.1.1"
        assert device.hostname == "router-01"
        assert device.vendor == "Cisco"
        assert device.device_type == DeviceType.ROUTER
        assert device.status == DeviceStatus.REACHABLE
    
    def test_device_update_status(self):
        """Test updating device status"""
        device = Device(ip_address="192.168.1.1")
        
        old_last_seen = device.last_seen
        
        device.update_status(DeviceStatus.CONNECTED)
        
        assert device.status == DeviceStatus.CONNECTED
        assert device.last_seen > old_last_seen
    
    def test_device_tags(self):
        """Test device tag management"""
        device = Device(ip_address="192.168.1.1")
        
        device.add_tag("production")
        device.add_tag("critical")
        
        assert "production" in device.tags
        assert "critical" in device.tags
        assert len(device.tags) == 2
        
        device.remove_tag("production")
        assert "production" not in device.tags
        assert len(device.tags) == 1
    
    def test_is_connected(self):
        """Test connection status check"""
        device = Device(
            ip_address="192.168.1.1",
            status=DeviceStatus.CONNECTED
        )
        
        assert device.is_connected() is True
        
        device.status = DeviceStatus.REACHABLE
        assert device.is_connected() is False
