import  telegram

TOKEN = '350553078:AAEu70JDqMFcG_x5eBD3nqccTvc4aFNMKkg'

bot = telegram.Bot(TOKEN)

for u in bot.get_updates():
    print('{}: [{}] {}'.format(u.message.date, u.message.chat_id, u.message.text))