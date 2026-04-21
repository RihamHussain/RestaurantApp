from fastapi import FastAPI
import models
from database import engine
from routers import auth, orders, admin, customers

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(customers.router)