import streamlit as st

from modules import auth
from modules import dashboard
from modules import employees
from modules import departments
from modules import positions
from modules import attendance
from modules import statistics
from modules import search
from modules import export_excel
from modules import ai_chat
from modules import ai_analysis


# =============================
# PAGE CONFIG
# =============================

st.set_page_config(
    page_title="Quản lý nhân viên SanCo",
    page_icon="👨‍💼",
    layout="wide"
)

# =============================
# HEADER
# =============================

st.title("HỆ THỐNG QUẢN LÝ NHÂN VIÊN CÔNG TY SANCO")

# =============================
# SESSION LOGIN
# =============================

if "login" not in st.session_state:
    st.session_state.login = False

# =============================
# LOGIN PAGE
# =============================

if not st.session_state.login:

    auth.show()

# =============================
# MAIN SYSTEM
# =============================

else:

    st.sidebar.success("Đã đăng nhập")

    menu = st.sidebar.selectbox(
        "Chức năng",
        [
            "Dashboard",
            "Quản lý nhân viên",
            "Quản lý phòng ban",
            "Quản lý vị trí",
            "Chấm công",
            "Thống kê",
            "Tìm kiếm nhân viên",
            "Xuất Excel",
            "AI Chat HR",
            "AI Phân tích nhân sự"
        ]
    )

    if menu == "Dashboard":
        dashboard.show()

    elif menu == "Quản lý nhân viên":
        employees.show()

    elif menu == "Quản lý phòng ban":
        departments.show()

    elif menu == "Quản lý vị trí":
        positions.show()

    elif menu == "Chấm công":
        attendance.show()

    elif menu == "Thống kê":
        statistics.show()

    elif menu == "Tìm kiếm nhân viên":
        search.show()

    elif menu == "Xuất Excel":
        export_excel.show()

    elif menu == "AI Chat HR":
        ai_chat.show()

    elif menu == "AI Phân tích nhân sự":
        ai_analysis.show()

    st.sidebar.divider()

    if st.sidebar.button("Đăng xuất"):

        st.session_state.login = False
        st.rerun()