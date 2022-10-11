import os

def create_dir_if_not_exists(required_dir: str = "tasks") -> None:
    """
    Проверяет наличие директории "tasks" в текущей директории.
    Если директории нет, то она создается.
    """
    if required_dir not in os.listdir():
        os.mkdir("tasks")
