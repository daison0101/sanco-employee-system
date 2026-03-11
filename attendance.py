import streamlit as st
import pandas as pd
import sqlalchemy as sa
from datetime import date
from database import engine, attendance, employees


def show():

    st.header("🕒 Chấm công nhân viên")

    conn = engine.connect()

    # ===== LẤY DANH SÁCH NHÂN VIÊN =====

    emp = pd.read_sql(sa.select(employees), conn)

    emp_option = st.selectbox(
        "Chọn nhân viên",
        emp["name"]
    )

    checkin = st.time_input("Giờ vào")
    checkout = st.time_input("Giờ ra")

    # ===== LƯU CHẤM CÔNG =====

    if st.button("Lưu chấm công"):

        emp_id = emp[emp["name"] == emp_option]["id"].values[0]

        with engine.begin() as conn:

            conn.execute(
                attendance.insert().values(
                    employee_id=int(emp_id),
                    date=date.today(),
                    checkin=str(checkin),
                    checkout=str(checkout)
                )
            )

        st.success("Đã lưu chấm công")

        st.rerun()

    st.divider()

    # ===== HIỂN THỊ LỊCH SỬ CHẤM CÔNG =====

    df = pd.read_sql(sa.select(attendance), conn)

    if not df.empty:

        # join bảng nhân viên để lấy tên
        df = df.merge(emp, left_on="employee_id", right_on="id", how="left")

        df_show = df[[
            "id_x",
            "name",
            "date",
            "checkin",
            "checkout"
        ]]

        df_show.columns = [
            "ID chấm công",
            "Tên nhân viên",
            "Ngày",
            "Giờ vào",
            "Giờ ra"
        ]

        st.dataframe(df_show, use_container_width=True)

    else:

        st.info("Chưa có dữ liệu chấm công")