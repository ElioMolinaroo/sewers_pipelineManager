@echo off

title Get Houdini Libs Path

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM Run file through the python exec
python utils/getHoudiniPythonLibPath.py

exit