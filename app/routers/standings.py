from fastapi import APIRouter, HTTPException
from typing import List, Dict
from uuid import UUID
from app.database import supabase
from app.schemas import Standing

router = APIRouter(
    prefix="/standings",
    tags=["standings"]
)

@router.get("/{tournament_id}", response_model=List[Standing])
def get_standings(tournament_id: UUID):
    # 1. Fetch all teams in the tournament
    teams_response = supabase.table("teams").select("id, name").eq("tournament_id", str(tournament_id)).execute()
    if not teams_response.data:
        return []
    
    teams = {t['id']: t for t in teams_response.data}
    
    # Initialize standings
    standings: Dict[str, Dict] = {}
    for team_id, team in teams.items():
        standings[team_id] = {
            "team_id": team_id,
            "team_name": team['name'],
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0
        }

    # 2. Fetch all finished matches
    matches_response = supabase.table("matches").select("*").eq("tournament_id", str(tournament_id)).eq("status", "finished").execute()
    matches = matches_response.data

    # 3. Calculate stats
    for match in matches:
        home_id = match['home_team_id']
        away_id = match['away_team_id']
        home_score = match['home_score']
        away_score = match['away_score']

        if home_id in standings:
            standings[home_id]["played"] += 1
            standings[home_id]["goals_for"] += home_score
            standings[home_id]["goals_against"] += away_score
            standings[home_id]["goal_difference"] += (home_score - away_score)
            
            if home_score > away_score:
                standings[home_id]["won"] += 1
                standings[home_id]["points"] += 3
            elif home_score == away_score:
                standings[home_id]["drawn"] += 1
                standings[home_id]["points"] += 1
            else:
                standings[home_id]["lost"] += 1

        if away_id in standings:
            standings[away_id]["played"] += 1
            standings[away_id]["goals_for"] += away_score
            standings[away_id]["goals_against"] += home_score
            standings[away_id]["goal_difference"] += (away_score - home_score)

            if away_score > home_score:
                standings[away_id]["won"] += 1
                standings[away_id]["points"] += 3
            elif away_score == home_score:
                standings[away_id]["drawn"] += 1
                standings[away_id]["points"] += 1
            else:
                standings[away_id]["lost"] += 1

    # 4. Sort standings
    # Sort by Points (desc), Goal Difference (desc), Goals For (desc)
    sorted_standings = sorted(
        standings.values(),
        key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]),
        reverse=True
    )

    return sorted_standings
