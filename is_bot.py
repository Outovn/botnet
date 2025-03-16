import os
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Ваши значения api_id и api_hash
api_id = 25034006
api_hash = '2e3df98a12d3755efed1742e4468de32'
SESSION_DIR = "sessions"
DELETED_SESSIONS_DIR = "deleted_sessions"

def create_directory(directory):
    """Создает директорию, если она не существует."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_bot_session(session_file):
    """Проверяет, является ли сессия ботом."""
    session_path = os.path.join(SESSION_DIR, session_file)
    try:
        with TelegramClient(session_path, api_id, api_hash) as client:
            me = client.get_me()
            return me.bot
    except SessionPasswordNeededError:
        print(f"[{session_file}] требует двухфакторную аутентификацию.")
        return None  # Возвращаем None, если требуется двухфакторная аутентификация
    except Exception as e:
        print(f"Ошибка при проверке [{session_file}]: {e}")
        return None  # Возвращаем None в случае ошибки

def main():
    # Создаем директории, если их нет
    create_directory(SESSION_DIR)
    create_directory(DELETED_SESSIONS_DIR)

    # Получаем все файлы с расширением .session в директории
    session_files = [f for f in os.listdir(SESSION_DIR) if f.endswith(".session")]

    # Проверка каждого файла на тип сессии
    for session_file in session_files:
        if is_bot_session(session_file):
            print(f"[{session_file}] это бот! Перемещаю файл...")
            src_path = os.path.join(SESSION_DIR, session_file)
            dest_path = os.path.join(DELETED_SESSIONS_DIR, session_file)
            os.rename(src_path, dest_path)  # Перемещение файла сессии
        else:
            print(f"[{session_file}] это не бот.")

if __name__ == "__main__":
    main()