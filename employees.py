import streamlit as st
import pandas as pd
import sqlalchemy as sa
from database import engine, employees, departments, positions

def show():

    st.header("👨‍💼 Quản lý nhân viên")

    conn = engine.connect()

    emp = pd.read_sql(sa.select(employees), conn)
    dep = pd.read_sql(sa.select(departments), conn)
    pos = pd.read_sql(sa.select(positions), conn)

    # ===== HIỂN THỊ DANH SÁCH =====

    if not emp.empty:

        emp = emp.merge(dep, left_on="department_id", right_on="id", how="left")
        emp = emp.merge(pos, left_on="position_id", right_on="id", how="left")

        emp_show = emp[[
            "id_x",
            "name_x",
            "email",
            "phone",
            "name_y",
            "name"
        ]]

        emp_show.columns = [
            "ID",
            "Tên nhân viên",
            "Email",
            "SĐT",
            "Phòng ban",
            "Vị trí"
        ]

        st.dataframe(emp_show, use_container_width=True)

    st.divider()

    # ===== THÊM NHÂN VIÊN =====

    st.subheader("Thêm nhân viên")

    name = st.text_input("Tên nhân viên")
    email = st.text_input("Email")
    phone = st.text_input("SĐT")
    salary = st.number_input("Lương")

    dep_option = st.selectbox(
        "Phòng ban",
        dep["name"]
    )

    pos_option = st.selectbox(
        "Vị trí",
        pos["name"]
    )

    if st.button("Thêm nhân viên"):

        dep_id = dep[dep["name"] == dep_option]["id"].values[0]
        pos_id = pos[pos["name"] == pos_option]["id"].values[0]

        with engine.begin() as conn:

            conn.execute(
                employees.insert().values(
                    name=name,
                    email=email,
                    phone=phone,
                    department_id=int(dep_id),
                    position_id=int(pos_id),
                    salary=salary
                )
            )

        st.success("Thêm nhân viên thành công")

        st.rerun()