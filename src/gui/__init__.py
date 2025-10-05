"""
GUI module initialization
"""

from gui.main_window import MainWindow
from gui.discovery_panel import DiscoveryPanel
from gui.diagnostics_panel import DiagnosticsPanel
from gui.backup_panel import BackupPanel
from gui.reports_panel import ReportsPanel
from gui.settings_panel import SettingsPanel

__all__ = [
    'MainWindow',
    'DiscoveryPanel',
    'DiagnosticsPanel',
    'BackupPanel',
    'ReportsPanel',
    'SettingsPanel',
]
