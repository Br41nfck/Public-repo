import string
import requests
import random

# CONSTS
ascii_l = string.ascii_lowercase
ascii_u = string.ascii_uppercase
digits = string.digits
specs = string.punctuation

# U can add another domains
domains = {
    1: '@gmail.com',
    2: '@mail.com',
    # 3: '<Another_domain>'
        }


# Generate mail
def create_email():
    # Select your length
    n = random.randint(3, 5)
    email = ''
    for i in range(n):
        email = email + random.choice(ascii_l) + random.choice(ascii_u) + random.choice(digits)
    domain = random.choice(list(domains.values()))
    return email + domain


# Check exists email
def check_exist():
    msg = create_email()
    response = requests.get("https://isitarealemail.com/api/email/validate", params = {'email': msg})
    status = response.json()['status']
    if status == "valid":
        print("mail already exist")
    elif status == "invalid":
        create_email()
    else:
        status = "unknown"
    return status


# Generate password
def passgen():
    n = random.randint(4, 10)
    password = ''
    for i in range(n):
        password = password + random.choice(ascii_l) + random.choice(ascii_u) + random.choice(digits)
    return password


def start():
    while check_exist() != "invalid":
        create_email()
    email = create_email()
    password = passgen()
    # status = check_exist()
    print("You can register this mail:", email, '\nWith this password:', password)
    # print(status)


# MAIN PROGRAM
start()
