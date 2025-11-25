"""
Direct database population script using Supabase client.
This bypasses the API authentication and adds data directly to Supabase.
"""
from app.database import supabase
from datetime import datetime
import sys

print("=" * 60)
print("Adding sample data directly to Supabase database...")
print("=" * 60)

try:
    # 1. Create a tournament
    print("\n1. Creating tournament...")
    tournament_data = {
        "name": "University Championship 2024",
        "year": 2024,
        "status": "ongoing",
        "start_date": "2024-01-15",
        "end_date": "2024-03-30"
    }
    
    response = supabase.table("tournaments").insert(tournament_data).execute()
    if response.data:
        tournament = response.data[0]
        tournament_id = tournament['id']
        print(f"✅ Tournament created: {tournament['name']}")
        print(f"   ID: {tournament_id}")
    else:
        print("❌ Failed to create tournament")
        sys.exit(1)

    # 2. Create teams
    print("\n2. Creating teams...")
    teams_data = [
        {"name": "Red Dragons", "tournament_id": tournament_id, "group": "A"},
        {"name": "Blue Tigers", "tournament_id": tournament_id, "group": "A"},
        {"name": "Green Eagles", "tournament_id": tournament_id, "group": "B"},
        {"name": "Yellow Lions", "tournament_id": tournament_id, "group": "B"}
    ]
    
    teams = []
    for team_data in teams_data:
        response = supabase.table("teams").insert(team_data).execute()
        if response.data:
            team = response.data[0]
            teams.append(team)
            print(f"✅ Team created: {team['name']} (Group {team.get('group', 'N/A')})")
        else:
            print(f"❌ Failed to create team: {team_data['name']}")

    # 3. Create players for each team
    print("\n3. Creating players...")
    player_names = {
        "Red Dragons": [
            {"name": "John Keeper", "position": "GK", "shirt_number": 1},
            {"name": "Mike Defender", "position": "DEF", "shirt_number": 4},
            {"name": "Alex Midfielder", "position": "MID", "shirt_number": 10},
            {"name": "Chris Striker", "position": "FWD", "shirt_number": 9}
        ],
        "Blue Tigers": [
            {"name": "Tom Keeper", "position": "GK", "shirt_number": 1},
            {"name": "Sam Defender", "position": "DEF", "shirt_number": 5},
            {"name": "Jake Midfielder", "position": "MID", "shirt_number": 8},
            {"name": "Ryan Striker", "position": "FWD", "shirt_number": 11}
        ]
    }
    
    for team in teams[:2]:  # Add players to first 2 teams
        team_name = team['name']
        if team_name in player_names:
            print(f"\n   Adding players to {team_name}:")
            for player_data in player_names[team_name]:
                player_data['team_id'] = team['id']
                response = supabase.table("players").insert(player_data).execute()
                if response.data:
                    player = response.data[0]
                    print(f"   ✅ {player['name']} #{player['shirt_number']} ({player.get('position', 'N/A')})")

    # 4. Create matches
    print("\n4. Creating matches...")
    matches_data = [
        {
            "tournament_id": tournament_id,
            "home_team_id": teams[0]['id'],
            "away_team_id": teams[1]['id'],
            "start_time": "2024-02-01T15:00:00+00:00",
            "status": "finished",
            "home_score": 2,
            "away_score": 1,
            "stage": "Group Stage"
        },
        {
            "tournament_id": tournament_id,
            "home_team_id": teams[2]['id'],
            "away_team_id": teams[3]['id'],
            "start_time": "2024-02-01T17:00:00+00:00",
            "status": "finished",
            "home_score": 1,
            "away_score": 1,
            "stage": "Group Stage"
        }
    ]
    
    for match_data in matches_data:
        response = supabase.table("matches").insert(match_data).execute()
        if response.data:
            match = response.data[0]
            home_team = next(t for t in teams if t['id'] == match['home_team_id'])
            away_team = next(t for t in teams if t['id'] == match['away_team_id'])
            print(f"✅ Match: {home_team['name']} {match['home_score']} - {match['away_score']} {away_team['name']}")

    # 5. Fetch and display standings
    print("\n5. Fetching standings...")
    teams_response = supabase.table("teams").select("id, name").eq("tournament_id", tournament_id).execute()
    matches_response = supabase.table("matches").select("*").eq("tournament_id", tournament_id).eq("status", "finished").execute()
    
    if teams_response.data and matches_response.data:
        # Calculate standings
        standings = {}
        for team in teams_response.data:
            standings[team['id']] = {
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
        
        for match in matches_response.data:
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
        
        # Sort and display
        sorted_standings = sorted(standings.values(), key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]), reverse=True)
        
        print("\n" + "=" * 60)
        print("📊 TOURNAMENT STANDINGS")
        print("=" * 60)
        print(f"{'Pos':<4} {'Team':<20} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<4} {'GA':<4} {'GD':<5} {'Pts':<4}")
        print("-" * 60)
        for i, standing in enumerate(sorted_standings, 1):
            print(f"{i:<4} {standing['team_name']:<20} {standing['played']:<3} {standing['won']:<3} "
                  f"{standing['drawn']:<3} {standing['lost']:<3} {standing['goals_for']:<4} "
                  f"{standing['goals_against']:<4} {standing['goal_difference']:<5} {standing['points']:<4}")
        print("=" * 60)

    print("\n✅ Sample data added successfully!")
    print(f"\nView data via API: http://127.0.0.1:8000/docs")
    print(f"Tournament ID: {tournament_id}")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
