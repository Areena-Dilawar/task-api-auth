import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(
    title="Task API Auth",
    description="FastAPI authentication API using Supabase Auth.",
    version="1.0"
)


@app.get("/")
def root():
    return {
        "name": "Task API Auth",
        "status": "ok"
    }

