
import logging
import os
from datetime import datetime
from typing import Optional


class SinhalaLogger:
    def __init__(self, name: str = "SinhalaApp", log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Generate log file name with current date and time
        log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_sinhala.log'
        log_filepath = os.path.join(log_dir, log_filename)
        
        # Configure logging with UTF-8 encoding for Sinhala text
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log info message in Sinhala or English"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_request(self, request_data: dict, user_message: str):
        """Log incoming requests with Sinhala support"""
        self.info(f"ලැබුණු ඉල්ලීම: {user_message}")
        self.debug(f"Request data: {request_data}")
    
    def log_response(self, response_data: str):
        """Log responses"""
        self.info(f"පිළිතුර යවන ලදී: {len(response_data)} characters")
    
    def log_error_sinhala(self, error: Exception, context: str = ""):
        """Log errors with Sinhala context"""
        error_msg = f"දෝෂයක් සිදුවිය: {str(error)}"
        if context:
            error_msg += f" - සන්දර්භය: {context}"
        self.error(error_msg)


# Global logger instance
sinhala_logger = SinhalaLogger()


def get_sinhala_logger():
    return sinhala_logger
