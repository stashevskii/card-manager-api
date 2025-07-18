from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import config

engine = create_engine(
    f"postgresql://{config.db_config.postgres_user}:{config.db_config.postgres_password}@postgres:5432/{config.db_config.postgres_db}",
    isolation_level="REPEATABLE READ"
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
