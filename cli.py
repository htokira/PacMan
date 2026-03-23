import argparse
from levels import LEVEL1, LEVEL2, LEVEL3


def parse_args():
    """
    Обробляє аргументи командного рядка для запуску гри з кастомними налаштуваннями
    Використовує модуль argparse для створення інтерфейсу командного рядка.
    Дозволяє користувачу вказати початковий рівень та колір стін.

    Returns:
        argparse.Namespace: Об'єкт, що містить розпарсені значення аргументів

    Приклад використання в терміналі:
        python main.py --level 2 --color red
    """
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


# Словник для відображення номера рівня
LEVEL_MAPPING = {
    1: LEVEL1,
    2: LEVEL2,
    3: LEVEL3
}

# Словник для конвертації назв кольорів
COLOR_MAPPING = {
    'blue': (0, 0, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0)}
