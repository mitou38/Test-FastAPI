import os
from typing import Dict, Any, Optional

import uvicorn
from starlette.responses import RedirectResponse
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from api.api_v1.api import router as api_router
from api.api_v1.storage.database import Database
from api.api_v1.settings import CORS_MIDDLEWARE_CONFIG
from api.utils import API_functools

API_BASE_URL = "/api/v1"
app = FastAPI(
    title="My Super API",
    description="This is a very fancy project, with auto \
        docs for the API and everything",
    version="1.0.0",
)

app.add_middleware(CORSMiddleware, **CORS_MIDDLEWARE_CONFIG)


@app.get("/data", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def load_fake_data(quantity: Optional[int] = 0) -> Dict[str, Any]:
    """loading fake data

    Returns:
        redirect to root path /
    """
    await API_functools.insert_default_data(quantity=quantity)
    return RedirectResponse(url="/")


@app.get("/", status_code=status.HTTP_200_OK)
async def index() -> Dict[str, Any]:
    """root path, returns some API paths

    Returns:
        Dict[str, Any]: Api routes
    """
    return {
        "detail": "Welcome to FastAPI",
        "apis": ["/api/v1/users"],
        "fake_data": "/data",
        "docs": ["/docs", "/redoc"],
        "openapi": "/openapi.json",
    }


app.include_router(api_router, prefix=API_BASE_URL)

if __name__ == "__main__":  # pragma no cover
    # DB connection
    Database.connect(app)

    uvicorn.run(
        app, host="0.0.0.0", port=int(os.getenv("APP_EXPOSED_PORT", 8000))
    )  # Run app
