from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

# PostgreSQL connection
SQLALCHEMY_DATABASE_URL = "postgresql://admin-db:admin@backend-db/library"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    category = Column(String)
    available = Column(Boolean, default=True)
    due_date = Column(Date, nullable=True)

class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    category: str

@app.post("/books")
def add_book(book: BookCreate):
    db = SessionLocal()
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()

    # Notify Frontend API via Redis
    # (e.g., publish new book info to Redis Pub/Sub)

    return {"message": "Book added successfully"}
