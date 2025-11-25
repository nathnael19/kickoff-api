from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from uuid import UUID
from app.database import supabase
from app.schemas import MatchEvent, MatchEventCreate, MatchEventUpdate
from app.dependencies import verify_admin

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.get("/", response_model=List[MatchEvent])
def get_events(match_id: UUID):
    # Events are usually fetched by match_id
    response = supabase.table("match_events").select("*").eq("match_id", str(match_id)).order("minute").execute()
    return response.data

@router.post("/", response_model=MatchEvent, dependencies=[Depends(verify_admin)])
def create_event(event: MatchEventCreate):
    data = event.dict(exclude_unset=True)
    
    response = supabase.table("match_events").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Could not create event")
    return response.data[0]

@router.patch("/{event_id}", response_model=MatchEvent, dependencies=[Depends(verify_admin)])
def update_event(event_id: UUID, event: MatchEventUpdate):
    data = event.dict(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    response = supabase.table("match_events").update(data).eq("id", str(event_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Event not found or update failed")
    return response.data[0]

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_admin)])
def delete_event(event_id: UUID):
    response = supabase.table("match_events").delete().eq("id", str(event_id)).execute()
    if not response.data:
         raise HTTPException(status_code=404, detail="Event not found")
    return None
