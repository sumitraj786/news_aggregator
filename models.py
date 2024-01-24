
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    
    hash_id = Column(String, primary_key=True)
    title = Column(String)
    content = Column(String)
    pub_date = Column(DateTime)
    source_url = Column(String)
    category = Column(String)

engine = create_engine('postgresql://postgres:Sumitraj%40786@localhost:5432/news_aggregator')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)