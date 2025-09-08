import requests
import xml.etree.ElementTree as ET
from flask import Flask, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import function
import data_base

app = Flask(__name__)
CORS(app)
scheduler = BackgroundScheduler()

async def job():
    first_day, last_day = function.found_date()
    data = await function.send_request_to_server(first_day, f'{first_day}-{last_day}')
    formatted_date = await function.date_format(data[0]['date'])
    await data_base.save_data(formatted_date, data[0]['rate'])
    await data_base.print_data()

@app.before_first_request
async def start_scheduler():
    data = get_data()
    await function.create_db_with_data(data)
    scheduler.add_job(job, 'cron', day=1, hour=0, minute=0)

@app.route('/')
async def in_loading_site() : 
    exchange_rates=get_data()
    await function.create_db_with_data(exchange_rates)
    asyncio.create_task(start_scheduler())
    return await data_base.get_data()

def get_data():
    first_day = request.args['first_day']
    last_day = request.args['last_day']
    url = (f'https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_USD_ILS.D.USD.ILS.ILS.OF00?startperiod={first_day}-01&endperiod={last_day}&normalisefreq=M;mean&locale=he')
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        exchange_rates = []
        for obs in root.findall('.//Obs'):
            time_period = obs.get('TIME_PERIOD')
            obs_value = obs.get('OBS_VALUE')
            exchange_rates.append({'date': time_period, 'rate': obs_value})
        return {'exchange_rates': exchange_rates}
    else:
        return {'error': 'Unable to fetch data'}, response.status_code

@app.route('/sort')
async def sort_data():
    value = request.args.get('value')
    try:
        return await data_base.sort_data(value)
    except Exception as e:
        return {'error': 'Unable to sort data'}

@app.route('/forecast')
async def forecast_for_next_month():
    return await data_base.select_last_three_months()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='8000')
