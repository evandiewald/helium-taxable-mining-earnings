import time
import numpy as np
import pandas as pd
import requests

from datetime import date, timedelta


def export_wallet_taxes(account_address, year=2021):
    # your HNT address
    print('Collecting earnings data for account address: ', account_address)

    url = 'https://api.helium.io/v1/accounts/' + account_address + '/hotspots'
    hotspot_data = request_json(url)

    hotspot_added_dates = []
    for i in range(len(hotspot_data['data'])):
        date_added_iso = hotspot_data['data'][i]['timestamp_added'].split('T')[0]
        date_added_ts = date.fromisoformat(date_added_iso)
        hotspot_added_dates.append(date_added_ts)
    account_start_date = min(hotspot_added_dates)

    hotspot_addresses = []
    for i in range(len(hotspot_data['data'])):
        hotspot_addresses.append(hotspot_data['data'][i]['address'])

    year_start_date = date.fromisoformat(f'{year}-01-01')
    start_date = max(year_start_date, account_start_date)
    end_day = date.fromisoformat(f'{year}-01-05')
    n_days = end_day - start_date  # need to add one to include 1st day of the year
    day_list_iso = []
    for i in range(n_days.days + 1):
        day = end_day - timedelta(days=i)
        iso = day.isoformat()
        day_list_iso.append(iso)

    mined_by_day = get_mined_by_day(hotspot_addresses, day_list_iso)

    hnt_price_usd = pd.read_csv(f'coingecko_prices_{year}.csv')['HNT_PRICE_USD']
    value_mined_usd = np.array(hnt_price_usd[:len(mined_by_day)]) * np.array(mined_by_day)
    df = pd.DataFrame(data=[day_list_iso, mined_by_day, hnt_price_usd[:len(mined_by_day)], value_mined_usd]).transpose()
    df.columns = ['DATE', 'HNT_MINED', 'HNT_PRICE_USD', 'VALUE_MINED_USD']
    # df.to_csv(EXPORT_PATH)

    # summary
    total_taxable_value_usd = np.sum(value_mined_usd)

    print(f'\n\nTOTAL TAXABLE INCOME (USD) FOR {year}: ', str(total_taxable_value_usd))
    return df, total_taxable_value_usd


def export_hotspot_taxes(hotspot_address, year=2021):
    # your hotspot address
    print('Collecting earnings data for hotspot address: ', hotspot_address)

    url = 'https://api.helium.io/v1/hotspots/' + hotspot_address
    hotspot_data = request_json(url)

    hotspot_start_date = date.fromisoformat(hotspot_data['data']['timestamp_added'].split('T')[0])

    hotspot_address = hotspot_data['data']['address']
    hotspot_name = hotspot_data['data']['name']

    # if the hotspot was added before the 1st of the year only check till that date.
    year_start_date = date.fromisoformat(f'{year}-01-01')
    start_date = max(year_start_date, hotspot_start_date)

    end_day = date.fromisoformat(f'{year}-12-31')

    n_days = end_day - start_date
    day_list_iso = []
    for i in range(n_days.days + 1):
        day = end_day - timedelta(days=i)
        iso = day.isoformat()
        day_list_iso.append(iso)

    mined_by_day = get_mined_by_day([hotspot_address], day_list_iso)

    hnt_price_usd = pd.read_csv(f'coingecko_prices_{year}.csv')['HNT_PRICE_USD']
    value_mined_usd = np.array(hnt_price_usd[:len(mined_by_day)]) * np.array(mined_by_day)
    df = pd.DataFrame(data=[day_list_iso, mined_by_day, hnt_price_usd[:len(mined_by_day)], value_mined_usd]).transpose()
    df.columns = ['DATE', 'HNT_MINED', 'HNT_PRICE_USD', 'VALUE_MINED_USD']
    # df.to_csv(EXPORT_PATH)

    # summary
    total_taxable_value_usd = np.sum(value_mined_usd)

    print(f'\n\nTOTAL TAXABLE INCOME (USD) FOR {year}: ', str(total_taxable_value_usd))
    return df, total_taxable_value_usd, hotspot_name


def get_mined_by_day(hotspot_addresses, day_list_iso):
    mined_by_day = []
    for j in range(len(day_list_iso)-1):
        daily_total = 0
        for hotspot in hotspot_addresses:
            url = "https://api.helium.io/v1/hotspots/" + hotspot +\
                  "/rewards/sum?max_time=" + day_list_iso[j] + "&min_time=" +\
                  day_list_iso[j+1]
            total = request_json(url)
            daily_total += total['data']['total']

        mined_by_day.append(daily_total)

        if np.remainder(j, 10) == 0:
            print(day_list_iso[j])

    return mined_by_day


def request_json(url, headers={}, payload={}):
    sleep_seconds = 0.5
    while True:
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = response.json()
        if 'data' in json_response.keys():
            break
        else:
            time.sleep(sleep_seconds)
            sleep_seconds += 0.5
            print("problem with GET request")
    return json_response
