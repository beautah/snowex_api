@ECHO OFF
call C:\ProgramData\Anaconda3\Scripts\activate.bat
set root=api-env
echo Activating Python Virtual Environment...
call activate %root%
echo api-env Activated!
call cd %~dp0
call python api.py