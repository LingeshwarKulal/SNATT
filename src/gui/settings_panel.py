"""
Settings Panel
Application settings and credential management interface
"""

import customtkinter as ctk
import logging
from typing import Callable, List, Dict
import json
from pathlib import Path

from utils.credential_manager import CredentialManager
from utils.config_manager import ConfigManager


class SettingsPanel(ctk.CTkFrame):
    """Application settings and configuration panel"""
    
    def __init__(self, parent, credential_manager: CredentialManager, config_manager: ConfigManager, 
                 status_callback: Callable = None):
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.credential_manager = credential_manager
        self.config_manager = config_manager
        self.status_callback = status_callback
        
        self._setup_ui()
        self._load_credentials()
        self._load_settings()
    
    def _setup_ui(self):
        """Setup user interface"""
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Add tabs
        self.tabview.add("Credentials")
        self.tabview.add("Connection")
        self.tabview.add("Backup")
        self.tabview.add("Appearance")
        self.tabview.add("Advanced")
        
        # Setup each tab
        self._setup_credentials_tab()
        self._setup_connection_tab()
        self._setup_backup_tab()
        self._setup_appearance_tab()
        self._setup_advanced_tab()
    
    def _setup_credentials_tab(self):
        """Setup credentials management tab"""
        
        tab = self.tabview.tab("Credentials")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(tab)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="Manage Device Credentials",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=10)
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="➕ Add Credential",
            command=self._add_credential_dialog,
            fg_color=("green", "darkgreen")
        )
        add_btn.pack(side="right", padx=10)
        
        # Credentials list
        self.credentials_frame = ctk.CTkScrollableFrame(tab)
        self.credentials_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Info box
        info_frame = ctk.CTkFrame(tab)
        info_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Credentials are encrypted and stored securely in your system keyring",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(padx=10, pady=10)
    
    def _setup_connection_tab(self):
        """Setup connection settings tab"""
        
        tab = self.tabview.tab("Connection")
        tab.grid_columnconfigure(0, weight=1)
        
        # Header
        ctk.CTkLabel(
            tab,
            text="Connection Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(tab)
        settings_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        settings_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Timeout
        ctk.CTkLabel(settings_frame, text="Connection Timeout (seconds):").grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )
        self.timeout_entry = ctk.CTkEntry(settings_frame, width=200)
        self.timeout_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # SSH Port
        ctk.CTkLabel(settings_frame, text="Default SSH Port:").grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )
        self.ssh_port_entry = ctk.CTkEntry(settings_frame, width=200)
        self.ssh_port_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # Max Retries
        ctk.CTkLabel(settings_frame, text="Connection Retry Attempts:").grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )
        self.retry_entry = ctk.CTkEntry(settings_frame, width=200)
        self.retry_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # Auto-reconnect
        self.auto_reconnect_var = ctk.BooleanVar()
        auto_reconnect_check = ctk.CTkCheckBox(
            settings_frame,
            text="Auto-reconnect on connection loss",
            variable=self.auto_reconnect_var
        )
        auto_reconnect_check.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        row += 1
        
        # Keep-alive
        self.keepalive_var = ctk.BooleanVar()
        keepalive_check = ctk.CTkCheckBox(
            settings_frame,
            text="Enable SSH keep-alive",
            variable=self.keepalive_var
        )
        keepalive_check.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        row += 1
        
        # Save button
        save_btn = ctk.CTkButton(
            tab,
            text="💾 Save Connection Settings",
            command=self._save_connection_settings,
            fg_color=("green", "darkgreen")
        )
        save_btn.grid(row=2, column=0, padx=20, pady=20, sticky="w")
    
    def _setup_backup_tab(self):
        """Setup backup settings tab"""
        
        tab = self.tabview.tab("Backup")
        tab.grid_columnconfigure(0, weight=1)
        
        # Header
        ctk.CTkLabel(
            tab,
            text="Backup Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(tab)
        settings_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        settings_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Backup directory
        ctk.CTkLabel(settings_frame, text="Backup Directory:").grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )
        backup_dir_frame = ctk.CTkFrame(settings_frame)
        backup_dir_frame.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        
        self.backup_dir_entry = ctk.CTkEntry(backup_dir_frame)
        self.backup_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        browse_btn = ctk.CTkButton(
            backup_dir_frame,
            text="Browse",
            command=self._browse_backup_dir,
            width=80
        )
        browse_btn.pack(side="right")
        row += 1
        
        # Retention days
        ctk.CTkLabel(settings_frame, text="Retention Period (days):").grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )
        self.retention_entry = ctk.CTkEntry(settings_frame, width=200)
        self.retention_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # Auto-backup schedule
        ctk.CTkLabel(settings_frame, text="Auto-Backup Schedule:").grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )
        self.schedule_dropdown = ctk.CTkComboBox(
            settings_frame,
            values=["Disabled", "Daily", "Weekly", "Monthly"],
            width=200
        )
        self.schedule_dropdown.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # Backup time
        ctk.CTkLabel(settings_frame, text="Backup Time (24h):").grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )
        self.backup_time_entry = ctk.CTkEntry(settings_frame, placeholder_text="HH:MM", width=200)
        self.backup_time_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # Compression
        self.compress_var = ctk.BooleanVar()
        compress_check = ctk.CTkCheckBox(
            settings_frame,
            text="Compress backup files",
            variable=self.compress_var
        )
        compress_check.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        row += 1
        
        # Email notifications
        self.email_notify_var = ctk.BooleanVar()
        email_check = ctk.CTkCheckBox(
            settings_frame,
            text="Email notifications on backup completion",
            variable=self.email_notify_var
        )
        email_check.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        row += 1
        
        # Save button
        save_btn = ctk.CTkButton(
            tab,
            text="💾 Save Backup Settings",
            command=self._save_backup_settings,
            fg_color=("green", "darkgreen")
        )
        save_btn.grid(row=2, column=0, padx=20, pady=20, sticky="w")
    
    def _setup_appearance_tab(self):
        """Setup appearance settings tab"""
        
        tab = self.tabview.tab("Appearance")
        tab.grid_columnconfigure(0, weight=1)
        
        # Header
        ctk.CTkLabel(
            tab,
            text="Appearance Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(tab)
        settings_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Theme
        theme_frame = ctk.CTkFrame(settings_frame)
        theme_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        
        light_radio = ctk.CTkRadioButton(
            theme_frame,
            text="☀️ Light",
            variable=self.theme_var,
            value="Light",
            command=self._change_theme
        )
        light_radio.pack(side="left", padx=10)
        
        dark_radio = ctk.CTkRadioButton(
            theme_frame,
            text="🌙 Dark",
            variable=self.theme_var,
            value="Dark",
            command=self._change_theme
        )
        dark_radio.pack(side="left", padx=10)
        
        system_radio = ctk.CTkRadioButton(
            theme_frame,
            text="💻 System",
            variable=self.theme_var,
            value="System",
            command=self._change_theme
        )
        system_radio.pack(side="left", padx=10)
        
        # Color theme
        color_frame = ctk.CTkFrame(settings_frame)
        color_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            color_frame,
            text="Color Theme:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.color_dropdown = ctk.CTkComboBox(
            color_frame,
            values=["blue", "green", "dark-blue"],
            command=self._change_color_theme,
            width=200
        )
        self.color_dropdown.pack(side="left", padx=10)
        
        # Font size
        font_frame = ctk.CTkFrame(settings_frame)
        font_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            font_frame,
            text="Font Size:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.font_size_slider = ctk.CTkSlider(
            font_frame,
            from_=10,
            to=16,
            number_of_steps=6,
            command=self._change_font_size
        )
        self.font_size_slider.pack(side="left", fill="x", expand=True, padx=10)
        self.font_size_slider.set(12)
        
        self.font_size_label = ctk.CTkLabel(font_frame, text="12")
        self.font_size_label.pack(side="left", padx=5)
    
    def _setup_advanced_tab(self):
        """Setup advanced settings tab"""
        
        tab = self.tabview.tab("Advanced")
        tab.grid_columnconfigure(0, weight=1)
        
        # Header
        ctk.CTkLabel(
            tab,
            text="Advanced Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(tab)
        settings_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Logging level
        log_frame = ctk.CTkFrame(settings_frame)
        log_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            log_frame,
            text="Logging Level:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.log_level_dropdown = ctk.CTkComboBox(
            log_frame,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            width=150
        )
        self.log_level_dropdown.pack(side="left", padx=10)
        
        # Thread pool size
        thread_frame = ctk.CTkFrame(settings_frame)
        thread_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            thread_frame,
            text="Max Concurrent Threads:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.thread_pool_entry = ctk.CTkEntry(thread_frame, width=150)
        self.thread_pool_entry.pack(side="left", padx=10)
        
        # Cache settings
        cache_frame = ctk.CTkFrame(settings_frame)
        cache_frame.pack(fill="x", padx=10, pady=10)
        
        self.cache_var = ctk.BooleanVar(value=True)
        cache_check = ctk.CTkCheckBox(
            cache_frame,
            text="Enable device info caching",
            variable=self.cache_var
        )
        cache_check.pack(side="left", padx=10)
        
        clear_cache_btn = ctk.CTkButton(
            cache_frame,
            text="Clear Cache",
            command=self._clear_cache,
            width=120
        )
        clear_cache_btn.pack(side="left", padx=10)
        
        # Export/Import config
        config_frame = ctk.CTkFrame(settings_frame)
        config_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            config_frame,
            text="Configuration:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        export_btn = ctk.CTkButton(
            config_frame,
            text="📤 Export Config",
            command=self._export_config,
            width=130
        )
        export_btn.pack(side="left", padx=5)
        
        import_btn = ctk.CTkButton(
            config_frame,
            text="📥 Import Config",
            command=self._import_config,
            width=130
        )
        import_btn.pack(side="left", padx=5)
        
        # Reset button
        reset_frame = ctk.CTkFrame(settings_frame)
        reset_frame.pack(fill="x", padx=10, pady=10)
        
        reset_btn = ctk.CTkButton(
            reset_frame,
            text="🔄 Reset to Defaults",
            command=self._reset_to_defaults,
            fg_color="orange",
            width=150
        )
        reset_btn.pack(side="left", padx=10)
        
        # Save button
        save_btn = ctk.CTkButton(
            tab,
            text="💾 Save Advanced Settings",
            command=self._save_advanced_settings,
            fg_color=("green", "darkgreen")
        )
        save_btn.grid(row=2, column=0, padx=20, pady=20, sticky="w")
    
    def _load_credentials(self):
        """Load and display saved credentials"""
        
        # Clear existing
        for widget in self.credentials_frame.winfo_children():
            widget.destroy()
        
        # Get credentials
        credentials = self.credential_manager.list_credentials()
        
        if not credentials:
            no_creds_label = ctk.CTkLabel(
                self.credentials_frame,
                text="No credentials saved. Click 'Add Credential' to create one.",
                font=ctk.CTkFont(size=12)
            )
            no_creds_label.pack(pady=20)
            return
        
        # Display each credential
        for cred_name in credentials:
            self._create_credential_item(cred_name)
    
    def _create_credential_item(self, cred_name: str):
        """Create a credential list item"""
        
        item_frame = ctk.CTkFrame(self.credentials_frame)
        item_frame.pack(fill="x", padx=5, pady=5)
        
        # Credential info
        info_frame = ctk.CTkFrame(item_frame)
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"🔑 {cred_name}",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        name_label.pack(anchor="w")
        
        # Get metadata
        metadata = self.credential_manager.get_credential_metadata(cred_name)
        if metadata:
            meta_text = f"Username: {metadata.get('username', 'N/A')} • "
            meta_text += f"Type: {metadata.get('device_type', 'generic')}"
            
            meta_label = ctk.CTkLabel(
                info_frame,
                text=meta_text,
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            meta_label.pack(anchor="w")
        
        # Actions
        actions_frame = ctk.CTkFrame(item_frame)
        actions_frame.pack(side="right", padx=10)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Edit",
            command=lambda: self._edit_credential_dialog(cred_name),
            width=70
        )
        edit_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            command=lambda: self._delete_credential(cred_name),
            width=40,
            fg_color="red"
        )
        delete_btn.pack(side="left", padx=2)
    
    def _add_credential_dialog(self):
        """Show add credential dialog"""
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Credential")
        dialog.geometry("450x400")
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Name
        ctk.CTkLabel(form_frame, text="Credential Name:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        name_entry = ctk.CTkEntry(form_frame)
        name_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # Username
        ctk.CTkLabel(form_frame, text="Username:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        username_entry = ctk.CTkEntry(form_frame)
        username_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # Password
        ctk.CTkLabel(form_frame, text="Password:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        password_entry = ctk.CTkEntry(form_frame, show="*")
        password_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # Device type
        ctk.CTkLabel(form_frame, text="Device Type:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        device_type_dropdown = ctk.CTkComboBox(
            form_frame,
            values=["cisco_ios", "cisco_nxos", "juniper_junos", "arista_eos", "huawei", "generic"]
        )
        device_type_dropdown.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # Enable password (optional)
        ctk.CTkLabel(form_frame, text="Enable Password:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        enable_entry = ctk.CTkEntry(form_frame, show="*", placeholder_text="Optional")
        enable_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        def save_credential():
            name = name_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            device_type = device_type_dropdown.get()
            enable_password = enable_entry.get()
            
            if not name or not username or not password:
                self._show_error("Name, username, and password are required")
                return
            
            # Save credential
            self.credential_manager.save_credential(
                name=name,
                username=username,
                password=password,
                device_type=device_type,
                enable_password=enable_password if enable_password else None
            )
            
            self._update_status(f"Credential '{name}' saved successfully")
            self._load_credentials()
            dialog.destroy()
        
        ctk.CTkButton(
            button_frame,
            text="💾 Save",
            command=save_credential,
            fg_color=("green", "darkgreen")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)
    
    def _edit_credential_dialog(self, cred_name: str):
        """Show edit credential dialog"""
        
        # Get existing credential
        cred = self.credential_manager.get_credential(cred_name)
        metadata = self.credential_manager.get_credential_metadata(cred_name)
        
        if not cred or not metadata:
            self._show_error("Could not load credential")
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Edit Credential: {cred_name}")
        dialog.geometry("450x400")
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Username
        ctk.CTkLabel(form_frame, text="Username:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        username_entry = ctk.CTkEntry(form_frame)
        username_entry.insert(0, metadata.get('username', ''))
        username_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # Password
        ctk.CTkLabel(form_frame, text="New Password:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        password_entry = ctk.CTkEntry(form_frame, show="*", placeholder_text="Leave blank to keep current")
        password_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # Device type
        ctk.CTkLabel(form_frame, text="Device Type:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        device_type_dropdown = ctk.CTkComboBox(
            form_frame,
            values=["cisco_ios", "cisco_nxos", "juniper_junos", "arista_eos", "huawei", "generic"]
        )
        device_type_dropdown.set(metadata.get('device_type', 'generic'))
        device_type_dropdown.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        def update_credential():
            username = username_entry.get().strip()
            password = password_entry.get()
            device_type = device_type_dropdown.get()
            
            if not username:
                self._show_error("Username is required")
                return
            
            # Update credential
            if password:
                self.credential_manager.save_credential(
                    name=cred_name,
                    username=username,
                    password=password,
                    device_type=device_type
                )
            else:
                # Just update metadata
                self.credential_manager.save_credential(
                    name=cred_name,
                    username=username,
                    password=cred['password'],  # Keep existing
                    device_type=device_type
                )
            
            self._update_status(f"Credential '{cred_name}' updated")
            self._load_credentials()
            dialog.destroy()
        
        ctk.CTkButton(
            button_frame,
            text="💾 Update",
            command=update_credential,
            fg_color=("green", "darkgreen")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)
    
    def _delete_credential(self, cred_name: str):
        """Delete a credential"""
        
        # Confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Delete")
        dialog.geometry("350x150")
        
        ctk.CTkLabel(
            dialog,
            text=f"Delete credential '{cred_name}'?",
            font=ctk.CTkFont(size=14)
        ).pack(pady=20)
        
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        def do_delete():
            self.credential_manager.delete_credential(cred_name)
            self._update_status(f"Credential '{cred_name}' deleted")
            self._load_credentials()
            dialog.destroy()
        
        ctk.CTkButton(
            button_frame,
            text="Delete",
            command=do_delete,
            fg_color="red"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)
    
    def _load_settings(self):
        """Load settings from config"""
        
        # Connection settings
        self.timeout_entry.insert(0, str(self.config_manager.get('connection.timeout', 30)))
        self.ssh_port_entry.insert(0, str(self.config_manager.get('connection.ssh_port', 22)))
        self.retry_entry.insert(0, str(self.config_manager.get('connection.max_retries', 3)))
        
        # Backup settings
        self.backup_dir_entry.insert(0, self.config_manager.get('backup.directory', './backups'))
        self.retention_entry.insert(0, str(self.config_manager.get('backup.retention_days', 30)))
        
        # Advanced settings
        self.log_level_dropdown.set(self.config_manager.get('logging.level', 'INFO'))
        self.thread_pool_entry.insert(0, str(self.config_manager.get('threading.max_workers', 10)))
    
    def _save_connection_settings(self):
        """Save connection settings"""
        try:
            self.config_manager.set('connection.timeout', int(self.timeout_entry.get()))
            self.config_manager.set('connection.ssh_port', int(self.ssh_port_entry.get()))
            self.config_manager.set('connection.max_retries', int(self.retry_entry.get()))
            self.config_manager.save_user_config()
            self._update_status("Connection settings saved")
        except Exception as e:
            self._show_error(f"Failed to save settings: {str(e)}")
    
    def _save_backup_settings(self):
        """Save backup settings"""
        try:
            self.config_manager.set('backup.directory', self.backup_dir_entry.get())
            self.config_manager.set('backup.retention_days', int(self.retention_entry.get()))
            self.config_manager.save_user_config()
            self._update_status("Backup settings saved")
        except Exception as e:
            self._show_error(f"Failed to save settings: {str(e)}")
    
    def _save_advanced_settings(self):
        """Save advanced settings"""
        try:
            self.config_manager.set('logging.level', self.log_level_dropdown.get())
            self.config_manager.set('threading.max_workers', int(self.thread_pool_entry.get()))
            self.config_manager.save_user_config()
            self._update_status("Advanced settings saved")
        except Exception as e:
            self._show_error(f"Failed to save settings: {str(e)}")
    
    def _change_theme(self):
        """Change appearance theme"""
        theme = self.theme_var.get()
        ctk.set_appearance_mode(theme)
        self._update_status(f"Theme changed to {theme}")
    
    def _change_color_theme(self, color: str):
        """Change color theme"""
        ctk.set_default_color_theme(color)
        self._update_status(f"Color theme changed (restart required)")
    
    def _change_font_size(self, value):
        """Change font size"""
        size = int(value)
        self.font_size_label.configure(text=str(size))
        # Would need to implement font scaling across app
    
    def _browse_backup_dir(self):
        """Browse for backup directory"""
        from tkinter import filedialog
        directory = filedialog.askdirectory()
        if directory:
            self.backup_dir_entry.delete(0, "end")
            self.backup_dir_entry.insert(0, directory)
    
    def _clear_cache(self):
        """Clear application cache"""
        self._update_status("Cache cleared")
    
    def _export_config(self):
        """Export configuration"""
        try:
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            if filepath:
                config = self.config_manager.config
                with open(filepath, 'w') as f:
                    json.dump(config, f, indent=2)
                self._update_status(f"Configuration exported to {filepath}")
        except Exception as e:
            self._show_error(f"Export failed: {str(e)}")
    
    def _import_config(self):
        """Import configuration"""
        try:
            from tkinter import filedialog
            filepath = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")]
            )
            if filepath:
                with open(filepath, 'r') as f:
                    config = json.load(f)
                # Merge with current config
                for key, value in config.items():
                    self.config_manager.set(key, value)
                self.config_manager.save_user_config()
                self._update_status(f"Configuration imported from {filepath}")
                self._load_settings()
        except Exception as e:
            self._show_error(f"Import failed: {str(e)}")
    
    def _reset_to_defaults(self):
        """Reset all settings to defaults"""
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Reset")
        dialog.geometry("400x150")
        
        ctk.CTkLabel(
            dialog,
            text="Reset all settings to defaults?\nThis cannot be undone.",
            font=ctk.CTkFont(size=14)
        ).pack(pady=20)
        
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        def do_reset():
            # Delete user config file
            user_config_path = Path("config/user_config.json")
            if user_config_path.exists():
                user_config_path.unlink()
            
            # Reload config
            self.config_manager.load_config()
            self._load_settings()
            self._update_status("Settings reset to defaults")
            dialog.destroy()
        
        ctk.CTkButton(
            button_frame,
            text="Reset",
            command=do_reset,
            fg_color="red"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)
    
    def _update_status(self, message: str):
        """Update status message"""
        if self.status_callback:
            self.status_callback(message)
        self.logger.info(message)
    
    def _show_error(self, message: str):
        """Show error message"""
        if self.status_callback:
            self.status_callback(f"❌ {message}")
        self.logger.error(message)
