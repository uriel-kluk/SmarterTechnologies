"""
Package sorting logic for Smarter Technologies robotic automation.
"""

def sort(width: float, height: float, length: float, mass: float) -> str:
    """
    Sorts a package into the appropriate stack based on its dimensions and mass.

    Args:
        width (float): Width in centimeters
        height (float): Height in centimeters
        length (float): Length in centimeters
        mass (float): Mass in kilograms

    Returns:
        str: The stack name ("STANDARD", "SPECIAL", or "REJECTED")
    """
    volume = width * height * length
    bulky = volume >= 1000000 or width >= 150 or height >= 150 or length >= 150
    heavy = mass >= 20

    if bulky and heavy:
        return "REJECTED"
    elif bulky or heavy:
        return "SPECIAL"
    else:
        return "STANDARD"