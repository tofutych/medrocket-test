import requests
from typing import List

def get_data_from_url(url: str, params: dict = {}, timeout=5) -> List[dict]:
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
