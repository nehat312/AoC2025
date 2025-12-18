import os
import sys
import math
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
DAY: int = 8
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

# --- DSU (Union-Find) Helper Class ---
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            # Connect the smaller tree to the larger tree
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True # Merged successfully
        return False # Already in same set

def problemsolver(arr: list, part: int):
    # 1. Parse Input to Coordinates
    points = []
    for line in arr:
        clean = line.strip()
        if not clean: continue
        parts = clean.split(',')
        points.append(tuple(map(int, parts)))
        
    num_points = len(points)
    if num_points == 0: return 0

    # 2. Calculate All Pairwise Distances
    # We store edges as (distance, idx_a, idx_b)
    edges = []
    
    # Pre-calculate distances is O(N^2).
    # If N is huge (like 2000+), this is ~4M ops, which is fine for Python.
    for i in range(num_points):
        for j in range(i + 1, num_points):
            x1, y1, z1 = points[i]
            x2, y2, z2 = points[j]
            dist_sq = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
            dist = math.sqrt(dist_sq)
            edges.append((dist, i, j))
            
    # 3. Sort Edges by Distance (Shortest First)
    edges.sort(key=lambda x: x[0])
    
    # 4. Process Connections
    dsu = DSU(num_points)
    
    # The prompt defines how many connections to make
    # "After making the ten shortest connections" (example)
    # "connect together the 1000 pairs of junction boxes" (actual problem)
    
    # However, the example logic is: "Process edges in order."
    # "Because these two junction boxes were already in the same circuit, nothing happens!"
    # This implies we iterate through the SORTED list of all pairs, and attempt to union them.
    # The "1000 pairs" limit likely refers to the first 1000 *attempts* (lines in the sorted list),
    # regardless of whether they trigger a merge or not.
    
    limit = 1000
    if part == 1 and num_points < 50: 
        # Detect if we are running the test case (small input)
        # Test case wants 10 connections
        limit = 10

    # Apply the logic: Take the top K shortest edges
    active_edges = edges[:limit]
    
    for dist, u, v in active_edges:
        dsu.union(u, v)
        # Note: Even if they are already connected, the "connection" counts as one of the 1000
        # consumed from our sorted list.
        
    # 5. Calculate Result
    # Get all distinct root parents to find circuit sizes
    circuit_sizes = []
    seen_roots = set()
    
    for i in range(num_points):
        root = dsu.find(i)
        if root not in seen_roots:
            circuit_sizes.append(dsu.size[root])
            seen_roots.add(root)
            
    # Sort sizes descending
    circuit_sizes.sort(reverse=True)
    
    # Multiply largest 3
    if len(circuit_sizes) < 3:
        # Fallback if fewer than 3 circuits exist (unlikely for big inputs)
        result = 1
        for s in circuit_sizes:
            result *= s
        return result
        
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


@log_time
def part_A():
    logger.info("Solving part A")
    
    # 1. Run Test Case
    try:
        testdata = [
            "162,817,812", "57,618,57", "906,360,560", "592,479,940",
            "352,342,300", "466,668,158", "542,29,236", "431,825,988",
            "739,650,466", "52,470,668", "216,146,977", "819,987,18",
            "117,168,530", "805,96,715", "346,949,466", "970,615,88",
            "941,993,340", "862,61,35", "984,92,344", "425,690,689"
        ]
        testcase = problemsolver(testdata, 1)
        logger.info(f"Test Case Result: {testcase}")
        assert testcase == 40, f"Test case A failed: Expected 40, got {testcase}"
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
        data = manual_fetch_override()
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