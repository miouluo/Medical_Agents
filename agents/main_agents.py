from typing import Dict, Any, List
from .base_agent import BaseAgent
from utils.text_processors import TextProcessor

class SummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__("SummaryAgent")
        self.text_processor = TextProcessor()
        
    async def process(self, input_text: str) -> Dict[str, Any]:
        # 处理PHI信息
        masked_result = self.text_processor.mask_phi(input_text)
        masked_text = masked_result['masked_text']
        
        # 分割长文本
        text_chunks = self.text_processor.split_text(masked_text)
        
        # 生成每个块的摘要
        summaries = []
        for chunk in text_chunks:
            prompt = f"""请总结以下医疗文本，保持专业性和准确性：
            
            {chunk}
            
            总结："""
            
            response = await self._get_completion(prompt)
            summaries.append(response['response'])
        
        # 合并所有摘要
        final_summary = " ".join(summaries)
        
        return {
            "original_text": input_text,
            "summary": final_summary,
            "masked_values": masked_result['masked_values']
        }

class AnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("AnalysisAgent")
        
    async def process(self, medical_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""请分析以下医疗信息并提供专业见解：
        
        病历摘要：{medical_data.get('summary', '')}
        
        请提供：
        1. 关键发现
        2. 可能的诊断
        3. 建议的后续步骤
        
        分析："""
        
        response = await self._get_completion(prompt)
        
        return {
            "analysis": response['response'],
            "source_data": medical_data
        } 