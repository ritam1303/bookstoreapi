import asyncpg
import bcrypt
import asyncio

async def get_conn():
    # Return the connection object
    return await asyncpg.connect(
        user='avnadmin',
        password='AVNS_zMgoZHzdafIONX5dlcc',
        database='defaultdb',
        host='pg-3f23df40-lambdatest-ca43.l.aivencloud.com',
        port=19490
    )

async def create_user_table():
    conn = await get_conn()
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL CHECK (LENGTH(password) >= 8),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        role VARCHAR(50) DEFAULT 'viewer'
    );
    """
    await conn.execute(query)
    await conn.close()

async def create_user(username: str, email: str, password: str, role: str):
    conn = await get_conn()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    query = """
    INSERT INTO users (username, email, password, updated_at, role)
    VALUES ($1, $2, $3, CURRENT_TIMESTAMP, $4);
    """
    # Pass all four parameters, including role
    await conn.execute(query, username, email, hashed_password, role)
    await conn.close()

async def check_user_by_email(email: str):
    conn = await get_conn()
    rows = await conn.fetch("SELECT * FROM users WHERE LOWER(email) = LOWER($1);", email)
    await conn.close()
    return rows

async def show_table():
    conn = await get_conn()
    rows = await conn.fetch("SELECT * FROM users;")
    await conn.close()
    return rows

async def drop_table():
    conn = await get_conn()
    await conn.execute("DROP TABLE IF EXISTS users;")
    await conn.close()

async def get_user_by_id(user_id: int):
    conn = await get_conn()
    row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    await conn.close()
    if row:
        return dict(row)
    return None
    
# async def main():
#     await drop_table()
#     await create_user_table()
#     await create_user("dummyuser", "dummy@example.com", "password123", "admin")
#     rows = await show_table()
#     print(rows)

# asyncio.run(main())
