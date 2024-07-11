import os
from datetime import datetime as dt
FILE_NAME = 'bot.log'

def logf(data):
    with open(FILE_NAME, 'a') as f:
        f.write(f'[INFO {str(dt.now().time())[:8]}]: {data}\n')


def errorf(data):
    with open(FILE_NAME, 'a') as f:
        f.write(f'[ERROR {str(dt.now().time())[:8]}]: {data}\n')


def log_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as f:
            f.write('')
