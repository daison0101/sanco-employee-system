import streamlit as st
import pandas as pd
import sqlalchemy as sa
import os
from google import genai
from database import engine, employees, departments, positions

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def show():

    st.header("🧠 AI Phân tích nhân sự")

    conn = engine.connect()

    emp = pd.read_sql(sa.select(employees), conn)
    dep = pd.read_sql(sa.select(departments), conn)
    pos = pd.read_sql(sa.select(positions), conn)

    if emp.empty:
        st.warning("Chưa có dữ liệu nhân viên")
        return

    emp = emp.merge(dep, left_on="department_id", right_on="id", how="left")
    emp = emp.merge(pos, left_on="position_id", right_on="id", how="left")

    if st.button("Phân tích nhân sự bằng AI"):

        prompt = f"""
Bạn là chuyên gia quản trị nhân sự.

Phân tích dữ liệu nhân viên sau:

{emp.to_string()}

Hãy viết báo cáo bằng TIẾNG VIỆT gồm:

1. Tổng quan nhân sự
2. Phòng ban có nhiều nhân viên
3. Phòng ban có ít nhân viên
4. Phân tích mức lương
5. Đề xuất cải thiện quản lý nhân sự

Trình bày rõ ràng từng mục.
"""

        response = client.models.generate_content(
            model="models/gemini-3-flash-preview",
            contents=prompt
        )

        st.write(response.text)