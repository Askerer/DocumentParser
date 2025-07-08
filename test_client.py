import requests
import json
import os
from pathlib import Path

class DocumentExtractionClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def test_health(self):
        """測試健康檢查端點"""
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"健康檢查: {response.status_code}")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            return response.json()
        except Exception as e:
            print(f"健康檢查失敗: {e}")
            return None
    
    def extract_document(self, file_path):
        """上傳檔案並擷取內容"""
        if not os.path.exists(file_path):
            print(f"檔案不存在: {file_path}")
            return None
        
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(f"{self.base_url}/extract", files=files)
            
            print(f"檔案擷取狀態: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("擷取成功!")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return result
            else:
                print(f"擷取失敗: {response.text}")
                return None
                
        except Exception as e:
            print(f"擷取過程發生錯誤: {e}")
            return None
    
    def create_test_files(self):
        """建立測試檔案"""
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)
        
        # 建立測試文字檔案
        with open(test_dir / "test.txt", "w", encoding="utf-8") as f:
            f.write("這是一個測試文字檔案\n包含中文內容\n測試編碼支援")
        
        # 建立測試XML檔案
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <title>測試XML檔案</title>
    <description>這是一個測試用的XML檔案</description>
    <data>
        <item id="1">項目一</item>
        <item id="2">項目二</item>
    </data>
    <image>iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==</image>
</root>"""
        
        with open(test_dir / "test.xml", "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        # 建立測試CSV檔案
        csv_content = """姓名,年齡,城市
張三,25,台北
李四,30,高雄
王五,28,台中"""
        
        with open(test_dir / "test.csv", "w", encoding="utf-8") as f:
            f.write(csv_content)
        
        print("測試檔案已建立在 test_files/ 目錄中")
        return test_dir

def main():
    client = DocumentExtractionClient()
    
    print("=== 文件內容擷取服務測試 ===\n")
    
    # 1. 測試健康檢查
    print("1. 測試健康檢查")
    client.test_health()
    print()
    
    # 2. 建立測試檔案
    print("2. 建立測試檔案")
    test_dir = client.create_test_files()
    print()
    
    # 3. 測試各種檔案格式
    test_files = [
        "test_files/test.txt",
        "test_files/test.xml", 
        "test_files/test.csv"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"3. 測試檔案: {file_path}")
            client.extract_document(file_path)
            print("-" * 50)
        else:
            print(f"測試檔案不存在: {file_path}")
    
    print("\n測試完成!")
    print("注意: 您也可以手動上傳其他格式的檔案進行測試")
    print("支援的格式: .xlsx, .xls, .pptx, .ppt, .xml, .pdf, .txt, .md, .csv, .docx")

if __name__ == "__main__":
    main() 