import sqlite3
import aiosqlite

async def connect_db():
    connection = await aiosqlite.connect('database.db')
    return connection

async def create_db():
    async with aiosqlite.connect('database.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS database (
            date DATETIME PRIMARY KEY,
            rate REAL
        )
        ''')
        await connection.commit()

async def save_data(month, average):
    async with aiosqlite.connect('database.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute('SELECT COUNT(*) FROM database WHERE date = ?', (month,))
        exists = await cursor.fetchone()
        if exists[0] == 0:
            await cursor.execute('''
                INSERT INTO database (date, rate)
                VALUES (?, ?)
            ''', (month, average))
            await connection.commit()

async def print_data():
    async with aiosqlite.connect('database.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute(''' SELECT * FROM database ''')
        rows = await cursor.fetchall()
        for row in rows:
            print(row)
        await connection.commit()

async def get_data():
    async with aiosqlite.connect('database.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute(''' SELECT * FROM database ''')
        rows = rows = await cursor.fetchall()
        data = [{'date': row[0], 'rate': row[1]} for row in rows]
        return {'exchange_rates': data}

async def sort_data(value):
    async with aiosqlite.connect('database.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute(f''' SELECT * FROM database ORDER BY {value} ASC ''')
        rows = await cursor.fetchall()
        data = [{'date': row[0], 'rate': row[1]} for row in rows]
        return {'exchange_rates': data}

async def select_last_three_months():
    async with aiosqlite.connect('database.db') as connection:
        cursor = await connection.cursor()
        await cursor.execute(''' SELECT *
        FROM database
        ORDER BY date DESC
        LIMIT 3;
         ''')
        rows = await cursor.fetchall()
        average = sum(row[1] for row in rows)/3
        return {'average':average}
