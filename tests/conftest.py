"""
Test configuration
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_config():
    """Sample configuration for testing"""
    return {
        'network': {
            'default_timeout': 10,
            'max_concurrent_connections': 50,
            'retry_attempts': 3,
            'retry_delay': 2,
            'ping_timeout': 1
        },
        'discovery': {
            'max_threads': 100
        },
        'diagnostics': {
            'workflows': {
                'test_workflow': {
                    'name': 'Test Workflow',
                    'commands': ['show version'],
                    'enabled': True
                }
            },
            'thresholds': {
                'cpu_warning': 80,
                'cpu_critical': 90
            }
        }
    }
