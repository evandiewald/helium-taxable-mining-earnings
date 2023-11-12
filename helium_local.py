import numpy as np
import pandas as pd

from datetime import date, timedelta
from Helium import MinedByDay

def export_wallet_taxes(fairspot_raw, year=2022):
    # your HNT address
    print(f"Collecting earnings data from file: {fairspot_raw}")

    hnt_price_usd = pd.read_csv(f'coingecko_prices_{year}.csv')['HNT_PRICE_USD']
    fairspot = pd.read_csv(fairspot_raw)

    # filter to only rewards
    rewards = fairspot.loc[fairspot['type'] == 'rewards_v1']

    # find start date in data
    start_date_iso = rewards['date'].min().split(' ')[0]
    start_date = date.fromisoformat(start_date_iso)

    hotspots = MinedByDayLocal([], year, start_date, rewards)
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

class MinedByDayLocal(MinedByDay):
    def __init__(self, hotspot_addresses, year, start_date, rewards):
        super().__init__(hotspot_addresses, year, start_date)
        self.rewards = rewards

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

        rewards = self.rewards
        mined_by_day = self.mined_by_day
        del day_list_iso[0]
        for j in range(len(day_list_iso)):
            day_rewards = rewards.loc[rewards['date'].str.contains(day_list_iso[j])]
            daily_total = day_rewards['hnt_amount'].sum()
            mined_by_day.append(daily_total)

            if np.remainder(j, 10) == 0:
                print(day_list_iso[j + 1])

        return day_list_iso, mined_by_day
