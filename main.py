from services import (TODOS_URL, USERS_URL, create_dir_if_not_exists,
                      get_data_from_url, write_report)

if __name__ == "__main__":
    create_dir_if_not_exists()

    users = get_data_from_url(USERS_URL)
    if users is not None:
        for user in users:
            user_id = user.get('id')
            todos = get_data_from_url(
                url=TODOS_URL,
                params={"userId": user_id}
            )
            if todos:
                write_report(user, todos)
