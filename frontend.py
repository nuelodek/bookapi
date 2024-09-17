from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime, timedelta
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient('mongodb://frontend-db:27017/')
db = client.library

class User(BaseModel):
    email: str
    firstname: str
    lastname: str

class BorrowBook(BaseModel):
    days: int

@app.post("/users")
def enroll_user(user: User):
    user_dict = user.dict()
    user_dict['borrowed_books'] = []
    db.users.insert_one(user_dict)
    return {"message": "User enrolled successfully"}

@app.get("/books")
def list_books():
    books = db.books.find({"available": True})
    return list(books)

@app.post("/books/borrow/{book_id}")
def borrow_book(book_id: str, borrow: BorrowBook):
    book = db.books.find_one({"_id": ObjectId(book_id), "available": True})
    if not book:
        raise HTTPException(status_code=404, detail="Book not available")

    # Mark the book as borrowed
    due_date = datetime.now() + timedelta(days=borrow.days)
    db.books.update_one({"_id": ObjectId(book_id)}, {"$set": {"available": False, "due_date": due_date}})
    
    return {"message": f"Book borrowed successfully, due on {due_date}"}

