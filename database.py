import os
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL chưa được cấu hình")

engine = sa.create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

metadata = sa.MetaData()

# ==============================
# USERS
# ==============================

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String(50), unique=True),
    sa.Column("password", sa.String(200)),
)

# ==============================
# DEPARTMENTS
# ==============================

departments = sa.Table(
    "departments",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(100))
)

# ==============================
# POSITIONS
# ==============================

positions = sa.Table(
    "positions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(100))
)

# ==============================
# EMPLOYEES
# ==============================

employees = sa.Table(
    "employees",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(150)),
    sa.Column("email", sa.String(150)),
    sa.Column("phone", sa.String(20)),
    sa.Column("department_id", sa.Integer, sa.ForeignKey("departments.id")),
    sa.Column("position_id", sa.Integer, sa.ForeignKey("positions.id")),
    sa.Column("salary", sa.Float),
)

# ==============================
# ATTENDANCE
# ==============================

attendance = sa.Table(
    "attendance",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("employee_id", sa.Integer, sa.ForeignKey("employees.id")),
    sa.Column("date", sa.Date),
    sa.Column("checkin", sa.String(20)),
    sa.Column("checkout", sa.String(20))
)

metadata.create_all(engine)