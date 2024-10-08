token = '7306002854:AAHIc35yMOXyho4bcYYeAS3W5PP0ey_1HXk'

import telebot
from telebot import types

bot = telebot.TeleBot(token)
cache = {'check_file': ''}
# utf-8
def create_call(message):
    class call(object):
        def __init__(self):
            self.message = message  # либо call.message
            self.data = message.text
            self.from_user = message.from_user
            self.id = message.message_id
    return call()


@bot.message_handler(commands=['send_file'])
def send_file(message):
    call = create_call(message)
    uid = call.from_user.id
    cache['check_file'] = 'send_file'
    bot.send_message(message.chat.id, 'Пожалуйста, отправьте файл для загрузки:')


@bot.message_handler(commands=['stop', 'exit'])
def send_file(message):
    bot.close()
    bot.send_message(message.chat.id, 'Бот выключен!>')


@bot.message_handler(content_types='text')
def text(message):
    call = create_call(message)
    uid = call.from_user.id
    print('ПРинято сообщение')


@bot.message_handler(content_types='document')
def files(message):
    if cache['check_file'] == 'send_file':
        bot.reply_to(message, 'Загрузка...')
        try:
            print('start')
            call = create_call(message)
            uid = call.from_user.id
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src ='C:/users/Буфет/Documents/GitHub/MC/doc/' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='Загружено!')
            except:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+2, text='Загружено!')
            print('end')
        except Exception as e:
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text=str(e))
            except:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+2, text='Загружено!')
            print('Ошибка:' + str(e))
        cache['check_file'] = ''


@bot.callback_query_handler(func=lambda call: True)
def default(call):
    uid = call.from_user.id


def send(text):
    id = 828853360
    bot.send_message(chat_id=id, text=text)


def start():
    bot.infinity_polling()