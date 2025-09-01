@echo off
echo Starting Automated Monthly Winners Script...
echo Date: %date%
echo Time: %time%

REM Change to the script directory
cd /d "C:\Users\danielbc\OneDrive - AIIMI LIMITED\Documents\Aiimi\Data CoP\Aiimi Code wars"

REM Run the automated script
python automated-monthly-winners.py

REM Pause to see the output (remove this line if running via Task Scheduler)
pause
