@echo on


:botstart
pskill python

timeout /T 10

python.exe assist_bot.py


rem timeout /T 72

goto botstart