import os
import tempfile
from .cd_to_tasks import cd_to_tasks_and_back


@cd_to_tasks_and_back
def atomic_write(content: str, name: str) -> None:
    """
    Функция безопасно записывает данные в файл,
    используя временный файл.
    """
    name += ".txt"

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        dir=os.path.dirname(name)
    )
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
