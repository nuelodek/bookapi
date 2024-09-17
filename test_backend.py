import pytest
from fastapi.testclient import TestClient
from app import app  # Assuming 'app' is the FastAPI instance

client = TestClient(app)

# Test adding a new book
def test_add_new_book():
    response = client.post("/books", json={
        "title": "Test Book",
        "author": "John Doe",
        "publisher": "Apress",
        "category": "Technology"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Book added successfully"

# Test adding a new book with missing fields
def test_add_book_missing_fields():
    response = client.post("/books", json={
        "title": "Incomplete Book",
        "author": "Jane Doe",
        # Missing publisher and category
    })
    assert response.status_code == 422  # Validation error due to missing fields

# Test listing all enrolled users
def test_list_enrolled_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list
    if len(response.json()) > 0:
        assert "email" in response.json()[0]  # Ensure user has 'email'

# Test fetching users who have borrowed books
def test_list_users_borrowed_books():
    response = client.get("/users/borrowed")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list
    for user in response.json():
        assert "borrowed_books" in user
        assert isinstance(user["borrowed_books"], list)

# Test fetching unavailable books
def test_list_unavailable_books():
    response = client.get("/books/unavailable")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for book in response.json():
        assert book["available"] is False
        assert "due_date" in book  # Should show when book will be available again

# Test removing a book by ID
def test_remove_book():
    book_id = "some-valid-book-id"  # Replace with a valid book ID
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book removed successfully"

# Test removing a non-existing book
def test_remove_nonexistent_book():
    book_id = "nonexistent-book-id"
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 404  # Not found

