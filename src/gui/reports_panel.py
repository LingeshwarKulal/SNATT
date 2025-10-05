"""
Reports Panel
Network reporting and analytics interface
"""

import customtkinter as ctk
import logging
from typing import Callable, List
import threading
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import sys

from models.device import Device


class ReportsPanel(ctk.CTkFrame):
    """Network reports and analytics panel"""
    
    def __init__(self, parent, reporting_engine, connection_manager, status_callback: Callable = None):
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.reporting_engine = reporting_engine
        self.connection_manager = connection_manager
        self.status_callback = status_callback
        
        self.generated_reports: List[Path] = []
        
        self._setup_ui()
        self._load_existing_reports()
    
    def _setup_ui(self):
        """Setup user interface"""
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="📊 Network Reports",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        
        # Left side - Report generation
        self._create_generation_panel()
        
        # Right side - Report history
        self._create_history_panel()
    
    def _create_generation_panel(self):
        """Create report generation panel"""
        
        gen_frame = ctk.CTkFrame(self)
        gen_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        gen_frame.grid_columnconfigure(0, weight=1)
        gen_frame.grid_rowconfigure(4, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            gen_frame,
            text="Generate New Report",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Report type selection
        type_frame = ctk.CTkFrame(gen_frame)
        type_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            type_frame,
            text="Report Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.report_types = {
            "Network Health": "Comprehensive network health assessment with device status and diagnostics",
            "Device Inventory": "Complete inventory of all discovered devices with details",
            "Configuration Audit": "Configuration backup status and compliance report",
            "Troubleshooting Summary": "Summary of all diagnostic activities and issues found",
            "Performance Metrics": "Device performance metrics (CPU, memory, uptime)",
            "Change Log": "Recent configuration changes and backup history"
        }
        
        self.selected_report_type = ctk.StringVar(value="Network Health")
        
        for report_type, description in self.report_types.items():
            frame = ctk.CTkFrame(type_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            radio = ctk.CTkRadioButton(
                frame,
                text=report_type,
                variable=self.selected_report_type,
                value=report_type,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=self._update_report_description
            )
            radio.pack(anchor="w", padx=5, pady=2)
            
            desc_label = ctk.CTkLabel(
                frame,
                text=description,
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            desc_label.pack(anchor="w", padx=25, pady=2)
        
        # Date range selection
        date_frame = ctk.CTkFrame(gen_frame)
        date_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        date_frame.grid_columnconfigure(1, weight=1)
        date_frame.grid_columnconfigure(3, weight=1)
        
        ctk.CTkLabel(
            date_frame,
            text="Date Range:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(date_frame, text="From:").grid(row=1, column=0, padx=10, pady=5)
        self.from_date_entry = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD")
        self.from_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.from_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        
        ctk.CTkLabel(date_frame, text="To:").grid(row=1, column=2, padx=10, pady=5)
        self.to_date_entry = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD")
        self.to_date_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        self.to_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Quick date buttons
        quick_date_frame = ctk.CTkFrame(date_frame)
        quick_date_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=5)
        
        ctk.CTkButton(
            quick_date_frame,
            text="Last 7 Days",
            command=lambda: self._set_date_range(7),
            width=100
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            quick_date_frame,
            text="Last 30 Days",
            command=lambda: self._set_date_range(30),
            width=100
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            quick_date_frame,
            text="Last 90 Days",
            command=lambda: self._set_date_range(90),
            width=100
        ).pack(side="left", padx=2)
        
        # Format selection
        format_frame = ctk.CTkFrame(gen_frame)
        format_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            format_frame,
            text="Output Format:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.format_var = ctk.StringVar(value="excel")
        
        format_options_frame = ctk.CTkFrame(format_frame)
        format_options_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkRadioButton(
            format_options_frame,
            text="📊 Excel (.xlsx)",
            variable=self.format_var,
            value="excel"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            format_options_frame,
            text="📄 CSV (.csv)",
            variable=self.format_var,
            value="csv"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            format_options_frame,
            text="📝 PDF (.pdf)",
            variable=self.format_var,
            value="pdf"
        ).pack(side="left", padx=10)
        
        # Description area
        desc_area_frame = ctk.CTkFrame(gen_frame)
        desc_area_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        desc_area_frame.grid_columnconfigure(0, weight=1)
        desc_area_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            desc_area_frame,
            text="Report Description:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.report_description = ctk.CTkTextbox(
            desc_area_frame,
            height=100,
            font=ctk.CTkFont(size=11)
        )
        self.report_description.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self._update_report_description()
        
        # Generate button
        button_frame = ctk.CTkFrame(gen_frame)
        button_frame.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
        
        self.generate_button = ctk.CTkButton(
            button_frame,
            text="📊 Generate Report",
            command=self._on_generate_report,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("green", "darkgreen")
        )
        self.generate_button.pack(fill="x", padx=10, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(button_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            button_frame,
            text="Ready to generate report",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
    
    def _create_history_panel(self):
        """Create report history panel"""
        
        history_frame = ctk.CTkFrame(self)
        history_frame.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(history_frame)
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="Generated Reports",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=5)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄",
            command=self._load_existing_reports,
            width=40
        )
        refresh_btn.grid(row=0, column=1, padx=5)
        
        # Reports list
        self.reports_list_frame = ctk.CTkScrollableFrame(history_frame)
        self.reports_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Actions
        actions_frame = ctk.CTkFrame(history_frame)
        actions_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkButton(
            actions_frame,
            text="📂 Open Reports Folder",
            command=self._open_reports_folder,
            width=180
        ).pack(pady=5)
        
        ctk.CTkButton(
            actions_frame,
            text="🗑️ Clear Old Reports",
            command=self._clear_old_reports,
            width=180
        ).pack(pady=5)
    
    def _update_report_description(self):
        """Update report description based on selected type"""
        report_type = self.selected_report_type.get()
        description = self.report_types.get(report_type, "")
        
        self.report_description.delete("1.0", "end")
        self.report_description.insert("1.0", description)
    
    def _set_date_range(self, days: int):
        """Set date range to last N days"""
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)
        
        self.from_date_entry.delete(0, "end")
        self.from_date_entry.insert(0, from_date.strftime('%Y-%m-%d'))
        
        self.to_date_entry.delete(0, "end")
        self.to_date_entry.insert(0, to_date.strftime('%Y-%m-%d'))
    
    def _on_generate_report(self):
        """Handle generate report button click"""
        
        report_type = self.selected_report_type.get()
        output_format = self.format_var.get()
        
        try:
            from_date = datetime.strptime(self.from_date_entry.get(), '%Y-%m-%d')
            to_date = datetime.strptime(self.to_date_entry.get(), '%Y-%m-%d')
        except ValueError:
            self._show_error("Invalid date format. Use YYYY-MM-DD")
            return
        
        # Generate in background
        self.generate_button.configure(state="disabled", text="⏳ Generating...")
        
        thread = threading.Thread(
            target=self._generate_report,
            args=(report_type, output_format, from_date, to_date)
        )
        thread.daemon = True
        thread.start()
    
    def _generate_report(self, report_type: str, output_format: str, from_date: datetime, to_date: datetime):
        """Generate report in background"""
        
        try:
            self._update_status(f"Generating {report_type} report...")
            self.after(0, lambda: self.progress_bar.set(0.2))
            
            # Get data based on report type
            if report_type == "Network Health":
                devices = self._get_all_devices()
                self.after(0, lambda: self.progress_bar.set(0.5))
                
                # Generate report
                report_path = self.reporting_engine.generate_network_health_report(
                    devices,
                    output_format=output_format
                )
            
            elif report_type == "Device Inventory":
                devices = self._get_all_devices()
                self.after(0, lambda: self.progress_bar.set(0.5))
                
                report_path = self.reporting_engine.generate_inventory_report(
                    devices,
                    output_format=output_format
                )
            
            else:
                # For other report types, use a generic report
                self.after(0, lambda: self.progress_bar.set(0.5))
                report_path = self._generate_generic_report(report_type, output_format)
            
            self.after(0, lambda: self.progress_bar.set(1.0))
            self.generated_reports.append(Path(report_path))
            
            self.after(0, lambda: self._update_status(f"✅ Report generated: {Path(report_path).name}"))
            self.after(0, self._load_existing_reports)
            
            # Ask to open
            self.after(0, lambda: self._ask_open_report(report_path))
        
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}", exc_info=True)
            self.after(0, lambda: self._show_error(f"Report generation failed: {str(e)}"))
        
        finally:
            self.after(0, lambda: self.generate_button.configure(state="normal", text="📊 Generate Report"))
    
    def _generate_generic_report(self, report_type: str, output_format: str) -> str:
        """Generate a generic report (placeholder)"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_type.replace(' ', '_')}_{timestamp}.{output_format}"
        filepath = Path("reports") / filename
        
        # Create simple report
        if output_format == "csv":
            with open(filepath, 'w') as f:
                f.write(f"Report Type,{report_type}\n")
                f.write(f"Generated,{datetime.now()}\n")
                f.write("\nThis report type is under development.\n")
        else:
            with open(filepath, 'w') as f:
                f.write(f"Report: {report_type}\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write("\nThis report type is under development.\n")
        
        return str(filepath)
    
    def _load_existing_reports(self):
        """Load existing reports from reports directory"""
        
        # Clear existing list
        for widget in self.reports_list_frame.winfo_children():
            widget.destroy()
        
        reports_dir = Path("reports")
        if not reports_dir.exists():
            reports_dir.mkdir(parents=True, exist_ok=True)
            no_reports_label = ctk.CTkLabel(
                self.reports_list_frame,
                text="No reports generated yet",
                font=ctk.CTkFont(size=12)
            )
            no_reports_label.pack(pady=20)
            return
        
        # Find all report files
        report_files = []
        for ext in ['*.xlsx', '*.csv', '*.pdf', '*.txt']:
            report_files.extend(reports_dir.glob(ext))
        
        if not report_files:
            no_reports_label = ctk.CTkLabel(
                self.reports_list_frame,
                text="No reports found",
                font=ctk.CTkFont(size=12)
            )
            no_reports_label.pack(pady=20)
            return
        
        # Sort by modification time (newest first)
        report_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Display each report
        for report_file in report_files:
            self._create_report_item(report_file)
    
    def _create_report_item(self, report_file: Path):
        """Create a report item widget"""
        
        item_frame = ctk.CTkFrame(self.reports_list_frame)
        item_frame.pack(fill="x", padx=5, pady=5)
        
        # Icon based on file type
        icon = "📊" if report_file.suffix == ".xlsx" else "📄" if report_file.suffix == ".csv" else "📝"
        
        # Info
        info_frame = ctk.CTkFrame(item_frame)
        info_frame.pack(fill="x", padx=5, pady=5)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{icon} {report_file.name}",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        name_label.pack(anchor="w", padx=5)
        
        # File info
        mtime = datetime.fromtimestamp(report_file.stat().st_mtime)
        size_kb = report_file.stat().st_size / 1024
        
        details_label = ctk.CTkLabel(
            info_frame,
            text=f"{mtime.strftime('%Y-%m-%d %H:%M')} • {size_kb:.1f} KB",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        details_label.pack(anchor="w", padx=5)
        
        # Actions
        actions_frame = ctk.CTkFrame(item_frame)
        actions_frame.pack(fill="x", padx=5, pady=2)
        
        open_btn = ctk.CTkButton(
            actions_frame,
            text="📂 Open",
            command=lambda: self._open_report(report_file),
            width=70,
            height=25
        )
        open_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            command=lambda: self._delete_report(report_file),
            width=40,
            height=25,
            fg_color="red"
        )
        delete_btn.pack(side="left", padx=2)
    
    def _ask_open_report(self, report_path: str):
        """Ask user if they want to open the report"""
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Report Generated")
        dialog.geometry("400x150")
        
        ctk.CTkLabel(
            dialog,
            text="Report generated successfully!",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialog,
            text=Path(report_path).name
        ).pack(pady=5)
        
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Open Report",
            command=lambda: [self._open_report(Path(report_path)), dialog.destroy()]
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Close",
            command=dialog.destroy
        ).pack(side="left", padx=5)
    
    def _open_report(self, report_file: Path):
        """Open report file with default application"""
        
        try:
            if sys.platform == 'win32':
                subprocess.run(['start', '', str(report_file)], shell=True, check=True)
            elif sys.platform == 'darwin':
                subprocess.run(['open', str(report_file)], check=True)
            else:
                subprocess.run(['xdg-open', str(report_file)], check=True)
            
            self._update_status(f"Opened report: {report_file.name}")
        except Exception as e:
            self._show_error(f"Could not open report: {str(e)}")
    
    def _delete_report(self, report_file: Path):
        """Delete a report file"""
        
        try:
            report_file.unlink()
            self._update_status(f"Deleted report: {report_file.name}")
            self._load_existing_reports()
        except Exception as e:
            self._show_error(f"Could not delete report: {str(e)}")
    
    def _open_reports_folder(self):
        """Open the reports folder in file explorer"""
        
        reports_dir = Path("reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if sys.platform == 'win32':
                subprocess.run(['explorer', str(reports_dir)], check=True)
            elif sys.platform == 'darwin':
                subprocess.run(['open', str(reports_dir)], check=True)
            else:
                subprocess.run(['xdg-open', str(reports_dir)], check=True)
        except Exception as e:
            self._show_error(f"Could not open folder: {str(e)}")
    
    def _clear_old_reports(self):
        """Clear reports older than 30 days"""
        
        try:
            reports_dir = Path("reports")
            if not reports_dir.exists():
                return
            
            cutoff_date = datetime.now() - timedelta(days=30)
            deleted_count = 0
            
            for report_file in reports_dir.iterdir():
                if report_file.is_file():
                    mtime = datetime.fromtimestamp(report_file.stat().st_mtime)
                    if mtime < cutoff_date:
                        report_file.unlink()
                        deleted_count += 1
            
            self._update_status(f"Cleared {deleted_count} old report(s)")
            self._load_existing_reports()
        
        except Exception as e:
            self._show_error(f"Could not clear old reports: {str(e)}")
    
    def _get_all_devices(self) -> List[Device]:
        """Get all devices (connected or discovered)"""
        # This would ideally come from a device manager or discovery panel
        connected_ips = self.connection_manager.get_connected_devices()
        devices = [Device(ip_address=ip) for ip in connected_ips]
        return devices
    
    def _update_status(self, message: str):
        """Update status message"""
        self.status_label.configure(text=message)
        if self.status_callback:
            self.status_callback(message)
    
    def _show_error(self, message: str):
        """Show error message"""
        self.status_label.configure(text=f"❌ {message}", text_color="red")
        self.logger.error(message)
