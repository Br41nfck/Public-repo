# Import external files
from config import TOKEN, DB, USER, PASS, HOST, TBNAME
from telebot import *
import psycopg2
from loguru import logger

# REPLACE 'COLUMN_NAME' on your column

# You can describe these variables here or in another file.
# TOKEN - get your token here: https://telegram.me/BotFather
# DB - name of your DataBase
# User - login in PostgreSQL
# Pass - pass in PostgreSQL to database
# Host - where located your DB
# TBNAME - name of your DB

COLUMN_NAME = "tasks"

# Logger
logger.add("log.json",
           rotation='1 week',
           compression='zip',
           serialize=True
           )

# WORK /W DB
connection = psycopg2.connect(dbname=DB,
                              user=USER,
                              password=PASS,
                              host=HOST)

cursor = connection.cursor()
if cursor.connection:
    print("Connection with BD successful!")
else:
    print("Connection with BD denied!")
connection.autocommit = True

# INITIALIZATION
bot = TeleBot(TOKEN)


class TODOAPP:

    def __init__(self):
        pass


# HELP MESSAGE
@bot.message_handler(commands=['help', 'start'])
def help_msg(message):
    try:
        bot.send_message(message.chat.id, "Hello there!\n"
                                          "Available commands:\n"
                                          "/add     - to add new task\n"  # WORK √
                                          "/all     - list all tasks\n"  # WORK, BUT /WO PRINT DATES ~ (SEE: FIXME)
                                          "/delete  - delete task\n"  # WORK √
                                          "/edit    - edit task and date\n"  # WORK √
                                          "/find    - find task\n"  # WORK √
                                          "/help    - get help info\n"  # WORK √
                                          "/list    - list task on day\n"  # WORK √
                                          "/today   - list tasks on today\n"  # WORK √
                                          "/sort    - sort by date or task\n"  #  WORK √
                                          "/deadline - list tasks with a date approaching\n"  # NOT REALIZED x
                         )

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {help_msg.__name__}")
        logger.exception(e)


# ADD TASK COMMAND
@bot.message_handler(commands=['add'])
def add_task(message):
    try:
        msg = message.text
        text = msg.split(' ')
        date = text[1]
        info = str(' '.join(text[2:]))
        cursor.execute(f"INSERT INTO {TBNAME} ({COLUMN_NAME}) values ('{info}', '{date}')")
        bot.send_message(message.chat.id, f"Task '{info}' successfully added!")

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {add_task.__name__}")
        logger.exception(e)


# EDIT TASK AND DATE COMMAND #  old date, old task, new date, new task
@bot.message_handler(commands=['edit'])
def edit_task_and_date(message):
    try:
        msg = message.text
        text = msg.split(' ')
        old_date = text[1]
        old_task = text[2]
        date = text[3]
        task = str(' '.join(text[4:]))
        cursor.execute(f"SELECT {COLUMN_NAME} FROM {TBNAME} WHERE {COLUMN_NAME} = '{old_task}' and {COLUMN_NAME} = '{old_date}'")
        res = cursor.fetchall()
        if not res:
            bot.send_message(message.chat.id, f"Not found task '{old_task}' and/or date '{old_date}'")
        else:
            cursor.execute(f"UPDATE {TBNAME} SET {COLUMN_NAME} = '{task}', {COLUMN_NAME} = '{date}' WHERE {COLUMN_NAME} = '{old_task}' AND {COLUMN_NAME} = '{old_date}'")
            bot.send_message(message.chat.id, "Task successfully updated!")

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {edit_task_and_date.__name__}")
        logger.exception(e)


# DELETE TASK COMMAND
@bot.message_handler(commands=['delete', 'remove'])
def delete_task(message):
    try:
        msg = message.text
        text = msg.split(' ')
        task = ' '.join(text[1:])
        cursor.execute(f"SELECT {COLUMN_NAME} FROM {TBNAME} WHERE {COLUMN_NAME} = '{task}'")
        res = cursor.fetchall()
        if not res:
            bot.send_message(message.chat.id, f"Task '{task}' isn't found and can't be removed!")
        else:
            cursor.execute(f"DELETE FROM {TBNAME} WHERE {COLUMN_NAME} = '{task}'")
            bot.send_message(message.chat.id, f"Task '{task}' successfully deleted!")

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {delete_task.__name__}")
        logger.exception(e)


# FIND TASK BY NAME
# FIXME: ADD DATA AROUND
@bot.message_handler(commands=['find', 'search'])
def find_task_by_name(message):
    try:
        msg = message.text
        text = msg.split(' ')
        task = ' '.join(text[1:])
        cursor.execute(f"SELECT * FROM {TBNAME} WHERE {COLUMN_NAME} = '{task}'")
        res = cursor.fetchall()
        print(res)
        if not res:
            bot.send_message(message.chat.id, f"Task by name '{task}' not found!")
        else:
            founded = ''.join([str(i[1]) + ' - ' + str(i[2]) + '\n' for i in res])

            bot.send_message(message.chat.id, founded)

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {find_task_by_name.__name__}. Can't found task!")
        logger.exception(e)


# LIST TASK ON DAY COMMAND
@bot.message_handler(commands=['list', 'tasks'])
def list_tasks_on_day(message):
    try:
        msg = message.text
        text = msg.split(' ')
        cursor.execute(f"SELECT {COLUMN_NAME} FROM {TBNAME} WHERE {COLUMN_NAME} = '{text[1]}'")
        res = cursor.fetchall()
        if not res:
            bot.send_message(message.chat.id, "No tasks on this day")
        else:
            on_day_msg = f"Tasks on {text[1]}:\n"
            tasks = ''.join([str(i[0]) + '\n' for i in res])
            ans = on_day_msg + tasks
            bot.reply_to(message, ans)

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {list_tasks_on_day.__name__}. Uncorrected syntax. Use '/help'")
        logger.exception(e)


# LIST TASK ON TODAY
@bot.message_handler(commands=['today'])
def today_tasks(message):
    try:
        today = datetime.today()
        cursor.execute(f"SELECT {COLUMN_NAME} FROM {TBNAME} where {COLUMN_NAME} = '{today}'")
        res = cursor.fetchall()
        if not res:
            bot.send_message(message.chat.id, "No today tasks")
        else:
            tasks_today = ''.join([str(i[0]) + '\n' for i in res])
            ans = "Today:\n" + tasks_today
            bot.reply_to(message, ans)

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {today_tasks.__name__}. There are no tasks on this day!")
        logger.exception(e)


# LIST ALL TASKS COMMAND
@bot.message_handler(commands=['all'])
def list_all_tasks(message):
    try:
        cursor.execute(f"SELECT {COLUMN_NAME}, {COLUMN_NAME} FROM {TBNAME}")
        res = cursor.fetchall()
        if not res:
            bot.send_message(message.chat.id, "List of tasks is empty!")
        else:
            tasks = ''.join([str(i[0]) + ' - ' + str(i[1]) + '\n' for i in res])
            # FIXME: GET TASKS ON EVERY DATE
            bot.reply_to(message, tasks)

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {list_all_tasks.__name__}")
        logger.exception(e)


# Sort By - dates, tasks
@bot.message_handler(commands=['sort'])
def sort_by(message):
    try:
        msg = message.text
        txt = msg.split(' ')
        cursor.execute(f"SELECT * FROM {TBNAME} ORDER BY {txt[1]}")
        res = cursor.fetchall()
        ans = ''.join([str(i[1]) + ' - ' + str(i[2]) + '\n' for i in res])
        print(ans)
        bot.send_message(message.chat.id, ans)

    except Exception as e:
        print(e)
        bot.reply_to(message, f"Something went wrong! In functon {sort_by.__name__}")
        logger.exception(e)


# Unregistered commands handler
@bot.message_handler(content_types=['text'])
def check(message):
    bot.send_message(message.from_user.id, "I don't understand :( See commands: /help")
    logger.exception(f"Unregistered command: {message.text}")


# Don't turn off a bot
print("Bot is running...")
bot.polling(none_stop=True)
print("Bot is stopped")
connection.close()
print("Connection closed!")
