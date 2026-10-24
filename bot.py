import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي أي رابط فيديو وسأقوم بتحميله وإرساله لك.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith('http'):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http")
        return

    msg = bot.reply_to(message, "جاري المعالجة والتحميل، اللحظات...")

    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        bot.delete_message(message.chat.id, msg.message_id)
        os.remove('video.mp4')
        
    except Exception as e:
        bot.edit_message_text("حدث خطأ أثناء التحميل، تأكد أن الرابط مدعوم.", message.chat.id, msg.message_id)

bot.infinity_polling()
