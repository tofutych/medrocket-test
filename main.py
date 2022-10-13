import os
import tempfile
from datetime import datetime
from typing import List

import requests


def main():
    if "tasks" not in os.listdir():
        os.mkdir("tasks")
    os.chdir("tasks")

    users_endpoint = "https://json.medrocket.ru/users"
    todos_endpoint = "https://json.medrocket.ru/todos"

    users = get_data_from_url(users_endpoint)
    if users is not None:
        for user in users:
            user_id = user.get("id")
            todos = get_data_from_url(url=todos_endpoint, params={"userId": user_id})
            if todos:
                write_report(user, todos)


def get_data_from_url(url: str, params: dict = {}) -> List[dict] | None:
    """
    Функция отправляет GET запрос c параметрами params
    на переданный url в формате str и возвращает
    либо dict, в котором будут находиться полученные
    данные, либо None, если что-то помешало корректной работе запроса.
    """
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.HTTPError as http_error:
        print("HTTP Error:", http_error)
    except requests.exceptions.ConnectionError as connection_error:
        print("Connection Error:", connection_error)
    except requests.exceptions.Timeout as timeour_error:
        print("Timeout Error:", timeour_error)
    except requests.exceptions.RequestException as request_error:
        print("Request Error:", request_error)


def write_report(user: dict, todos: List[dict]) -> None:
    """
    Функция принимает пользователя user и список todos.
    Затем формируется отчет.
    Потом проверяется существование отчета для user.
    Если отчет уже был создан, то название старого отчета меняется.
    В конце идет запись отчета в файл.
    """
    name = user.get("name")
    report = create_report(user, todos)

    if is_file_exist(name):
        rename_file(name)

    atomic_write(report, name)


def create_report(user: dict, todos: List[dict]) -> str:
    """
    Функиця принимает пользователя user и todos.
    По полученным данным формируется и возвращается отчет.
    """
    todos_summary = get_user_todos_summary(todos)
    completed_titles = get_validated_titles(todos_summary.get("completed_titles"))
    uncompleted_titles = get_validated_titles(todos_summary.get("uncompleted_titles"))
    creation_date = datetime.today().strftime("%d.%m.%Y %H:%M")

    report = (
        f"# Отчет для {user.get('company').get('name')}.\n"
        f"{user.get('name')} <{user.get('email')}> {creation_date}\n"
        f"Всего задач: {todos_summary.get('total')}\n"
        "\n"
        f"## Актуальные задачи ({todos_summary.get('uncompleted')}):\n"
        f"{uncompleted_titles}"
        "\n\n"
        f"## Завершённые задачи ({todos_summary.get('completed')}):\n"
        f"{completed_titles}"
    )
    return report


def get_user_todos_summary(todos: List[dict]) -> dict:
    """
    Функция принимает список туду todos.
    Проверяя каждый todo, формируется summary, хранящий общую
    статистику о юзере.
    """
    summary = {
        "total": 0,
        "completed": 0,
        "completed_titles": [],
        "uncompleted": 0,
        "uncompleted_titles": [],
    }

    for todo in todos:
        summary["total"] += 1
        if todo.get("completed"):
            summary["completed"] += 1
            summary["completed_titles"].append(todo.get("title"))
        else:
            summary["uncompleted"] += 1
            summary["uncompleted_titles"].append(todo.get("title"))

    return summary


def get_validated_titles(titles: List[str]) -> str:
    """
    Функция получает список titles.
    Далее идет валидация каждого title.
    В конце возвращаем строку, где каждый
    title начинается с новой строки и тире.
    """
    titles = list(
        map(lambda title: title[:46] + "…" if len(title) > 46 else title, titles)
    )
    return "— " + "\n— ".join(titles)


def is_file_exist(file_name: str) -> bool:
    """
    Проверяем наличие файла с именем file_name
    в директории tasks.
    """
    file_path = os.path.join(os.getcwd(), f"{file_name}.txt")
    return os.path.exists(file_path)


def rename_file(name: str) -> None:
    """
    Изменяет имя файла в формат
    old_<name>_<Y-m-dTH:M>
    """
    rename_date = datetime.today().strftime("%Y-%m-%dT%H:%M")
    os.rename(f"{name}.txt", f"old_{name}_{rename_date}.txt")


def atomic_write(content: str, name: str, extension: str = ".txt") -> None:
    """
    Функция безопасно записывает данные в файл,
    используя временный файл.
    """
    name += extension

    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(name))
    with open(temp_file.name, "w") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())

    os.replace(temp_file.name, name)

    if os.path.exists(temp_file.name):
        try:
            os.unlink(temp_file.name)
        except FileNotFoundError as e:
            print("File not found")


if __name__ == "__main__":
    main()
