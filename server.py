from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Разрешаем CORS для разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель для POST-запроса
class LocationData(BaseModel):
    latitude: float
    longitude: float
    timestamp: int

# Инициализация базы данных SQLite
conn = sqlite3.connect("locations.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        timestamp INTEGER
    )
''')
conn.commit()

# Ваши маршруты (эндпоинты) — работают как обычно
@app.post("/location")
async def receive_location(data: LocationData):
    cursor.execute(
        'INSERT INTO locations (latitude, longitude, timestamp) VALUES (?, ?, ?)',
        (data.latitude, data.longitude, data.timestamp)
    )
    conn.commit()
    return JSONResponse({"status": "ok", "message": "Location saved"})

@app.get("/progress")
async def get_progress():
    cursor.execute('SELECT latitude, longitude, timestamp FROM locations')
    rows = cursor.fetchall()
    return JSONResponse({"locations": rows})

# Монтируем папку static на адрес /static
# => index.html будет доступен по /static/index.html
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
