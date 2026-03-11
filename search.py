import streamlit as st
import pandas as pd
import sqlalchemy as sa
from database import engine, employees

def show():

    st.header("Tìm kiếm nhân viên")

    keyword = st.text_input("Tên nhân viên")

    conn = engine.connect()

    df = pd.read_sql(sa.select(employees), conn)

    if keyword:

        df = df[df["name"].str.contains(keyword)]

    st.dataframe(df)