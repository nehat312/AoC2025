import os
import sys
import requests

# 1. SETUP PATHS
# Current file: .../AoC2025/scripts/day3/day3.py
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(current_dir)   # .../AoC2025/scripts
project_root = os.path.dirname(scripts_dir)  # .../AoC2025

# Add scripts dir to python path so we can import utils
sys.path.append(scripts_dir)

from utils.support import log_time, _877_cache_now, logger, console
from utils import support

# Set day/year global variables
DAY: int = 3
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

def get_max_joltage(line: str) -> int:
    """
    Finds the largest 2-digit number possible by picking two digits 
    at indices i and j where i < j.
    """
    digits = line.strip()
    if len(digits) < 2:
        return 0
        
    max_val = -1
    
    # Iterate through every possible first digit (tens place)
    # We stop at len-1 because the first digit must have at least one digit after it
    for i in range(len(digits) - 1):
        digit1 = digits[i]
        
        # Optimization: Find the largest digit in the remainder of the string
        remainder = digits[i+1:]
        max_digit2 = max(remainder) # '9' > '8' > ... string comparison works for single digits
        
        # Form the number
        val = int(digit1 + max_digit2)
        
        if val > max_val:
            max_val = val
            
            # Optimization: If we found '99', we can't get better.
            if max_val == 99:
                return 99
                
    return max_val

def problemsolver(arr: list, part: int):
    if not arr:
        return 0

    total_joltage = 0

    if part == 1:
        for line in arr:
            if not line.strip(): continue
            total_joltage += get_max_joltage(line)
        return total_joltage

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
            "987654321111111",
            "811111111111119",
            "234234234234278",
            "818181911112111"
        ]
        testcase = problemsolver(testdata, 1)
        logger.info(f"Test Case Result: {testcase}")
        assert testcase == 357, f"Test case A failed: Expected 357, got {testcase}"
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