import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import auth, matches, teams, leagues, standings
from app.websocket.live import live_router
from app.database import engine
from app.models import user, favorite_team, match_cache
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    user.Base.metadata.create_all(bind=engine)
    favorite_team.Base.metadata.create_all(bind=engine)
    match_cache.Base.metadata.create_all(bind=engine)
    yield
    # Shutdown


app = FastAPI(
    title="Football Live Hub API",
    description="Backend API for Football Live Hub",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(matches.router, prefix="/api/matches", tags=["matches"])
app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
app.include_router(leagues.router, prefix="/api/leagues", tags=["leagues"])
app.include_router(standings.router, prefix="/api/standings", tags=["standings"])
app.include_router(live_router, prefix="/api/ws")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
