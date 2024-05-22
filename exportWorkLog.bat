@echo off
REM 检查是否提供了参数
IF "%~1"=="" (
    ECHO please provide tag name
    EXIT /B 1
)

REM 参数 1 作为 Python 脚本的输入
python "%~dp0/exportWorkLog.py" %1
