"""
Diagnostic Result Model
Represents results from device diagnostics
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class Severity(Enum):
    """Issue severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    NORMAL = "normal"


@dataclass
class Issue:
    """Individual issue found during diagnostics"""
    
    type: str
    severity: Severity
    description: str
    details: Optional[Dict[str, Any]] = None
    recommendation: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'type': self.type,
            'severity': self.severity.value if isinstance(self.severity, Severity) else self.severity,
            'description': self.description,
            'details': self.details,
            'recommendation': self.recommendation
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Issue':
        """Create from dictionary"""
        if isinstance(data.get('severity'), str):
            data['severity'] = Severity(data['severity'])
        return cls(**data)


@dataclass
class CommandResult:
    """Result from executing a single command"""
    
    command: str
    output: str
    success: bool
    error_message: Optional[str] = None
    execution_time: float = 0.0
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'command': self.command,
            'output': self.output,
            'success': self.success,
            'error_message': self.error_message,
            'execution_time': self.execution_time
        }


@dataclass
class DiagnosticResult:
    """Complete diagnostic result for a device"""
    
    device_ip: str
    device_hostname: Optional[str]
    workflow_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    overall_severity: Severity = Severity.NORMAL
    issues: List[Issue] = field(default_factory=list)
    command_results: List[CommandResult] = field(default_factory=list)
    summary: str = ""
    execution_time: float = 0.0
    success: bool = True
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Determine overall severity from issues
        if self.issues:
            severities = [issue.severity for issue in self.issues]
            if Severity.CRITICAL in severities:
                self.overall_severity = Severity.CRITICAL
            elif Severity.WARNING in severities:
                self.overall_severity = Severity.WARNING
            else:
                self.overall_severity = Severity.INFO
    
    def add_issue(self, issue: Issue) -> None:
        """Add an issue to the result"""
        self.issues.append(issue)
        # Update overall severity
        if issue.severity == Severity.CRITICAL:
            self.overall_severity = Severity.CRITICAL
        elif issue.severity == Severity.WARNING and self.overall_severity != Severity.CRITICAL:
            self.overall_severity = Severity.WARNING
    
    def add_command_result(self, result: CommandResult) -> None:
        """Add a command result"""
        self.command_results.append(result)
        if not result.success:
            self.success = False
    
    def get_critical_issues(self) -> List[Issue]:
        """Get all critical issues"""
        return [i for i in self.issues if i.severity == Severity.CRITICAL]
    
    def get_warning_issues(self) -> List[Issue]:
        """Get all warning issues"""
        return [i for i in self.issues if i.severity == Severity.WARNING]
    
    def has_issues(self) -> bool:
        """Check if any issues were found"""
        return len(self.issues) > 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'device_ip': self.device_ip,
            'device_hostname': self.device_hostname,
            'workflow_name': self.workflow_name,
            'timestamp': self.timestamp.isoformat(),
            'overall_severity': self.overall_severity.value if isinstance(self.overall_severity, Severity) else self.overall_severity,
            'issues': [issue.to_dict() for issue in self.issues],
            'command_results': [cr.to_dict() for cr in self.command_results],
            'summary': self.summary,
            'execution_time': self.execution_time,
            'success': self.success
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DiagnosticResult':
        """Create from dictionary"""
        if isinstance(data.get('timestamp'), str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        if isinstance(data.get('overall_severity'), str):
            data['overall_severity'] = Severity(data['overall_severity'])
        
        if 'issues' in data:
            data['issues'] = [Issue.from_dict(i) for i in data['issues']]
        if 'command_results' in data:
            data['command_results'] = [CommandResult(**cr) for cr in data['command_results']]
        
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"DiagnosticResult(device={self.device_ip}, workflow={self.workflow_name}, severity={self.overall_severity.value}, issues={len(self.issues)})"
