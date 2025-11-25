-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Tournaments Table
create table public.tournaments (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  year integer not null,
  status text not null check (status in ('upcoming', 'ongoing', 'completed')),
  start_date date,
  end_date date,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Teams Table
create table public.teams (
  id uuid primary key default gen_random_uuid(),
  tournament_id uuid references public.tournaments(id) on delete cascade,
  name text not null,
  logo_url text,
  "group" text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Players Table
create table public.players (
  id uuid primary key default gen_random_uuid(),
  team_id uuid references public.teams(id) on delete cascade,
  name text not null,
  position text check (position in ('GK', 'DEF', 'MID', 'FWD')),
  shirt_number integer,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Matches Table
create table public.matches (
  id uuid primary key default gen_random_uuid(),
  tournament_id uuid references public.tournaments(id) on delete cascade,
  home_team_id uuid references public.teams(id),
  away_team_id uuid references public.teams(id),
  start_time timestamptz not null,
  status text not null default 'scheduled' check (status in ('scheduled', 'live', 'finished', 'postponed')),
  home_score integer default 0,
  away_score integer default 0,
  stage text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Match Events Table
create table public.match_events (
  id uuid primary key default gen_random_uuid(),
  match_id uuid references public.matches(id) on delete cascade,
  team_id uuid references public.teams(id),
  player_id uuid references public.players(id),
  type text not null check (type in ('goal', 'yellow_card', 'red_card', 'substitution_in', 'substitution_out')),
  minute integer not null,
  extra_info jsonb,
  created_at timestamptz default now()
);

-- Enable Row Level Security (RLS)
alter table public.tournaments enable row level security;
alter table public.teams enable row level security;
alter table public.players enable row level security;
alter table public.matches enable row level security;
alter table public.match_events enable row level security;

-- Create Policies
-- Public Read Access
create policy "Public tournaments are viewable by everyone" on public.tournaments for select using (true);
create policy "Public teams are viewable by everyone" on public.teams for select using (true);
create policy "Public players are viewable by everyone" on public.players for select using (true);
create policy "Public matches are viewable by everyone" on public.matches for select using (true);
create policy "Public match_events are viewable by everyone" on public.match_events for select using (true);

-- Admin Full Access (Assuming authenticated users are admins for now, or check specific role)
-- For simplicity in this phase, we allow any authenticated user to modify. 
-- In production, you'd check for a specific role claim.
create policy "Admins can insert tournaments" on public.tournaments for insert to authenticated with check (true);
create policy "Admins can update tournaments" on public.tournaments for update to authenticated using (true);
create policy "Admins can delete tournaments" on public.tournaments for delete to authenticated using (true);

create policy "Admins can insert teams" on public.teams for insert to authenticated with check (true);
create policy "Admins can update teams" on public.teams for update to authenticated using (true);
create policy "Admins can delete teams" on public.teams for delete to authenticated using (true);

create policy "Admins can insert players" on public.players for insert to authenticated with check (true);
create policy "Admins can update players" on public.players for update to authenticated using (true);
create policy "Admins can delete players" on public.players for delete to authenticated using (true);

create policy "Admins can insert matches" on public.matches for insert to authenticated with check (true);
create policy "Admins can update matches" on public.matches for update to authenticated using (true);
create policy "Admins can delete matches" on public.matches for delete to authenticated using (true);

create policy "Admins can insert match_events" on public.match_events for insert to authenticated with check (true);
create policy "Admins can update match_events" on public.match_events for update to authenticated using (true);
create policy "Admins can delete match_events" on public.match_events for delete to authenticated using (true);
