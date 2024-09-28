import telebot
import os

bot = telebot.TeleBot('API')

@bot.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"Привет, <b>{message.from_user.first_name}</b>!"
    bot.send_message(message.chat.id, first_mess, parse_mode='html')

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = os.getcwd() + '/book_fb2/' + message.document.file_name;
    new_file = open(src, 'wb')
    new_file.write(downloaded_file)
    msg = bot.reply_to(message, "Отлично, сейчас конвертирую ваш файл, ожидайте)")

    os.chdir(os.getcwd())
    command = '.\\fb2converter\\fb2c.exe -c .\\fb2converter\\configuration.toml convert --to azw3 .\\book_fb2 .\\book_azw3'
    os.system(command)
    new_file.close()
    os.remove(src)

    src = os.getcwd() + '/book_azw3/' + str(message.document.file_name).replace('.fb2', '.azw3')
    bot.delete_message(msg.chat.id, msg.message_id)
    bot.send_document(msg.chat.id, open(src, 'rb'))
    os.remove(src)

bot.infinity_polling()