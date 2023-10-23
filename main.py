import db
import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def insert_into_db(message):
    if message.text == '/cancel':
        cancel(message)
        return
    msg = message.text.split()
    date_text = '/'.join(msg[0].split('-'))
    task_text = ' '.join(msg[1:])
    user_id = message.from_user.id

    try:
        db.insert_into_db(user=user_id, date_str=date_text, task=task_text)
        bot.send_message(message.chat.id, "Задача успешно сохранена")
    except Exception:
        bot.send_message(message.chat.id,
                         "Что-то пошло не так... Возможные причины ошибки:\n\n1) Такая задача уже существует\n2) Дата введена некорректно\n3) Дата стоит задним числом\n\nПопробуйте снова или используйте команду /cancel для отмены последнего действия")
        message_create_deadline(message)


def remove_from_db(message):
    if message.text == '/cancel':
        cancel(message)
        return
    msg = get_from_db(message)
    key = message.text
    if key in msg:
        db.remove_from_db(user=message.from_user.id, task=msg[key][1])
        bot.send_message(message.chat.id, "Задача успешно удалена")
    else:
        bot.send_message(message.chat.id,
                         "Что-то пошло не так... Скорее всего ввод некорректен\n\nПопробуйте снова или используйте команду /cancel для отмены последнего действия")
        message_delete_deadline(message)


def get_from_db(message):
    tasks = db.get_from_db(user=message.from_user.id)
    msg = dict()
    for i in range(len(tasks)):
        date = '-'.join(str(tasks[i]['deadline']).split()[0].split('-')[::-1])
        task = str(tasks[i]['task'])
        msg[str(i + 1)] = [date, task]
    return msg


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "/help - Подсказка\n/create_deadline - Добавить задачу\n/delete_deadline - Удалить задачу\n/get_deadlines - Посмотреть все задачи\n/cancel - Отмена последнего действия")


@bot.message_handler(commands=['cancel'])
def cancel(message):
    bot.send_message(message.chat.id, "Отмена последнего действия")


@bot.message_handler(commands=['create_deadline'])
def message_create_deadline(message):
    msg = bot.send_message(message.chat.id,
                           'Введите дату дедлайна и задачу через пробел (дата в формате дд-мм-гггг), например:\n29-11-2023 Сходить к врачу')
    bot.register_next_step_handler(msg, insert_into_db)


@bot.message_handler(commands=['delete_deadline'])
def message_delete_deadline(message):
    lst = []
    get_items = get_from_db(message).items()
    for key, value in get_items:
        lst.append(f'{key}) {" ".join(value)}')
    if len(lst) == 0:
        bot.send_message(message.chat.id, 'Пока что нет задач')
        return
    msg = bot.send_message(message.chat.id, 'Для удаления задачи выберите ее номер:\n\n' + '\n'.join(lst))
    bot.register_next_step_handler(msg, remove_from_db)


@bot.message_handler(commands=['get_deadlines'])
def message_get_deadlines(message):
    lst = []
    get_values = get_from_db(message).values()
    for elem in get_values:
        lst.append(' '.join(elem))
    if len(lst) == 0:
        bot.send_message(message.chat.id, 'Пока что нет задач')
    else:
        bot.send_message(message.chat.id, 'Ваши задачи (ближайшие дедлайны сверху):\n\n' + '\n--------------------------------------\n'.join(lst))


bot.infinity_polling()
