import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Sample data
print("Adding sample data to Kickoff API...")

# 1. Create a tournament
print("\n1. Creating tournament...")
tournament_data = {
    "name": "University Championship 2024",
    "year": 2024,
    "status": "ongoing",
    "start_date": "2024-01-15",
    "end_date": "2024-03-30"
}

response = requests.post(f"{BASE_URL}/tournaments/", json=tournament_data)
if response.status_code == 201 or response.status_code == 200:
    tournament = response.json()
    tournament_id = tournament['id']
    print(f"✅ Tournament created: {tournament['name']} (ID: {tournament_id})")
else:
    print(f"❌ Failed to create tournament: {response.status_code}")
    print(response.text)
    exit(1)

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
    response = requests.post(f"{BASE_URL}/teams/", json=team_data)
    if response.status_code in [200, 201]:
        team = response.json()
        teams.append(team)
        print(f"✅ Team created: {team['name']} (ID: {team['id']})")
    else:
        print(f"❌ Failed to create team {team_data['name']}: {response.status_code}")

# 3. Create players for first team
print("\n3. Creating players for Red Dragons...")
players_data = [
    {"name": "John Keeper", "team_id": teams[0]['id'], "position": "GK", "shirt_number": 1},
    {"name": "Mike Defender", "team_id": teams[0]['id'], "position": "DEF", "shirt_number": 4},
    {"name": "Alex Midfielder", "team_id": teams[0]['id'], "position": "MID", "shirt_number": 10},
    {"name": "Chris Striker", "team_id": teams[0]['id'], "position": "FWD", "shirt_number": 9}
]

for player_data in players_data:
    response = requests.post(f"{BASE_URL}/players/", json=player_data)
    if response.status_code in [200, 201]:
        player = response.json()
        print(f"✅ Player created: {player['name']} #{player['shirt_number']}")
    else:
        print(f"❌ Failed to create player {player_data['name']}: {response.status_code}")

# 4. Create a match
print("\n4. Creating a match...")
match_data = {
    "tournament_id": tournament_id,
    "home_team_id": teams[0]['id'],
    "away_team_id": teams[1]['id'],
    "start_time": "2024-02-01T15:00:00",
    "status": "finished",
    "home_score": 2,
    "away_score": 1,
    "stage": "Group Stage"
}

response = requests.post(f"{BASE_URL}/matches/", json=match_data)
if response.status_code in [200, 201]:
    match = response.json()
    match_id = match['id']
    print(f"✅ Match created: {teams[0]['name']} vs {teams[1]['name']} (ID: {match_id})")
else:
    print(f"❌ Failed to create match: {response.status_code}")
    print(response.text)

# 5. Get standings
print("\n5. Fetching standings...")
response = requests.get(f"{BASE_URL}/standings/{tournament_id}")
if response.status_code == 200:
    standings = response.json()
    print("\n📊 Current Standings:")
    print("-" * 60)
    for i, standing in enumerate(standings, 1):
        print(f"{i}. {standing['team_name']}: {standing['points']} pts | "
              f"P:{standing['played']} W:{standing['won']} D:{standing['drawn']} L:{standing['lost']} | "
              f"GF:{standing['goals_for']} GA:{standing['goals_against']} GD:{standing['goal_difference']}")
else:
    print(f"❌ Failed to fetch standings: {response.status_code}")

print("\n✅ Sample data added successfully!")
print(f"\nView all data at: {BASE_URL}/docs")
