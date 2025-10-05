"""
Troubleshooting Engine
Executes diagnostic workflows and analyzes results
"""

import logging
import time
import re
from typing import List, Dict, Optional
from datetime import datetime

from models.device import Device
from models.diagnostic_result import DiagnosticResult, Issue, CommandResult, Severity
from engines.connection_manager import ConnectionManager


class TroubleshootingEngine:
    """Handles device diagnostics and troubleshooting"""
    
    def __init__(self, config: dict, connection_manager: ConnectionManager):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.connection_manager = connection_manager
        self.workflows = config.get('diagnostics', {}).get('workflows', {})
        self.thresholds = config.get('diagnostics', {}).get('thresholds', {})
    
    def run_workflow(self, device: Device, workflow_name: str) -> DiagnosticResult:
        """
        Run a diagnostic workflow on a device.
        
        Args:
            device: Device to diagnose
            workflow_name: Name of workflow to run
            
        Returns:
            DiagnosticResult object
        """
        self.logger.info(f"Running workflow '{workflow_name}' on {device.ip_address}")
        
        result = DiagnosticResult(
            device_ip=device.ip_address,
            device_hostname=device.hostname,
            workflow_name=workflow_name
        )
        
        # Check if workflow exists
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            result.success = False
            result.summary = f"Workflow '{workflow_name}' not found"
            self.logger.error(result.summary)
            return result
        
        if not workflow.get('enabled', True):
            result.success = False
            result.summary = f"Workflow '{workflow_name}' is disabled"
            self.logger.warning(result.summary)
            return result
        
        # Check connection
        if not self.connection_manager.is_connected(device):
            result.success = False
            result.summary = f"Device {device.ip_address} is not connected"
            self.logger.error(result.summary)
            return result
        
        start_time = time.time()
        
        # Execute commands
        commands = workflow.get('commands', [])
        for command in commands:
            cmd_start = time.time()
            success, output = self.connection_manager.execute_command(device, command)
            cmd_time = time.time() - cmd_start
            
            cmd_result = CommandResult(
                command=command,
                output=output,
                success=success,
                error_message=None if success else output,
                execution_time=cmd_time
            )
            result.add_command_result(cmd_result)
            
            if success:
                # Analyze output based on workflow
                self._analyze_output(workflow_name, command, output, result)
        
        result.execution_time = time.time() - start_time
        result.summary = self._generate_summary(result)
        
        self.logger.info(f"Workflow '{workflow_name}' completed on {device.ip_address}")
        return result
    
    def run_multiple_workflows(
        self,
        device: Device,
        workflow_names: List[str]
    ) -> List[DiagnosticResult]:
        """
        Run multiple workflows on a device.
        
        Args:
            device: Device to diagnose
            workflow_names: List of workflow names
            
        Returns:
            List of DiagnosticResult objects
        """
        results = []
        for workflow_name in workflow_names:
            result = self.run_workflow(device, workflow_name)
            results.append(result)
        return results
    
    def _analyze_output(
        self,
        workflow_name: str,
        command: str,
        output: str,
        result: DiagnosticResult
    ) -> None:
        """Analyze command output and add issues to result"""
        
        if workflow_name == 'interface_health':
            self._analyze_interface_health(output, result)
        
        elif workflow_name == 'cpu_memory':
            self._analyze_cpu_memory(output, command, result)
        
        elif workflow_name == 'connectivity':
            self._analyze_connectivity(output, command, result)
        
        elif workflow_name == 'log_analysis':
            self._analyze_logs(output, result)
    
    def _analyze_interface_health(self, output: str, result: DiagnosticResult) -> None:
        """Analyze interface status output"""
        
        # Parse output for down interfaces
        lines = output.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            
            # Check for down interfaces
            if 'down' in line_lower and 'line protocol' in line_lower:
                # Extract interface name
                interface_match = re.search(r'(\S+)\s+is\s+(administratively\s+)?down', line, re.IGNORECASE)
                if interface_match:
                    interface_name = interface_match.group(1)
                    is_admin_down = bool(interface_match.group(2))
                    
                    severity = Severity.WARNING if is_admin_down else Severity.CRITICAL
                    description = f"Interface {interface_name} is "
                    description += "administratively down" if is_admin_down else "down"
                    
                    issue = Issue(
                        type='interface_down',
                        severity=severity,
                        description=description,
                        details={'interface': interface_name, 'admin_down': is_admin_down},
                        recommendation="Check interface configuration and physical connectivity"
                    )
                    result.add_issue(issue)
            
            # Check for error-disabled interfaces
            if 'err-disabled' in line_lower or 'error-disabled' in line_lower:
                interface_match = re.search(r'(\S+)', line)
                if interface_match:
                    interface_name = interface_match.group(1)
                    
                    issue = Issue(
                        type='interface_err_disabled',
                        severity=Severity.CRITICAL,
                        description=f"Interface {interface_name} is error-disabled",
                        details={'interface': interface_name},
                        recommendation="Check for port security violations or spanning tree issues"
                    )
                    result.add_issue(issue)
    
    def _analyze_cpu_memory(self, output: str, command: str, result: DiagnosticResult) -> None:
        """Analyze CPU and memory usage"""
        
        if 'cpu' in command.lower():
            # Extract CPU usage percentage (Cisco format)
            cpu_match = re.search(r'CPU utilization.*?(\d+)%', output, re.IGNORECASE)
            if not cpu_match:
                # Try alternative format
                cpu_match = re.search(r'(\d+)%\s+CPU', output, re.IGNORECASE)
            
            if cpu_match:
                cpu_usage = int(cpu_match.group(1))
                
                cpu_critical = self.thresholds.get('cpu_critical', 90)
                cpu_warning = self.thresholds.get('cpu_warning', 80)
                
                if cpu_usage >= cpu_critical:
                    issue = Issue(
                        type='high_cpu',
                        severity=Severity.CRITICAL,
                        description=f"Critical CPU usage: {cpu_usage}%",
                        details={'cpu_usage': cpu_usage, 'threshold': cpu_critical},
                        recommendation="Investigate high CPU processes and consider optimization"
                    )
                    result.add_issue(issue)
                
                elif cpu_usage >= cpu_warning:
                    issue = Issue(
                        type='high_cpu',
                        severity=Severity.WARNING,
                        description=f"High CPU usage: {cpu_usage}%",
                        details={'cpu_usage': cpu_usage, 'threshold': cpu_warning},
                        recommendation="Monitor CPU usage and investigate if sustained"
                    )
                    result.add_issue(issue)
        
        if 'memory' in command.lower():
            # Extract memory usage percentage
            mem_match = re.search(r'(\d+)%.*?used', output, re.IGNORECASE)
            if mem_match:
                mem_usage = int(mem_match.group(1))
                
                mem_critical = self.thresholds.get('memory_critical', 90)
                mem_warning = self.thresholds.get('memory_warning', 80)
                
                if mem_usage >= mem_critical:
                    issue = Issue(
                        type='high_memory',
                        severity=Severity.CRITICAL,
                        description=f"Critical memory usage: {mem_usage}%",
                        details={'memory_usage': mem_usage, 'threshold': mem_critical},
                        recommendation="Check for memory leaks and consider memory upgrade"
                    )
                    result.add_issue(issue)
                
                elif mem_usage >= mem_warning:
                    issue = Issue(
                        type='high_memory',
                        severity=Severity.WARNING,
                        description=f"High memory usage: {mem_usage}%",
                        details={'memory_usage': mem_usage, 'threshold': mem_warning},
                        recommendation="Monitor memory usage trends"
                    )
                    result.add_issue(issue)
    
    def _analyze_connectivity(self, output: str, command: str, result: DiagnosticResult) -> None:
        """Analyze connectivity-related output"""
        
        if 'route' in command.lower():
            # Check for default route
            if 'default' not in output.lower() and '0.0.0.0' not in output:
                issue = Issue(
                    type='no_default_route',
                    severity=Severity.WARNING,
                    description="No default route found",
                    recommendation="Configure default gateway if required"
                )
                result.add_issue(issue)
        
        if 'ping' in command.lower():
            # Check ping success
            if 'success rate is 0' in output.lower() or '0 received' in output.lower():
                issue = Issue(
                    type='ping_failure',
                    severity=Severity.CRITICAL,
                    description="Ping test failed",
                    recommendation="Check routing and connectivity to target"
                )
                result.add_issue(issue)
    
    def _analyze_logs(self, output: str, result: DiagnosticResult) -> None:
        """Analyze system logs for errors"""
        
        lines = output.split('\n')
        
        error_keywords = ['error', 'critical', 'alert', 'emergency', 'fail']
        warning_keywords = ['warning', 'notice']
        
        for line in lines:
            line_lower = line.lower()
            
            # Check for critical errors
            if any(keyword in line_lower for keyword in error_keywords):
                issue = Issue(
                    type='log_error',
                    severity=Severity.CRITICAL,
                    description=f"Error found in logs: {line.strip()}",
                    recommendation="Investigate and resolve error condition"
                )
                result.add_issue(issue)
            
            # Check for warnings
            elif any(keyword in line_lower for keyword in warning_keywords):
                issue = Issue(
                    type='log_warning',
                    severity=Severity.WARNING,
                    description=f"Warning found in logs: {line.strip()}",
                    recommendation="Review warning and take action if needed"
                )
                result.add_issue(issue)
    
    def _generate_summary(self, result: DiagnosticResult) -> str:
        """Generate summary text for diagnostic result"""
        
        if not result.success:
            return "Diagnostic workflow failed to execute"
        
        critical_count = len(result.get_critical_issues())
        warning_count = len(result.get_warning_issues())
        
        if critical_count > 0:
            return f"Found {critical_count} critical issue(s) and {warning_count} warning(s)"
        elif warning_count > 0:
            return f"Found {warning_count} warning(s), no critical issues"
        else:
            return "All checks passed, no issues found"
    
    def get_available_workflows(self) -> List[str]:
        """Get list of available workflow names"""
        return list(self.workflows.keys())
