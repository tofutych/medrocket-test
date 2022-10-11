from datetime import datetime
import os
from typing import List
from .cd_to_tasks import cd_to_tasks_and_back


def write_report(user: dict, todos: List[dict]) -> None:
    report = create_report(user, todos)
    print(report)
    name = user.get('name')
    if is_file_exist(name):
        rename_file(name)

    print(os.getcwd())


def create_report(user: dict, todos: List[dict]) -> str:
    """
    Принимает dict user и List[dict] todos и возвращает str report.
    По полученным параметрам формируется отчет в соответствие с ТЗ.
    """
    todos_summary = get_user_todos_summary(todos)
    completed_titles = get_validated_titles(
        todos_summary.get("completed_titles")
    )
    uncompleted_titles = get_validated_titles(
        todos_summary.get("uncompleted_titles")
    )
    creation_date = datetime.today().strftime("%d-%m-%Y %H:%M")

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
    Принимает List[dict] todos и возращает dict summary.
    Проверяя каждый todo, формируется summary, хранящий общую статистику
    юзера.
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
    if len(title) > 46:
        return title[:46] + "…"
    return title


def get_validated_titles(titles: List[str]):
    titles = [validate_title(title) for title in titles]
    return "—" + "\n—".join(titles)


@cd_to_tasks_and_back
def is_file_exist(file_name: str) -> bool:
    file_path = os.path.join(os.getcwd(), f"{file_name}.txt")
    return os.path.exists(file_path)


@cd_to_tasks_and_back
def rename_file():
    creation_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
