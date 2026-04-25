import os
from pathlib import Path

# Ensure logs directory exists
LOGS_DIR = Path(__file__).resolve().parent.parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    # Define log formats
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} | {name} | {funcName}:{lineno} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'standard': {
            'format': '[{levelname}] {asctime} | {name} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    
    # Define handlers (where logs go)
    'handlers': {
        # Console output
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
        
        # General application log file
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'encoding': 'utf-8',
        },
        
        # Debug log file (verbose, includes everything)
        'debug_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'debug.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 3,
            'encoding': 'utf-8',
        },
        
        # Error log file (only errors and critical)
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'errors.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'encoding': 'utf-8',
        },
        
        # Security log file (authentication, permissions, suspicious activity)
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'security.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        
        # Database queries log file
        'database_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'database.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 3,
            'encoding': 'utf-8',
        },
        
        # Null handler (for disabling logs when needed)
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    
    # Define loggers (what gets logged)
    'loggers': {
        # Root logger - catches everything not caught by more specific loggers
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file', 'error_file'],
        },
        
        # Django framework logs
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False,
        },
        
        # Django database queries
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['database_file'],
            'propagate': False,
        },
        
        # Django request/response
        'django.request': {
            'level': 'INFO',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False,
        },
        
        # Django security warnings
        'django.security': {
            'level': 'INFO',
            'handlers': ['security_file', 'error_file'],
            'propagate': False,
        },
        
        # Your application logs
        'rabbitmq': {
            'level': 'DEBUG',
            'handlers': ['console', 'debug_file', 'error_file'],
            'propagate': False,
        },
        
        # Application views
        'rabbitmq.views': {
            'level': 'INFO',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False,
        },
        
        # Application models
        'rabbitmq.models': {
            'level': 'DEBUG',
            'handlers': ['console', 'debug_file', 'error_file'],
            'propagate': False,
        },
        
        # Application services/business logic
        'rabbitmq.services': {
            'level': 'INFO',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False,
        },
        
        # Application signals
        'rabbitmq.signals': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        
        # Authentication logs
        'rabbitmq.auth': {
            'level': 'INFO',
            'handlers': ['security_file', 'error_file'],
            'propagate': False,
        },
        
        # Task queue logs (Celery, etc.)
        'celery': {
            'level': 'INFO',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False,
        },
    },
}