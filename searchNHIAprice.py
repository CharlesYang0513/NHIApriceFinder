# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 22:35:14 2025
@author: flysk
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 讓使用者輸入藥品成分
DrugName = input("請輸入藥品成分: ")

# 設定 ChromeDriver 路徑與下載資料夾
PATH = r"C:\Users\flysk\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
download_path = r"C:\Users\flysk\Downloads"

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_path}
options.add_experimental_option("prefs", prefs)

# 啟動瀏覽器
service = Service(PATH)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://info.nhi.gov.tw/INAE3000/INAE3000S01")

# 等待輸入框出現，然後輸入
try:
    wait = WebDriverWait(driver, 10)
    search = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[title="成分名稱"]')))
    search.send_keys(DrugName)
    search.send_keys(Keys.RETURN)

    # 等待頁面載入資料與下載按鈕出現
    download = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-download')))
    time.sleep(1)  # 保險再等一點
    download.click()

    print("✅ 已點擊下載按鈕。請等待檔案下載...")
    time.sleep(5)  # 等檔案下載（視檔案大小可加長）

except Exception as e:
    print("⚠ 發生錯誤：", e)

finally:
    driver.quit()
