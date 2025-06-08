# 📚 Book Collection RESTful API

A RESTful API built with **FastAPI** for managing a book collection. The API provides secure user authentication, supports role-based access control (RBAC), and performs CRUD operations on book data stored in a **PostgreSQL** database.

## 🚀 Features

- **FastAPI** framework for high-performance, asynchronous API endpoints
- **PostgreSQL** for robust and scalable database management
- **JWT Authentication** for secure access to API endpoints
- **Role-Based Access Control (RBAC)**:
  - **Admins** can perform full CRUD operations
  - **Editors** can add, update, and view books
  - **Users** can only view books
- **Hashed User Keys** to ensure data security and protect sensitive information
- Well-structured and efficient routing to avoid redundancy

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Authentication**: JSON Web Tokens (JWT)
- **Security**: Password hashing, RBAC

## 📦 API Endpoints

### Authentication
- `POST /auth/signup` – Register a new user
- `POST /auth/login` – Login and receive JWT token

### Books
- `GET /books` – View all books (User, Editor, Admin)
- `GET /books/{id}` – View a single book by ID
- `POST /books` – Add a new book (Editor, Admin)
- `PUT /books/{id}` – Update book details (Editor, Admin)
- `DELETE /books/{id}` – Delete a book (Admin only)

## 🔐 Roles and Permissions

| Role   | View Books | Add Books | Update Books | Delete Books |
|--------|------------|-----------|--------------|---------------|
| User   | ✅         | ❌        | ❌           | ❌            |
| Editor | ✅         | ✅        | ✅           | ❌            |
| Admin  | ✅         | ✅        | ✅           | ✅            |

## 🧪 Setup and Run Locally

### Prerequisites
- Python 3.9+
- PostgreSQL installed and running

### Installation

```bash
git clone https://github.com/yourusername/book-api.git
cd book-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
fastapi dev 

