@echo off

title Get Applications Data
echo Get Applications Data
echo Working... Do not close the file...

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM Run files through the python exec
"C:\Users\Elio\anaconda3\envs\sewers\python.exe" utils/getPythonPath.py
"C:\Users\Elio\anaconda3\envs\sewers\python.exe" utils/getMayaPath.py
"C:\Users\Elio\anaconda3\envs\sewers\python.exe" utils/getHoudiniPythonLibPath.py
"C:\Users\Elio\anaconda3\envs\sewers\python.exe" utils/initSewersShelf.py

pause
