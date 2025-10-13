# generate_pixel_days.py
from datetime import datetime, timedelta
import json

START_DATE = datetime(2025, 10, 13)  # Monday, Oct 13, 2025
WORD = "MENTEE"

FONT = {
    'L': [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
    'O': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
    'V': [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0]],
    'E': [[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
    'M': [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]],
    'N': [[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]],
    'T': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
    ' ': [[0],[0],[0],[0],[0],[0],[0]],
}

# Build grid
grid = [[] for _ in range(7)]
for i, char in enumerate(WORD.upper()):
    letter = FONT.get(char, FONT[' '])
    for row in range(7):
        grid[row].extend(letter[row])
    if i < len(WORD) - 1:
        for row in range(7):
            grid[row].append(0)

# Generate dates
pixel_days = []
for week in range(len(grid[0])):
    for day in range(7):
        if grid[day][week] == 1:
            d = START_DATE + timedelta(weeks=week, days=day)
            pixel_days.append(d.strftime("%Y-%m-%d"))

# Save
with open("pixel_days.json", "w") as f:
    json.dump(sorted(set(pixel_days)), f, indent=2)

print(f"✅ Generated {len(set(pixel_days))} dates for MENTEE")