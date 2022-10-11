import requests


def get_data_as_dict(url: str, params: dict = {}, timeout=5) -> dict | None:
    """
    Функция отправляет GET запрос c параметрами paramsна переданный url в формате str
    и возвращает либо dict, в котором будут находиться полученные
    данные, либо None, если что-то помешало корректной работе запроса.
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)
