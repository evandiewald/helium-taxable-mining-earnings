import time
import numpy as np
import pandas as pd
import requests

from datetime import date, timedelta


def export_wallet_taxes_by_hotspot(account_address, year=2021):
    # your HNT address
    print('Collecting earnings data for account address: ', account_address)

    url = 'https://api.helium.io/v1/accounts/' + account_address + '/hotspots'
    hotspot_data = request_json(url)

    hotspot_added_dates = []
    for i in range(len(hotspot_data['data'])):
        date_added_iso = hotspot_data['data'][i]['timestamp_added'].split('T')[0]
        date_added_ts = date.fromisoformat(date_added_iso)
        hotspot_added_dates.append(date_added_ts)

    hnt_price_usd = pd.read_csv(f'coingecko_prices_{year}.csv')['HNT_PRICE_USD']
    total_taxable_value_usd = 0
    hotspots = {}
    dfs = {}
    for i in range(len(hotspot_data['data'])):
        hotspot_address = hotspot_data['data'][i]['address']
        hotspot_name = hotspot_data['data'][i]['name']
        hotspot = MinedByDay([hotspot_address], year, hotspot_added_dates[i])
        hotspots[hotspot_name] = hotspot
        hotspot.get_data()
        dfs[hotspot_name] = hotspot.calc_value(hnt_price_usd)
        hotspot.export_to_csv(name=hotspot_name)
        total_taxable_value_usd += np.sum(hotspot.value_mined_usd)

    print(f'\n\nTOTAL TAXABLE INCOME (USD) FOR {year}: ', str(total_taxable_value_usd))
    return dfs, total_taxable_value_usd


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

    hotspots = MinedByDay(hotspot_addresses, year, account_start_date)
    day_list_iso, mined_by_day = hotspots.get_data()

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

    hotspot = MinedByDay([hotspot_address], year, hotspot_start_date)
    hotspot.get_data()
    df = hotspot.calc_value()

    # summary
    total_taxable_value_usd = np.sum(hotspot.value_mined_usd)

    print(f'\n\nTOTAL TAXABLE INCOME (USD) FOR {year}: ', str(total_taxable_value_usd))
    return df, total_taxable_value_usd, hotspot_name


class MinedByDay:
    def __init__(self, hotspot_addresses, year, start_date):
        self.hotspot_addresses = hotspot_addresses
        self.year = year
        self.start_date = start_date
        self.mined_by_day = []
        self.day_list_iso = []
        self.value_mined_usd = None
        self.df = None

    def get_data(self):
        year_start_date = date.fromisoformat(f'{self.year}-01-01')
        start_date = max(year_start_date, self.start_date)
        # need the 1st day of new year in the day list to get every day
        end_day = date.fromisoformat(f'{self.year + 1}-01-01')
        n_days = end_day - start_date
        day_list_iso = self.day_list_iso
        for i in range(n_days.days + 1):
            day = end_day - timedelta(days=i)
            iso = day.isoformat()
            day_list_iso.append(iso)

        mined_by_day = self.mined_by_day
        for j in range(len(day_list_iso) - 1):
            daily_total = 0
            for hotspot in self.hotspot_addresses:
                url = "https://api.helium.io/v1/hotspots/" + hotspot +\
                      "/rewards/sum?max_time=" + day_list_iso[j] + "&min_time=" +\
                      day_list_iso[j + 1]
                total = request_json(url)
                daily_total += total['data']['total']

            mined_by_day.append(daily_total)

            if np.remainder(j, 10) == 0:
                print(day_list_iso[j + 1])

        del day_list_iso[0]

        return day_list_iso, mined_by_day

    def calc_value(self, hnt_price_usd):
        mined_by_day = self.mined_by_day
        day_list_iso = self.day_list_iso
        self.value_mined_usd = np.array(hnt_price_usd[:len(mined_by_day)]) * np.array(mined_by_day)
        df = pd.DataFrame(
            data=[day_list_iso, mined_by_day, hnt_price_usd[:len(mined_by_day)], self.value_mined_usd]).transpose()
        df.columns = ['DATE', 'HNT_MINED', 'HNT_PRICE_USD', 'VALUE_MINED_USD']
        self.df = df
        return df

    def export_to_csv(self, export_path='', name=''):
        if not export_path:
            export_path = f'{self.year}_{name}.csv'

        self.df.to_csv(export_path)


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
