# helium-taxable-mining-earnings

A brutally simple script + application for exporting a CSV of taxable earnings for a given account based on the USD/HNT price on Coingecko. A public version of the application is hosted [here](http://heliumtaxtool.com).
## ***Disclaimer**: This is not official tax advice - I have zero qualifications and take no responsibility for how you use this code. Use at your own risk and make sure to consult a tax professional.*

I suspect that Helium is many folks' first experience with crypto mining (it is for me) and thus, maneuvering crypto taxes. My understanding is that the IRS considers mined crypto as income, based on the USD value of the token on that day.

e.g. If I mined 10 HNT on 12/30/2020 and the market price on that day was $1.50/HNT, that is considered $15 in eligible income.

If you then sell this mined HNT, the difference between the mined price and sell price will be realized as a capital gain/loss. 
Some more details here: https://cryptotrader.tax/blog/how-to-handle-cryptocurrency-mining-on-your-taxes

Most exchanges and tax preparation software can help you handle the capital gains aspect, but I haven't seen a straightforward way to calculate your eligible income for mined HNT. This extremely simple script is meant for my own purposes, but I figured I'd share in case it helps others. Simply plug in your account address and it will generate a CSV file with four columns: 
- DATE: the script starts from 12-31-2020 and works backward for N_DAYS (I have it set at 365, but it depends when you got your first hotspot)
- HNT_MINED: total HNT mined on that day for all hotspots associated with your address (gathered by calling the [Helium API](https://developer.helium.com/blockchain/api/api-hotspots)
- HNT_PRICE_USD: the Coingecko price for HNT (in USD) on that date
- VALUE_MINED_USD: calculated as HNT_MINED * HNT_PRICE_USD (total eligible mined income for that date)

## Usage
1. Clone the repo. 
`git clone https://github.com/evandiewald/helium-taxable-mining-earnings.git`
2. `cd` into the directory
3. Install `requirements.txt`
`pip install -r requirements.txt`
4. Example usage (from [`examples.py`](examples.py):
```
from Helium import export_wallet_taxes, export_hotspot_taxes

## Example 1: Exporting earnings for all hotspots in a given wallet
# wallet that the hotspots are owned by
ACCOUNT_ADDRESS = '14b7gkGPca2zyRCbUr1uuykiJwdtYnDhdZ3XBKgXocKQANrSavd'
WALLET_EXPORT_PATH = 'account_earnings_2020.csv'

wallet_earnings_df, total_wallet_earnings = export_wallet_taxes(ACCOUNT_ADDRESS)
# export a CSV
wallet_earnings_df.to_csv(WALLET_EXPORT_PATH)

## Example 2: Exporting earnings for a single hotspot
# hotspot address
HOTSPOT_ADDRESS = '112X1p7bucmicDfr8jAausQYjbXPor2iFTkkko43HT7CS4ziR9kB'

hotspot_earnings_df, total_hotspot_earnings, hotspot_name = export_hotspot_taxes(HOTSPOT_ADDRESS)
# export
hotspot_export_path = hotspot_name + '.csv'
hotspot_earnings_df.to_csv(hotspot_export_path)
```
5. Running the browser based [Streamlit](https://streamlit.io) app locally:

`streamlit run app.py`

The app is served by default at http://localhost:8501

Like I said, nothing special, but if it saves someone a few minutes of coding then it's worth it. 
