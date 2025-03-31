# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 22:39:45 2025

@author: flysk
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("健保署藥品成分查詢工具")

drug_name = st.text_input("請輸入藥品成分（例如 bisoprolol）")

if st.button("查詢") and drug_name:
    # 發送 POST 請求模擬表單查詢
    url = "https://info.nhi.gov.tw/INAE3000/INAE3000S01"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "INGR_NAME": drug_name,
        "qryFlag": "true"
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("div", class_="table-responsive")

        if table:
            st.success("查詢成功！以下是結果：")
            st.write(table.get_text(separator="\n"))
        else:
            st.warning("查無資料，請確認成分名稱拼寫正確。")

    except Exception as e:
        st.error(f"查詢失敗：{e}")
