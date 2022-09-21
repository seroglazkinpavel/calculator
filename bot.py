import logging
import config
import telebot
from fractions import Fraction
from telebot import types
from calculations import div, mult, diff, sum

bot = telebot.TeleBot(config.token)

logging.basicConfig(
    level=logging.INFO,
    filename = "mylog.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("I")
    button2 = types.KeyboardButton("R")
    button3 = types.KeyboardButton("C")
    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id, "Привет " + message.from_user.first_name + ", я бот-Калькулятор\n Выберите числовое множество для ввода:\n целое число 'I',\n рациональное 'R'\n или комплексное 'C'", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == "I":
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(message.chat.id, 'Введите число', reply_markup=markup)
            bot.register_next_step_handler(msg, first_number)
        elif message.text == "R":
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(message.chat.id, 'Введите Делитель_1:', reply_markup=markup)
            bot.register_next_step_handler(msg, divider_1)
        elif message.text == "C":
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, 'Пока с комплексными числами до канца не разобрался: ', reply_markup=markup)

a = ''
b = ''
act = ''
c = ''
d = ''

number1 = ''
number2 = ''
calculation = ''
result = None

# Действия с рациональными числами

def enter_divider_1(message):
    send = bot.send_message(message.chat.id, 'Введите Делитель_1')
    bot.register_next_step_handler(send, divider_1)

# Введите Делитель_1
def divider_1(message):
    try:
        global a
        # запоминаем число
        a = int(message.text)

        msg = bot.send_message(message.chat.id, "Выберите Делимое_1:")
        bot.register_next_step_handler(msg, divisible_1)

    except Exception as e:
        bot.reply_to(message, 'Должно быть число')
        enter_divider_1(message)

def enter_divisible_1(message):
    send = bot.send_message(message.chat.id, 'Введите Делимое_1')
    bot.register_next_step_handler(send, divisible_1)

# Введите Делимое_1
def divisible_1(message):
    try:
        global b
        # запоминаем число
        b = int(message.text)
        if b == 0:
            bot.send_message(message.chat.id, 'На ноль делить нельзя. Введите Делимое_1 не равное 0')
            enter_divisible_1(message)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button1 = types.KeyboardButton('+')
            button2 = types.KeyboardButton('-')
            button3 = types.KeyboardButton('*')
            button4 = types.KeyboardButton('/')
            markup.add(button1, button2, button3, button4)

            msg = bot.send_message(message.chat.id, "Выберите операцию", reply_markup=markup)
            bot.register_next_step_handler(msg, process_act_step)

    except Exception as e:
        bot.reply_to(message, 'Должно быть число')
        enter_divisible_1(message)

# Выберите операцию +, -, *, /
def process_act_step(message):
    global act
    # запоминаем операцию
    act = message.text
    # убрать клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Введите Делитель_2", reply_markup=markup)
    bot.register_next_step_handler(msg, divider_2)

def enter_divider_2(message):
    send = bot.send_message(message.chat.id, 'Введите Делитель_2')
    bot.register_next_step_handler(send, divider_2)

# Введите Делитель_2
def divider_2(message):
    try:
        global c
        # запоминаем число
        c = int(message.text)

        msg = bot.send_message(message.chat.id, "Выберите Делимое_2:")
        bot.register_next_step_handler(msg, divisible_2)

    except Exception as e:
        bot.reply_to(message, 'Должно быть число')
        enter_divider_2(message)

def enter_divisible_2(message):
    send = bot.send_message(message.chat.id, 'Введите Делимое_2')
    bot.register_next_step_handler(send, divisible_2)

# Введите Делимое_2
def divisible_2(message):
    try:
        global d
        # запоминаем число
        d = int(message.text)
        if d == 0:
            bot.send_message(message.chat.id, 'На ноль делить нельзя. Введите Делимое_2 не равное 0')

        calc_fraction()

        bot.send_message(message.chat.id, "Результат: " + str(calc_fraction()))
    except Exception as e:
        bot.reply_to(message, 'Должно быть число')
        enter_divisible_2(message)

# Вычисление
def calc_fraction():
    global act, a, b, c, d, result_calc_fraction
    if act == "+":
        result_calc_fraction = sum(Fraction(a, b), Fraction(c, d))
        return result_calc_fraction
    elif act == "-":
        result_calc_fraction = diff(Fraction(a, b), Fraction(c, d))
        return result_calc_fraction
    elif act == "*":
        result_calc_fraction = mult(Fraction(a, b), Fraction(c, d))
        return result_calc_fraction
    elif act == "/":
        result_calc_fraction = div(Fraction(a, b), Fraction(c, d))
        return result_calc_fraction


# Действия с целыми и вещественными числами  result = eval(str(number1) + calculation + str(number2))

def enter_second_number1(message):
    send = bot.send_message(message.chat.id, 'Введите первое число')
    bot.register_next_step_handler(send, first_number)

# Введите первое число
def first_number(message, result = None):
    try:
        global number1
        # запоминаем число
        if result == None:
            number1 = float(message.text)
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

    except Exception as e:
        bot.reply_to(message, 'Должно быть число')
        enter_second_number1(message)

# Выберите операцию +, -, *, /
def process_calculation_step(message):

    global calculation
    # запоминаем операцию
    calculation = message.text
    # убрать клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Введите еще число", reply_markup=markup)
    bot.register_next_step_handler(msg, second_number)

def enter_second_number2(message):
    send = bot.send_message(message.chat.id, 'Введите второе число')
    bot.register_next_step_handler(send, second_number)

# Введите второе число
def second_number(message):
    try:
        global number2
        # запоминаем число
        number2 = float(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton('Результат')
        button2 = types.KeyboardButton('Продолжить вычисления')
        markup.add(button1, button2)

        msg = bot.send_message(message.chat.id, "Показать результат или продолжить операцию?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
    except Exception as e:
        bot.reply_to(message, 'Должно быть число')
        enter_second_number2(message)

# показать результат или продолжить операция
def process_alternative_step(message):
    # сделать вычисления
    if calculation == '/' and number2 == 0:
        markup = types.ReplyKeyboardRemove(selective=False)
        send = bot.send_message(message.chat.id, 'На ноль делить нельзя. Введите второе число не равное 0', reply_markup=markup)
        bot.register_next_step_handler(send, second_number)
    else:
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