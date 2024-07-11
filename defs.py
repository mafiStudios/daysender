# -*- coding: utf-8 -*-
from datetime import date as dt
from json import loads
import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from config import VKTOKEN, group_id,TGTOKEN
from dates import DATES

vk_session = vk_api.VkApi(token=VKTOKEN)
longpool = VkBotLongPoll(vk_session, group_id)

# def parse_from_file(name):
#     with open(f"{name}.json", "r") as op:
#         return load(op)

def send_chats_tg(message, ids):
    url = f'https://api.telegram.org/bot{TGTOKEN}/sendMessage'
    if type(ids) == list:
        for chat_id in ids:
            response = requests.request("POST", url, data={'chat_id': chat_id, 'text': message}, files=[])
    elif type(ids) == int:
        response = requests.request("POST", url, data={'chat_id': ids, 'text': message}, files=[])
    return loads(response.text)["ok"]

def send_chats_vk(text, ids):
    if type(ids) == list:
        for id1 in ids:
            vk_session.method("messages.send", {"chat_id": id1, "message": text, "random_id": 0})
    elif type(ids) == int:
        vk_session.method("messages.send", {"chat_id": ids, "message": text, "random_id": 0})

def declination(value):
    words = ['день', 'дня', 'дней']
    try:
        if all((value % 10 == 1, value % 100 != 11)):return words[0]
        elif all((2 <= value % 10 <= 4, any((value % 100 < 10, value % 100 >= 20)))):return words[1]
        return words[2]
    except:
        return "дня"  # Если нет даты(Unknown например)

def sort_days(num):
    if num[1][0] == "UNKNOWN":return 99999
    else:return int(num[1])

def get_days():
    now, full = dt.today(), []
    for daydate in DATES:
        name, date = daydate["name"], daydate["date"].split("-")
        match date[0]:
            case "UNKNOWN":
                full.append([name, date, "non"])
            case _:
                today = dt(int(date[2]),int(date[1]),int(date[0]))
                full.append([name, str((today - now).days), "day"])
    return sorted(full, key=sort_days)


def new_day():
    datelist, message = get_days(), ""
    for i in range(0, len(DATES)):
        match datelist[i][2]:
            case "day":
                if int(datelist[i][1].split("|")[0]) > 0:
                    message += f"До '{datelist[i][0]}' осталось {datelist[i][1]} {declination(int(datelist[i][1]))}.\n"
                elif int(datelist[i][1].split("|")[0]) == 0:
                    message += f"{datelist[i][0]} сегодня.\n"
                else:
                    message += f"{datelist[i][0]} было.\n"
            case "non":
                message += f"До '{datelist[i][0]}' осталось {datelist[i][1][0].lower()}.\n"
    return message