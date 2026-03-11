import streamlit as st
import pandas as pd
import sqlalchemy as sa
import os
from google import genai
from database import engine, employees, departments, positions

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def show():

    st.header("🤖 AI Chat HR")

    # ===== LƯU LỊCH SỬ CHAT =====

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ===== HIỂN THỊ LỊCH SỬ =====

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ===== INPUT =====

    question = st.chat_input("Hỏi về nhân sự...")

    if question:

        # hiển thị câu hỏi
        st.chat_message("user").write(question)

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        conn = engine.connect()

        emp = pd.read_sql(sa.select(employees), conn)
        dep = pd.read_sql(sa.select(departments), conn)
        pos = pd.read_sql(sa.select(positions), conn)

        if not emp.empty:
            emp = emp.merge(dep, left_on="department_id", right_on="id", how="left")
            emp = emp.merge(pos, left_on="position_id", right_on="id", how="left")

        prompt = f"""
Bạn là trợ lý quản lý nhân sự của công ty SanCo.

QUY TẮC:
- Trả lời bằng tiếng Việt
- Trả lời đúng câu hỏi
- Ngắn gọn dễ hiểu

Dữ liệu nhân viên:

{emp.head(100).to_string()}

Câu hỏi:
{question}
"""

        response = client.models.generate_content(
            model="models/gemini-3-flash-preview",
            contents=prompt
        )

        answer = response.text

        # hiển thị AI trả lời
        st.chat_message("assistant").write(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })