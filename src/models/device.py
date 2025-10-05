"""
Device Model
Represents a network device
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class DeviceStatus(Enum):
    """Device connection status"""
    UNKNOWN = "unknown"
    REACHABLE = "reachable"
    UNREACHABLE = "unreachable"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class DeviceType(Enum):
    """Device type classification"""
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    ACCESS_POINT = "access_point"
    LOAD_BALANCER = "load_balancer"
    UNKNOWN = "unknown"


@dataclass
class Device:
    """Network device model"""
    
    ip_address: str
    hostname: Optional[str] = None
    vendor: Optional[str] = None
    device_type: DeviceType = DeviceType.UNKNOWN
    model: Optional[str] = None
    os_version: Optional[str] = None
    serial_number: Optional[str] = None
    status: DeviceStatus = DeviceStatus.UNKNOWN
    credential_name: Optional[str] = None
    last_seen: Optional[datetime] = None
    first_discovered: Optional[datetime] = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    
    # Connection details
    ssh_port: int = 22
    connection_timeout: int = 10
    
    # Device information
    uptime: Optional[str] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    interface_count: Optional[int] = None
    
    def __post_init__(self):
        """Post-initialization processing"""
        if self.last_seen is None:
            self.last_seen = datetime.now()
        
        # Convert string enums to enum objects if needed
        if isinstance(self.status, str):
            self.status = DeviceStatus(self.status)
        if isinstance(self.device_type, str):
            self.device_type = DeviceType(self.device_type)
    
    def to_dict(self) -> dict:
        """Convert device to dictionary"""
        return {
            'ip_address': self.ip_address,
            'hostname': self.hostname,
            'vendor': self.vendor,
            'device_type': self.device_type.value if isinstance(self.device_type, DeviceType) else self.device_type,
            'model': self.model,
            'os_version': self.os_version,
            'serial_number': self.serial_number,
            'status': self.status.value if isinstance(self.status, DeviceStatus) else self.status,
            'credential_name': self.credential_name,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'first_discovered': self.first_discovered.isoformat() if self.first_discovered else None,
            'tags': self.tags,
            'notes': self.notes,
            'ssh_port': self.ssh_port,
            'connection_timeout': self.connection_timeout,
            'uptime': self.uptime,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'interface_count': self.interface_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Device':
        """Create device from dictionary"""
        # Convert datetime strings to datetime objects
        if data.get('last_seen'):
            data['last_seen'] = datetime.fromisoformat(data['last_seen'])
        if data.get('first_discovered'):
            data['first_discovered'] = datetime.fromisoformat(data['first_discovered'])
        
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"Device(ip={self.ip_address}, hostname={self.hostname}, vendor={self.vendor}, status={self.status.value})"
    
    def is_reachable(self) -> bool:
        """Check if device is reachable"""
        return self.status in [DeviceStatus.REACHABLE, DeviceStatus.CONNECTED]
    
    def is_connected(self) -> bool:
        """Check if device has active connection"""
        return self.status == DeviceStatus.CONNECTED
    
    def update_status(self, status: DeviceStatus) -> None:
        """Update device status and last_seen timestamp"""
        self.status = status
        self.last_seen = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the device"""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the device"""
        if tag in self.tags:
            self.tags.remove(tag)
