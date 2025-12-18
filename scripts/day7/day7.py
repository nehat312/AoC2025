import os
import sys
import requests
from collections import Counter

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(current_dir)   # .../AoC2025/scripts
project_root = os.path.dirname(scripts_dir)  # .../AoC2025

# Add scripts dir to python path
sys.path.append(scripts_dir)

from utils.support import log_time, _877_cache_now, logger, console
from utils import support

# Set day/year global variables
DAY: int = 7
YEAR: int = 2025

def manual_fetch_override():
    """
    Bypasses support.py to fetch data directly.
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
    # Filter empty lines
    grid = [row for row in arr if row.strip()]
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    
    # Find Start 'S'
    start_col = -1
    for c in range(cols):
        if grid[0][c] == 'S':
            start_col = c
            break
            
    if start_col == -1:
        logger.error("No start 'S' found!")
        return 0

    # --- PART 1: Count Splits (Simulation) ---
    if part == 1:
        active_cols = {start_col}
        total_splits = 0
        
        for r in range(rows):
            next_active = set()
            for c in active_cols:
                # Boundary check
                if c < 0 or c >= cols:
                    continue
                
                char = grid[r][c]
                
                if char == '^':
                    total_splits += 1
                    # Split logic: next row gets c-1 and c+1
                    next_active.add(c - 1)
                    next_active.add(c + 1)
                else:
                    # Pass through logic: next row gets c
                    next_active.add(c)
            
            active_cols = next_active
            if not active_cols: break
            
        return total_splits

    # --- PART 2: Count Timelines (Path Counting) ---
    if part == 2:
        # Map of column_index -> count_of_timelines
        # We start with 1 timeline at S
        timeline_counts = Counter()
        timeline_counts[start_col] = 1
        
        final_timelines = 0
        
        for r in range(rows):
            next_counts = Counter()
            
            for c, count in timeline_counts.items():
                # If a beam is out of bounds, it has "exited the manifold"
                # We count it as a finished timeline and don't propagate it.
                if c < 0 or c >= cols:
                    final_timelines += count
                    continue
                
                char = grid[r][c]
                
                if char == '^':
                    # Split: The count propagates to both Left and Right in next row
                    next_counts[c - 1] += count
                    next_counts[c + 1] += count
                else:
                    # Pass through: The count propagates straight down
                    next_counts[c] += count
            
            timeline_counts = next_counts
            
            # Optimization: Stop if empty
            if not timeline_counts:
                break
        
        # Add any timelines remaining at the bottom of the grid
        final_timelines += sum(timeline_counts.values())
        
        return final_timelines

@log_time
def part_A():
    logger.info("Solving part A")
    # Mock Test Case Part A
    try:
        testdata = [
            ".......S.......",
            "...............",
            ".......^.......",
            "...............",
            "......^.^......",
            "...............",
            ".....^.^.^.....",
            "...............",
            "....^.^...^....",
            "...............",
            "...^.^...^.^...",
            "...............",
            "..^...^.....^..",
            "...............",
            ".^.^.^.^.^...^.",
            "..............."
        ]
        testcase = problemsolver(testdata, 1)
        assert testcase == 21, f"Test case A failed: Expected 21, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case warning: {e}")

    if not data: return 0
    return problemsolver(data, 1)

@log_time
def part_B():
    logger.info("Solving part B")
    
    # Mock Test Case Part B
    try:
        testdata = [
            ".......S.......",
            "...............",
            ".......^.......",
            "...............",
            "......^.^......",
            "...............",
            ".....^.^.^.....",
            "...............",
            "....^.^...^....",
            "...............",
            "...^.^...^.^...",
            "...............",
            "..^...^.....^..",
            "...............",
            ".^.^.^.^.^...^.",
            "..............."
        ]
        testcase = problemsolver(testdata, 2)
        logger.info(f"Test Case B Result: {testcase}")
        assert testcase == 40, f"Test case B failed: Expected 40, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case B warning: {e}")

    if not data: return 0
    return problemsolver(data, 2)

def main():
    global data
    data = support.pull_inputdata(DAY, YEAR)
    if not data:
        logger.warning("Standard fetch failed. Attempting manual override...")
        data = manual_fetch_override()
    if not data:
        logger.error("CRITICAL: Failed to fetch input data.")
        return

    resultA = part_A()
    logger.info(f"part A solution: \n{resultA}\n")
    
    resultB = part_B()
    logger.info(f"part B solution: \n{resultB}\n")

    LOC = support.recurse_dir(f'./scripts/day{DAY}/')
    logger.info(f"Lines of code \n{LOC}")
    
if __name__ == "__main__":
    main()