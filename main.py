import telebot
import os
import re
import json
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.chat.id == config.USER_ID:
        old_size = 0  # Starting size
        while True:
            fz = os.path.getsize(config.PATH_TO_FAST)  # Fin size
            if fz != old_size:
                with open(config.PATH_TO_FAST) as f:
                    for line in f:
                        pass
                    last_line = line
                full_text = "❗" + last_line + "\n\n"
                #bot.send_message(message.chat.id, full_text)
                old_size = fz
                f.close()

                text = re.search('([0-9/]+)-([0-9:.]+)\s+.*?', last_line)  # Takes date:time from last query. Use text.group() for taking val

                form_time = text.group()
                form_time = form_time.replace(' ', '')
                form_time = form_time.replace('-', '/')
                form_time = form_time.split('/')
                res = form_time[2] + "-" + form_time[0] + "-" + form_time[1] + "T" + form_time[3] + "+0000"

                with open(config.PATH_TO_EVE) as file:
                    for line in file:
                        if res in line:
                            data = json.loads(line)
                            report = full_text + data['payload_printable']
                            if "/assets/js/" not in report and "/assets/css/" not in report and "favicon.ico" not in report:
                                if len(report) > 4096:
                                    for x in range(0, len(report), 4096):
                                        bot.send_message(message.chat.id, report[x:x + 4096])
                                else:
                                    bot.send_message(message.chat.id, report)

                print(text)


bot.polling(none_stop=True)