import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)

number1 = ''
number2 = ''
calculation = ''
result = None

@bot.message_handler(commands=['start', 'help'])
def beginning(message):
    # убрать клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Привет " + message.from_user.first_name + ", я бот-Калькулятор\n Введите число", reply_markup=markup)
    bot.register_next_step_handler(msg, first_number)

'''def enter_second_number1(message):
    send = bot.send_message(message.chat.id, 'Введите первое число')
    bot.register_next_step_handler(send, first_number)'''

# Введите первое число
def first_number(message, result = None):
    #if int(message.text.isdigit()):
        global number1
        # запоминаем число
        if result == None:
            number1 = int(message.text)
        else:

            number1 = str(result)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton('+')
        button2 = types.KeyboardButton('-')
        button3 = types.KeyboardButton('*')
        button4 = types.KeyboardButton('/')
        markup.add(button1, button2, button3, button4)

        msg = bot.send_message(message.chat.id, "Выберите операцию", reply_markup=markup)
        bot.register_next_step_handler(msg, process_calculation_step)
	#else:
        #bot.send_message(message.chat.id, 'Должно быть число')
        #enter_second_number1(message)

# Выберите операцию +, -, *, /
def process_calculation_step(message):

        global calculation
        # запоминаем операцию
        calculation = message.text
        # убрать клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, "Введите еще число", reply_markup=markup)
        bot.register_next_step_handler(msg, second_number)

'''def enter_second_number2(message):
    send = bot.send_message(message.chat.id, 'Введите второе число')
    bot.register_next_step_handler(send, second_number)'''

# Введите второе число
def second_number(message):
    #if int(message.text.isdigit()):
        global number2
        # запоминаем число
        number2 = int(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton('Результат')
        button2 = types.KeyboardButton('Продолжить вычисления')
        markup.add(button1, button2)

        msg = bot.send_message(message.chat.id, "Показать результат или продолжить операцию?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
    #else:
        #bot.send_message(message.chat.id, 'Должно быть число')
        #enter_second_number2(message)

# показать результат или продолжить операция
def process_alternative_step(message):
        # сделать вычисления
        calc()

        # убрать клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        if message.text.lower() == 'результат':
            bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
        elif message.text.lower() == 'продолжить вычисления':

            first_number(message, result)


# Вывод результата пользователю
def calcResultPrint():
    global number1, number2, calculation, result
    return "Результат: " + str(number1) + ' ' + calculation + ' ' + str(number2) + ' = ' + str(result)

# Вычисление
def calc():
    global number1, number2, calculation, result
    result = eval(str(number1) + calculation + str(number2))
    return result

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)