import sqlite3


def create_tables_weatherConditions():
    connection = sqlite3.connect('Weather_db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS WeatherConditions ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'Temperature REAL,'
                   'TemperatureFells REAL,'
                   'WindSpeed REAL,'
                   'WindDirection TEXT,'
                   'Condition TEXT,'
                   'Precipitation REAL,'
                   'Humidity INTEGER,'
                   'Visibility REAL,'
                   'Pressure REAL,'
                   'UVIndex REAL)')
    connection.commit()
    connection.close()


def create_tables_cities():
    connection = sqlite3.connect('Weather_db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Cities ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'CityName TEXT)')
    connection.close()


def create_tables_weathers():
    connection = sqlite3.connect('Weather_db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Weathers ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'idWeatherCondition INTEGER,'
                   'idCity INTEGER,'
                   'date TEXT NOT NULL,'
                   'CONSTRAINT Weathers_WeatherConditions_fk '
                   'FOREIGN KEY (idWeatherCondition) REFERENCES WeatherConditions (id),'
                   'CONSTRAINT Weathers_Cities_fk FOREIGN KEY (idCity) REFERENCES Cities (id))')
    connection.commit()
    connection.close()


def fill_db(*, response_dict: dict):
    connection = sqlite3.connect('Weather_db')
    cursor = connection.cursor()

    list_of_tables = cursor.execute(
        """SELECT name FROM sqlite_master WHERE type='table' AND name='WeatherConditions'; """).fetchall()
    if list_of_tables == []:
        create_tables_weatherConditions()

    list_of_tables = cursor.execute(
        """SELECT name FROM sqlite_master WHERE type='table' AND name='Cities'; """).fetchall()
    if list_of_tables == []:
        create_tables_cities()

    list_of_tables = cursor.execute(
        """SELECT name FROM sqlite_master WHERE type='table' AND name='Weathers'; """).fetchall()
    if list_of_tables == []:
        create_tables_weathers()

    for city_keys, city_values in response_dict.items():

        city_name = city_keys

        cursor.execute('SELECT COUNT(*) FROM Cities WHERE CityName = ?', (city_name,))
        total_city = cursor.fetchone()[0]

        if total_city == 0:
            cursor.execute('INSERT INTO Cities (CityName) VALUES (?)', (city_name,))
            connection.commit()

        for date_values in city_values:
            for hour_keys, hour_values in date_values.items():

                date_value = hour_keys

                cursor.execute('SELECT COUNT(*) FROM Weathers JOIN Cities ON Cities.id = Weathers.idCity '
                               'WHERE date = ? and Cities.CityName = ?', (date_value, city_name))
                total_weather_in_city_in_date = cursor.fetchone()[0]

                if total_weather_in_city_in_date != 0:
                    continue

                weather_condition = dict()

                for weather_values in hour_values:
                    for key, value in weather_values.items():
                        weather_condition[key] = value

                cursor.execute('INSERT INTO WeatherConditions (Temperature, TemperatureFells, WindSpeed, '
                               'WindDirection, Condition, Precipitation, Humidity, Visibility, '
                               'Pressure, UVIndex) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                               (weather_condition['Температура'], weather_condition['Ощущается как'],
                                weather_condition['Ветер'], weather_condition['Направление ветра'],
                                weather_condition['Состояние'], weather_condition['Осадки'],
                                weather_condition['Влажность'], weather_condition['Видимость'],
                                weather_condition['Давление'], weather_condition['УФ-индекс']))
                connection.commit()

                cursor.execute('SELECT MAX(id) FROM WeatherConditions')
                weather_id = cursor.fetchone()[0]

                cursor.execute('SELECT id FROM Cities WHERE CityName = ?', (city_name,))
                city_id = cursor.fetchone()[0]

                cursor.execute('INSERT INTO Weathers (idWeatherCondition, idCity, date) VALUES (?, ?, ?)',
                               (weather_id, city_id, date_value))
                connection.commit()

    connection.close()
