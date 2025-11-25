from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID
from enum import Enum

# Enums
class TournamentStatus(str, Enum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    completed = "completed"

class PlayerPosition(str, Enum):
    GK = "GK"
    DEF = "DEF"
    MID = "MID"
    FWD = "FWD"

class MatchStatus(str, Enum):
    scheduled = "scheduled"
    live = "live"
    finished = "finished"
    postponed = "postponed"

class MatchEventType(str, Enum):
    goal = "goal"
    yellow_card = "yellow_card"
    red_card = "red_card"
    substitution_in = "substitution_in"
    substitution_out = "substitution_out"

# --- Tournament Schemas ---
class TournamentBase(BaseModel):
    name: str
    year: int
    status: TournamentStatus = TournamentStatus.upcoming
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class TournamentCreate(TournamentBase):
    pass

class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
    status: Optional[TournamentStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class Tournament(TournamentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --- Team Schemas ---
class TeamBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    group: Optional[str] = None

class TeamCreate(TeamBase):
    tournament_id: UUID

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    group: Optional[str] = None

class Team(TeamBase):
    id: UUID
    tournament_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --- Player Schemas ---
class PlayerBase(BaseModel):
    name: str
    position: Optional[PlayerPosition] = None
    shirt_number: Optional[int] = None

class PlayerCreate(PlayerBase):
    team_id: UUID

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[PlayerPosition] = None
    shirt_number: Optional[int] = None

class Player(PlayerBase):
    id: UUID
    team_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --- Match Schemas ---
class MatchBase(BaseModel):
    start_time: datetime
    status: MatchStatus = MatchStatus.scheduled
    home_score: int = 0
    away_score: int = 0
    stage: Optional[str] = None

class MatchCreate(MatchBase):
    tournament_id: UUID
    home_team_id: UUID
    away_team_id: UUID

class MatchUpdate(BaseModel):
    start_time: Optional[datetime] = None
    status: Optional[MatchStatus] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    stage: Optional[str] = None
    home_team_id: Optional[UUID] = None
    away_team_id: Optional[UUID] = None

class Match(MatchBase):
    id: UUID
    tournament_id: UUID
    home_team_id: UUID
    away_team_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --- Match Event Schemas ---
class MatchEventBase(BaseModel):
    type: MatchEventType
    minute: int
    extra_info: Optional[Dict[str, Any]] = None

class MatchEventCreate(MatchEventBase):
    match_id: UUID
    team_id: UUID
    player_id: Optional[UUID] = None

class MatchEventUpdate(BaseModel):
    type: Optional[MatchEventType] = None
    minute: Optional[int] = None
    extra_info: Optional[Dict[str, Any]] = None
    team_id: Optional[UUID] = None
    player_id: Optional[UUID] = None

class MatchEvent(MatchEventBase):
    id: UUID
    match_id: UUID
    team_id: UUID
    player_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        orm_mode = True

# --- Standings Schemas ---
class Standing(BaseModel):
    team_id: UUID
    team_name: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    goal_difference: int = 0
    points: int = 0
