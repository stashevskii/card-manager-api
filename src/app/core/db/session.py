from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.config import config

engine = create_engine(
    f"postgresql://{config.db_config.db_username}:{config.db_config.db_password}@{config.db_config.db_username}:5432/{config.db_config.db_name}",
    isolation_level="REPEATABLE READ"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
