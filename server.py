#----------------
# 리눅스, db, backend 연결
# 담당자 : 김예은
#----------------

import os
import psycopg2
from dot_env import load_dotenv
from fastapi import FastAPI, Request
from psycopg2.extras import RealDictCursor

#.env 파일 로드
load_dotenv()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        dbname=os.getenv("PGDATABASE")
    )

app = FastAPI()

@app.post("/submit")
async def submit_data(request: Request):
    data = await request.json()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name, value) VALUES (%s, %s)", (data['name'], data['value']))
    conn.commit()
    conn.close()
    return {"status":"ok"}

@app.post("/data")
async def get_data():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, value FROM items")
    rows = cur.fetchall()
    conn.close()
    return rows