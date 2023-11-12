from Helium import export_wallet_taxes, export_wallet_taxes_by_hotspot, export_hotspot_taxes
from helium_local import export_wallet_taxes as export_wallet_taxes_local

# the functions in Helium.py give you three options for exporting earnings data:
#   1) export_wallet_taxes scrapes the data for all hotspots attached to your HNT wallet
#   2) export_wallet_taxes_by_hotspot saves the hotspot earnings individually based on name
#   3) export_hotspot_taxes scrapes data for an individual hotspot
# All functions return the following outputs:
#   - a pandas dataframe containing columns for (DATE, HNT_MINED, HNT_PRICE_USD, VALUE_MINED_USD)
#   - the total taxable earnings for 2020 for that wallet/hotspot (i.e. the sum of VALUE_MINED_USD)
#   - (for export_hotspot_taxes ONLY) the name of the hotspot (e.g. energetic-brown-bear)
# to export a CSV with methods 1 or 3 use the built-in pandas method: df.to_csv(EXPORT_PATH)
# *** DISCLAIMER: THIS IS NOT OFFICIAL TAX ADVICE AND SHOULD ONLY BE USED FOR EDUCATIONAL/EXPLORATORY PURPOSES ***


# Example 1: Exporting earnings for all hotspots in a given wallet
ACCOUNT_ADDRESS = 'ae9iurqijoaFAKEADDRESSsdfiojewroijssn'  # wallet that the hotspots are owned by
WALLET_EXPORT_PATH = 'account_earnings_2022.csv'

wallet_earnings_df, total_wallet_earnings = export_wallet_taxes(ACCOUNT_ADDRESS, year=2022)
# export a CSV
wallet_earnings_df.to_csv(WALLET_EXPORT_PATH)

# Example 2: Exporting earnings for all hotspots individually in a given wallet
ACCOUNT_ADDRESS = 'ae9iurqijoaFAKEADDRESSsdfiojewroijssn'  # wallet that the hotspots are owned by
# csvs export to the working directory
wallet_earnings_dfs, total_wallet_earnings = export_wallet_taxes_by_hotspot(ACCOUNT_ADDRESS)

# Example 3: Exporting earnings for a single hotspot
# hotspot address
HOTSPOT_ADDRESS = '112BTTz2TLqqmGiP7Zi2j1oyFyakjrJhumSoukEvQuzQ4ztQQVuB'

hotspot_earnings_df, total_hotspot_earnings, hotspot_name = export_hotspot_taxes(HOTSPOT_ADDRESS)
# export
hotspot_export_path = hotspot_name + '.csv'
hotspot_earnings_df.to_csv(hotspot_export_path)

# Example 4: local wallet data
year = 2022
address = "WALLET_ADDRESS"
fairspot_raw = fr"{year}\helium-{address}-{year}-raw.csv"
WALLET_EXPORT_PATH = f"helium-{address}-{year}-earnings.csv"
wallet_earnings_df, total_wallet_earnings = export_wallet_taxes_local(fairspot_raw, year=2022)
# export a CSV
wallet_earnings_df.to_csv(WALLET_EXPORT_PATH)