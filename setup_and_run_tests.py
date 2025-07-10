#!/usr/bin/env python3
"""
測試環境設置和運行腳本

這個腳本會自動：
1. 安裝必要的測試依賴
2. 建立測試檔案
3. 運行測試程式
"""

import subprocess
import sys
import os
import tempfile
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path

def install_dependencies():
    """安裝測試依賴"""
    print("📦 安裝測試依賴...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依賴安裝完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依賴安裝失敗: {e}")
        return False

def create_sample_test_files():
    """建立範例測試檔案"""
    print("📁 建立範例測試檔案...")
    
    # 建立測試目錄
    test_files_dir = Path("sample_test_files")
    test_files_dir.mkdir(exist_ok=True)
    
    try:
        # 建立Excel檔案
        excel_path = test_files_dir / "sample.xlsx"
        data = {
            '產品名稱': ['蘋果', '香蕉', '橘子', '葡萄'],
            '價格': [30, 20, 25, 40],
            '數量': [100, 150, 80, 60],
            '供應商': ['供應商A', '供應商B', '供應商A', '供應商C']
        }
        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False)
        
        # 建立XML檔案
        xml_path = test_files_dir / "sample.xml"
        root = ET.Element("產品清單")
        
        for i, product in enumerate(['筆記型電腦', '手機', '平板'], 1):
            product_elem = ET.SubElement(root, "產品", id=str(i))
            
            name_elem = ET.SubElement(product_elem, "名稱")
            name_elem.text = product
            
            price_elem = ET.SubElement(product_elem, "價格")
            price_elem.text = str(20000 + i * 5000)
            
            desc_elem = ET.SubElement(product_elem, "描述")
            desc_elem.text = f"這是{product}的詳細描述"
        
        tree = ET.ElementTree(root)
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)
        
        # 建立文字檔案
        txt_path = test_files_dir / "sample.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("""範例文字檔案
            
這是一個測試用的文字檔案，包含中文內容。

內容包括：
- 第一項測試項目
- 第二項測試項目
- 第三項測試項目

這個檔案用於測試文字檔案的內容擷取功能。
支援UTF-8編碼，能正確處理中文字符。

檔案結束。""")
        
        # 建立CSV檔案
        csv_path = test_files_dir / "sample.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("""員工編號,姓名,部門,薪資
E001,張三,工程部,50000
E002,李四,市場部,45000
E003,王五,人資部,48000
E004,趙六,財務部,52000
E005,陳七,工程部,55000""")
        
        print(f"✅ 範例測試檔案已建立在 {test_files_dir} 目錄中")
        return True
        
    except Exception as e:
        print(f"❌ 建立範例檔案失敗: {e}")
        return False

def run_quick_test():
    """運行快速測試"""
    print("🚀 運行快速測試...")
    
    try:
        # 確保有範例檔案
        sample_files = [
            "sample_test_files/sample.xlsx",
            "sample_test_files/sample.xml", 
            "sample_test_files/sample.txt",
            "sample_test_files/sample.csv"
        ]
        
        existing_files = [f for f in sample_files if os.path.exists(f)]
        
        if not existing_files:
            print("❌ 沒有找到測試檔案，請先運行 create_sample_test_files()")
            return False
        
        # 運行自定義檔案測試
        cmd = [sys.executable, "test_runner.py", "--mode", "custom", "--files"] + existing_files
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("測試輸出:")
        print(result.stdout)
        
        if result.stderr:
            print("錯誤輸出:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 運行測試失敗: {e}")
        return False

def run_unit_tests():
    """運行單元測試"""
    print("🧪 運行單元測試...")
    
    try:
        cmd = [sys.executable, "test_runner.py", "--mode", "unit"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("單元測試輸出:")
        print(result.stdout)
        
        if result.stderr:
            print("錯誤輸出:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 運行單元測試失敗: {e}")
        return False

def main():
    """主程式"""
    print("🔧 文件內容擷取服務測試環境設置")
    print("=" * 50)
    
    # 1. 安裝依賴
    if not install_dependencies():
        print("❌ 無法繼續，請手動安裝依賴")
        return
    
    # 2. 建立範例檔案
    if not create_sample_test_files():
        print("❌ 無法建立測試檔案")
        return
    
    # 3. 運行快速測試
    print("\n" + "=" * 50)
    success = run_quick_test()
    
    if success:
        print("\n✅ 快速測試完成！")
        print("\n你可以使用以下命令運行更多測試：")
        print("  python test_runner.py --mode unit           # 單元測試")
        print("  python test_runner.py --mode integration    # 整合測試") 
        print("  python test_runner.py --mode performance    # 效能測試")
        print("  python test_runner.py --mode all            # 所有測試")
        print("  python test_runner.py --mode custom --files file1.xlsx file2.pdf  # 自定義檔案測試")
    else:
        print("\n❌ 測試失敗，請檢查錯誤訊息")

if __name__ == "__main__":
    main()