from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import create_db, seed_prices
from routes.public import router as public_router
from routes.admin import router as admin_router
from routes.reminders import router as reminders_router

app = FastAPI(title="AjayCuts Booking")

app.include_router(public_router)
app.include_router(admin_router)
app.include_router(reminders_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    create_db()
    seed_prices()


@app.get("/")
def serve_index():
    return FileResponse("static/index.html")


@app.get("/admin")
def serve_admin():
    return FileResponse("static/admin.html")
