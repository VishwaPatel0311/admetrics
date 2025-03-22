from typing import Generator

from db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()


