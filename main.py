from database.db_config import Base , engine
from accounts.apis import router as accounts_router
from accounts import events
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.settings import settings
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  
    await engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(accounts_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],

    )

    return app



app = create_app()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}