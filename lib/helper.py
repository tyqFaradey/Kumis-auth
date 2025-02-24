from os import walk
from datetime import date

import re, pathlib, os



main_directory = pathlib.Path(__file__).parent.parent.resolve()

def get_files_dict(folder_path, extension=None):
    """
    Возвращает словарь, где ключ — название файла, а значение — полный путь к файлу.

    :param folder_path: Путь к папке.
    :param extension: Фильтр по расширению файла (например, ".txt").
    :return: Словарь {имя_файла: путь_к_файлу}.
    """
    files_dict = {}

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Папка '{folder_path}' не существует.")

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Пропускаем скрытые файлы
            if file_name.startswith("."):
                continue
            # Фильтр по расширению
            if extension and not file_name.endswith(extension):
                continue
            full_path = os.path.join(root, file_name)
            files_dict[file_name] = full_path

    return files_dict

def get_path(name: str) -> str:
    return str(pathlib.PurePath(main_directory, name))

def get_whitelist_path() -> str:
    return str(pathlib.PurePath(main_directory, "whitelist"))

def get_date() -> str:
    return str(date.today())

def get_token():
    with open(get_path("token"), "r", encoding="utf-8") as file:
        return str(file.readline())

def __massages():
    res = {}
    for _, _, file in walk(get_path("Assets")):
        files = file
    for item in files:
        res[item.split('.')[0]] = str(pathlib.PurePath("Assets", item))
    return res

massages = __massages()

def get_path_database() -> str:
    return get_path("data-0.1.0.db")

def nick_is_not_valid(nickname: str) -> int:
    if len(nickname) < 3 or len(nickname) > 16:
        return 101

    if not re.match(r'^[a-zA-Z0-9_]+$', nickname):
        return 102
    
    forbidden_words = []

    for word in forbidden_words:
        if word.strip().lower() == nickname.lower():
            return 103
        
    return 100

def oneline_text_from_file(name: str) -> str:
        full_path = get_path(massages[name])

        with open(full_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        return "\n".join(lines)

