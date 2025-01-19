from typing import Dict, Any
from .base_agent import BaseAgent
from config.settings import VALIDATION_PROMPTS, VALIDATION_THRESHOLD
import logging

logger = logging.getLogger(__name__)

class ValidationAgent(BaseAgent):
    def __init__(self):
        super().__init__("ValidationAgent")
        
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        task_type = data.get('task_type', 'summarize')
        input_text = data.get('input_text', '')
        output_text = data.get('output_text', '')
        
        prompt = f"""请评估以下医疗文本摘要的质量:

原文: {input_text}

摘要: {output_text}

请按照以下格式回复:
评分: [1-5分]
状态: [有效/无效]
说明: [你的解释]

注意: 必须严格按照上述格式回复，每项单独一行。
"""
        
        response = await self._get_completion(prompt)
        validation_result = self._parse_validation_response(response['response'])
        
        # 日志记录
        logger.info(f"验证结果: 分数={validation_result['score']}, 阈值={VALIDATION_THRESHOLD}")
        
        # 验证逻辑
        is_valid = (
            validation_result['score'] >= VALIDATION_THRESHOLD and 
            validation_result['status'] == "有效"
        )
        
        return {
            "is_valid": is_valid,
            "score": validation_result['score'],
            "status": validation_result['status'],
            "explanation": validation_result['explanation']
        }
        
    def _parse_validation_response(self, response: str) -> Dict[str, Any]:
        """解析验证响应"""
        try:
            logger.info(f"验证响应原文:\n{response}")
            
            # 解析方法
            lines = [line.strip() for line in response.split('\n') if line.strip()]
            result = {
                "score": 0,
                "status": "无效",
                "explanation": "解析失败"
            }
            
            for line in lines:
                if "评分" in line:
                    try:
                        # 提取数字部分
                        score_text = line.split("：")[1].strip() if "：" in line else line.split(":")[1].strip()
                        score_text = score_text.replace("分", "").strip()
                        result["score"] = float(score_text)
                    except:
                        logger.error(f"分数解析失败: {line}")
                        
                elif "状态" in line:
                    status_text = line.split("：")[1].strip() if "：" in line else line.split(":")[1].strip()
                    result["status"] = status_text
                    
                elif "说明" in line:
                    explanation_text = line.split("：")[1].strip() if "：" in line else line.split(":")[1].strip()
                    result["explanation"] = explanation_text
            
            # 如果没有找到说明，使用所有未匹配的行作为说明
            if result["explanation"] == "解析失败":
                unmatched_lines = [
                    line for line in lines 
                    if not any(key in line for key in ["评分", "状态", "说明"])
                ]
                if unmatched_lines:
                    result["explanation"] = " ".join(unmatched_lines)
            
            logger.info(f"解析结果: {result}")
            return result
            
        except Exception as e:
            logger.error(f"验证响应解析错误: {str(e)}")
            return {
                "score": 0,
                "status": "无效",
                "explanation": f"解析错误: {str(e)}"
            } 