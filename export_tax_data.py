import requests
import pandas as pd
from datetime import date, timedelta
import numpy as np

END_DATE = '2020-12-31'
# working backwards from END_DATE, how many days to check
N_DAYS = 365
# your HNT address
ACCOUNT_ADDRESS = 'PLACE_WALLET_ADDRESS_HERE'
EXPORT_PATH = 'hnt_tax_data_2020.csv'

url = 'https://api.helium.io/v1/accounts/' + ACCOUNT_ADDRESS + '/hotspots'
payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
hotspot_data = response.json()

hotspot_addresses = []
for i in range(len(hotspot_data['data'])):
    hotspot_addresses.append(hotspot_data['data'][i]['address'])

end_day = date.fromisoformat(END_DATE)
day_list_iso = []
for i in range(N_DAYS):
    day = end_day - timedelta(days=i)
    iso = day.isoformat()
    day_list_iso.append(iso)

mined_by_day = []
hnt_price_usd = []
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
    try:
        # coingecko price
        # rearrange date to DD-MM-YYYY
        date_str = day_list_iso[j]
        date_split = date_str.split('-')
        coingecko_date = date_split[2] + '-' + date_split[1] + '-' + date_split[0]
        url = "https://api.coingecko.com/api/v3/coins/helium/history?date=" + coingecko_date + "&localization=false"
        response = requests.request("GET", url, headers=headers, data=payload)

        prices = response.json()

        hnt_price_usd.append(prices['market_data']['current_price']['usd'])
        if np.remainder(j, 10) == 0:
            print(day_list_iso[j])

    except:
        hnt_price_usd.append(hnt_price_usd[j-1])

value_mined_usd = np.array(hnt_price_usd) * np.array(mined_by_day)
df = pd.DataFrame(data=[day_list_iso, mined_by_day, hnt_price_usd, value_mined_usd]).transpose()
df.columns = ['DATE', 'HNT_MINED', 'HNT_PRICE_USD', 'VALUE_MINED_USD']
df.to_csv(EXPORT_PATH)

# summary
total_taxable_value_usd = np.sum(value_mined_usd)

print(f"\nTOTAL TAXABLE INCOME (USD) FOR {END_DATE[:4]}: {total_taxable_value_usd}")
