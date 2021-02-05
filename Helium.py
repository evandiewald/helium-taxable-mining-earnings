import requests
import pandas as pd
from datetime import date, timedelta
import numpy as np


def export_wallet_taxes(account_address):
    # your HNT address
    print('Collecting earnings data for account address: ', account_address)

    url = 'https://api.helium.io/v1/accounts/' + account_address + '/hotspots'
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    hotspot_data = response.json()

    hotspot_added_dates = []
    for i in range(len(hotspot_data['data'])):
        date_added_iso = hotspot_data['data'][i]['timestamp_added'].split('T')[0]
        date_added_ts = date.fromisoformat(date_added_iso)
        hotspot_added_dates.append(date_added_ts)
    account_start_date = min(hotspot_added_dates)


    hotspot_addresses = []
    for i in range(len(hotspot_data['data'])):
        hotspot_addresses.append(hotspot_data['data'][i]['address'])

    end_day = date.fromisoformat('2020-12-31')
    n_days = end_day - account_start_date
    day_list_iso = []
    for i in range(n_days.days):
        day = end_day - timedelta(days=i)
        iso = day.isoformat()
        day_list_iso.append(iso)

    mined_by_day = []
    hnt_price_usd = pd.read_csv('coingecko_prices_2020.csv')['HNT_PRICE_USD']
    for j in range(len(day_list_iso)-1):
        daily_total = 0
        for hotspot in hotspot_addresses:
            url = "https://api.helium.io/v1/hotspots/" + hotspot + "/rewards/sum?max_time=" + day_list_iso[j] + "&min_time=" + day_list_iso[j+1]
            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            total = response.json()
            daily_total += total['data']['total']
        mined_by_day.append(daily_total)

        if np.remainder(j, 10) == 0:
            print(day_list_iso[j])


    value_mined_usd = np.array(hnt_price_usd[:len(mined_by_day)]) * np.array(mined_by_day)
    df = pd.DataFrame(data=[day_list_iso, mined_by_day, hnt_price_usd[:len(mined_by_day)], value_mined_usd]).transpose()
    df.columns = ['DATE', 'HNT_MINED', 'HNT_PRICE_USD', 'VALUE_MINED_USD']
    # df.to_csv(EXPORT_PATH)

    # summary
    total_taxable_value_usd = np.sum(value_mined_usd)

    print('\n\nTOTAL TAXABLE INCOME (USD) FOR 2020: ', str(total_taxable_value_usd))
    return df, total_taxable_value_usd


def export_hotspot_taxes(hotspot_address):
    # your hotspot address
    print('Collecting earnings data for hotspot address: ', hotspot_address)

    url = 'https://api.helium.io/v1/hotspots/' + hotspot_address
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    hotspot_data = response.json()

    account_start_date = date.fromisoformat(hotspot_data['data']['timestamp_added'].split('T')[0])

    hotspot_addresses = hotspot_data['data']['address']
    hotspot_name = hotspot_data['data']['name']

    end_day = date.fromisoformat('2020-12-31')

    n_days = end_day - account_start_date
    day_list_iso = []
    for i in range(n_days.days):
        day = end_day - timedelta(days=i)
        iso = day.isoformat()
        day_list_iso.append(iso)

    mined_by_day = []
    hnt_price_usd = pd.read_csv('coingecko_prices_2020.csv')['HNT_PRICE_USD']
    for j in range(len(day_list_iso)-1):

        url = "https://api.helium.io/v1/hotspots/" + hotspot_addresses + "/rewards/sum?max_time=" + day_list_iso[j] + "&min_time=" + day_list_iso[j+1]
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        total = response.json()
        daily_total = total['data']['total']
        mined_by_day.append(daily_total)

        if np.remainder(j, 10) == 0:
            print(day_list_iso[j])


    value_mined_usd = np.array(hnt_price_usd[:len(mined_by_day)]) * np.array(mined_by_day)
    df = pd.DataFrame(data=[day_list_iso, mined_by_day, hnt_price_usd[:len(mined_by_day)], value_mined_usd]).transpose()
    df.columns = ['DATE', 'HNT_MINED', 'HNT_PRICE_USD', 'VALUE_MINED_USD']
    # df.to_csv(EXPORT_PATH)

    # summary
    total_taxable_value_usd = np.sum(value_mined_usd)

    print('\n\nTOTAL TAXABLE INCOME (USD) FOR 2020: ', str(total_taxable_value_usd))
    return df, total_taxable_value_usd, hotspot_name
