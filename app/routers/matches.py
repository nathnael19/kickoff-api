from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from uuid import UUID
from app.database import supabase
from app.schemas import Match, MatchCreate, MatchUpdate
from app.dependencies import verify_admin

router = APIRouter(
    prefix="/matches",
    tags=["matches"]
)

@router.get("/", response_model=List[Match])
def get_matches(tournament_id: UUID = None, status: str = None):
    query = supabase.table("matches").select("*")
    if tournament_id:
        query = query.eq("tournament_id", str(tournament_id))
    if status:
        query = query.eq("status", status)
    
    # Order by start_time
    response = query.order("start_time").execute()
    return response.data

@router.get("/{match_id}", response_model=Match)
def get_match(match_id: UUID):
    response = supabase.table("matches").select("*").eq("id", str(match_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Match not found")
    return response.data[0]

@router.post("/", response_model=Match, dependencies=[Depends(verify_admin)])
def create_match(match: MatchCreate):
    data = match.dict(exclude_unset=True)
    # Convert datetime to string
    if data.get('start_time'): data['start_time'] = data['start_time'].isoformat()
    
    # Validate FKs (optional but good practice, though DB will enforce it too)
    # For speed, we let DB enforce it and catch error if needed, or just trust client + DB error.
    
    response = supabase.table("matches").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Could not create match")
    return response.data[0]

@router.patch("/{match_id}", response_model=Match, dependencies=[Depends(verify_admin)])
def update_match(match_id: UUID, match: MatchUpdate):
    data = match.dict(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    if data.get('start_time'): data['start_time'] = data['start_time'].isoformat()

    response = supabase.table("matches").update(data).eq("id", str(match_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Match not found or update failed")
    return response.data[0]

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_admin)])
def delete_match(match_id: UUID):
    response = supabase.table("matches").delete().eq("id", str(match_id)).execute()
    if not response.data:
         raise HTTPException(status_code=404, detail="Match not found")
    return None
