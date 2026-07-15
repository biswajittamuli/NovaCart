from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.products import router as product_router
from app.api.v1.categories import router as category_router


app = FastAPI(
    title = settings.app_name,
    description = "AI powered e-commerce platform",
    version = settings.app_version,
)

app.include_router(product_router)
app.include_router(category_router)

@app.get("/")
def root():
    return{
        "message" : "NovaCart ON",
        "status": "Running",
    }