from sqlalchemy import Integer, ForeignKey, String, Column, Boolean, DateTime, Float,Table, create_engine,MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os 
load_dotenv(override=True)
SQLALCHEMY_DATABASE_URL = os.environ.get("AIVEN")
engine = create_engine(SQLALCHEMY_DATABASE_URL)


meta = MetaData()
Base = declarative_base(metadata=meta)


class Prediction(Base):
    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True)
    model_name=Column(String)
    date = Column(String) # à changer pour déploiement
    product = Column(String)
    Prediction = Column(Float)
    mape=Column(Float)
    interval_min = Column(Float)
    interval_max = Column(Float)


product_spend = Table("Product_spend",meta,autoload_with=engine)