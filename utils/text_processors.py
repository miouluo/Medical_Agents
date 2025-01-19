import re
from typing import List, Dict

class TextProcessor:
    @staticmethod
    def split_text(text: str, max_length: int = 1000) -> List[str]:
        """将长文本分割成更小的块"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            if current_length + sentence_length > max_length:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
                
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
            
        return chunks
    
    @staticmethod
    def mask_phi(text: str) -> Dict[str, str]:
        """掩盖受保护的健康信息(PHI)"""
        # 保存原始值以便验证
        masked_values = {}
        
        # 定义掩码模式
        patterns = {
            'PATIENT_NAME': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'DATE': r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
            'PHONE': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'EMAIL': r'\b[\w\.-]+@[\w\.-]+\.\w+\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'MRN': r'\b[A-Z]{2}\d{6}\b'
        }
        
        masked_text = text
        for mask_type, pattern in patterns.items():
            matches = re.finditer(pattern, masked_text)
            for match in matches:
                original = match.group()
                if original not in masked_values:
                    masked_values[original] = f'[{mask_type}]'
                masked_text = masked_text.replace(original, f'[{mask_type}]')
                
        return {
            'masked_text': masked_text,
            'masked_values': masked_values
        } 