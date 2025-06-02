import psycopg2

books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "genre": "Fiction", "isbn": "9780743273565", "pages": 180},
    {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian", "isbn": "9780451524935", "pages": 328},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "genre": "Fiction", "isbn": "9780061120084", "pages": 281},
    {"title": "Moby-Dick", "author": "Herman Melville", "year": 1851, "genre": "Adventure", "isbn": "9781503280786", "pages": 585},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813, "genre": "Romance", "isbn": "9781503290563", "pages": 279},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951, "genre": "Fiction", "isbn": "9780316769488", "pages": 277},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "genre": "Fantasy", "isbn": "9780261103344", "pages": 310},
    {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "genre": "Dystopian", "isbn": "9780060850524", "pages": 268},
    {"title": "War and Peace", "author": "Leo Tolstoy", "year": 1869, "genre": "Historical Fiction", "isbn": "9781400079988", "pages": 1225},
    {"title": "The Alchemist", "author": "Paulo Coelho", "year": 1988, "genre": "Adventure", "isbn": "9780061122415", "pages": 208}
]

# DB connection info
conn = psycopg2.connect(
    dbname="defaultdb",
    user="avnadmin",
    password="AVNS_zMgoZHzdafIONX5dlcc",
    host="pg-3f23df40-lambdatest-ca43.l.aivencloud.com",
    port="19490",
    sslmode="require"
)

cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    title TEXT,
    author TEXT,
    year INT,
    genre TEXT,
    isbn TEXT PRIMARY KEY,
    pages INT
);
""")

for book in books:
    cur.execute("""
        INSERT INTO books (title, author, year, genre, isbn, pages)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (isbn) DO NOTHING;
    """, (book['title'], book['author'], book['year'], book['genre'], book['isbn'], book['pages']))

conn.commit()
print("Books inserted successfully.")


cur = conn.cursor()
cur.execute("SELECT title, author, year, genre, isbn, pages FROM books;")
rows = cur.fetchall()

for row in rows:
    print(f"The title is: {row[0]}, and the author is: {row[1]}")

cur.close()
conn.close()