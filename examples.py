from Helium import export_wallet_taxes, export_hotspot_taxes

# the functions in Helium.py give you two options for exporting earnings data:
#   1) export_wallet_taxes(account_address) scrapes the data for all hotspots attached to your HNT wallet
#   2) export_hotspot_taxes(hotspot_address) scrapes data for an individual hotspot
# both functions return the following outputs:
#   - a pandas dataframe containing columns for (DATE, HNT_MINED, HNT_PRICE_USD, VALUE_MINED_USD)
#   - the total taxable earnings for 2020 for that wallet/hotspot (i.e. the sum of VALUE_MINED_USD)
#   - (for export_hotspot_taxes ONLY) the name of the hotspot (e.g. energetic-brown-bear)
# to export a CSV, use the built-in pandas method: df.to_csv(EXPORT_PATH)
# *** DISCLAIMER: THIS IS NOT OFFICIAL TAX ADVICE AND SHOULD ONLY BE USED FOR EDUCATIONAL/EXPLORATORY PURPOSES ***


## Example 1: Exporting earnings for all hotspots in a given wallet
# wallet that the hotspots are owned by
ACCOUNT_ADDRESS = '14b7gkGPca2zyRCbUr1uuykiJwdtYnDhdZ3XBKgXocKQANrSavd'
WALLET_EXPORT_PATH = 'account_earnings_2020.csv'

wallet_earnings_df, total_wallet_earnings = export_wallet_taxes(ACCOUNT_ADDRESS)
# export a CSV
wallet_earnings_df.to_csv(WALLET_EXPORT_PATH)

## Example 2: Exporting earnings for a single hotspot
# hotspot address
HOTSPOT_ADDRESS = '112BTTz2TLqqmGiP7Zi2j1oyFyakjrJhumSoukEvQuzQ4ztQQVuB'

hotspot_earnings_df, total_hotspot_earnings, hotspot_name = export_hotspot_taxes(HOTSPOT_ADDRESS)
# export
hotspot_export_path = hotspot_name + '.csv'
hotspot_earnings_df.to_csv(hotspot_export_path)
