from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers.v1 import user, template, presentation



app = FastAPI(
    title="My API",
    version="1.0.0"
)
app.mount("/templates/static/uploads", StaticFiles(directory="static/uploads"), name="static")


app.include_router(user, prefix="/users", tags=["users"])
app.include_router(template, prefix="/templates", tags=["templates"])
app.include_router(presentation, prefix="/presentation", tags=["presentations"])


@app.get("/health")
async def health():
    return {"status": "ok"}