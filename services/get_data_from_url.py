import requests
from typing import List


def get_data_from_url(url: str, params: dict = {}, timeout=5) -> List[dict] | None:
    """
    Функция отправляет GET запрос c параметрами params
    на переданный url в формате str и возвращает
    либо dict, в котором будут находиться полученные
    данные, либо None, если что-то помешало корректной работе запроса.
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_error:
        print("HTTP Error:", http_error)
    except requests.exceptions.ConnectionError as connection_error:
        print("Connection Error:", connection_error)
    except requests.exceptions.Timeout as timeour_error:
        print("Timeout Error:", timeour_error)
    except requests.exceptions.RequestException as request_error:
        print("Request Error:", request_error)
