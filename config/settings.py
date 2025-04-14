import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_CONFIG = {
    "host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    "model": os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    "timeout": 30,
}

DEBUG = os.getenv("DEBUG", "True").lower() == "true"
MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", 5000))
VALIDATION_THRESHOLD = float(os.getenv("VALIDATION_THRESHOLD", 3.0))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/medical_ai_agents.log")

VALIDATION_PROMPTS = {
    "summarize": """评估此摘要是否准确代表原文:
    原文: {input_text}
    摘要: {output_text}
    
    请提供:
    1. 5分制评分(5分为最佳)
    2. '有效' 或 '无效'
    3. 简要说明
    
    格式: 评分: X/5\n状态: 有效/无效\n说明: ...""",
 
} 