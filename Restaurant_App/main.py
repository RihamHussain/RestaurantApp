from fastapi import FastAPI, Request
from .models import Base
from .database import engine
from .routers import auth, orders, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)

# ── Use absolute paths so it works on both localhost and Render ──
base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"message": "Welcome to the Restaurant App!"}
    )

@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy"}

@app.get("/menu")
def menu_page(request: Request):
    return templates.TemplateResponse(request=request, name="menu.html")

