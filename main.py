import streamlit as st
from utils import model23 as model
import pandas as pd
from utils import constants as c


st.title('AAVE liquidations model')



with st.expander("Estimation of stETH:ETH rate after big swap of stETH for ETH in Curve pool and following liquidation"):
    steth_amount = st.number_input('Enter stETH amount', step=1)
    exchange = st.button('Calculate')
    if exchange:
        result1 = model.get_peg_after_exchange_steth_for_eth(steth_amount)
        st.write(f'stETH:ETH rate after swap of **{steth_amount}** stETH for ETH and following liquidations: **{result1}**')


with st.expander("Estimation of stETH:ETH rate after remove of big amount of ETH from Curve pool and following liquidation"):
    remove_amount = st.number_input('Enter ETH amount', step=1)
    remove = st.button('Remove')
    if remove:
        result2 = model.get_peg_after_remove_eth_one(remove_amount)
        st.write(f'stETH:ETH rate after swap of **{remove_amount}** stETH for ETH and following liquidations: **{result2}**')

with st.expander("Estimation of stETH:ETH rate and amount of stETH to swap which could start cascade liquidation"):

    cascade_liq = st.button('Get estimation')
    if cascade_liq:
        cascade_liquidation = model.get_peg_and_exchange_amount_to_start_cascade_liq()
        st.write(f'stETH:ETH rate after remove of {cascade_liquidation[1]} ETH from pool and following liquidations: {cascade_liquidation[0]}')

with st.expander("Estimation of ETH price which could lead to cascade liquidation"):

    cascade_liq_price = st.button('Get price')
    if cascade_liq_price:
        cascade_liquidation_price = model.get_eth_price_to_start_cascade_liq()
        st.write(f'ETH price that could lead to cascade liquidations: **{ cascade_liquidation_price}**$')

with st.expander("Get the riskiest positions in order by (w)stETH collateral amount"):
    riskiest_amount=steth_amount = st.number_input('Enter amount of positions', step=1)

    riskiest_positions= st.button('Get positions')
    if riskiest_positions:
        riskiest_positions_df = model.get_aave_riskiest_positions(riskiest_amount)
        st.dataframe(riskiest_positions_df)