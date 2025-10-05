"""
SNATT - Smart Network Automation and Troubleshooting Tool
Main Application Entry Point
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from gui.main_window import MainWindow
from utils.logger import setup_logger
from utils.config_manager import ConfigManager


def main():
    """Main entry point for SNATT application"""
    
    # Setup logger
    logger = setup_logger()
    logger.info("Starting SNATT application...")
    
    try:
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        logger.info("Configuration loaded successfully")
        
        # Create necessary directories
        create_directories()
        logger.info("Directory structure verified")
        
        # Launch GUI
        logger.info("Launching GUI...")
        app = MainWindow(config)
        app.mainloop()
        
    except Exception as e:
        logger.error(f"Fatal error during application startup: {e}", exc_info=True)
        sys.exit(1)
    
    logger.info("SNATT application closed")


def create_directories():
    """Create necessary application directories if they don't exist"""
    directories = [
        'backups',
        'reports',
        'logs',
        'config',
        'data'
    ]
    
    base_path = Path(__file__).parent.parent
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(exist_ok=True)
        
        # Create .gitkeep files to preserve empty directories in git
        gitkeep_path = dir_path / '.gitkeep'
        if not gitkeep_path.exists():
            gitkeep_path.touch()


if __name__ == "__main__":
    main()
