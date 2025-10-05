"""
Main Window
SNATT GUI Main Window
"""

import logging
import customtkinter as ctk
from typing import Dict

# Import GUI panels
from gui.discovery_panel import DiscoveryPanel
from gui.diagnostics_panel import DiagnosticsPanel
from gui.backup_panel import BackupPanel
from gui.reports_panel import ReportsPanel
from gui.settings_panel import SettingsPanel

from engines import (
    DiscoveryEngine,
    ConnectionManager,
    TroubleshootingEngine,
    BackupManager,
    ReportingEngine
)
from utils import CredentialManager


class MainWindow(ctk.CTk):
    """Main application window"""
    
    def __init__(self, config: Dict):
        super().__init__()
        
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Initialize engines
        self.logger.info("Initializing engines...")
        self.discovery_engine = DiscoveryEngine(config)
        self.connection_manager = ConnectionManager(config)
        self.troubleshooting_engine = TroubleshootingEngine(config, self.connection_manager)
        self.backup_manager = BackupManager(config, self.connection_manager)
        self.reporting_engine = ReportingEngine(config)
        self.credential_manager = CredentialManager()
        
        # Device storage
        self.devices = []
        self.diagnostic_results = []
        
        # Panel instances
        self.panels = {}
        self.current_panel = None
        
        # Setup GUI
        self._setup_window()
        self._create_widgets()
        
        self.logger.info("Main window initialized")
    
    def _setup_window(self):
        """Configure main window properties"""
        
        # Window title and size
        window_title = self.config.get('gui', {}).get('window_title', 'SNATT - Smart Network Automation Tool')
        window_size = self.config.get('gui', {}).get('window_size', '1200x800')
        
        self.title(window_title)
        self.geometry(window_size)
        
        # Set theme
        theme = self.config.get('application', {}).get('theme', 'dark')
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """Create main GUI widgets"""
        
        # Navigation panel (left side)
        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_rowconfigure(6, weight=1)  # Push buttons to top
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.nav_frame,
            text="SNATT",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("Discovery", "🔍", 1),
            ("Diagnostics", "🧰", 2),
            ("Backup", "💾", 3),
            ("Reports", "📊", 4),
            ("Settings", "⚙️", 5),
        ]
        
        for name, icon, row in nav_items:
            btn = ctk.CTkButton(
                self.nav_frame,
                text=f"{icon} {name}",
                width=180,
                height=40,
                corner_radius=8,
                command=lambda n=name: self._switch_panel(n)
            )
            btn.grid(row=row, column=0, padx=10, pady=5)
            self.nav_buttons[name] = btn
        
        # Status bar at bottom of nav
        self.status_label = ctk.CTkLabel(
            self.nav_frame,
            text="Ready",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.grid(row=7, column=0, padx=10, pady=10, sticky="s")
        
        # Main content area (right side)
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome screen (placeholder for now)
        self._create_welcome_screen()
    
    def _create_welcome_screen(self):
        """Create welcome/home screen"""
        
        welcome_frame = ctk.CTkFrame(self.content_frame)
        welcome_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        welcome_frame.grid_rowconfigure(0, weight=1)
        welcome_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome text
        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text="Welcome to SNATT",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        welcome_text.pack(pady=(100, 20))
        
        subtitle = ctk.CTkLabel(
            welcome_frame,
            text="Smart Network Automation and Troubleshooting Tool",
            font=ctk.CTkFont(size=16)
        )
        subtitle.pack(pady=10)
        
        # Quick start info
        info_frame = ctk.CTkFrame(welcome_frame)
        info_frame.pack(pady=40, padx=40, fill="both", expand=True)
        
        info_text = """
        Quick Start Guide:
        
        1. 🔍 Discovery - Scan your network to find devices
        2. 🧰 Diagnostics - Run health checks on devices
        3. 💾 Backup - Save device configurations
        4. 📊 Reports - Generate professional reports
        5. ⚙️ Settings - Configure credentials and preferences
        
        Click any button on the left to get started!
        """
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        info_label.pack(pady=20, padx=20)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(welcome_frame)
        stats_frame.pack(pady=20, padx=40, fill="x")
        
        # Display some stats
        stats_text = f"Devices Discovered: {len(self.devices)} | " \
                    f"Active Connections: {self.connection_manager.get_active_connections_count()}"
        
        stats_label = ctk.CTkLabel(
            stats_frame,
            text=stats_text,
            font=ctk.CTkFont(size=12)
        )
        stats_label.pack(pady=10)
    
    def _switch_panel(self, panel_name: str):
        """Switch to different panel"""
        
        self.logger.info(f"Switching to {panel_name} panel")
        self.update_status(f"Loading {panel_name}...")
        
        # Hide current panel
        if self.current_panel:
            self.current_panel.grid_forget()
        
        # Update button colors
        for name, btn in self.nav_buttons.items():
            if name == panel_name:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Load or retrieve panel
        if panel_name not in self.panels:
            # Create panel on first access
            if panel_name == "Discovery":
                self.panels[panel_name] = DiscoveryPanel(
                    self.content_frame,
                    self.discovery_engine,
                    self.connection_manager,
                    self.credential_manager,
                    self.update_status
                )
            
            elif panel_name == "Diagnostics":
                self.panels[panel_name] = DiagnosticsPanel(
                    self.content_frame,
                    self.troubleshooting_engine,
                    self.connection_manager,
                    self.update_status
                )
            
            elif panel_name == "Backup":
                self.panels[panel_name] = BackupPanel(
                    self.content_frame,
                    self.backup_manager,
                    self.connection_manager,
                    self.update_status
                )
            
            elif panel_name == "Reports":
                self.panels[panel_name] = ReportsPanel(
                    self.content_frame,
                    self.reporting_engine,
                    self.connection_manager,
                    self.update_status
                )
            
            elif panel_name == "Settings":
                from utils import ConfigManager
                config_manager = ConfigManager()
                config_manager.load_config()
                
                self.panels[panel_name] = SettingsPanel(
                    self.content_frame,
                    self.credential_manager,
                    config_manager,
                    self.update_status
                )
        
        # Show panel
        self.current_panel = self.panels[panel_name]
        self.current_panel.grid(row=0, column=0, sticky="nsew")
        
        self.update_status(f"{panel_name} panel loaded")
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.configure(text=message)
        self.update_idletasks()
    
    def _on_closing(self):
        """Handle window close event"""
        self.logger.info("Application closing...")
        
        # Disconnect all devices
        self.connection_manager.disconnect_all()
        
        # Save any pending configuration
        # (Add config save logic here if needed)
        
        self.logger.info("Cleanup complete")
        self.destroy()


def main():
    """Main function for testing GUI"""
    from utils import setup_logger, ConfigManager
    
    setup_logger()
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    app = MainWindow(config)
    app.mainloop()


if __name__ == "__main__":
    main()
