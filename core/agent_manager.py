import asyncio
from typing import Dict, Any, List
from agents.main_agents import SummaryAgent, AnalysisAgent
from agents.validator_agents import ValidationAgent
from core.logger import get_logger

logger = get_logger(__name__)

class AgentManager:
    def __init__(self):
        self.summary_agent = SummaryAgent()
        self.analysis_agent = AnalysisAgent()
        self.validator_agent = ValidationAgent()
        
    async def process_medical_text(self, text: str) -> Dict[str, Any]:
        """处理医疗文本的主要流程"""
        try:
            # 1. 生成摘要
            logger.info("开始生成摘要...")
            summary_result = await self.summary_agent.process(text)
            
            # 2. 验证摘要
            logger.info("验证摘要...")
            validation_data = {
                "task_type": "summarize",
                "input_text": text,
                "output_text": summary_result['summary']
            }
            validation_result = await self.validator_agent.process(validation_data)
            
            # 3. 如果验证通过，进行分析
            if validation_result['is_valid']:
                logger.info("摘要验证通过，开始分析...")
                analysis_result = await self.analysis_agent.process(summary_result)
                
                return {
                    "status": "success",
                    "summary": summary_result,
                    "validation": validation_result,
                    "analysis": analysis_result
                }
            else:
                logger.warning("摘要验证未通过")
                return {
                    "status": "validation_failed",
                    "summary": summary_result,
                    "validation": validation_result
                }
                
        except Exception as e:
            logger.error(f"处理失败: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            } 