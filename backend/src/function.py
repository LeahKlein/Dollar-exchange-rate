import data_base
import requests
from datetime import datetime
import json
from datetime import datetime
import calendar


def last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

def found_date():
    date = datetime.now()
    first_day = last_month(date.year, date.month)
    last_day = last_day_of_month(date.year, date.month)
    return first_day, last_day

def last_month(year_now, month_now):# מציאת החודש האחרון
    year_now = int(year_now)
    month_now = int(month_now)
    if month_now == 1:
        return f'{year_now - 1}-12'
    else:
        return f'{year_now}-{month_now - 1:02}'

def date_format(date):
    date_object = datetime.strptime(date + '-01', '%Y-%m-%d')
    formatted_date = date_object.strftime('%Y-%m')
    return formatted_date

def send_request_to_server(month ,last_day):
    url = f'http://host.docker.internal:8000/?first_day={month}&last_day={last_day}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['exchange_rates']
        return data
    else:
        return f'Error: {response.status_code}, {response.text}'

async def create_db_with_data(data):
    await data_base.create_db()
    for item in data['exchange_rates']:
        try:
            await data_base.save_data(item['date'], item['rate'])
        except ValueError as e:
            raise ValueError(f"Error inserting row: {e}")  from e
