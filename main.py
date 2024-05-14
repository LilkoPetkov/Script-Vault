import time
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from addons.tags_metadata import tags_metadata
from database.db import engine, Base, get_db
from routers import user_router, token_router, script_router, settings_router


# SQL Engine binding
Base.metadata.create_all(bind=engine)

# APP initialisation
app = FastAPI(
    title="Script storage",
    description="",
    version="0.0.1",
    license_info={
        "name": "License Info",
        "identifier": "MIT",
    },
    openapi_tags=tags_metadata
)

# DB Setup
get_db()

# Middleware
app.add_middleware(
    CORSMiddleware,
)

# Use Prometheus middleware
Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Routers 
app.include_router(user_router.router)
app.include_router(token_router.router)
app.include_router(script_router.router)
app.include_router(settings_router.router)

# Run APP
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
