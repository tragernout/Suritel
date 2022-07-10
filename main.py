import telebot
import os
import re
import json
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.chat.id == config.USER_ID:
        bot.send_message(message.chat.id, message.text)
        old_size = 0  # Starting size
        while True:
            fz = os.path.getsize(config.PATH_TO_FAST)  # Fin size
            if fz != old_size:
                f = open(config.PATH_TO_FAST)
                text = f.readline()
                full_text = "File log size in bytes: " + str(fz) + "\n" + text
                bot.send_message(message.chat.id, full_text)
                old_size = fz
                f.close()

                text = re.search('([0-9/]+)-([0-9:.]+)\s+.*?', text)  # Takes date:time from last query. Use text.group() for taking val

                form_time = text.group()
                form_time = form_time.replace(' ', '')
                form_time = form_time.replace('-', '/')
                form_time = form_time.split('/')
                res = form_time[2] + "-" + form_time[0] + "-" + form_time[1] + "T" + form_time[3] + "+0000"

                with open(config.PATH_TO_EVE) as file:
                    for line in file:
                        if res in line:
                            data = json.loads(line)
                            bot.send_message(message.chat.id, data['timestamp'])
                            bot.send_message(message.chat.id, data['payload_printable'] )

                print(text)


bot.polling(none_stop=True)
