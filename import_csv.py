import csv
import json
from datetime import datetime
import uuid

# Read the stadium CSV file into a dictionary

with open('stadium.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    stadiums = {row['Team']: row['Stadium'] + ', ' + row['City'] for row in reader}

with open('stadium.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    stadiums = {row['Team']: row['Stadium'] for row in reader}

def csv_row_to_json(row):
    away_team, home_team, time, time_zone = '', '', '', ''
    if ' at ' in row['Game']:
        away_team, home_team = row['Game'].split(' at ')
    if ' (' in row['Time']:
        time, time_zone = row['Time'].split(' (')  # Split the 'Time' field into time and time zone
        time_zone = time_zone.rstrip(')')  # Remove the closing parenthesis from the time zone
    createdAt = datetime.utcnow().isoformat() + "Z"
    updatedAt = datetime.utcnow().isoformat() + "Z"
    
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
        "stadium": stadiums.get(home_team, ''),
        "image": "adminImage/1K5BK64J9E9756KF68271059H9D6.png",  # Hardcode the image
        "winner": 0,  # Set winner to 0 for all records
        "createdAt": createdAt.replace(".000+00:00", ""),
        "updatedAt": updatedAt.replace(".000+00:00", "")
    }
with open('schedule.csv', 'r') as f:
    reader = csv.DictReader(f)
    games = [csv_row_to_json(row) for row in reader]

with open('schedule.json', 'w') as f:
    json.dump(games, f, indent=4)

print("The file has been written successfully.")