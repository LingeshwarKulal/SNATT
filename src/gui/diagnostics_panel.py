"""
Diagnostics Panel
Device troubleshooting and diagnostics interface
"""

import customtkinter as ctk
import logging
from typing import List, Callable
import threading
from datetime import datetime

from models.device import Device
from models.diagnostic_result import DiagnosticResult, Severity


class DiagnosticsPanel(ctk.CTkFrame):
    """Diagnostics and troubleshooting panel"""
    
    def __init__(self, parent, troubleshooting_engine, connection_manager, status_callback: Callable = None):
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.troubleshooting_engine = troubleshooting_engine
        self.connection_manager = connection_manager
        self.status_callback = status_callback
        
        self.diagnostic_results: List[DiagnosticResult] = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup user interface"""
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="🧰 Device Diagnostics",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Control frame
        self._create_control_frame()
        
        # Results frame
        self._create_results_frame()
        
        # Actions frame
        self._create_actions_frame()
    
    def _create_control_frame(self):
        """Create control frame"""
        
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(3, weight=1)
        
        # Device selection
        device_label = ctk.CTkLabel(
            control_frame,
            text="Select Device:",
            font=ctk.CTkFont(size=14)
        )
        device_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.device_dropdown = ctk.CTkComboBox(
            control_frame,
            values=["No devices connected"],
            width=200,
            state="readonly"
        )
        self.device_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Workflow selection
        workflow_label = ctk.CTkLabel(
            control_frame,
            text="Workflow:",
            font=ctk.CTkFont(size=14)
        )
        workflow_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        workflows = self.troubleshooting_engine.get_available_workflows()
        workflow_names = [wf.replace('_', ' ').title() for wf in workflows]
        
        self.workflow_dropdown = ctk.CTkComboBox(
            control_frame,
            values=workflow_names if workflow_names else ["No workflows"],
            width=200,
            state="readonly"
        )
        self.workflow_dropdown.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        if workflow_names:
            self.workflow_dropdown.set(workflow_names[0])
        
        # Run button
        self.run_button = ctk.CTkButton(
            control_frame,
            text="▶️ Run Diagnostics",
            command=self._on_run_diagnostics,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("green", "darkgreen")
        )
        self.run_button.grid(row=0, column=4, padx=10, pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(control_frame)
        self.progress_bar.grid(row=1, column=0, columnspan=5, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            control_frame,
            text="Select a device and workflow to begin",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=2, column=0, columnspan=5, padx=10, pady=(0, 10))
    
    def _create_results_frame(self):
        """Create results display frame"""
        
        results_frame = ctk.CTkFrame(self)
        results_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        # Results header
        header_frame = ctk.CTkFrame(results_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        self.results_header_label = ctk.CTkLabel(
            header_frame,
            text="Diagnostic Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.results_header_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Summary stats
        self.summary_frame = ctk.CTkFrame(header_frame)
        self.summary_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        self.critical_label = ctk.CTkLabel(
            self.summary_frame,
            text="🔴 Critical: 0",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.critical_label.pack(side="left", padx=10)
        
        self.warning_label = ctk.CTkLabel(
            self.summary_frame,
            text="🟡 Warnings: 0",
            font=ctk.CTkFont(size=12),
            text_color="orange"
        )
        self.warning_label.pack(side="left", padx=10)
        
        self.info_label = ctk.CTkLabel(
            self.summary_frame,
            text="🟢 Info: 0",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.info_label.pack(side="left", padx=10)
        
        # Results display (scrollable)
        self.results_textbox = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.results_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def _create_actions_frame(self):
        """Create actions frame"""
        
        actions_frame = ctk.CTkFrame(self)
        actions_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Run All button
        run_all_btn = ctk.CTkButton(
            actions_frame,
            text="▶️ Run All Workflows",
            command=self._on_run_all_workflows,
            width=150,
            fg_color=("green", "darkgreen")
        )
        run_all_btn.pack(side="left", padx=5, pady=10)
        
        # Clear button
        clear_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Clear Results",
            command=self._clear_results,
            width=150
        )
        clear_btn.pack(side="left", padx=5, pady=10)
        
        # Export button
        export_btn = ctk.CTkButton(
            actions_frame,
            text="💾 Export Results",
            command=self._export_results,
            width=150
        )
        export_btn.pack(side="left", padx=5, pady=10)
        
        # View Raw Output button
        raw_btn = ctk.CTkButton(
            actions_frame,
            text="📋 View Raw Output",
            command=self._view_raw_output,
            width=150
        )
        raw_btn.pack(side="left", padx=5, pady=10)
        
        # Refresh Devices button
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Refresh Devices",
            command=self.refresh_devices,
            width=150
        )
        refresh_btn.pack(side="right", padx=5, pady=10)
    
    def _on_run_diagnostics(self):
        """Handle run diagnostics button click"""
        
        device_str = self.device_dropdown.get()
        workflow_name = self.workflow_dropdown.get()
        
        if device_str == "No devices connected":
            self._show_error("No devices connected. Please connect devices first.")
            return
        
        if workflow_name == "No workflows":
            self._show_error("No workflows available")
            return
        
        # Get device IP from dropdown text
        device_ip = device_str.split()[0] if device_str else None
        if not device_ip:
            self._show_error("Invalid device selection")
            return
        
        # Find device object
        connected_devices = self._get_connected_devices()
        device = next((d for d in connected_devices if d.ip_address == device_ip), None)
        
        if not device:
            self._show_error("Device not found")
            return
        
        # Convert workflow name back to key
        workflow_key = workflow_name.lower().replace(' ', '_')
        
        # Run diagnostics in background
        self.run_button.configure(state="disabled", text="⏳ Running...")
        self.progress_bar.set(0)
        
        thread = threading.Thread(
            target=self._run_diagnostic_workflow,
            args=(device, workflow_key, workflow_name)
        )
        thread.daemon = True
        thread.start()
    
    def _run_diagnostic_workflow(self, device: Device, workflow_key: str, workflow_name: str):
        """Run diagnostic workflow in background"""
        
        try:
            self._update_status(f"Running {workflow_name} on {device.ip_address}...")
            self.after(0, lambda: self.progress_bar.set(0.3))
            
            # Execute workflow
            result = self.troubleshooting_engine.run_workflow(device, workflow_key)
            self.diagnostic_results.append(result)
            
            self.after(0, lambda: self.progress_bar.set(0.7))
            
            # Update UI on main thread
            self.after(0, lambda: self._display_result(result))
            self.after(0, lambda: self._update_summary())
            self.after(0, lambda: self.progress_bar.set(1.0))
            
            if result.success:
                self._update_status(f"✅ Diagnostics completed: {result.summary}")
            else:
                self._update_status(f"❌ Diagnostics failed: {result.summary}")
        
        except Exception as e:
            self.logger.error(f"Error running diagnostics: {e}", exc_info=True)
            self.after(0, lambda: self._show_error(f"Diagnostics failed: {str(e)}"))
        
        finally:
            self.after(0, lambda: self.run_button.configure(state="normal", text="▶️ Run Diagnostics"))
    
    def _display_result(self, result: DiagnosticResult):
        """Display diagnostic result"""
        
        # Clear previous results
        self.results_textbox.delete("1.0", "end")
        
        # Header
        self.results_textbox.insert("end", "="*80 + "\n", "header")
        self.results_textbox.insert("end", f"DIAGNOSTIC RESULT - {result.workflow_name}\n", "header")
        self.results_textbox.insert("end", "="*80 + "\n\n", "header")
        
        # Device info
        self.results_textbox.insert("end", f"Device: {result.device_hostname or result.device_ip}\n")
        self.results_textbox.insert("end", f"IP Address: {result.device_ip}\n")
        self.results_textbox.insert("end", f"Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.results_textbox.insert("end", f"Execution Time: {result.execution_time:.2f}s\n")
        self.results_textbox.insert("end", f"Overall Severity: {result.overall_severity.value.upper()}\n\n")
        
        # Summary
        self.results_textbox.insert("end", "SUMMARY\n", "section")
        self.results_textbox.insert("end", "-"*80 + "\n")
        self.results_textbox.insert("end", f"{result.summary}\n\n")
        
        # Issues
        if result.issues:
            self.results_textbox.insert("end", f"ISSUES FOUND ({len(result.issues)})\n", "section")
            self.results_textbox.insert("end", "-"*80 + "\n")
            
            for idx, issue in enumerate(result.issues, 1):
                severity_icon = self._get_severity_icon(issue.severity)
                severity_tag = f"severity_{issue.severity.value}"
                
                self.results_textbox.insert("end", f"\n{idx}. {severity_icon} ", severity_tag)
                self.results_textbox.insert("end", f"[{issue.severity.value.upper()}] ", severity_tag)
                self.results_textbox.insert("end", f"{issue.type}\n")
                self.results_textbox.insert("end", f"   Description: {issue.description}\n")
                
                if issue.recommendation:
                    self.results_textbox.insert("end", f"   Recommendation: {issue.recommendation}\n")
                
                if issue.details:
                    self.results_textbox.insert("end", f"   Details: {issue.details}\n")
        else:
            self.results_textbox.insert("end", "✅ No issues found - All checks passed!\n\n", "success")
        
        # Configure tags for coloring
        self.results_textbox.tag_config("header", font=("Consolas", 12, "bold"))
        self.results_textbox.tag_config("section", font=("Consolas", 12, "bold"))
        self.results_textbox.tag_config("severity_critical", foreground="red")
        self.results_textbox.tag_config("severity_warning", foreground="orange")
        self.results_textbox.tag_config("severity_info", foreground="blue")
        self.results_textbox.tag_config("success", foreground="green")
    
    def _get_severity_icon(self, severity: Severity) -> str:
        """Get icon for severity"""
        icons = {
            Severity.CRITICAL: "🔴",
            Severity.WARNING: "🟡",
            Severity.INFO: "🔵",
            Severity.NORMAL: "🟢"
        }
        return icons.get(severity, "⚪")
    
    def _update_summary(self):
        """Update summary statistics"""
        
        critical_count = sum(len(r.get_critical_issues()) for r in self.diagnostic_results)
        warning_count = sum(len(r.get_warning_issues()) for r in self.diagnostic_results)
        info_count = sum(len(r.issues) - len(r.get_critical_issues()) - len(r.get_warning_issues()) 
                        for r in self.diagnostic_results)
        
        self.critical_label.configure(text=f"🔴 Critical: {critical_count}")
        self.warning_label.configure(text=f"🟡 Warnings: {warning_count}")
        self.info_label.configure(text=f"🟢 Info: {info_count}")
    
    def _on_run_all_workflows(self):
        """Run all available workflows"""
        
        device_str = self.device_dropdown.get()
        
        if device_str == "No devices connected":
            self._show_error("No devices connected")
            return
        
        device_ip = device_str.split()[0]
        connected_devices = self._get_connected_devices()
        device = next((d for d in connected_devices if d.ip_address == device_ip), None)
        
        if not device:
            self._show_error("Device not found")
            return
        
        workflows = self.troubleshooting_engine.get_available_workflows()
        
        # Run in background
        thread = threading.Thread(target=self._run_all_workflows, args=(device, workflows))
        thread.daemon = True
        thread.start()
    
    def _run_all_workflows(self, device: Device, workflows: List[str]):
        """Run all workflows on a device"""
        
        self.after(0, lambda: self.run_button.configure(state="disabled"))
        
        for idx, workflow in enumerate(workflows):
            progress = (idx + 1) / len(workflows)
            self.after(0, lambda p=progress: self.progress_bar.set(p))
            
            workflow_name = workflow.replace('_', ' ').title()
            self._update_status(f"Running {workflow_name}...")
            
            result = self.troubleshooting_engine.run_workflow(device, workflow)
            self.diagnostic_results.append(result)
        
        self.after(0, lambda: self._update_status(f"Completed all workflows!"))
        self.after(0, lambda: self._update_summary())
        self.after(0, lambda: self.run_button.configure(state="normal"))
    
    def _clear_results(self):
        """Clear all results"""
        self.results_textbox.delete("1.0", "end")
        self.diagnostic_results.clear()
        self._update_summary()
        self._update_status("Results cleared")
    
    def _export_results(self):
        """Export results to file"""
        if not self.diagnostic_results:
            self._show_error("No results to export")
            return
        
        from pathlib import Path
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"diagnostic_results_{timestamp}.txt"
        filepath = Path("reports") / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for result in self.diagnostic_results:
                    f.write(f"{'='*80}\n")
                    f.write(f"Device: {result.device_ip}\n")
                    f.write(f"Workflow: {result.workflow_name}\n")
                    f.write(f"Timestamp: {result.timestamp}\n")
                    f.write(f"Severity: {result.overall_severity.value}\n")
                    f.write(f"Summary: {result.summary}\n")
                    f.write(f"\nIssues ({len(result.issues)}):\n")
                    
                    for issue in result.issues:
                        f.write(f"  - [{issue.severity.value}] {issue.description}\n")
                    
                    f.write(f"\n")
            
            self._update_status(f"Results exported to {filepath}")
        except Exception as e:
            self._show_error(f"Export failed: {str(e)}")
    
    def _view_raw_output(self):
        """View raw command output"""
        if not self.diagnostic_results:
            self._show_error("No results available")
            return
        
        # Create dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Raw Command Output")
        dialog.geometry("800x600")
        
        textbox = ctk.CTkTextbox(dialog, font=("Consolas", 10))
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        for result in self.diagnostic_results:
            textbox.insert("end", f"{'='*80}\n")
            textbox.insert("end", f"Device: {result.device_ip}\n")
            textbox.insert("end", f"Workflow: {result.workflow_name}\n\n")
            
            for cmd_result in result.command_results:
                textbox.insert("end", f"Command: {cmd_result.command}\n")
                textbox.insert("end", f"{'-'*80}\n")
                textbox.insert("end", f"{cmd_result.output}\n\n")
    
    def refresh_devices(self):
        """Refresh connected devices list"""
        connected_devices = self._get_connected_devices()
        
        if connected_devices:
            device_strings = [
                f"{d.ip_address} ({d.hostname or 'Unknown'})" 
                for d in connected_devices
            ]
            self.device_dropdown.configure(values=device_strings)
            self.device_dropdown.set(device_strings[0])
            self._update_status(f"Found {len(connected_devices)} connected device(s)")
        else:
            self.device_dropdown.configure(values=["No devices connected"])
            self.device_dropdown.set("No devices connected")
            self._update_status("No connected devices found")
    
    def _get_connected_devices(self) -> List[Device]:
        """Get list of connected devices"""
        # This would typically come from the discovery panel or device manager
        # For now, we'll get it from the connection manager
        connected_ips = self.connection_manager.get_connected_devices()
        
        # Create minimal device objects for connected IPs
        devices = []
        for ip in connected_ips:
            device = Device(ip_address=ip)
            devices.append(device)
        
        return devices
    
    def _update_status(self, message: str):
        """Update status label"""
        self.status_label.configure(text=message)
        if self.status_callback:
            self.status_callback(message)
    
    def _show_error(self, message: str):
        """Show error message"""
        self.status_label.configure(text=f"❌ {message}", text_color="red")
        self.logger.error(message)
    
    def display_results(self):
        """Display all diagnostic results in the textbox"""
        if not self.diagnostic_results:
            return
        
        self.results_textbox.delete("1.0", "end")
        
        for result in self.diagnostic_results:
            # Header
            self.results_textbox.insert("end", f"{'='*80}\n", "header")
            self.results_textbox.insert("end", f"🖥️  Device: {result.device_hostname} ({result.device_ip})\n", "header")
            self.results_textbox.insert("end", f"🔧 Workflow: {result.workflow_name}\n", "section")
            self.results_textbox.insert("end", f"📅 Time: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Severity
            severity_icon = self._get_severity_icon(result.overall_severity)
            severity_text = result.overall_severity.value.upper()
            severity_tag = f"severity_{result.overall_severity.value}"
            self.results_textbox.insert("end", f"{severity_icon} Overall Status: {severity_text}\n", severity_tag)
            self.results_textbox.insert("end", f"📝 Summary: {result.summary}\n\n")
            
            # Issues
            if result.issues:
                self.results_textbox.insert("end", f"Issues Found ({len(result.issues)}):\n", "section")
                for issue in result.issues:
                    issue_icon = self._get_severity_icon(issue.severity)
                    issue_tag = f"severity_{issue.severity.value}"
                    self.results_textbox.insert("end", f"  {issue_icon} [{issue.type.upper()}] ", issue_tag)
                    self.results_textbox.insert("end", f"{issue.description}\n")
                    if issue.recommendation:
                        self.results_textbox.insert("end", f"      💡 Recommendation: {issue.recommendation}\n", "info")
                self.results_textbox.insert("end", "\n")
            else:
                self.results_textbox.insert("end", "  ✅ No issues found\n\n", "success")
        
        # Update summary
        self._update_summary()
        self._update_status(f"Displaying {len(self.diagnostic_results)} diagnostic result(s)")
    
    def get_diagnostic_results(self) -> List[DiagnosticResult]:
        """Get all diagnostic results"""
        return self.diagnostic_results
