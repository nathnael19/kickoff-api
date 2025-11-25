from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from uuid import UUID
from app.database import supabase
from app.schemas import Tournament, TournamentCreate, TournamentUpdate
from app.dependencies import verify_admin

router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"]
)

@router.get("/", response_model=List[Tournament])
def get_tournaments():
    response = supabase.table("tournaments").select("*").order("created_at", desc=True).execute()
    return response.data

@router.get("/{tournament_id}", response_model=Tournament)
def get_tournament(tournament_id: UUID):
    response = supabase.table("tournaments").select("*").eq("id", str(tournament_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return response.data[0]

@router.post("/", response_model=Tournament, dependencies=[Depends(verify_admin)])
def create_tournament(tournament: TournamentCreate):
    # Convert date objects to string if necessary, but Supabase client usually handles it.
    # json serialization might be needed for dates if using raw requests, but client is smart.
    # We use jsonable_encoder or just dict() with string conversion if needed.
    # For now, let's try direct dict.
    data = tournament.dict(exclude_unset=True)
    if data.get('start_date'): data['start_date'] = data['start_date'].isoformat()
    if data.get('end_date'): data['end_date'] = data['end_date'].isoformat()
    
    response = supabase.table("tournaments").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Could not create tournament")
    return response.data[0]

@router.patch("/{tournament_id}", response_model=Tournament, dependencies=[Depends(verify_admin)])
def update_tournament(tournament_id: UUID, tournament: TournamentUpdate):
    data = tournament.dict(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
        
    if data.get('start_date'): data['start_date'] = data['start_date'].isoformat()
    if data.get('end_date'): data['end_date'] = data['end_date'].isoformat()

    response = supabase.table("tournaments").update(data).eq("id", str(tournament_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tournament not found or update failed")
    return response.data[0]

@router.delete("/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_admin)])
def delete_tournament(tournament_id: UUID):
    response = supabase.table("tournaments").delete().eq("id", str(tournament_id)).execute()
    # Supabase delete returns the deleted rows. If empty, maybe it didn't exist.
    if not response.data:
         raise HTTPException(status_code=404, detail="Tournament not found")
    return None
