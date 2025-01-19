@echo off

:: 创建虚拟环境
python -m venv venv
call venv\Scripts\activate

:: 安装依赖
pip install -r requirements.txt

:: 创建必要的目录
if not exist logs mkdir logs

:: 检查是否安装了Ollama
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 请访问 https://ollama.ai/download 下载并安装Ollama
    echo 安装完成后,请运行: ollama pull llama3.2:3b
    pause
) else (
    :: 下载必要的模型
    echo 下载LLaMA模型...
    ollama pull llama3.2:3b
)

echo 设置完成! 使用以下命令运行应用:
echo venv\Scripts\activate
echo streamlit run app.py

pause 