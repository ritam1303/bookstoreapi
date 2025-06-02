from fastapi import FastAPI
from books import router as book_router
from users import router as users

app = FastAPI()
app.include_router(book_router,prefix="/books")
app.include_router(users,prefix="/user")

#kill -9 $(lsof -t -i :8000)   