import os
import sys
import requests

# 1. SETUP PATHS
# Current file: .../AoC2025/scripts/day2/day2.py
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(current_dir)   # .../AoC2025/scripts
project_root = os.path.dirname(scripts_dir)  # .../AoC2025

# Add scripts dir to python path so we can import utils
sys.path.append(scripts_dir)

from utils.support import log_time, _877_cache_now, logger, console
from utils import support

# Set day/year global variables
DAY: int = 2
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

def is_invalid_part1(num: int) -> bool:
    """
    Part 1 Rule: Sequence repeated EXACTLY twice.
    Strict split in half check.
    """
    s = str(num)
    length = len(s)
    if length % 2 != 0:
        return False
    mid = length // 2
    return s[:mid] == s[mid:]

def is_invalid_part2(num: int) -> bool:
    """
    Part 2 Rule: Sequence repeated AT LEAST twice.
    Logic: If a string S is composed of a repeating pattern P (k >= 2),
    then S will appear inside (S + S) after removing the first and last chars.
    """
    s = str(num)
    # Check if S is a rotation of itself (implies periodicity)
    # (s+s)[1:-1] effectively searches for s in a shifted version of itself
    return s in (s + s)[1:-1]

def problemsolver(arr: list, part: int):
    if not arr:
        return 0

    full_input = "".join(arr).strip()
    range_strings = full_input.split(',')
    
    total_sum = 0
    
    # Parse ranges
    ranges = []
    for r in range_strings:
        if '-' in r:
            start_s, end_s = r.split('-')
            ranges.append((int(start_s), int(end_s)))

    if part == 1:
        for start, end in ranges:
            for num in range(start, end + 1):
                if is_invalid_part1(num):
                    total_sum += num
                    
    elif part == 2:
        for start, end in ranges:
            for num in range(start, end + 1):
                if is_invalid_part2(num):
                    total_sum += num
                    
    return total_sum

@log_time
def part_A():
    logger.info("Solving part A")
    try:
        tellstory, testdata = support.pull_puzzle(DAY, YEAR, 1)
        if not testdata:
             testdata = ["11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"]
        
        testcase = problemsolver(testdata, 1)
        assert testcase == 1227775554, f"Test case A failed: Expected 1227775554, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case warning: {e}")

    if not data: return 0
    return problemsolver(data, 1)

@log_time
def part_B():
    logger.info("Solving part B")
    try:
        # Re-use the same test string from Part A/Prompt
        testdata = ["11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"]
        
        testcase = problemsolver(testdata, 2)
        logger.info(f"Test Case B Result: {testcase}")
        assert testcase == 4174379265, f"Test case B failed: Expected 4174379265, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case B warning: {e}")

    if not data: return 0
    return problemsolver(data, 2)

def main():
    global data
    data = support.pull_inputdata(DAY, YEAR)
    if not data:
        logger.warning("Standard fetch failed. Attempting manual override...")
        data = manual_fetch()
    if not data:
        logger.error("CRITICAL: Failed to fetch input data via any method.")
        return

    resultA = part_A()
    logger.info(f"part A solution: \n{resultA}\n")
    
    resultB = part_B()
    logger.info(f"part B solution: \n{resultB}\n")

    LOC = support.recurse_dir(f'./scripts/day{DAY}/')
    logger.info(f"Lines of code \n{LOC}")
    
if __name__ == "__main__":
    main()