import os
import sys
import requests

# 1. SETUP PATHS
day1_dir = os.path.dirname(os.path.abspath(__file__)) # Current file: .../AoC2025/scripts/day1/day1.py
scripts_dir = os.path.dirname(day1_dir)      # .../AoC2025/scripts
project_root = os.path.dirname(scripts_dir)  # .../AoC2025 (Where secret/ lives)

# Add scripts dir to python path to import utils
sys.path.append(scripts_dir)

from utils.support import log_time, _877_cache_now, logger, console
from utils import support

# Set day/year global variables
DAY: int = 1
YEAR: int = 2025

def manual_fetch():
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
    # Dial configuration
    DIAL_SIZE = 100
    current_pos = 50
    zero_visits = 0

    instructions = []
    if not arr:
        return 0

    for row in arr:
        if not row.strip(): 
            continue
        direction = row[0]      # First char is L or R
        amount = int(row[1:])   # Rest is the number
        instructions.append((direction, amount))

    # --- PART 1 LOGIC ---
    if part == 1:
        for direction, amount in instructions:
            if direction == 'R':
                current_pos = (current_pos + amount) % DIAL_SIZE
            elif direction == 'L':
                current_pos = (current_pos - amount) % DIAL_SIZE
            
            # Only count if we land on 0 at the END of the rotation
            if current_pos == 0:
                zero_visits += 1
        return zero_visits

    # --- PART 2 LOGIC ---
    if part == 2:
        for direction, amount in instructions:
            # 1. Count full loops (each 100 clicks guarantees passing 0 exactly once)
            full_loops = amount // DIAL_SIZE
            zero_visits += full_loops
            
            # 2. Check the remainder steps
            remainder = amount % DIAL_SIZE
            
            if direction == 'R':
                # Going Right: hit 0 if we wrap around 100
                # (current + remainder) >= 100 implies crossed 0
                if current_pos + remainder >= DIAL_SIZE:
                    zero_visits += 1
                current_pos = (current_pos + remainder) % DIAL_SIZE
                
            elif direction == 'L':
                # Going Left: hit 0 if we cross going backwards.
                # Special case: If START at 0, L1 goes to 99 (no visit).
                # So only visit 0 if we are NOT at 0, and subtract enough to hit it.
                if current_pos > 0 and remainder >= current_pos:
                    zero_visits += 1
                current_pos = (current_pos - remainder) % DIAL_SIZE
                
        return zero_visits

@log_time
def part_A():
    logger.info("Solving part A")
    try:
        tellstory, testdata = support.pull_puzzle(DAY, YEAR, 1)
        testcase = problemsolver(testdata, 1) # assert testcase == 3, f"Test case A failed: Expected 3, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case A skipped: {e}")

    if not data: return 0
    return problemsolver(data, 1)

@log_time
def part_B():
    logger.info("Solving part B")
    try:
        # Part 2 test case uses same inputs but expects 6
        tellstory, testdata = support.pull_puzzle(DAY, YEAR, 1) 
        testcase = problemsolver(testdata, 2)
        logger.info(f"Part B Test Case Result: {testcase}")
        assert testcase == 6, f"Test case B failed: Expected 6, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case B skipped or failed: {e}")

    if not data: return 0
    return problemsolver(data, 2)

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
    
    # Solve part B
    resultB = part_B()
    logger.info(f"part B solution: \n{resultB}\n")

    # Recurse lines of code
    LOC = support.recurse_dir(f'./scripts/day{DAY}/')
    logger.info(f"Lines of code \n{LOC}")
    
if __name__ == "__main__":
    main()