import warnings
import streamlit as st
import sectorial_flow as dc
import equity_chart as ec
import option_chart as oc
import socket

warnings.filterwarnings('ignore')

equity_market_categories = ['PRE MARKET NIFTY', 'PRE MARKET FO', 'NIFTY 50', 'NIFTY BANK', 'NIFTY AUTO', 'NIFTY ENERGY',
                            'NIFTY FINANCIAL SERVICES',
                            'NIFTY FMCG', 'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY PHARMA',
                            'NIFTY PSU BANK', 'NIFTY REALTY', 'NIFTY PRIVATE BANK', 'NIFTY MIDCAP SELECT', ]

st.set_page_config(page_title='iNSIGHTS', page_icon=':bar_chart', layout='wide')
st.sidebar.header('iNSIGHTS')
menu = ['Sectorial Flow', 'Equity Market', 'Option Chain']
value = st.sidebar.radio('Select Menu', menu)
if st.button("Refresh"):
    st.experimental_rerun()
try:
    if value == 'Sectorial Flow':
        dc.sectorial_flow()


    elif value == 'Equity Market':
        value = st.sidebar.selectbox('Select index here', equity_market_categories)
        ec.equity_data_chart(value)


    elif value == 'Option Chain':
        indices_list = ['NIFTY', 'FINNIFTY', 'BANKNIFTY', 'MIDCPNIFTY']
        value = st.sidebar.selectbox('Select Index', indices_list)

        if value == 'NIFTY':
            exp_dates = st.sidebar.selectbox('Select expiry', oc.nifty_expdates())
            oc.plot_option_chain_analysis(value, exp_dates)

        elif value == 'BANKNIFTY':
            exp_dates = st.sidebar.selectbox('Select expiry', oc.bn_expdates())
            oc.plot_option_chain_analysis(value, exp_dates)

        elif value == 'FINNIFTY':
            exp_dates = st.sidebar.selectbox('Select expiry', oc.fn_expdates())
            oc.plot_option_chain_analysis(value, exp_dates)

        elif value == 'MIDCPNIFTY':
            exp_dates = st.sidebar.selectbox('Select expiry', oc.midn_expdates())

            oc.plot_option_chain_analysis(value, exp_dates)

        else:
            st.error('Wrong Input')
except socket.error as e:
    st.error(f"Error: {e}. Connection closed by the remote host.")
    # Delayed rerun to refresh the page after a connection error
    st.experimental_rerun()
