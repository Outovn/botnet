import os
import random
from telethon import TelegramClient
import asyncio

# Ваши данные для подключения
api_id = '21311892'  # Замените на ваш api_id
api_hash = 'a67a0cd8341689490ac5104ee83b25ab'  # Замените на ваш api_hash

# Директория, где хранятся файлы сессий
session_directory = 'sessions'  # Укажите путь к директории с сессиями

# Чтение прокси из файла
def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

# Получение случайного прокси из файла
proxies = read_proxies_from_file('proxy.txt')
if not proxies:
    raise ValueError("Не найдено прокси в файле.")

# Получение всех файлов сессий в указанной директории
session_files = [f for f in os.listdir(session_directory) if f.endswith('.session')]
if not session_files:
    raise ValueError("Не найдено файлов сессий в указанной директории.")

async def process_session(session_file, proxy):
    proxy_host, proxy_port, proxy_login, proxy_password = proxy.split(':')
    proxy_port = int(proxy_port)

    session_path = os.path.join(session_directory, session_file)

    # Создание клиента Telegram с прокси
    client = TelegramClient(
        session_path,
        api_id,
        api_hash,
        proxy=('socks5', proxy_host, proxy_port, True, proxy_login, proxy_password)
    )

    try:
        await client.start()  # Запускаем клиента без параметров
        print(f"Подключено к прокси: {proxy} с сессией: {session_file}")

        # Получение информации о текущем пользователе
        me = await client.get_me()
        print(f'Вы вошли как: @{me.username} (ID: {me.id})')

    except Exception as e:
        print(f"Ошибка подключения для сессии {session_file}: {e}")

async def main():
    # Создаем список задач для обработки всех сессий
    tasks = []
    for session_file in session_files:
        random_proxy = random.choice(proxies)  # Выбор случайного прокси для каждой сессии
        tasks.append(process_session(session_file, random_proxy))

    # Запуск всех задач параллельно
    await asyncio.gather(*tasks)

# Запуск основного асинхронного цикла
with TelegramClient('temp', api_id, api_hash) as client:
    client.loop.run_until_complete(main())