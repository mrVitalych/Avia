import requests
from datetime import datetime, timedelta
import pandas as pd
import sys
from conf import BASE_URL, TOKEN, DAYS_OFFSET
import logging

PARAMS = {
    "origin": "LED",
    "destination": "MOW",
    "unique": "true",
    "sorting": "price",
    "direct": "true",
    "currency": "rub",
    "limit": 30,
    "page": 1,
    "one_way": "true",
    "token": TOKEN
}

args = sys.argv

if len(args) < 3:
    print('Not enough args')
    sys.exit(1)
    
ORIGIN = args[1]
DESTINATION = args[2]
CURRENT_DTTM = args[3]
TODAY = datetime.now()

PARAMS['origin'] = ORIGIN
PARAMS['destination'] = DESTINATION

logger = logging.getLogger('avia_logger')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(f'logs/data_{ORIGIN}_{DESTINATION}.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def main():

    current_date = TODAY
    result = []

    for _ in range(DAYS_OFFSET):
        today_str = current_date.strftime('%Y-%m-%d')
        PARAMS['departure_at'] = today_str
        try:
            response = requests.get(BASE_URL, params=PARAMS, timeout=20)
            if response.status_code == 200:
                response = response.json()
                if response['data']:
                    row = response['data'][0]
                    result.append(row)
                    logger.info(f'Processed date = {today_str}')
                else:
                    logger.info(f'No data for date = {today_str}')
            else:
                logger.warning(f'{response.status_code = }')
        except requests.exceptions.ReadTimeout as e:
            logger.error(f'{today_str} - {e}')
        except requests.exceptions.RequestException as e:
            logger.error(f'{today_str} - {e}')

        current_date += timedelta(days=1)

    df = pd.DataFrame.from_dict(result)
    df['process_dttm'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csv_filename = f'files/data_{ORIGIN}_{DESTINATION}_{CURRENT_DTTM}.txt'
    df.to_csv(csv_filename, sep='\t', index=False, header=False)
    logger.info(f'CSV file is ready: {csv_filename}')
    return True

if __name__=='__main__':
    logger.info(f'Started! {CURRENT_DTTM}')
    main()
    logger.info(f'Completed! {CURRENT_DTTM}\n')
