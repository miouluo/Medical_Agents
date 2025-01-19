import aiohttp
import json
from typing import Dict, Any
from config.settings import OLLAMA_CONFIG
import logging

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        # 确保base_url是完整的URL
        self.base_url = OLLAMA_CONFIG['host']
        if not self.base_url.startswith('http'):
            self.base_url = f"http://localhost{self.base_url}" if self.base_url.startswith(':') else f"http://{self.base_url}"
        
        self.model = OLLAMA_CONFIG['model']
        self.timeout = OLLAMA_CONFIG['timeout']
        logger.info(f"初始化OllamaClient: URL={self.base_url}, Model={self.model}")
    
    async def generate_completion(self, prompt: str) -> Dict[str, Any]:
        """异步获取Ollama API响应"""
        try:
            url = f"{self.base_url}/api/generate"
            logger.info(f"尝试连接Ollama API: {url}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=self.timeout
                ) as response:
                    logger.info(f"API响应状态码: {response.status}")
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        logger.error(f"API错误响应: {error_text}")
                        raise Exception(f"Ollama API错误: {response.status} - {error_text}")
        except Exception as e:
            logger.error(f"API调用异常: {str(e)}")
            raise
    
    async def chat_completion(self, messages: list) -> Dict[str, Any]:
        """异步获取聊天完成响应"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                timeout=self.timeout
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Ollama API错误: {response.status}") 