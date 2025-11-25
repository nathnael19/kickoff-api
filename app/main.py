from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import supabase
from app.routers import tournaments, teams, players, matches, events, standings

app = FastAPI(title="Kickoff API", version="1.0.0")

# Enable CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tournaments.router)
app.include_router(teams.router)
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(events.router)
app.include_router(standings.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Kickoff API"}

@app.get("/health")
def health_check():
    return {"status": "ok", "supabase_connected": bool(supabase)}
