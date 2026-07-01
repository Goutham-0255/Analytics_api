import time
from sqlmodel import SQLModel, create_engine, Session, text
from api.db.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    # Retry connecting up to 10 times while the DB service wakes up
    for attempt in range(10):
        try:
            # 1. Test connection and create standard layouts
            SQLModel.metadata.create_all(engine)

            # 2. Configure the hypertable mapping
            with Session(engine) as session:
                session.exec(
                    text("SELECT create_hypertable('events', 'time', if_not_exists => TRUE);"))
                session.commit()
            print("Successfully initialized database and TimescaleDB hypertable!")
            return
        except Exception as e:
            print(f"Database not ready yet (Attempt {attempt + 1}/10): {e}")
            time.sleep(2)

    raise RuntimeError(
        "Could not connect to the database after multiple attempts.")


def get_session():
    with Session(engine) as session:
        yield session
