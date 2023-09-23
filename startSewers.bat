@echo off

title Sewers

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM Run __init__.py file through the python exec
"C:\Users\Elio\anaconda3\envs\sewers\python.exe" __init__.py

pause