#!/bin/bash

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建必要的目录
mkdir -p logs

# 检查ollama是否已安装
if ! command -v ollama &> /dev/null
then
    echo "正在安装Ollama..."
    curl https://ollama.ai/install.sh | sh
fi

# 下载必要的模型
echo "下载LLaMA模型..."
ollama pull llama3.2:3b

echo "设置完成! 使用以下命令运行应用:"
echo "source venv/bin/activate"
echo "streamlit run app.py" 