README.md for Todo-bot
- CODE: Python
- LIBS: telebot, psycopg2, loguru
- FILES: todoapp.py, config.py (last file is confidential)
- DATABASE: PostgreSQL
- COMMANDS:
* /help 	- syntax: /help - show help message in telegram chat 
* /add  	- syntax: /add {date} {task} - add a task to the database - example: /add 10.07.2022 buy new computer
* /all  	- syntax: /all - print all tasks
* /delete - syntax: /delete {task} - delete chosen task - example: /delete buy new computer
* /edit 	- syntax: /edit {old date} {old task} {new date} {new task} - edit chosen task - example: /edit 10.07.2022 go to the movie theater 11.07.2022 go to the theater
* /find 	- syntax: /find {task} - find and print founded task - example: /find go to the theater
* /list 	- syntax: /list {date} - find date and print tasks on this day - example: /list 11.07.2022
* /today 	- syntax: /today - print tasks on current day
