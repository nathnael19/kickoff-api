from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from uuid import UUID
from app.database import supabase
from app.schemas import Player, PlayerCreate, PlayerUpdate
from app.dependencies import verify_admin

router = APIRouter(
    prefix="/players",
    tags=["players"]
)

@router.get("/", response_model=List[Player])
def get_players(team_id: UUID = None):
    query = supabase.table("players").select("*")
    if team_id:
        query = query.eq("team_id", str(team_id))
    response = query.order("shirt_number").execute()
    return response.data

@router.get("/{player_id}", response_model=Player)
def get_player(player_id: UUID):
    response = supabase.table("players").select("*").eq("id", str(player_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Player not found")
    return response.data[0]

@router.post("/", response_model=Player, dependencies=[Depends(verify_admin)])
def create_player(player: PlayerCreate):
    data = player.dict(exclude_unset=True)
    # Ensure team exists
    team_check = supabase.table("teams").select("id").eq("id", str(player.team_id)).execute()
    if not team_check.data:
        raise HTTPException(status_code=404, detail="Team not found")

    response = supabase.table("players").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Could not create player")
    return response.data[0]

@router.patch("/{player_id}", response_model=Player, dependencies=[Depends(verify_admin)])
def update_player(player_id: UUID, player: PlayerUpdate):
    data = player.dict(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    response = supabase.table("players").update(data).eq("id", str(player_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Player not found or update failed")
    return response.data[0]

@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_admin)])
def delete_player(player_id: UUID):
    response = supabase.table("players").delete().eq("id", str(player_id)).execute()
    if not response.data:
         raise HTTPException(status_code=404, detail="Player not found")
    return None
