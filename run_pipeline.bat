@echo off
echo [1/2] ПЕРЕВІРКА СТИЛЮ КОДУ...
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m flake8 . --count --exit-zero --max-complexity=10 --statistics

echo.
echo [2/2] ЗАПУСК ТЕСТІВ...
python -m pytest --cov=.

echo.
echo Pipeline завершено!
pause