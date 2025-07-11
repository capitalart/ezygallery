from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    seo_filename = Column(String(255), unique=True, nullable=False)
    artist_name = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    tags = Column(String(255))
    aspect_ratio = Column(String(50))
    primary_colour = Column(String(50))
    mockups_folder = Column(String(255))
    price = Column(Float)
    discount_price = Column(Float)
    status = Column(String(50), default='active')

    def __repr__(self):
        return f"<Artwork {self.seo_filename}>"
