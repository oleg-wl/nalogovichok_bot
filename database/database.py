import os

from sqlalchemy import create_engine, text

# Укажите параметры подключения к вашей базе данных PostgreSQL
db_user = os.environ['db_user']
db_password = os.environ['db_password']
db_host = os.environ['db_host']
db_port = int(os.environ['db_port'])
db_name = os.environ['db_name']

# Формируем строку подключения
connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Создаем объект Engine для подключения к базе данных
engine = create_engine(connection_string)

# Подключаемся к базе данных
connection = engine.connect()

# Выполняем SQL-запрос
result = connection.execute(text('SELECT version()'))

# Выводим результат запроса
for row in result:
    print(row)

# Закрываем соединение
connection.close()
