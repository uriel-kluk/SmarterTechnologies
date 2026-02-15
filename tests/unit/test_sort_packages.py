"""
Unit tests for package sorting function.
"""

import pytest
from src.sort_packages import sort


class TestSortPackages:
    """Test cases for the sort function."""

    def test_standard_package(self):
        """Test sorting of standard packages."""
        # Small package, light weight
        assert sort(10, 10, 10, 5) == "STANDARD"

        # Medium package, still under limits
        assert sort(50, 50, 50, 10) == "STANDARD"

        # Large but not bulky volume, light weight
        assert sort(99, 99, 99, 15) == "STANDARD"  # volume = 970299 < 1000000

    def test_special_bulky_package(self):
        """Test sorting of bulky packages."""
        # Single dimension >= 150
        assert sort(150, 10, 10, 5) == "SPECIAL"
        assert sort(10, 150, 10, 5) == "SPECIAL"
        assert sort(10, 10, 150, 5) == "SPECIAL"

        # Volume >= 1,000,000
        assert sort(100, 100, 100, 5) == "SPECIAL"  # volume = 1,000,000

        # Large volume, light weight
        assert sort(200, 50, 100, 5) == "SPECIAL"  # volume = 1,000,000

    def test_special_heavy_package(self):
        """Test sorting of heavy packages."""
        # Mass >= 20
        assert sort(10, 10, 10, 20) == "SPECIAL"
        assert sort(10, 10, 10, 25) == "SPECIAL"

    def test_rejected_package(self):
        """Test sorting of packages that are both bulky and heavy."""
        # Bulky by dimension + heavy
        assert sort(150, 10, 10, 20) == "REJECTED"
        assert sort(10, 150, 10, 25) == "REJECTED"

        # Bulky by volume + heavy
        assert sort(100, 100, 100, 20) == "REJECTED"  # volume = 1,000,000

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Exactly at boundaries
        assert sort(100, 100, 100, 19.9) == "SPECIAL"  # volume = 1M, mass < 20
        assert sort(149.9, 10, 10, 5) == "STANDARD"  # dimension < 150
        assert sort(10, 10, 10, 19.9) == "STANDARD"  # mass < 20

        # Exactly at limits
        assert sort(150, 10, 10, 19.9) == "SPECIAL"  # bulky but not heavy
        assert sort(149.9, 10, 10, 20) == "SPECIAL"  # heavy but not bulky

        # Exactly rejected
        assert sort(150, 10, 10, 20) == "REJECTED"

    @pytest.mark.parametrize("width,height,length,mass,expected", [
        # Standard cases
        (10, 10, 10, 5, "STANDARD"),
        (50, 50, 50, 10, "STANDARD"),

        # Bulky cases
        (150, 10, 10, 5, "SPECIAL"),
        (10, 150, 10, 5, "SPECIAL"),
        (10, 10, 150, 5, "SPECIAL"),
        (100, 100, 100, 5, "SPECIAL"),

        # Heavy cases
        (10, 10, 10, 20, "SPECIAL"),
        (10, 10, 10, 25, "SPECIAL"),

        # Rejected cases
        (150, 10, 10, 20, "REJECTED"),
        (100, 100, 100, 20, "REJECTED"),
    ])
    def test_sort_parametrized(self, width, height, length, mass, expected):
        """Parametrized test for various package combinations."""
        assert sort(width, height, length, mass) == expected