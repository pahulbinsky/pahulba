# To run the parser, follow these steps:
# Install Python on your device
# Install the required libraries - pip install fastapi uvicorn httpx beautifulsoup4
# Navigate to the directory - cd "D:link\link"
# Enter the following command - python server.py
# Enter the host and port on line 117

import asyncio
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from bs4 import BeautifulSoup
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

weather_cache = {
    "last_updated": None,
    "table_data": [],
    "surface_data": {},
    "user_stations": [],
    "error": None
}

URL = "https://tower.obninskiy.net/"

async def fetch_weather_data():
    global weather_cache
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(URL)
            if response.status_code != 200:
                raise Exception(f"Код {response.status_code}")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table_rows = []
        table = soup.find('table') 
        if table:
            rows = table.find_all('tr')[1:] 
            for row in rows:
                cols = [node.get_text(strip=True) for node in row.find_all(['td', 'th'])]
                if len(cols) >= 5:
                    table_rows.append({
                        "height": cols[0],
                        "wind_speed": cols[1],
                        "wind_dir": cols[2],
                        "temp": cols[3],
                        "humidity": cols[4]
                    })

        surface = {}
        page_text = soup.get_text()
        
        for line in page_text.split('\n'):
            line_str = line.strip()
            if "Давление:" in line_str:
                surface["pressure"] = line_str.replace("Давление:", "").strip()
            if "Относительная влажность:" in line_str:
                surface["humidity"] = line_str.replace("Относительная влажность:", "").strip()

        user_stations = []
        for strong_tag in soup.find_all('strong'):
            text = strong_tag.get_text(strip=True)
            if any(place in text for place in ["Обнинск", "Локонское", "Кабицыно"]):
                next_text = strong_tag.next_sibling
                if next_text:
                    val = next_text.strip() if isinstance(next_text, str) else next_text.get_text(strip=True)
                    user_stations.append({
                        "name": text.replace(":", ""),
                        "value": val
                    })

        weather_cache = {
            "last_updated": datetime.now().strftime("%H:%M:%S"),
            "table_data": table_rows,
            "surface_data": surface,
            "user_stations": user_stations,
            "error": None
        }
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Успех! Данные обновлены.")

    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        weather_cache["error"] = f"Ошибка сервера: {str(e)}"

async def weather_scheduler():
    while True:
        await fetch_weather_data()
        await asyncio.sleep(600) 

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(weather_scheduler())

@app.get("/api/weather")
async def get_weather():
    return weather_cache

@app.get("/", response_class=HTMLResponse)
async def read_index():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Файл index.html не найден в папке с сервером!</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="231.0.0.1", port=7789)