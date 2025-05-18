from API import APIQueries
from excel.ExcelWorker import *
from sql_lite.SQLConnect import *
from Cities import *

wb = Workbook()

for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    wb.remove(sheet)

wsc = wb.create_sheet('Погода на сегодня')

wsh = wb.create_sheet('Погода за прошедшую неделю')

wsf = wb.create_sheet('Прогноз погоды на 3 дня')

tomsk = Tomsk()
abakan = Abakan()
yekaterinburg = Yekaterinburg()
moscow = Moscow()

city_list = (tomsk, abakan, yekaterinburg, moscow)
response_dict = dict()

try:

    for city in city_list:
        os.system('cls')
        print(f'Подождите, выполняется заполнение excel-таблиц города - {city.name}')
        response_dict[city.name] = APIQueries.get_weather_for_db(city=city)

        response = APIQueries.get_current_weather(city=city)
        fill_excel(dict_list=response, city=city, ws=wsc, wb=wb)

        response = APIQueries.get_forecast_weather(city=city)
        fill_excel(dict_list=response, city=city, ws=wsf, wb=wb)

        response = APIQueries.get_history_weather(city=city)
        fill_excel(dict_list=response, city=city, ws=wsh, wb=wb)

        os.system('cls')
        print(f'Подождите, выполняется заполнение БД города - {city.name}')
        fill_db(response_dict=response_dict)

except KeyError:
    print('Исчерпан лимит API-запросов')

print('Закройте приложение')
s = input()
