from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

MYSQL_USER="root"
MYSQL_PASSWORD=""
MYSQL_SERVER="localhost"
MYSQL_PORT=3306
MYSQL_DB="db1"

DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:%s@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}" % quote_plus(MYSQL_PASSWORD)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()