import logging
from config.logging_config import setup_logger

def get_logger(name: str) -> logging.Logger:
    """获取配置好的logger实例"""
    logger = logging.getLogger(name)
    
    # 如果logger还没有处理器，则设置它
    if not logger.handlers:
        setup_logger()
        
    return logger 