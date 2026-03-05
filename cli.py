import argparse
from levels import *

def parse_args():
    parser = argparse.ArgumentParser(description="Pac-Man Game Settings")
    
    # Аргумент для рівня (приймає числа 1, 2 або 3)
    parser.add_argument(
        '--level', 
        type=int, 
        choices=[1, 2, 3], 
        default=None, 
        help="Select level to start: 1, 2, or 3"
    )
    
    # Аргумент для кольору (приймає назви кольорів)
    parser.add_argument(
        '--color', 
        type=str, 
        choices=['blue', 'red', 'green', 'yellow'], 
        default='blue', 
        help="Select wall color"
    )

    return parser.parse_args()

LEVEL_MAPPING = {
    1: LEVEL1,
    2: LEVEL2,
    3: LEVEL3
}

COLOR_MAPPING = {
    'blue': (0, 0, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0)
}