from fastapi import FastAPI, Request
from .models import Base
from .database import engine
from .routers import auth, orders, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="Restaurant_App/templates")

app.mount("/static", StaticFiles(directory="Restaurant_App/static"), name="static")

@app.get("/")
def test(request: Request):
    # Use keyword arguments: request=..., name=..., context=...
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


app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(users.router)