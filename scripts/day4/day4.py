import os
import sys
import requests

# 1. SETUP PATHS
# Current file: .../AoC2025/scripts/day4/day4.py
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(current_dir)   # .../AoC2025/scripts
project_root = os.path.dirname(scripts_dir)  # .../AoC2025

# Add scripts dir to python path so we can import utils
sys.path.append(scripts_dir)

from utils.support import log_time, _877_cache_now, logger, console
from utils import support

# Set day/year global variables
DAY: int = 4
YEAR: int = 2025

def manual_fetch():
    """
    Bypasses support.py to fetch data directly using the confirmed working logic.
    """
    cookie_path = os.path.join(project_root, 'secret', 'cookie.txt')
    try:
        with open(cookie_path, 'r') as f:
            cookie = f.read().strip()
    except FileNotFoundError:
        logger.error(f"Cookie file not found at: {cookie_path}")
        return None

    url = f"https://adventofcode.com/{YEAR}/day/{DAY}/input"
    headers = {
        "Cookie": f"session={cookie}",
        "User-Agent": "github.com/nehat312/AoC2025 by nehat312"
    }
    
    try:
        logger.info(f"Attempting manual fetch from: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logger.info("Manual fetch successful!")
            return response.text.splitlines()
        else:
            logger.error(f"Manual fetch failed. Status: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Manual fetch crashed: {e}")
        return None

def problemsolver(arr: list, part: int):
    # Filter out empty lines to ensure clean grid
    grid = [row.strip() for row in arr if row.strip()]
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    accessible_count = 0
    
    # 8 neighbor offsets (diagonals included)
    # (-1, -1) (-1, 0) (-1, 1)
    # (0, -1)    XXX    (0, 1)
    # (1, -1)  (1, 0)  (1, 1)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    if part == 1:
        for r in range(rows):
            for c in range(cols):
                # We only care if the current spot is a paper roll '@'
                if grid[r][c] != '@':
                    continue
                
                neighbor_rolls = 0
                
                # Check all 8 neighbors
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    
                    # Boundary Check: Is the neighbor inside the grid?
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '@':
                            neighbor_rolls += 1
                
                # Rule: "accessible if fewer than 4 rolls in adjacent positions"
                if neighbor_rolls < 4:
                    accessible_count += 1
                    
        return accessible_count

    if part == 2:
        # Placeholder for Part 2
        return 0

@log_time
def part_A():
    logger.info("Solving part A")
    
    # 1. Run Test Case
    try:
        # Mock data from prompt
        testdata = [
            "..@@.@@@@.",
            "@@@.@.@.@@",
            "@@@@@.@.@@",
            "@.@@@@..@.",
            "@@.@@@@.@@",
            ".@@@@@@@.@",
            ".@.@.@.@@@",
            "@.@@@.@@@@",
            ".@@@@@@@@.",
            "@.@.@@@.@."
        ]
        testcase = problemsolver(testdata, 1)
        logger.info(f"Test Case Result: {testcase}")
        assert testcase == 13, f"Test case A failed: Expected 13, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case warning: {e}")

    # 2. Run Real Data
    if not data:
        logger.error("No data available for Part A.")
        return 0
        
    answerA = problemsolver(data, 1)
    return answerA

@log_time
def part_B():
    logger.info("Solving part B")
    # Placeholder
    answerB = problemsolver(data, 2)
    return answerB

def main():
    global data
    
    # 1. Try Standard Fetch
    data = support.pull_inputdata(DAY, YEAR)
    
    # 2. If Standard Fetch fails, use Manual Override
    if not data:
        logger.warning("Standard fetch failed. Attempting manual override...")
        data = manual_fetch()

    # 3. Hard Stop
    if not data:
        logger.error("CRITICAL: Failed to fetch input data via any method.")
        return

    # Solve part A
    resultA = part_A()
    logger.info(f"part A solution: \n{resultA}\n")
    
    # Solve part B (Will be 0)
    resultB = part_B()
    logger.info(f"part B solution: \n{resultB}\n")

    # Recurse lines of code
    LOC = support.recurse_dir(f'./scripts/day{DAY}/')
    logger.info(f"Lines of code \n{LOC}")
    
if __name__ == "__main__":
    main()