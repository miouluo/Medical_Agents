import logging
import os
from datetime import datetime

def setup_logger():
    # logs文件夹不存在则创建
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(
                f'logs/medical_ai_agents_{datetime.now().strftime("%Y%m%d")}.log'
            ),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__) 