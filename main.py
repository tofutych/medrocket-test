from operator import ge
from services import create_dir_if_not_exists, get_data_as_dict
import json

if __name__ == "__main__":
    create_dir_if_not_exists()

    users_url = "https://json.medrocket.ru/users/1"
    todos_url = "https://json.medrocket.ru/todos"
    users = get_data_as_dict(users_url)
    todos = get_data_as_dict("https://json.medrocket.ru/todos", {"userId": 1})