#!/bin/bash

echo "啟動文件內容擷取服務..."
echo

# 檢查虛擬環境是否存在
if [ -d ".venv" ]; then
    echo "啟動虛擬環境..."
    source .venv/bin/activate
else
    echo "虛擬環境不存在，使用系統Python..."
fi

# 安裝依賴套件
echo "安裝依賴套件..."
pip install -r requirements.txt

# 啟動服務
echo "啟動服務..."
echo "服務將在 http://localhost:8000 啟動"
echo "按 Ctrl+C 停止服務"
echo
python main.py 