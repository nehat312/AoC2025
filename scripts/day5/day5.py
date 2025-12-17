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

    fresh_count = 0

    if part == 1:
        # Check each ID against all ranges
        for ingred_id in available_ids:
            is_fresh = False
            for start, end in fresh_ranges:
                if start <= ingred_id <= end:
                    is_fresh = True
                    break  # Found a valid range, no need to check others
            
            if is_fresh:
                fresh_count += 1
                
        return fresh_count

    if part == 2:
        # Placeholder for Part 2
        return 0

@log_time
def part_A():
    logger.info("Solving part A")
    
    # 1. Run Test Case
    try:
        testdata = [
            "3-5",
            "10-14",
            "16-20",
            "12-18",
            "",
            "1",
            "5",
            "8",
            "11",
            "17",
            "32"
        ]
        testcase = problemsolver(testdata, 1)
        logger.info(f"Test Case Result: {testcase}")
        assert testcase == 3, f"Test case A failed: Expected 3, got {testcase}"
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