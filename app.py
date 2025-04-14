import streamlit as st
import asyncio
from core.agent_manager import AgentManager
from core.logger import get_logger

logger = get_logger(__name__)

# 初始化AgentManager
@st.cache_resource
def get_agent_manager():
    return AgentManager()

def main():
    st.title("医疗AI助手")
    st.write("这是一个基于AI的医疗文本处理系统，可以进行文本总结、分析和验证。")
    
    # 侧边栏
    st.sidebar.title("设置")
    st.sidebar.markdown("---")
    st.sidebar.write("当前版本: v1.0.0")
    
    # 主界面
    text_input = st.text_area(
        "请输入医疗文本:",
        height=200,
        placeholder="在此输入需要分析的医疗文本..."
    )
    
    if st.button("开始分析"):
        if not text_input:
            st.error("请输入文本内容！")
            return
            
        with st.spinner("正在处理中..."):
            try:
                # 获取AgentManager实例
                agent_manager = get_agent_manager()
                
                # 异步处理
                result = asyncio.run(agent_manager.process_medical_text(text_input))
                
                if result["status"] == "success":
                    st.subheader("文本摘要")
                    st.write(result["summary"]["summary"])
                    
                    st.subheader("验证结果")
                    validation = result["validation"]
                    st.write(f"验证分数: {validation['score']}/5")
                    st.write(f"状态: {validation['status']}")
                    st.write(f"说明: {validation['explanation']}")
                    
                    st.subheader("分析结果")
                    st.write(result["analysis"]["analysis"])
                    
                elif result["status"] == "validation_failed":
                    st.error("验证未通过，请检查输入文本质量。")
                    st.write(result["validation"]["explanation"])
                    
                else:
                    st.error(f"处理出错: {result.get('error', '未知错误')}")
                    
            except Exception as e:
                logger.error(f"处理过程中出错: {str(e)}")
                st.error(f"处理过程中出错: {str(e)}")

if __name__ == "__main__":
    main() 