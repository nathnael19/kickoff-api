from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from uuid import UUID
from app.database import supabase
from app.schemas import Team, TeamCreate, TeamUpdate
from app.dependencies import verify_admin

router = APIRouter(
    prefix="/teams",
    tags=["teams"]
)

@router.get("/", response_model=List[Team])
def get_teams(tournament_id: UUID = None):
    query = supabase.table("teams").select("*")
    if tournament_id:
        query = query.eq("tournament_id", str(tournament_id))
    response = query.order("name").execute()
    return response.data

@router.get("/{team_id}", response_model=Team)
def get_team(team_id: UUID):
    response = supabase.table("teams").select("*").eq("id", str(team_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Team not found")
    return response.data[0]

@router.post("/", response_model=Team, dependencies=[Depends(verify_admin)])
def create_team(team: TeamCreate):
    data = team.dict(exclude_unset=True)
    # Ensure tournament exists
    tournament_check = supabase.table("tournaments").select("id").eq("id", str(team.tournament_id)).execute()
    if not tournament_check.data:
        raise HTTPException(status_code=404, detail="Tournament not found")

    response = supabase.table("teams").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Could not create team")
    return response.data[0]

@router.patch("/{team_id}", response_model=Team, dependencies=[Depends(verify_admin)])
def update_team(team_id: UUID, team: TeamUpdate):
    data = team.dict(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    response = supabase.table("teams").update(data).eq("id", str(team_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Team not found or update failed")
    return response.data[0]

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_admin)])
def delete_team(team_id: UUID):
    response = supabase.table("teams").delete().eq("id", str(team_id)).execute()
    if not response.data:
         raise HTTPException(status_code=404, detail="Team not found")
    return None
