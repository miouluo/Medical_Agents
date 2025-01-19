from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from utils.ollama_utils import OllamaClient

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.ollama_client = OllamaClient()
        self.context: Dict[str, Any] = {}
        
    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """处理输入数据的抽象方法"""
        pass
    
    async def _get_completion(self, prompt: str) -> Dict[str, Any]:
        """获取LLM响应"""
        try:
            response = await self.ollama_client.generate_completion(prompt)
            return response
        except Exception as e:
            raise Exception(f"Agent {self.name} 处理失败: {str(e)}")
            
    async def _get_chat_completion(self, messages: list) -> Dict[str, Any]:
        """获取聊天完成响应"""
        try:
            response = await self.ollama_client.chat_completion(messages)
            return response
        except Exception as e:
            raise Exception(f"Agent {self.name} 聊天处理失败: {str(e)}")
    
    def update_context(self, key: str, value: Any) -> None:
        """更新代理上下文"""
        self.context[key] = value
    
    def get_context(self, key: str) -> Optional[Any]:
        """获取上下文值"""
        return self.context.get(key) 