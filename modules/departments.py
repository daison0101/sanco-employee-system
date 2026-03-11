import streamlit as st
import pandas as pd
import sqlalchemy as sa
from database import engine, departments

def show():

    st.header("🏢 Quản lý phòng ban")

    conn = engine.connect()

    df = pd.read_sql(sa.select(departments), conn)

    # ===== HIỂN THỊ DANH SÁCH =====

    if not df.empty:

        df_show = df.copy()

        df_show.columns = [
            "ID phòng ban",
            "Tên phòng ban",
        ]

        st.dataframe(df_show, use_container_width=True)

    st.divider()

    # ===== THÊM PHÒNG BAN =====

    st.subheader("➕ Thêm phòng ban")

    name = st.text_input("Tên phòng ban")
    description = st.text_input("Mô tả")

    if st.button("Thêm phòng ban"):

        with engine.begin() as conn:

            conn.execute(
                departments.insert().values(
                    name=name,
                    description=description
                )
            )

        st.success("Thêm phòng ban thành công")

        st.rerun()

    st.divider()

    # ===== XÓA PHÒNG BAN =====

    if not df.empty:

        st.subheader("❌ Xóa phòng ban")

        dep_id = st.selectbox(
            "Chọn phòng ban",
            df["id"]
        )

        if st.button("Xóa phòng ban"):

            with engine.begin() as conn:

                conn.execute(
                    departments.delete().where(
                        departments.c.id == dep_id
                    )
                )

            st.success("Đã xóa phòng ban")

            st.rerun()