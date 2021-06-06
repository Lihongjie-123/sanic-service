from sqlalchemy import Column, String, create_engine
from sqlalchemy.dialects.postgres import DATE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FakeTable(declarative_base()):
    __tablename__ = "fake_table"


