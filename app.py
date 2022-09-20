import telebot
from config import keys, TOKEN
from extensions import ConvertionException, Converter



bot = telebot.TeleBot(TOKEN)

welcome_text = 'Бот позволяет узнать о курсе валют. ' \
'\nДля начала работы введите команду боту в следующем формате:' \
'\n<имя валюты><в какую валюту перевести> <количество переводимой валюты>' \
'\nУвидить список всех доступных валют:/values'


@bot.message_handler(commands=['start','help'])
def start(message: telebot.types.Message):
    if message.text == '/start':
        markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('/start')
        markup.row('/values')
    bot.reply_to(message, welcome_text, reply_markup=markup)


@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text',])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команды.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
