import asyncpg
import asyncio

books={
    "title": "1",
    "author": "Paulo Coelho",
    "year": 1988,
    "genre": "Adventure",
    "isbn": "1",
    "pages": 208
}

async def get_books(query: str):
    conn = await asyncpg.connect(
        user='avnadmin',
        password='AVNS_zMgoZHzdafIONX5dlcc',
        database='defaultdb',
        host='pg-3f23df40-lambdatest-ca43.l.aivencloud.com',
        port=19490
    )
    rows = await conn.fetch(query)
    await conn.close()
    return rows

async def getBoooksByIsbn(query: str):
    conn = await asyncpg.connect(
        user='avnadmin',
        password='AVNS_zMgoZHzdafIONX5dlcc',
        database='defaultdb',
        host='pg-3f23df40-lambdatest-ca43.l.aivencloud.com',
        port=19490
    )
    rows = await conn.fetch(query)
    await conn.close()

    return rows

async def updateBooks(query: str):
    conn = await asyncpg.connect(
        user='avnadmin',
        password='AVNS_zMgoZHzdafIONX5dlcc',
        database='defaultdb',
        host='pg-3f23df40-lambdatest-ca43.l.aivencloud.com',
        port=19490
    )
    try:
        rows = await conn.execute(query)
    except asyncpg.PostgresError as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    await conn.close()



