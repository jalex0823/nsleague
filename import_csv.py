import csv
import json
from datetime import datetime

# Read the stadium CSV file into a dictionary
with open('stadium.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    stadiums = {row['Team']: row['City'] + ', ' + row['Stadium'] for row in reader}

def csv_row_to_json(row):
    away_team, home_team, time, time_zone = '', '', '', ''
    if ' at ' in row['Game']:
        away_team, home_team = row['Game'].split(' at ')
    if ' (' in row['Time']:
        time, time_zone = row['Time'].split(' (')  # Split the 'Time' field into time and time zone
        time_zone = time_zone.rstrip(')')  # Remove the closing parenthesis from the time zone
    return {
        "game": {"$oid": "64d4878161069f450ebac5da"},
        "team1": home_team,
        "team2": away_team,
        "date": row['Date'] + "T" + time if time else row['Date'],
        "timeZone": time_zone,
        "location": stadiums.get(home_team, ''),
        "image": "adminImage/1K5BK64J9E9756KF68271059H9D6.png",
        "winner": 0,
        "createdAt": {"$date": datetime.utcnow().isoformat() + "Z"},
        "updatedAt": {"$date": datetime.utcnow().isoformat() + "Z"},
        "__v": 0
    }

with open('schedule.csv', 'r') as f:
    reader = csv.DictReader(f)
    games = [csv_row_to_json(row) for row in reader]

with open('schedule.json', 'w') as f:
    json.dump(games, f)

print("The file has been written successfully.")