import pymysql.cursors
from config import host, user, password, database
from datetime import datetime

try:  # подключение к базе данных
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=database,
                                 charset="utf8mb4",
                                 cursorclass=pymysql.cursors.DictCursor)
    print("Подключение к базе данных прошло успешно...")

    cursor = connection.cursor()
    create_table_query = "CREATE TABLE IF NOT EXISTS tasks (id int(11) NOT NULL AUTO_INCREMENT, user varchar(255) COLLATE utf8_bin NOT NULL, deadline datetime, task varchar(255) COLLATE utf8_bin NOT NULL, primary key (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1 ;"
    cursor.execute(create_table_query)


    def convert_to_deadline(date_str):  # перевод строки в объект datetime
        date_format = "%d/%m/%Y"
        deadline = datetime.strptime(date_str, date_format).date()
        return deadline


    def insert_into_db(user_name, date_str, task):  # добавление ответа пользователя в таблицу
        insert_query = "INSERT INTO tasks (user, deadline, task) VALUES (%s, %s, %s)"
        deadline = convert_to_deadline(date_str)
        cursor.execute(insert_query, (user_name, deadline, task))
        connection.commit()
        return "Дедлайн пользователя был успешно сохранен!"


    def remove_from_db(user_name, task):  # удаление задачи из таблицы
        remove_query = "DELETE FROM tasks WHERE user = %s AND task = %s"
        cursor.execute(remove_query, (user_name, task))
        connection.commit()
        return "Дедлайн пользователя был успешно удален!"


    def get_from_db(user_name):  # получение всех задач пользователя
        today = datetime.today().date()
        select_query = "SELECT deadline, task FROM tasks WHERE user = %s AND deadline >= %s"
        cursor.execute(select_query, (user_name, today))
        rows = cursor.fetchall()
        return rows


    def clear_db():  # очистить базу данных
        clear_query = "DROP TABLE tasks"
        cursor.execute(clear_query)
        connection.commit()
        return "Таблица успешно очищена"


except Exception as ex:
    print("Ошибка подключения к базе данных...")
    print(ex)
