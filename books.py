from fastapi import APIRouter, HTTPException, Body,Depends
from booksdb import get_books,getBoooksByIsbn,updateBooks  # Ensure this is asynchronous now
import asyncio
from users import verify_token, require_roles

router = APIRouter()
@router.get("/")
async def get_books_list(payload: dict = Depends(require_roles("viewer", "editor", "admin"))):
    query = "SELECT title, author, year, genre, isbn, pages FROM books;"
    rows = await get_books(query)  # Await the async call
    books_from_db = [{"title": row['title'], "author": row['author'], "year": row['year'], 
                      "genre": row['genre'], "isbn": row['isbn'], "pages": row['pages']} for row in rows]
    return books_from_db

# Create a new book
@router.post("/")
async def create_book(
    title: str = Body(...),
    author: str = Body(...),
    year: int = Body(...),
    genre: str = Body(...),
    isbn: str = Body(...),
    pages: int = Body(...),
    payload: dict = Depends(require_roles("admin"))
    
):
    query = f"SELECT title, author, year, genre, isbn, pages FROM books WHERE isbn = '{isbn}';"
    rows = await getBoooksByIsbn(query)
    if len(rows)>0:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists.")
    query = f"""
    INSERT INTO books (title, author, year, genre, isbn, pages)
    VALUES ('{title}','{author}',{year},'{genre}',{isbn},{pages})
    """
    rows = await updateBooks(query)
    
    return {"mesage":"updated"}

# Update book details
@router.patch("/{isbn}")
async def update_book(isbn: str, title: str = Body(...), author: str = Body(...), pages: int = Body(...), year: int = Body(...),payload: dict = Depends(require_roles("editor", "admin"))):
    query = f"SELECT title, author, year, genre, isbn, pages FROM books WHERE isbn = '{isbn}';"
    rows = await getBoooksByIsbn(query)
    books_from_db = [{"title": row['title'], "author": row['author'], "year": row['year'], 
                      "genre": row['genre'], "isbn": row['isbn'], "pages": row['pages']} for row in rows]
    for book in books_from_db:
            print(f"The author is {author}")
            query = f"""
            UPDATE books
            SET title = '{title}',
                author = '{author}',
                pages = {pages},
                year = {year}
            WHERE isbn = '{isbn}';
            """
            await updateBooks(query)
            return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book by ISBN
@router.delete("/{isbn}")
async def delete_book(isbn: str,payload: dict = Depends(require_roles("admin"))):
    query = f"SELECT title, author, year, genre, isbn, pages FROM books WHERE isbn = '{isbn}';"
    rows = await getBoooksByIsbn(query)
    if len(rows)>0:
            query = f"DELETE FROM books WHERE isbn ='{isbn}'"
            rows = await updateBooks(query)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
