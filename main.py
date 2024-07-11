# -*- coding: utf-8 -*-
import time
from config import VK_CHATS_ID, TG_CHATS_ID
from logger import logf,errorf, log_file
from datetime import datetime as dt
import defs
#Запуск логирования
log_file()
FILE_NAME = 'bot.log'
def main():
    olddate = "None"
    while True:
        try:
            if dt.now().time().hour == 0 and olddate != dt.now().date():
                olddate = dt.now().date()
                logf(defs.send_chats_tg("Новый день!",TG_CHATS_ID))
                logf(defs.send_chats_tg(defs.new_day(), TG_CHATS_ID))
                logf(defs.send_chats_vk("Новый день!", VK_CHATS_ID))
                logf(defs.send_chats_vk(defs.new_day(), VK_CHATS_ID))
            continue
        except Exception as error:
            errorf(error)
            time.sleep(1)
if __name__ == "__main__":
    main()


