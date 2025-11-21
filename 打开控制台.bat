@echo off
chcp 65001
title 作品集控制台 - 最终诊断模式

echo ====================================
echo  正在启动 manager.py
echo ====================================
echo.

:: 检查 manager.py 是否存在于当前目录
if not exist "manager.py" (
    echo [错误] 致命错误：找不到 manager.py 文件！
    echo 请确认您已将 manager.py 文件和 build.py 等文件放在同一个文件夹内。
    goto :end
)

:: 尝试使用 Python 启动器 (py) 运行脚本，这比直接使用 python 命令更可靠。
py manager.py

:end
echo.
echo ====================================
echo  程序执行完毕。
echo  如果工具没打开，请仔细查看上方的错误信息 (可能是红色文字)。
echo ====================================
pause