from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.products import router as product_router
from app.api.v1.categories import router as category_router
from app.api.v1.users import router as users_router
from app.api.v1.orders import router as orders_router

app = FastAPI(
    title = settings.app_name,
    description = "AI powered e-commerce platform",
    version = settings.app_version,
)

app.include_router(product_router)
app.include_router(category_router)
app.include_router(users_router)
app.include_router(orders_router)
 

@app.get("/")
def root():
    return{
        "message" : "NovaCart ON",
        "status": "Running",
    }