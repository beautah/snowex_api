@ECHO OFF
call C:\ProgramData\Anaconda3\Scripts\activate.bat
set venv=snowex-env
echo Activating Python Virtual Environment...
call activate %venv%
echo api-env Activated!
call cd %~dp0
call python api.py --debug
pause