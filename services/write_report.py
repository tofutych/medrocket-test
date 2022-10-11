from datetime import datetime
from get_data_as_dict import get_data_as_dict
from typing import List


def write_report(report: dict) -> None:
    pass


user = get_data_as_dict("https://json.medrocket.ru/users/1")
todos = get_data_as_dict("https://json.medrocket.ru/todos", {"userId": 1})


def create_report(user: dict, todos: List[dict]) -> str:
    """
    Принимает dict user и List[dict] todos и возвращает str report.
    По полученным параметрам формируется отчет в соответствие с ТЗ.
    """
    todos_summary = get_user_todos_summary(todos)

    completed_titles = get_validated_titles(todos_summary.get("completed_titles"))
    uncompleted_titles = get_validated_titles(todos_summary.get("uncompleted_titles"))

    creation_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")

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

