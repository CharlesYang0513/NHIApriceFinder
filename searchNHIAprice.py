# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 22:39:45 2025

@author: flysk
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st

PATH = r"C:\Users\flysk\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
drug_name = st.text_input("請輸入藥品成分：")

if st.button("查詢"):
    service = Service(PATH)
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://info.nhi.gov.tw/INAE3000/INAE3000S01")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[title="成分名稱"]'))
        )

        search = driver.find_element(By.CSS_SELECTOR, '[title="成分名稱"]')
        search.send_keys(drug_name)
        search.send_keys(Keys.RETURN)

        # 等候結果表格出現
        result_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table-responsive'))
        )
        result_text = result_element.text
        st.text_area("查詢結果：", result_text, height=300)

    except Exception as e:
        st.error(f"查詢失敗：{e}")
        # st.text(driver.page_source)  # 可打開這行來除錯
    finally:
        driver.quit()