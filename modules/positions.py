import streamlit as st
import pandas as pd
import sqlalchemy as sa
from database import engine, positions

def show():

    st.header("💼 Quản lý vị trí công việc")

    conn = engine.connect()

    df = pd.read_sql(sa.select(positions), conn)

    # ===== HIỂN THỊ =====

    if not df.empty:

        df_show = df.copy()

        df_show.columns = [
            "ID vị trí",
            "Tên vị trí",
        ]

        st.dataframe(df_show, use_container_width=True)

    st.divider()

    # ===== THÊM VỊ TRÍ =====

    st.subheader("➕ Thêm vị trí")

    name = st.text_input("Tên vị trí")
    description = st.text_input("Mô tả")

    if st.button("Thêm vị trí"):

        with engine.begin() as conn:

            conn.execute(
                positions.insert().values(
                    name=name,
                    description=description
                )
            )

        st.success("Thêm vị trí thành công")

        st.rerun()

    st.divider()

    # ===== XÓA VỊ TRÍ =====

    if not df.empty:

        st.subheader("❌ Xóa vị trí")

        pos_id = st.selectbox(
            "Chọn vị trí",
            df["id"]
        )

        if st.button("Xóa vị trí"):

            with engine.begin() as conn:

                conn.execute(
                    positions.delete().where(
                        positions.c.id == pos_id
                    )
                )

            st.success("Đã xóa vị trí")

            st.rerun()