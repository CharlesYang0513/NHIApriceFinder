# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 16:24:48 2025

@author: flysk
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO

st.title("健保署藥品查詢工具（自動儲存 Excel）")

drug_name = st.text_input("請輸入藥品成分名稱（如 bisoprolol）")

if st.button("查詢並下載 Excel") and drug_name:
    url = "https://info.nhi.gov.tw/INAE3000/INAE3000S01"
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {
        "INGR_NAME": drug_name,
        "qryFlag": "true"
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("div", class_="table-responsive")
        if not table:
            st.warning("查無資料，請確認藥品成分名稱拼寫正確。")
        else:
            rows = table.find_all("tr")
            data = [  # 擷取資料列
                [td.text.strip() for td in row.find_all("td")]
                for row in rows[1:]
            ]
            headers = [th.text.strip() for th in rows[0].find_all("th")]
            df = pd.DataFrame(data, columns=headers)

            st.success("查詢成功！以下為查詢結果：")
            st.dataframe(df)

            # 轉換為 Excel 並提供下載
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='查詢結果')
            output.seek(0)

            st.download_button(
                label="點此下載 Excel 檔案",
                data=output,
                file_name=f"{drug_name}_查詢結果.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"查詢失敗：{e}")
