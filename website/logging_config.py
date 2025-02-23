import os
import configparser
import logging.config
from functools import lru_cache
from pathlib import Path
import sys

class LoggingSetup:
    _instance = None
    _is_initialized = False

    def __new__(cls, base_dir=None):
        if cls._instance is None:
            cls._instance = super(LoggingSetup, cls).__new__(cls)
        return cls._instance

    def __init__(self, base_dir=None):
        self.base_dir = base_dir
        if not LoggingSetup._is_initialized:
            self._setup_logging()
            LoggingSetup._is_initialized = True

    def _get_file_path(self, filename):
        """Construct absolute path for file using BASE_DIR if available"""
        if self.base_dir:
            file_path = os.path.join(self.base_dir, filename)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, filename)
        """Check if a file exists at the given file path."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")
        return file_path

    @lru_cache(maxsize=None)
    def _read_config(self):
        """Read the INI file (cached to avoid multiple reads)"""
        config = configparser.ConfigParser()
        ini_path = self._get_file_path('logging.ini')
        config.read(ini_path)
        return config

    def _setup_logging(self):
        """Configure logging based on INI file settings"""
        config = self._read_config()
        
        app_name = config.get('loggers', 'app_name', fallback='app')
        log_file_path = self._get_file_path('debug.log')

        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                    'style': '{',
                },
                'simple': {
                    'format': '{levelname} {message}',
                    'style': '{',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': log_file_path,
                    'formatter': 'verbose',
                    'mode': 'a',
                },
            },
            'loggers': {}
        }

        if config.getboolean('loggers', 'django_enabled', fallback=False):
            logging_config['loggers']['django'] = {
                'handlers': ['console', 'file'],
                'level': config.get('loggers', 'django_level', fallback='INFO'),
                'propagate': True,
            }

        if config.getboolean('loggers', 'app_enabled', fallback=False):
            logging_config['loggers'][app_name] = {
                'handlers': ['console', 'file'],
                'level': config.get('loggers', 'app_level', fallback='DEBUG'),
                'propagate': True,
            }

        logging.config.dictConfig(logging_config)

def initialize_logging(base_dir=None):
    """
    Initialize logging configuration.
    
    Args:
        base_dir: Optional directory path to logging.ini file and debug.log file
    """
    LoggingSetup(base_dir=base_dir)
