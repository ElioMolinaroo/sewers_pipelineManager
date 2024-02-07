@echo off

title Get Applications Data
echo Get Applications Data
echo Working... Do not close the file...

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM Run files through the python exec
python utils/cloneDatabases.py
python utils/getPythonPath.py
python utils/getMayaPath.py
REM python utils/getHoudiniPythonLibPath.py
python utils/initSewersShelf.py

pause
