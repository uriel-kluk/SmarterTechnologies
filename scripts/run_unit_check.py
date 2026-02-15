import sys
from pathlib import Path

# Ensure repository root is on sys.path so `src` is importable
ROOT = str(Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.sort_packages import sort

def run():
    try:
        # From tests/unit/test_sort_packages.py - representative checks
        assert sort(10,10,10,5) == "STANDARD"
        assert sort(50,50,50,10) == "STANDARD"
        assert sort(99,99,99,15) == "STANDARD"

        assert sort(150,10,10,5) == "SPECIAL"
        assert sort(10,150,10,5) == "SPECIAL"
        assert sort(10,10,150,5) == "SPECIAL"
        assert sort(100,100,100,5) == "SPECIAL"

        assert sort(10,10,10,20) == "SPECIAL"

        assert sort(150,10,10,20) == "REJECTED"
        assert sort(100,100,100,20) == "REJECTED"

        # edge cases
        assert sort(100,100,100,19.9) == "SPECIAL"
        assert sort(149.9,10,10,5) == "STANDARD"
        assert sort(10,10,10,19.9) == "STANDARD"
        assert sort(150,10,10,19.9) == "SPECIAL"
        assert sort(149.9,10,10,20) == "SPECIAL"

    except AssertionError as e:
        print("Unit check failed:", e)
        sys.exit(1)

    print("Unit check passed")

if __name__ == '__main__':
    run()
