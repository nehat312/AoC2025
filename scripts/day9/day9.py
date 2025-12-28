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
DAY: int = 9
YEAR: int = 2025

def manual_fetch():
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
    # 1. Parse Input
    points = []
    for line in arr:
        clean = line.strip()
        if not clean: continue
        try:
            x_str, y_str = clean.split(',')
            points.append((int(x_str), int(y_str)))
        except ValueError:
            continue
            
    if not points:
        return 0
        
    n = len(points)
    max_area = 0

    if part == 1:
        # Iterate all unique pairs
        # O(N^2) complexity. If N <= 3000, this is instant (~4.5M ops).
        for i in range(n):
            x1, y1 = points[i]
            for j in range(i + 1, n):
                x2, y2 = points[j]
                
                # Area logic is inclusive based on examples
                # Example: 2 to 9 is 8 units wide (2,3,4,5,6,7,8,9)
                width = abs(x1 - x2) + 1
                height = abs(y1 - y2) + 1
                area = width * height
                
                if area > max_area:
                    max_area = area
                    
        return max_area

    if part == 2:
        return 0

@log_time
def part_A():
    logger.info("Solving part A")
    
    # 1. Run Test Case
    try:
        testdata = [
            "7,1", "11,1", "11,7", "9,7",
            "9,5", "2,5", "2,3", "7,3"
        ]
        testcase = problemsolver(testdata, 1)
        logger.info(f"Test Case Result: {testcase}")
        assert testcase == 50, f"Test case A failed: Expected 50, got {testcase}"
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
    return 0

def main():
    global data
    data = support.pull_inputdata(DAY, YEAR)
    if not data:
        logger.warning("Standard fetch failed. Attempting manual override...")
        data = manual_fetch()
    if not data:
        logger.error("CRITICAL: Failed to fetch input data.")
        return

    resultA = part_A()
    logger.info(f"part A solution: \n{resultA}\n")
    
    # Recurse lines of code
    LOC = support.recurse_dir(f'./scripts/day{DAY}/')
    logger.info(f"Lines of code \n{LOC}")
    
if __name__ == "__main__":
    main()