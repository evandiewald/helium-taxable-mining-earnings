import streamlit as st
import numpy as np
from Helium import export_wallet_taxes, export_hotspot_taxes

st.set_page_config(
    page_title="HNT Tax Tool",
    page_icon=":rocket:",
    menu_items={
             'Report a bug': "https://github.com/evandiewald/helium-taxable-mining-earnings/issues"         }
)
st.title("Helium Taxable Mining Earnings")

with st.expander("About this Tool"):
    st.write("""A simple tool for exporting a CSV of taxable earnings for a given account based on the USD/HNT price on Coingecko.""")
    st.subheader("""**Disclaimer**: This is not official tax advice - I have zero qualifications and take no responsibility for how you use this code. Use at your own risk and make sure to consult a tax professional.""")
    
    st.markdown("""I suspect that Helium is many folks' first experience with crypto mining (it is for me) and thus, maneuvering crypto taxes. My understanding is that the IRS considers mined crypto as income, based on the USD value of the token on that day.
    e.g. If I mined 10 HNT on 12/30/2020 and the market price on that day was \$1.50/HNT, that is considered \$15 in eligible income.""")

    st.markdown("""If you then sell this mined HNT, the difference between the mined price and sell price will be realized as a capital gain/loss.
    Some more details [here](https://cryptotrader.tax/blog/how-to-handle-cryptocurrency-mining-on-your-taxes).""")

    st.markdown("""Check us out on [Github](https://github.com/evandiewald/helium-taxable-mining-earnings)""")

year = st.selectbox("Select Year", [2021, 2020])
mode = st.radio("Export Mode", ["By Wallet", "By Hotspot"])
address = st.text_input("Address")

submit = st.button("Submit")
if submit:
    with st.spinner("Processing...this may take a while"):
        if mode == "By Wallet":
            df, total_wallet_earnings = export_wallet_taxes(address, year=year)
            st.metric(f"Total Wallet Earnings for {year}", value=f"$ {np.round(total_wallet_earnings, 2)}")
        elif mode == "By Hotspot":
            df, total_hotspot_earnings, hotspot_name = export_hotspot_taxes(address, year=year)
            st.metric(f"Total Earnings for {hotspot_name} in {year}", value=f"$ {np.round(total_hotspot_earnings, 2)}")
        st.dataframe(df)
        download_button = st.download_button("Download CSV", data=df.to_string(), file_name=f"{address}.csv")