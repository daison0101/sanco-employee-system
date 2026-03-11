import streamlit as st
import pandas as pd
import sqlalchemy as sa
from database import engine, employees

def show():

    st.header("Xuất Excel")

    conn = engine.connect()

    df = pd.read_sql(sa.select(employees), conn)

    file = "employees.xlsx"

    df.to_excel(file)

    with open(file, "rb") as f:

        st.download_button(
            "Tải file Excel",
            f,
            file_name=file
        )