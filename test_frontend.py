import pytest
from fastapi.testclient import TestClient
from app import app  # Assuming 'app' is the FastAPI instance

client = TestClient(app)

# Test user enrollment with valid data
def test_enroll_user():
    response = client.post("/users", json={
        "email": "testuser@example.com",
        "firstname": "Test",
        "lastname": "User"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User enrolled successfully"

# Test user enrollment with missing fields
def test_enroll_user_missing_field():
    response = client.post("/users", json={
        "email": "incompleteuser@example.com",
        # missing firstname and lastname
    })
    assert response.status_code == 422  # Unprocessable Entity (validation error)

# Test listing all available books
def test_list_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list
    if len(response.json()) > 0:
        assert "title" in response.json()[0]  # Ensure book has 'title'

# Test fetching a single book by ID (assuming ID is provided)
def test_get_single_book():
    book_id = "some-valid-book-id"  # Replace with an actual book ID
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert "title" in response.json()
    assert "author" in response.json()

# Test fetching a non-existing book (invalid ID)
def test_get_nonexistent_book():
    book_id = "nonexistent-book-id"
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404  # Not found

# Test filtering books by publisher
def test_filter_books_by_publisher():
    response = client.get("/books/filter?publisher=Wiley")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for book in response.json():
        assert book['publisher'] == "Wiley"

# Test borrowing a book
def test_borrow_book():
    book_id = "some-valid-book-id"  # Replace with an actual book ID
    response = client.post(f"/books/borrow/{book_id}", json={"days": 7})
    assert response.status_code == 200
    assert "Book borrowed successfully" in response.json()["message"]

# Test borrowing a book that's already borrowed
def test_borrow_already_borrowed_book():
    book_id = "borrowed-book-id"  # Replace with an ID of a borrowed book
    response = client.post(f"/books/borrow/{book_id}", json={"days": 7})
    assert response.status_code == 400  # Should return an error
    assert "Book not available" in response.json()["detail"]

# Test borrowing a book with invalid days input
def test_borrow_book_invalid_days():
    book_id = "some-valid-book-id"  # Replace with an actual book ID
    response = client.post(f"/books/borrow/{book_id}", json={"days": -1})
    assert response.status_code == 422  # Invalid input (negative days)

