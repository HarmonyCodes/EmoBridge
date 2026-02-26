import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine
from app.routers import user_router, emotion_router
from app import models

def create_app() -> FastAPI:
    app = FastAPI(title="EmoBridge - Server")

    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(user_router.router)
    app.include_router(emotion_router.router)

    @app.on_event("startup")
    async def on_startup() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await engine.dispose()

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)