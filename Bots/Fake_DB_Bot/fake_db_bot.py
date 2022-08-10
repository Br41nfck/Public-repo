# Create Fake Data Base with TeleBot
import telebot
import string
import random
from faker import Faker
import pandas as pd

# Consts
TOKEN = "Insert your token here"
bot = telebot.TeleBot(TOKEN)
# You can add 'ru_RU', 'jr_JR' and etc.
fake = Faker(['en_US'])
number = 10


def generate_random_password(num):
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    length = int(num)
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)


# Type: /reg {number} - count of created accounts
@bot.message_handler(commands = ['reg'])
def register_new_user(message):
    msg = message.text
    msg = msg.split(' ')
    list_of_names = []
    list_of_passes = []
    list_of_dates = []
    list_of_jobs = []
    for i in range(int(msg[1])):

        # Create fake information about person
        username = fake.name()
        date = fake.date()
        job = fake.job()
        password = generate_random_password(number)

        lst = username.split(' ')
        fname = lst[0]
        sname = lst[1]

        # Send to chat
        bot.send_message(message.chat.id, fname + '_' + sname + '\n' + password + '\n' + date + '\n' + job)

        list_of_names.append(fname + '_' + sname)
        list_of_passes.append(password)
        list_of_dates.append(date)
        list_of_jobs.append(job)

        # Work with DataFrame
        df = pd.DataFrame(dict(Name = list_of_names, Pass = list_of_passes, Birthday = list_of_dates, Job = list_of_jobs))

        # Write to Excel file
        df.to_excel('out.xlsx', sheet_name = 'Users', index = False)


print('bot is starting...')
bot.polling()
print('bot is stopped')
