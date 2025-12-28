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

def is_valid_rect(p1, p2, edges):
    """
    Checks if the rectangle defined by corners p1 and p2 is strictly inside the polygon.
    """
    x1, y1 = p1
    x2, y2 = p2
    
    # Normalize coordinates (Left, Right, Bottom, Top)
    xL, xR = min(x1, x2), max(x1, x2)
    yB, yT = min(y1, y2), max(y1, y2)
    
    # 1. Edge Intersection Check
    # If any polygon edge passes strictly THROUGH the rectangle, it's invalid.
    # (Touching the boundary is allowed).
    for (px1, py1), (px2, py2) in edges:
        # Check Vertical Edges of polygon
        if px1 == px2: 
            edge_x = px1
            edge_y_min, edge_y_max = min(py1, py2), max(py1, py2)
            
            # Does this vertical line cut through the rectangle's x-range?
            if xL < edge_x < xR:
                # Does the y-range overlap?
                # Overlap logic: max(start1, start2) < min(end1, end2)
                overlap_start = max(yB, edge_y_min)
                overlap_end = min(yT, edge_y_max)
                if overlap_start < overlap_end:
                    return False

        # Check Horizontal Edges of polygon
        elif py1 == py2:
            edge_y = py1
            edge_x_min, edge_x_max = min(px1, px2), max(px1, px2)
            
            # Does this horizontal line cut through the rectangle's y-range?
            if yB < edge_y < yT:
                overlap_start = max(xL, edge_x_min)
                overlap_end = min(xR, edge_x_max)
                if overlap_start < overlap_end:
                    return False

    # 2. Inside Check (Ray Casting)
    # If no edges cross, we just need to know if the rectangle is "inside" or "outside".
    # We test the CENTER point of the rectangle.
    mid_x = (xL + xR) / 2
    mid_y = (yB + yT) / 2
    
    intersect_count = 0
    for (px1, py1), (px2, py2) in edges:
        # Ray cast to the Right (increasing X)
        # We only care about vertical polygon edges for this standard algorithm
        if px1 == px2:
            edge_x = px1
            edge_y_min, edge_y_max = min(py1, py2), max(py1, py2)
            
            # Is the edge to the right of our point?
            if edge_x > mid_x:
                # Does the edge span our y-coordinate?
                if edge_y_min <= mid_y < edge_y_max:
                    intersect_count += 1
    
    # Odd intersections = Inside
    return (intersect_count % 2 == 1)

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
            
    if not points: return 0
    n = len(points)
    
    # --- PART 1: Any Rectangle ---
    if part == 1:
        max_area = 0
        for i in range(n):
            x1, y1 = points[i]
            for j in range(i + 1, n):
                x2, y2 = points[j]
                width = abs(x1 - x2) + 1
                height = abs(y1 - y2) + 1
                area = width * height
                if area > max_area:
                    max_area = area
        return max_area

    # --- PART 2: Red/Green Only (Inside Polygon) ---
    if part == 2:
        # Build Polygon Edges
        # The list wraps, so connect last to first
        edges = []
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            edges.append((p1, p2))
            
        max_valid_area = 0
        
        # Iterate all pairs
        for i in range(n):
            p1 = points[i]
            for j in range(i + 1, n):
                p2 = points[j]
                
                # Calculate Area
                width = abs(p1[0] - p2[0]) + 1
                height = abs(p1[1] - p2[1]) + 1
                area = width * height
                
                # Optimization: Prune if smaller than best found
                if area <= max_valid_area:
                    continue
                
                # Geometric Validation
                if is_valid_rect(p1, p2, edges):
                    max_valid_area = area
                    
        return max_valid_area

@log_time
def part_A():
    logger.info("Solving part A")
    try:
        testdata = [
            "7,1", "11,1", "11,7", "9,7",
            "9,5", "2,5", "2,3", "7,3"
        ]
        testcase = problemsolver(testdata, 1)
        assert testcase == 50, f"Test case A failed: Expected 50, got {testcase}"
    except Exception as e:
        logger.warning(f"Test case warning: {e}")

    if not data: return 0
    return problemsolver(data, 1)

@log_time
def part_B():
    logger.info("Solving part B")
    try:
        testdata = [
            "7,1", "11,1", "11,7", "9,7",
            "9,5", "2,5", "2,3", "7,3"
        ]
        testcase = problemsolver(testdata, 2)
        logger.info(f"Test Case B Result: {testcase}")
        assert testcase == 24, f"Test case B failed: Expected 24, got {testcase}"
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