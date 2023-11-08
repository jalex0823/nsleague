import csv
import json
from datetime import datetime, timezone
import uuid

with open('stadium.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    stadiums = {row['Team']: row['Stadium'] for row in reader}

def csv_row_to_json(row):
    away_team, home_team, time, time_zone = '', '', '', ''
    if ' at ' in row['Game']:
        game = row['Game'].split(' (')[0]  # Exclude everything in parentheses
        away_team, home_team = game.split(' at ')
    if ' (' in row['Time']:
        time, time_zone = row['Time'].split(' (')  # Split the 'Time' field into time and time zone
        time_zone = time_zone.rstrip(')')  # Remove the closing parenthesis from the time zone
    createdAt = datetime.now(timezone.utc).isoformat()
    updatedAt = datetime.now(timezone.utc).isoformat()
    
    # Convert the date to the format "2023-10-26"
    date = datetime.strptime(row['Date'], "%A, %B %d, %Y").strftime("%Y-%m-%d")
    
    # Add a space before 'PM' and 'AM'
    time = time.replace('p', ' PM').replace('a', ' AM')
    
    # Convert the time to 24-hour format if time is not empty
    time_24hr = datetime.strptime(time, "%I:%M %p").strftime("%H:%M") if time else ''
    
    # Append the time from the schedule to the date string
    date_time = date + "T" + time_24hr if time else date
    return {
        "game": {"$oid": "64d4878161069f450ebac5da"},  # Hardcode the game $oid
        "team1": home_team,
        "team2": away_team,
        "date": date_time,
        "timeZone": time_zone,
        "location": stadiums.get(home_team, 'unk'),  # Use 'unk' if stadium is unknown
        "image": "adminImage/5HJ94G6JK18G4E10GD67J179CDGH.png",  # Updated hardcoded image
        "winner": 0,  # Set winner to 0 for all records
        "createdAt": {"$date": createdAt.replace(".000+00:00", "")},
        "updatedAt": {"$date": updatedAt.replace(".000+00:00", "")}
    }

games_by_week = {}

with open('schedule.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        game = csv_row_to_json(row)
        week = row['Week']  # Using the 'Week' column
        if week not in games_by_week:
            games_by_week[week] = []
        games_by_week[week].append(game)

for week, games in games_by_week.items():
    with open(f'schedule_week_{week}.json', 'w') as f:
        json.dump(games, f, indent=4)

print("The files have been written successfully.")