from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import h3

app = FastAPI()

# Разрешаем запросы с любых сайтов (для тестов)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Структура запроса от клиента
class LocationData(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    timestamp: int

# Подключаемся к базе
conn = sqlite3.connect("locations.db", check_same_thread=False)
cursor = conn.cursor()

# Таблица для истории перемещений
cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        latitude REAL,
        longitude REAL,
        timestamp INTEGER
    )
''')

# Таблица для уже открытых H3-зон
cursor.execute('''
    CREATE TABLE IF NOT EXISTS visited_cells (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        h3_index TEXT,
        UNIQUE(user_id, h3_index)
    )
''')
conn.commit()

@app.post("/location")
async def receive_location(data: LocationData):
    # Сохраняем координаты
    cursor.execute(
        'INSERT INTO locations (user_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)',
        (data.user_id, data.latitude, data.longitude, data.timestamp)
    )

    # Вычисляем H3-ячейку (уровень детализации 9)
    h3_index = h3.geo_to_h3(data.latitude, data.longitude, 9)

    # Сохраняем ячейку, если раньше её не было
    cursor.execute(
        'INSERT OR IGNORE INTO visited_cells (user_id, h3_index) VALUES (?, ?)',
        (data.user_id, h3_index)
    )

    conn.commit()
    return JSONResponse({"status": "ok", "h3_index": h3_index})

@app.get("/visited")
async def get_visited(user_id: str):
    cursor.execute('SELECT h3_index FROM visited_cells WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    return JSONResponse({"visited": [row[0] for row in rows]})

# Раздаём статику
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
