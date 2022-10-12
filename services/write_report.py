from datetime import datetime
import os
from typing import List
from .cd_to_tasks import cd_to_tasks_and_back
from .atomic_write import atomic_write


def write_report(user: dict, todos: List[dict]) -> None:
    """
    Функция принимает пользователя user и список todos.
    Затем формируется отчет.
    Потом проверяется существование отчета для user.
    Если отчет уже был создан, то название старого отчета меняется.
    В конце идет запись отчета в файл.
    """
    name = user.get('name')
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
    completed_titles = get_validated_titles(
        todos_summary.get("completed_titles")
    )
    uncompleted_titles = get_validated_titles(
        todos_summary.get("uncompleted_titles")
    )
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


def validate_title(title: str) -> str:
    """
    Функция проверяет длину title.
    Если длина больше 46, то title изменяется.
    """
    if len(title) > 46:
        return title[:46] + "…"
    return title


def get_validated_titles(titles: List[str]) -> str:
    """
    Функция получает список titles.
    Далее идет валидация каждого title.
    В конце возвращаем строку, где каждый
    title начинается с новой строки и тире.
    """
    titles = [validate_title(title) for title in titles]
    return "—" + "\n—".join(titles)


@cd_to_tasks_and_back
def is_file_exist(file_name: str) -> bool:
    """
    Проверяем наличие файла с именем file_name
    в директории tasks.
    """
    file_path = os.path.join(os.getcwd(), f"{file_name}.txt")
    return os.path.exists(file_path)


@cd_to_tasks_and_back
def rename_file(name: str) -> None:
    """
    Изменяем имя файла в формат
    old_<name>_<Y-m-dTH:M>
    """
    rename_date = datetime.today().strftime("%Y-%m-%dT%H:%M")
    os.rename(f"{name}.txt", f"old_{name}_{rename_date}.txt")
