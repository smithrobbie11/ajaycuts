import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, echo=False)


def create_db():
    SQLModel.metadata.create_all(engine)


def seed_prices():
    from backend.config import SERVICES
    from backend.models import ServiceConfig
    with Session(engine) as session:
        for svc in SERVICES:
            if session.get(ServiceConfig, svc["name"]) is None:
                session.add(ServiceConfig(name=svc["name"], price=svc["price"]))
        session.commit()


def get_session():
    with Session(engine) as session:
        yield session