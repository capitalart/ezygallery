"""Utility to initialize the SQLite database schema."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.artwork import Base, Artwork

DB_URL = 'sqlite:///app.db'

def init_db(url: str = DB_URL):
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    # Uncomment the lines below to add a sample entry
    # with Session() as session:
    #     sample = Artwork(title='Sample Artwork', seo_filename='sample-artwork')
    #     session.add(sample)
    #     session.commit()

if __name__ == '__main__':
    init_db()
    print('Database initialized.')
