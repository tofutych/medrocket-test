import os


def cd_to_tasks_and_back(func):
    """
    Декоратор позволяет нам во время выполнения
    функции сменить рабочую директорию на ./tasks,
    а затем вернуться обратно. 
    """
    def wrapper(*args, **kwargs):
        os.chdir("tasks")
        res = func(*args, **kwargs)
        os.chdir("..")
        return res
    return wrapper
