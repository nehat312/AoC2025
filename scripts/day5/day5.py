import os
import sys
import requests

# 1. SETUP PATHS
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(current_dir)   # .../AoC2025/scripts
project_root = os.path.dirname(scripts_dir)  # .../AoC2025

# Add scripts dir to python path
sys.path.append(scripts_dir)

from utils.support import log_time, _877_cache_now, logger, console
from utils import support

# Set day/year global variables
DAY: int = 5
YEAR: int = 2025

def manual_fetche():
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
    # 1. Parse Input
    fresh_ranges = []
    available_ids = []
    
    parsing_ranges = True
    
    for row in arr:
        line = row.strip()
        
        # Blank line separates ranges from IDs
        if not line:
            parsing_ranges = False
            continue
            
        if parsing_ranges:
            # Parse Range "Start-End"
            if '-' in line:
                start, end = map(int, line.split('-'))
                fresh_ranges.append((start, end))
        else:
            # Parse ID
            available_ids.append(int(line))

    # --- PART 1: Check Candidates ---
    if part == 1:
        fresh_count = 0
        for ingred_id in available_ids:
            is_fresh = False
            for start, end in fresh_ranges:
                if start <= ingred_id <= end:
                    is_fresh = True
                    break
            if is_fresh:
                fresh_count += 1
        return fresh_count

    # --- PART 2: Calculate Union Volume ---
    if part == 2:
        # Sort by start time
        fresh_ranges.sort(key=lambda x: x[0])
        
        if not fresh_ranges:
            return 0
            
        merged_count = 0
        
        # Initialize with the first range
        curr_start, curr_end = fresh_ranges[0]
        
        for i in range(1, len(fresh_ranges)):
            next_start, next_end = fresh_ranges[i]
            
            # Check for overlap or adjacency
            # If next starts inside (or immediately after) current, we merge.
            # (Using +1 allows 3-4 and 5-6 to merge into 3-6)
            if next_start <= curr_end + 1:
                curr_end = max(curr_end, next_end)
            else:
                # No overlap. Add current block to total and start a new one.
                merged_count += (curr_end - curr_start + 1)
                curr_start, curr_end = next_start, next_end
        
        # Add the final block
        merged_count += (curr_end - curr_start + 1)
        
        return merged_count

@log_time
def part_A():
    logger.info("Solving part A")
    # Mock Test Case for Part A
    try:
        testdata = ["3-5", "10-14", "16-20", "12-18", "", "1", "5", "8", "11", "17", "32"]
        testcase = problemsolver(testdata, 1)
        assert testcase == 3, f"Test case A failed: Expected 3, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case warning: {e}")

    if not data: return 0
    return problemsolver(data, 1)

@log_time
def part_B():
    logger.info("Solving part B")
    
    # Mock Test Case for Part B
    try:
        # Same ranges as above
        testdata = ["3-5", "10-14", "16-20", "12-18", "", "1", "5", "8", "11", "17", "32"]
        testcase = problemsolver(testdata, 2)
        logger.info(f"Test Case B Result: {testcase}")
        # Ranges: 3-5 (3), 10-14, 12-18, 16-20 -> Merge 10-20 (11). Total 14.
        assert testcase == 14, f"Test case B failed: Expected 14, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case B warning: {e}")

    if not data: return 0
    return problemsolver(data, 2)

def main():
    global data
    data = support.pull_inputdata(DAY, YEAR)
    if not data:
        logger.warning("Standard fetch failed. Attempting manual override...")
        data = manual_fetche()
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