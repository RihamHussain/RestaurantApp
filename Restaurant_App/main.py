from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, orders, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(users.router)