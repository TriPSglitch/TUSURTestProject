from typing import Any
import requests
from datetime import timedelta, datetime

from Cities import City
from API import APIConnect


def do_request(*, qery_string: dict, URL: str) -> list:
    responce = requests.get(url=URL, headers=APIConnect.headers, params=qery_string).json()['forecast']['forecastday']
    return responce


def get_current_weather(*, city: City) -> dict[Any, Any]:
    qery_string = {'q': f'{city.q_name}', 'days': '1', 'lang': 'ru'}
    response = do_request(URL=APIConnect.forecast_URL, qery_string=qery_string)[0]['hour']

    response_dict = get_values(dict_list=response)

    return response_dict


def get_history_weather(*, city: City) -> dict[Any, Any]:
    date_now = datetime.now()
    week_ago = datetime.now() - timedelta(weeks=1)

    qery_string = {'q': f'{city.q_name}', 'lang': 'ru', 'dt': f'{week_ago.date()}',
                   'end_dt': f'{date_now.date()}'}
    response = do_request(URL=APIConnect.history_URL, qery_string=qery_string)

    response_dict = dict()

    for value in response:
        response_dict[f'{value.get('date')}'] = [
            {'Средняя температура за день': f'{value.get('day').get('avgtemp_c')}'}]

    return response_dict


def get_forecast_weather(*, city: City) -> dict[Any, Any]:
    qery_string = {'q': f'{city.q_name}', 'days': '3', 'lang': 'ru'}
    response = do_request(URL=APIConnect.forecast_URL, qery_string=qery_string)

    response_dict = dict()

    for value in response:
        response_dict[f'{value.get('date')}'] = [
            {'Средняя температура за день': f'{value.get('day').get('avgtemp_c')}'}]

    return response_dict


def get_weather_for_db(*, city: City) -> list:
    response_dict = list()

    now = datetime.now()
    date_now = now - timedelta(days=1)
    week_ago = now - timedelta(weeks=1)

    qery_string = {'q': f'{city.q_name}', 'lang': 'ru', 'dt': f'{week_ago.date()}',
                   'end_dt': f'{date_now.date()}'}
    response = do_request(URL=APIConnect.history_URL, qery_string=qery_string)

    for day in response:
        response_dict.append(get_values(dict_list=day['hour']))

    qery_string = {'q': f'{city.q_name}', 'days': '3', 'lang': 'ru'}
    response = do_request(URL=APIConnect.forecast_URL, qery_string=qery_string)

    for day in response:
        response_dict.append(get_values(dict_list=day['hour']))

    return response_dict


def get_values(*, dict_list: dict) -> dict[Any, Any]:
    values = dict()

    for value in dict_list:
        values[f'{value.get('time')}'] = [{'Температура': f'{value.get('temp_c')}',
                                           'Ощущается как': f'{value.get('feelslike_c')}',
                                           'Состояние': f'{value.get('condition').get('text')}',
                                           'Ветер': f'{value.get('wind_kph')}',
                                           'Направление ветра': f'{value.get('wind_dir')}',
                                           'Осадки': f'{value.get('precip_mm')}',
                                           'Влажность': f'{value.get('humidity')}',
                                           'Видимость': f'{value.get('vis_km')}',
                                           'Давление': f'{value.get('pressure_mb')}',
                                           'УФ-индекс': f'{value.get('uv')}'}]

    return values
