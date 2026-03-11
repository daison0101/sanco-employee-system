import streamlit as st
import sqlalchemy as sa
import bcrypt
from database import engine, users


def show():

    conn = engine.connect()

    st.subheader("Đăng nhập")

    username = st.text_input("Tài khoản")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Đăng nhập"):

        query = sa.select(users).where(users.c.username == username)

        result = conn.execute(query).fetchone()

        if result:

            stored_password = result.password.encode()

            if bcrypt.checkpw(password.encode(), stored_password):

                st.session_state.login = True
                st.success("Đăng nhập thành công")
                st.rerun()

            else:
                st.error("Sai mật khẩu")

        else:
            st.error("Tài khoản không tồn tại")

    st.divider()

    st.subheader("Đăng ký")

    new_user = st.text_input("Username mới")
    new_pass = st.text_input("Password mới", type="password")

    if st.button("Tạo tài khoản"):

        hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())

        with engine.begin() as conn:

            conn.execute(
                users.insert().values(
                    username=new_user,
                    password=hashed.decode()
                )
            )

        st.success("Đăng ký thành công")