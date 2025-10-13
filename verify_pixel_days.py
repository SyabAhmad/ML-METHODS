# verify_pixel_days.py
import json
from datetime import datetime, timedelta

# ===== CONFIG =====
START_DATE = datetime(2025, 10, 13)  # Must match what you used to generate pixel_days.json
WORD = "MENTEE"

# Original font (must match your generation script)
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

def build_expected_grid():
    """Build the expected 7-row grid from FONT"""
    grid = [[] for _ in range(7)]
    for i, char in enumerate(WORD.upper()):
        letter = FONT.get(char, FONT[' '])
        for row in range(7):
            grid[row].extend(letter[row])
        if i < len(WORD) - 1:
            for row in range(7):
                grid[row].append(0)
    return grid

def dates_to_grid(pixel_days):
    """Convert list of dates to 7-row grid"""
    if not pixel_days:
        return [[0]*1 for _ in range(7)]
    
    # Sort and find range
    sorted_dates = sorted(datetime.strptime(d, "%Y-%m-%d") for d in pixel_days)
    start = sorted_dates[0]
    end = sorted_dates[-1]
    
    # Build grid
    grid = {}
    for d in sorted_dates:
        week = (d - start).days // 7
        weekday = d.weekday()  # Mon=0, Sun=6
        if weekday not in grid:
            grid[weekday] = set()
        grid[weekday].add(week)
    
    # Convert to dense grid
    max_week = max(w for weeks in grid.values() for w in weeks) if grid else 0
    result = []
    for row in range(7):
        row_data = []
        for col in range(max_week + 1):
            row_data.append(1 if col in grid.get(row, set()) else 0)
        result.append(row_data)
    return result

def grids_equal(grid1, grid2):
    """Compare two grids"""
    if len(grid1) != len(grid2):
        return False
    max_cols = max(len(grid1[0]) if grid1 else 0, len(grid2[0]) if grid2 else 0)
    for r in range(7):
        row1 = grid1[r] if r < len(grid1) else []
        row2 = grid2[r] if r < len(grid2) else []
        # Pad rows to same length
        while len(row1) < max_cols:
            row1.append(0)
        while len(row2) < max_cols:
            row2.append(0)
        if row1[:max_cols] != row2[:max_cols]:
            return False
    return True

def print_grid(grid, title):
    print(f"\n{title}")
    print("-" * len(grid[0]) * 2)
    for row in grid:
        print(''.join('█' if cell else '.' for cell in row))

def main():
    # Load saved dates
    try:
        with open("pixel_days.json") as f:
            pixel_days = json.load(f)
        print(f"✅ Loaded {len(pixel_days)} dates from pixel_days.json")
    except FileNotFoundError:
        print("❌ pixel_days.json not found. Run generate script first.")
        return

    # Build expected grid
    expected_grid = build_expected_grid()
    print(f"✅ Expected grid width: {len(expected_grid[0])} columns")

    # Reconstruct grid from dates
    reconstructed_grid = dates_to_grid(pixel_days)
    print(f"✅ Reconstructed grid width: {len(reconstructed_grid[0]) if reconstructed_grid else 0} columns")

    # Compare
    if grids_equal(expected_grid, reconstructed_grid):
        print("\n🎉 VALIDATION PASSED! Your pixel_days.json matches 'MENTEE' exactly.")
    else:
        print("\n❌ VALIDATION FAILED! Mismatch detected.")
        print_grid(expected_grid, "Expected Grid (MENTEE):")
        print_grid(reconstructed_grid, "Reconstructed Grid (from dates):")
        return

    # Final preview
    print_grid(expected_grid, "\nFinal Preview (what will appear on GitHub):")

if __name__ == "__main__":
    main()