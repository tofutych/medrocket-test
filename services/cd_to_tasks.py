import os


def cd_to_tasks_and_back(func):
    def wrapper(*args, **kwargs):
        os.chdir("tasks")
        res = func(*args, **kwargs)
        os.chdir("..")
        return res
    return wrapper
