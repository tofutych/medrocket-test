from services import create_dir_if_not_exists, get_data_as_dict, write_report
from services import TODOS_URL, USERS_URL


if __name__ == "__main__":
    create_dir_if_not_exists()

    users = get_data_as_dict(USERS_URL)

    for user in users:
        user_id = user.get('id')
        todos = get_data_as_dict(
            TODOS_URL,
            {"userId": user_id}
        )
        write_report(user, todos)
