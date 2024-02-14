import matplotlib.pyplot as plt
import pandas as pd
import squarify
import streamlit as st

from equity_market import equity_market_data

nse = equity_market_data.NSE()

equity_market_categories = ['PRE MARKET NIFTY', 'PRE MARKET FO', 'NIFTY 50', 'NIFTY BANK', 'NIFTY AUTO', 'NIFTY ENERGY',
                            'NIFTY FINANCIAL SERVICES',
                            'NIFTY FMCG', 'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY PHARMA',
                            'NIFTY PSU BANK', 'NIFTY REALTY', 'NIFTY PRIVATE BANK', 'NIFTY MIDCAP SELECT', ]


def percent_chart(data):
    # Sort values into positive and negative
    positive_df = data[data['pChange'] > 0].sort_values(by='pChange', ascending=False)
    negative_df = data[data['pChange'] < 0].sort_values(by='pChange',
                                                        ascending=False)  # Sort negative values ascending for squarify

    # Define colors for positive and negative values
    colors = ['green'] * len(positive_df) + ['red'] * len(negative_df)

    # Concatenate positive and negative DataFrames
    sorted_df = pd.concat([positive_df, negative_df])

    # Remove gap between boxes
    fig, ax = plt.subplots(figsize=(16, 8))
    squarify.plot(sizes=sorted_df['pChange'].abs(),
                  label=sorted_df['symbol'] + '\n' + sorted_df['pChange'].apply(lambda x: "{:.2f}".format(x)),
                  color=colors, alpha=0.7, edgecolor="white", linewidth=0.5,
                  text_kwargs={'color': 'white'})

    # Show label and value in each box
    plt.axis('off')

    plt.gca().invert_yaxis()

    # Display the chart using Streamlit
    return fig


def equity_data_chart(value):
    # Retrieve data
    if value in ["PRE MARKET NIFTY", "PRE MARKET FO"]:
        data = nse.pre_market_data("NIFTY 50" if value == "PRE MARKET NIFTY" else "FO")
    else:
        data = nse.equity_market_data(value)

    fig = percent_chart(data)
    st.pyplot(fig, use_container_width=True)
    st.write(data)

# if __name__ == "__main__":
#     df = nse.equity_market_data('NIFTY 50')
#     df = pd.DataFrame(df)
#     print(df)
