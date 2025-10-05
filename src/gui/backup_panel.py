"""
Backup Panel
Configuration backup management interface
"""

import customtkinter as ctk
import logging
from typing import List, Callable
import threading
from datetime import datetime
from pathlib import Path

from models.device import Device
from models.backup_record import BackupRecord


class BackupPanel(ctk.CTkFrame):
    """Configuration backup management panel"""
    
    def __init__(self, parent, backup_manager, connection_manager, status_callback: Callable = None):
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.backup_manager = backup_manager
        self.connection_manager = connection_manager
        self.status_callback = status_callback
        
        self.selected_devices: List[Device] = []
        self.backup_history: List[BackupRecord] = []
        
        self._setup_ui()
        self._load_backup_history()
    
    def _setup_ui(self):
        """Setup user interface"""
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="💾 Configuration Backup",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Control frame
        self._create_control_frame()
        
        # Main content (tabview)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Add tabs
        self.tabview.add("Backup")
        self.tabview.add("History")
        self.tabview.add("Compare")
        
        # Setup each tab
        self._setup_backup_tab()
        self._setup_history_tab()
        self._setup_compare_tab()
    
    def _create_control_frame(self):
        """Create top control frame"""
        
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)
        
        # Refresh devices button
        refresh_btn = ctk.CTkButton(
            control_frame,
            text="🔄 Refresh Devices",
            command=self._refresh_devices,
            width=150
        )
        refresh_btn.pack(side="right", padx=5, pady=10)
    
    def _setup_backup_tab(self):
        """Setup backup creation tab"""
        
        tab = self.tabview.tab("Backup")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        # Options frame
        options_frame = ctk.CTkFrame(tab)
        options_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        options_frame.grid_columnconfigure(1, weight=1)
        
        # Config type selection
        type_label = ctk.CTkLabel(
            options_frame,
            text="Configuration Type:",
            font=ctk.CTkFont(size=14)
        )
        type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.config_type_var = ctk.StringVar(value="running")
        
        running_radio = ctk.CTkRadioButton(
            options_frame,
            text="Running Config",
            variable=self.config_type_var,
            value="running"
        )
        running_radio.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        startup_radio = ctk.CTkRadioButton(
            options_frame,
            text="Startup Config",
            variable=self.config_type_var,
            value="startup"
        )
        startup_radio.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        both_radio = ctk.CTkRadioButton(
            options_frame,
            text="Both",
            variable=self.config_type_var,
            value="both"
        )
        both_radio.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        
        # Auto-backup toggle
        self.auto_backup_var = ctk.BooleanVar(value=False)
        auto_backup_check = ctk.CTkCheckBox(
            options_frame,
            text="Enable Auto-Backup (Daily)",
            variable=self.auto_backup_var,
            command=self._toggle_auto_backup
        )
        auto_backup_check.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Device selection frame
        device_frame = ctk.CTkFrame(tab)
        device_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        device_frame.grid_columnconfigure(0, weight=1)
        device_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        device_header = ctk.CTkLabel(
            device_frame,
            text="Select Devices to Backup:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        device_header.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Select all button
        select_all_frame = ctk.CTkFrame(device_frame)
        select_all_frame.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        select_all_btn = ctk.CTkButton(
            select_all_frame,
            text="Select All",
            command=self._select_all_devices,
            width=100
        )
        select_all_btn.pack(side="left", padx=2)
        
        deselect_all_btn = ctk.CTkButton(
            select_all_frame,
            text="Deselect All",
            command=self._deselect_all_devices,
            width=100
        )
        deselect_all_btn.pack(side="left", padx=2)
        
        # Device list (scrollable)
        self.device_list_frame = ctk.CTkScrollableFrame(device_frame)
        self.device_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.device_checkboxes = []
        
        # Actions frame
        actions_frame = ctk.CTkFrame(tab)
        actions_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        # Backup button
        self.backup_button = ctk.CTkButton(
            actions_frame,
            text="💾 Backup Selected Devices",
            command=self._on_backup_devices,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("green", "darkgreen")
        )
        self.backup_button.pack(side="left", padx=5, pady=10)
        
        # Progress bar
        self.backup_progress = ctk.CTkProgressBar(actions_frame)
        self.backup_progress.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.backup_progress.set(0)
        
        # Status label
        self.backup_status_label = ctk.CTkLabel(
            actions_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.backup_status_label.pack(side="right", padx=10, pady=10)
    
    def _setup_history_tab(self):
        """Setup backup history tab"""
        
        tab = self.tabview.tab("History")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        # Controls
        controls_frame = ctk.CTkFrame(tab)
        controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Filter by device
        filter_label = ctk.CTkLabel(
            controls_frame,
            text="Filter by Device:",
            font=ctk.CTkFont(size=12)
        )
        filter_label.pack(side="left", padx=5)
        
        self.filter_dropdown = ctk.CTkComboBox(
            controls_frame,
            values=["All Devices"],
            command=self._filter_history,
            width=200
        )
        self.filter_dropdown.pack(side="left", padx=5)
        
        # Cleanup button
        cleanup_btn = ctk.CTkButton(
            controls_frame,
            text="🗑️ Cleanup Old Backups",
            command=self._cleanup_old_backups,
            width=150
        )
        cleanup_btn.pack(side="right", padx=5)
        
        # History table
        self.history_frame = ctk.CTkScrollableFrame(tab)
        self.history_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Table header
        header_frame = ctk.CTkFrame(self.history_frame)
        header_frame.pack(fill="x", pady=5)
        
        headers = ["Device", "Config Type", "Timestamp", "Size", "Actions"]
        widths = [150, 120, 180, 100, 200]
        
        for header, width in zip(headers, widths):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width
            )
            label.pack(side="left", padx=5)
        
        # History rows container
        self.history_rows_frame = ctk.CTkFrame(self.history_frame)
        self.history_rows_frame.pack(fill="both", expand=True)
    
    def _setup_compare_tab(self):
        """Setup configuration compare tab"""
        
        tab = self.tabview.tab("Compare")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        # Controls
        controls_frame = ctk.CTkFrame(tab)
        controls_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # First config selection
        ctk.CTkLabel(controls_frame, text="Config 1:").pack(side="left", padx=5)
        self.compare_config1_dropdown = ctk.CTkComboBox(
            controls_frame,
            values=["Select backup..."],
            width=250
        )
        self.compare_config1_dropdown.pack(side="left", padx=5)
        
        # Second config selection
        ctk.CTkLabel(controls_frame, text="Config 2:").pack(side="left", padx=5)
        self.compare_config2_dropdown = ctk.CTkComboBox(
            controls_frame,
            values=["Select backup..."],
            width=250
        )
        self.compare_config2_dropdown.pack(side="left", padx=5)
        
        # Compare button
        compare_btn = ctk.CTkButton(
            controls_frame,
            text="⚖️ Compare",
            command=self._compare_configs,
            width=120
        )
        compare_btn.pack(side="left", padx=10)
        
        # Left config display
        left_frame = ctk.CTkFrame(tab)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            left_frame,
            text="Configuration 1",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.compare_text1 = ctk.CTkTextbox(
            left_frame,
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        self.compare_text1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Right config display
        right_frame = ctk.CTkFrame(tab)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            right_frame,
            text="Configuration 2",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.compare_text2 = ctk.CTkTextbox(
            right_frame,
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        self.compare_text2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    def _refresh_devices(self):
        """Refresh connected devices list"""
        
        connected_devices = self._get_connected_devices()
        
        # Clear existing checkboxes
        for widget in self.device_list_frame.winfo_children():
            widget.destroy()
        self.device_checkboxes.clear()
        
        # Create new checkboxes
        if connected_devices:
            for device in connected_devices:
                var = ctk.BooleanVar(value=False)
                checkbox = ctk.CTkCheckBox(
                    self.device_list_frame,
                    text=f"{device.ip_address} ({device.hostname or 'Unknown'}) - {device.vendor or 'Unknown'}",
                    variable=var
                )
                checkbox.pack(anchor="w", padx=10, pady=5)
                self.device_checkboxes.append((device, var, checkbox))
            
            self._update_status(f"Found {len(connected_devices)} connected device(s)")
        else:
            no_devices_label = ctk.CTkLabel(
                self.device_list_frame,
                text="No connected devices found. Please connect devices first.",
                font=ctk.CTkFont(size=12)
            )
            no_devices_label.pack(padx=10, pady=20)
            self._update_status("No connected devices")
    
    def _select_all_devices(self):
        """Select all devices"""
        for _, var, _ in self.device_checkboxes:
            var.set(True)
    
    def _deselect_all_devices(self):
        """Deselect all devices"""
        for _, var, _ in self.device_checkboxes:
            var.set(False)
    
    def _on_backup_devices(self):
        """Handle backup devices button click"""
        
        # Get selected devices
        selected = [(device, var) for device, var, _ in self.device_checkboxes if var.get()]
        
        if not selected:
            self._show_error("No devices selected")
            return
        
        config_type = self.config_type_var.get()
        
        # Run backup in background
        self.backup_button.configure(state="disabled", text="⏳ Backing up...")
        
        thread = threading.Thread(
            target=self._perform_backup,
            args=([device for device, _ in selected], config_type)
        )
        thread.daemon = True
        thread.start()
    
    def _perform_backup(self, devices: List[Device], config_type: str):
        """Perform backup operation"""
        
        total = len(devices)
        
        for idx, device in enumerate(devices):
            try:
                progress = (idx + 1) / total
                self.after(0, lambda p=progress: self.backup_progress.set(p))
                
                status = f"Backing up {device.ip_address} ({idx+1}/{total})..."
                self.after(0, lambda s=status: self._update_backup_status(s))
                
                # Perform backup
                record = self.backup_manager.backup_device(device, config_type)
                self.backup_history.append(record)
                
                self.logger.info(f"Backup completed: {device.ip_address}")
            
            except Exception as e:
                self.logger.error(f"Backup failed for {device.ip_address}: {e}")
                self.after(0, lambda d=device, e=e: self._show_error(
                    f"Backup failed for {d.ip_address}: {str(e)}"
                ))
        
        # Update UI
        self.after(0, lambda: self._update_backup_status(f"✅ Backup completed for {total} device(s)"))
        self.after(0, lambda: self.backup_button.configure(state="normal", text="💾 Backup Selected Devices"))
        self.after(0, self._load_backup_history)
    
    def _load_backup_history(self):
        """Load backup history from disk"""
        
        try:
            # Clear existing rows
            for widget in self.history_rows_frame.winfo_children():
                widget.destroy()
            
            # Load all backups from backup directory
            backup_dir = Path("backups")
            if not backup_dir.exists():
                return
            
            backups = []
            for backup_file in backup_dir.glob("**/*.cfg"):
                try:
                    # Parse filename: YYYYMMDD_HHMMSS_IP_type.cfg
                    parts = backup_file.stem.split('_')
                    if len(parts) >= 4:
                        timestamp_str = f"{parts[0]}_{parts[1]}"
                        timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                        device_ip = parts[2]
                        config_type = parts[3] if len(parts) > 3 else "unknown"
                        size = backup_file.stat().st_size
                        
                        backups.append({
                            'file': backup_file,
                            'device': device_ip,
                            'type': config_type,
                            'timestamp': timestamp,
                            'size': size
                        })
                except Exception as e:
                    self.logger.warning(f"Could not parse backup file {backup_file}: {e}")
            
            # Sort by timestamp (newest first)
            backups.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Display rows
            for backup in backups:
                self._create_history_row(backup)
            
            # Update filter dropdown
            devices = list(set(b['device'] for b in backups))
            self.filter_dropdown.configure(values=["All Devices"] + devices)
            
            # Update compare dropdowns
            backup_labels = [
                f"{b['device']} - {b['type']} - {b['timestamp'].strftime('%Y-%m-%d %H:%M')}"
                for b in backups
            ]
            self.compare_config1_dropdown.configure(values=backup_labels if backup_labels else ["No backups"])
            self.compare_config2_dropdown.configure(values=backup_labels if backup_labels else ["No backups"])
        
        except Exception as e:
            self.logger.error(f"Error loading backup history: {e}", exc_info=True)
    
    def _create_history_row(self, backup: dict):
        """Create a history table row"""
        
        row_frame = ctk.CTkFrame(self.history_rows_frame)
        row_frame.pack(fill="x", pady=2)
        
        # Device
        ctk.CTkLabel(row_frame, text=backup['device'], width=150).pack(side="left", padx=5)
        
        # Config type
        ctk.CTkLabel(row_frame, text=backup['type'], width=120).pack(side="left", padx=5)
        
        # Timestamp
        timestamp_str = backup['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        ctk.CTkLabel(row_frame, text=timestamp_str, width=180).pack(side="left", padx=5)
        
        # Size
        size_kb = backup['size'] / 1024
        ctk.CTkLabel(row_frame, text=f"{size_kb:.1f} KB", width=100).pack(side="left", padx=5)
        
        # Actions
        actions_frame = ctk.CTkFrame(row_frame, width=200)
        actions_frame.pack(side="left", padx=5)
        
        view_btn = ctk.CTkButton(
            actions_frame,
            text="👁️ View",
            command=lambda: self._view_backup(backup['file']),
            width=60
        )
        view_btn.pack(side="left", padx=2)
        
        restore_btn = ctk.CTkButton(
            actions_frame,
            text="↩️ Restore",
            command=lambda: self._restore_backup(backup),
            width=70
        )
        restore_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            command=lambda: self._delete_backup(backup['file']),
            width=40,
            fg_color="red"
        )
        delete_btn.pack(side="left", padx=2)
    
    def _view_backup(self, filepath: Path):
        """View backup configuration"""
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create dialog
            dialog = ctk.CTkToplevel(self)
            dialog.title(f"View Backup - {filepath.name}")
            dialog.geometry("800x600")
            
            textbox = ctk.CTkTextbox(dialog, font=("Consolas", 10))
            textbox.pack(fill="both", expand=True, padx=10, pady=10)
            textbox.insert("1.0", content)
            textbox.configure(state="disabled")
        
        except Exception as e:
            self._show_error(f"Could not view backup: {str(e)}")
    
    def _restore_backup(self, backup: dict):
        """Restore configuration to device"""
        
        # Confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Restore")
        dialog.geometry("400x200")
        
        message = f"Are you sure you want to restore configuration to {backup['device']}?\n\n"
        message += "This will overwrite the current configuration!"
        
        ctk.CTkLabel(dialog, text=message, wraplength=350).pack(padx=20, pady=20)
        
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Restore",
            command=lambda: self._do_restore(backup, dialog),
            fg_color="red"
        ).pack(side="left", padx=5)
    
    def _do_restore(self, backup: dict, dialog):
        """Actually perform the restore"""
        dialog.destroy()
        self._show_error("Restore functionality not yet implemented")
        # TODO: Implement restore via connection manager
    
    def _delete_backup(self, filepath: Path):
        """Delete backup file"""
        
        try:
            filepath.unlink()
            self._update_status(f"Deleted backup: {filepath.name}")
            self._load_backup_history()
        except Exception as e:
            self._show_error(f"Could not delete backup: {str(e)}")
    
    def _filter_history(self, selected_device: str):
        """Filter history by device"""
        # Reload history with filter
        self._load_backup_history()
    
    def _cleanup_old_backups(self):
        """Cleanup old backups based on retention policy"""
        
        try:
            deleted_count = self.backup_manager.cleanup_old_backups()
            self._update_status(f"Cleaned up {deleted_count} old backup(s)")
            self._load_backup_history()
        except Exception as e:
            self._show_error(f"Cleanup failed: {str(e)}")
    
    def _compare_configs(self):
        """Compare two configurations"""
        
        config1_label = self.compare_config1_dropdown.get()
        config2_label = self.compare_config2_dropdown.get()
        
        if config1_label == "Select backup..." or config2_label == "Select backup...":
            self._show_error("Please select two backups to compare")
            return
        
        # Parse labels to get files
        # TODO: Implement actual comparison logic
        self.compare_text1.delete("1.0", "end")
        self.compare_text1.insert("1.0", f"Configuration 1:\n{config1_label}\n\n(Comparison feature coming soon)")
        
        self.compare_text2.delete("1.0", "end")
        self.compare_text2.insert("1.0", f"Configuration 2:\n{config2_label}\n\n(Comparison feature coming soon)")
    
    def _toggle_auto_backup(self):
        """Toggle auto-backup"""
        if self.auto_backup_var.get():
            self._update_status("Auto-backup enabled")
            # TODO: Setup scheduled backup task
        else:
            self._update_status("Auto-backup disabled")
    
    def _get_connected_devices(self) -> List[Device]:
        """Get list of connected devices"""
        connected_ips = self.connection_manager.get_connected_devices()
        devices = []
        for ip in connected_ips:
            device = Device(ip_address=ip)
            devices.append(device)
        return devices
    
    def _update_status(self, message: str):
        """Update status message"""
        if self.status_callback:
            self.status_callback(message)
        self.logger.info(message)
    
    def _update_backup_status(self, message: str):
        """Update backup-specific status"""
        self.backup_status_label.configure(text=message)
        self._update_status(message)
    
    def _show_error(self, message: str):
        """Show error message"""
        self.backup_status_label.configure(text=f"❌ {message}", text_color="red")
        self.logger.error(message)
    
    def display_backup_history(self, backup_records: List[BackupRecord]):
        """Display backup history from demo data or loaded records"""
        
        # Store the records
        self.backup_history = backup_records
        
        # Clear existing rows
        for widget in self.history_rows_frame.winfo_children():
            widget.destroy()
        
        if not backup_records:
            no_data_label = ctk.CTkLabel(
                self.history_rows_frame,
                text="No backup records found",
                font=ctk.CTkFont(size=12)
            )
            no_data_label.pack(pady=20)
            return
        
        # Sort by timestamp (newest first)
        sorted_backups = sorted(backup_records, key=lambda x: x.timestamp, reverse=True)
        
        # Display each backup
        for backup in sorted_backups:
            row_frame = ctk.CTkFrame(self.history_rows_frame)
            row_frame.pack(fill="x", pady=2, padx=5)
            
            # Device
            device_label = ctk.CTkLabel(
                row_frame,
                text=f"{backup.device_hostname or 'Unknown'}\n({backup.device_ip})",
                width=150,
                anchor="w"
            )
            device_label.pack(side="left", padx=5)
            
            # Config Type
            config_label = ctk.CTkLabel(
                row_frame,
                text=backup.config_type,
                width=120,
                anchor="w"
            )
            config_label.pack(side="left", padx=5)
            
            # Timestamp
            time_label = ctk.CTkLabel(
                row_frame,
                text=backup.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                width=180,
                anchor="w"
            )
            time_label.pack(side="left", padx=5)
            
            # Size
            size_kb = backup.size_bytes / 1024
            size_label = ctk.CTkLabel(
                row_frame,
                text=f"{size_kb:.1f} KB",
                width=100,
                anchor="w"
            )
            size_label.pack(side="left", padx=5)
            
            # Actions
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.pack(side="left", padx=5)
            
            # Status indicator
            if backup.backup_successful:
                status_label = ctk.CTkLabel(
                    actions_frame,
                    text="✅",
                    width=30
                )
            else:
                status_label = ctk.CTkLabel(
                    actions_frame,
                    text="❌",
                    width=30
                )
            status_label.pack(side="left", padx=2)
            
            # View button (disabled for demo)
            view_btn = ctk.CTkButton(
                actions_frame,
                text="👁️ View",
                width=60,
                height=25,
                command=lambda b=backup: self._view_backup(b)
            )
            view_btn.pack(side="left", padx=2)
        
        # Update status
        self._update_backup_status(f"✅ Loaded {len(backup_records)} backup record(s)")
        self.logger.info(f"Displayed {len(backup_records)} backup records")
    
    def _view_backup(self, backup: BackupRecord):
        """View backup content (for demo, show info dialog)"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Backup Information")
        dialog.geometry("500x400")
        dialog.transient(self)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 200
        dialog.geometry(f"+{x}+{y}")
        
        # Content
        info_text = f"""
Backup Information
{'='*60}

Device: {backup.device_hostname} ({backup.device_ip})
Config Type: {backup.config_type}
Timestamp: {backup.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
File Path: {backup.file_path}
File Size: {backup.size_bytes / 1024:.2f} KB
Checksum: {backup.checksum[:16]}...
Status: {'✅ Successful' if backup.backup_successful else '❌ Failed'}

{'='*60}

Note: This is demo data. In production, the actual
configuration file content would be displayed here.
        """
        
        text_widget = ctk.CTkTextbox(dialog, wrap="word")
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")
        
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            width=100
        )
        close_btn.pack(pady=10)
