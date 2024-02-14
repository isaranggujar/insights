import time
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
from matplotlib import pyplot as plt
from derivatives import option_data
from equity_market import equity_market_data

od = option_data.NSE()
nse = equity_market_data.NSE()

data_dict = nse.indices_data().to_dict()


def nifty_expdates():
    # Get the current date
    current_date = datetime.now()

    # Calculate the difference in days between the current day and the next Thursday (weekday 3)
    days_until_next_thursday = (3 - current_date.weekday() + 7) % 7

    # Calculate the date for the next Thursday
    next_thursday = current_date + timedelta(days=days_until_next_thursday)

    # Initialize a list to store Thursday dates
    thursday_dates = []

    # Collect all Thursdays for the current week and the next five weeks
    for _ in range(4):  # Six weeks total (current week + next five weeks)
        thursday_dates.append(next_thursday.strftime("%d-%m-%Y"))
        next_thursday += timedelta(days=7)

    return thursday_dates


def bn_expdates():
    # Get the current date
    current_date = datetime.now()

    # Calculate the difference in days between the current day and the next Wednesday (weekday 2)
    days_until_next_wednesday = (2 - current_date.weekday() + 7) % 7

    # Calculate the date for the next Wednesday
    next_wednesday = current_date + timedelta(days=days_until_next_wednesday)

    # Initialize a list to store Wednesday dates
    wednesday_dates = []

    # Collect all Wednesdays for the current week and the next five weeks
    for _ in range(4):  # Six weeks total (current week + next five weeks)
        wednesday_dates.append(next_wednesday.strftime("%d-%m-%Y"))
        next_wednesday += timedelta(days=7)

    # Drop the first Wednesday (current week's Wednesday)
    # wednesday_dates.pop(0)

    return wednesday_dates


def fn_expdates():
    # Get the current date
    current_date = datetime.now()

    # Calculate the difference in days between the current day and the next Tuesday (weekday 1)
    days_until_next_tuesday = (1 - current_date.weekday() + 7) % 7

    # Calculate the date for the next Tuesday
    next_tuesday = current_date + timedelta(days=days_until_next_tuesday)

    # Initialize a list to store Tuesday dates
    tuesday_dates = []

    # Collect all Tuesdays for the current week and the next five weeks
    for _ in range(4):  # Six weeks total (current week + next five weeks)
        tuesday_dates.append(next_tuesday.strftime("%d-%m-%Y"))
        next_tuesday += timedelta(days=7)

    # Drop the first Tuesday (current week's Tuesday)

    return tuesday_dates


def midn_expdates():
    # Get the current date
    current_date = datetime.now()

    # Calculate the difference in days between the current day and the next Monday (weekday 0)
    days_until_next_monday = (0 - current_date.weekday() + 7) % 7

    # Calculate the date for the next Monday
    next_monday = current_date + timedelta(days=days_until_next_monday)

    # Initialize a list to store Monday dates
    monday_dates = []

    # Collect all Mondays for the current week and the next five weeks
    for _ in range(4):  # Six weeks total (current week + next five weeks)
        monday_dates.append(next_monday.strftime("%d-%m-%Y"))
        next_monday += timedelta(days=7)

    return monday_dates


def oc_pcr(labels1, values1):
    # Custom colors
    custom_colors = ['#d36135', '#08bdbd']  # Example custom colors

    # Create a donut chart
    fig, ax = plt.subplots(figsize=(6, 7))
    ax.pie(values1, labels=labels1, colors=custom_colors, autopct='%1.1f%%',
           startangle=90,
           textprops={'fontsize': 14},
           wedgeprops=dict(width=0.4))

    # Draw a circle in the middle to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    # Add title in the middle
    plt.title('CE/PE Total OI', fontsize=20, y=1.1)

    return fig


def oc_dial(labels, values):
    # Sample data
    categories = labels
    values = values

    # Default colors for bars
    default_colors = ['#08bdbd', '#d36135']

    # Determine colors based on conditions
    for i, value in enumerate(values):
        if value >= 0:
            if i == 0:
                default_colors[i] = '#08bdbd'  # First bar color: green if value crosses above 0
            else:
                default_colors[i] = '#d36135'  # Second bar color: red if value crosses above 0
        elif value <= 0:
            if i == 0:
                default_colors[i] = '#d36135'  # First bar color: red if value crosses below 0
            else:
                default_colors[i] = '#08bdbd'  # Second bar color: green if value crosses below 0

    # Create bar chart with custom colors
    fig, ax = plt.subplots(figsize=(6, 6))
    bars = ax.bar(categories, values, color=default_colors)

    # Add labels and title
    # ax.set_xlabel('Categories')
    # ax.set_ylabel('Values')
    ax.set_title('CE/PE Change in OI', fontsize=20, y=1.1)
    ax.tick_params(axis='x', labelsize=14)

    # Remove the border
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Add values on top of the bars
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 1, str(value), ha='center', color='black',
                 fontsize=14)

    return fig


def change_in_oi_bar_chart(CALLS_Chng_in_OI, PUTS_Chng_in_OI, Strike_Price, current_strike_price):
    # Create a dataframe from the data
    data = {
        'CALLS_Chng_in_OI': CALLS_Chng_in_OI,
        'PUTS_Chng_in_OI': PUTS_Chng_in_OI,
        'Strike_Price': Strike_Price
    }
    df = pd.DataFrame(data)

    # Define colors based on the conditions
    call_colors = ['#d36135' if val >= 0 else '#08bdbd' for val in df['CALLS_Chng_in_OI']]
    put_colors = ['#08bdbd' if val >= 0 else '#d36135' for val in df['PUTS_Chng_in_OI']]

    # Create the bar chart using Plotly Express
    fig = px.bar(df, y='Strike_Price', x=['CALLS_Chng_in_OI', 'PUTS_Chng_in_OI'],
                 labels={'value': 'Change in Open Interest', 'variable': 'Option Type'},
                 orientation='h',
                 height=2500,
                 text='value',
                 # barmode='group',
                 color_discrete_sequence=[call_colors, put_colors])

    # Customize hover details to include strike price and set font size
    fig.update_traces(hovertemplate='Strike Price: %{y}<br>' +
                                    'Change in OI: %{value}<br>' +
                                    '<extra></extra>',
                      hoverlabel=dict(font_size=14),  # Set font size for hover text
                      insidetextfont=dict(size=14, color='white')  # Set font size and color for the values
                      )

    # Add a solid white line for the current strike price
    fig.add_shape(type="line",
                  y0=current_strike_price,
                  x0=0,
                  y1=current_strike_price,
                  x1=min(max(df['CALLS_Chng_in_OI']), max(df['PUTS_Chng_in_OI'])),
                  line=dict(color="black", width=1, dash="solid")
                  )

    # Remove zoom
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=40),
        xaxis=dict(title_text='Change in Open Interest', fixedrange=True,
                   title_font=dict(family='Arial'), tickfont=dict(size=14, family='Arial')),
        # Set x-axis title name and font size
        yaxis=dict(title_text='Strike Price', fixedrange=True,
                   title_font=dict(family='Arial'), tickfont=dict(size=14, family='Arial')),
        # Set y-axis title name and font size
        showlegend=False,
        font=dict(size=18, family='Calibri'),
        title=dict(text='CE/PE Change in OI', x=0.4, y=None)  # Centered title
    )

    return fig


def total_oi_bar_chart(CALLS_OI, PUTS_OI, Strike_Price, current_strike_price):
    # Create a dataframe from the data
    data = {
        'CALLS_OI': CALLS_OI,
        'PUTS_OI': PUTS_OI,
        'Strike_Price': Strike_Price
    }
    df = pd.DataFrame(data)

    # Define colors based on the conditions
    call_colors = ['#d36135' if val >= 0 else '#08bdbd' for val in CALLS_OI]
    put_colors = ['#08bdbd' if val >= 0 else '#d36135' for val in PUTS_OI]

    # Create the bar chart using Plotly Express
    fig = px.bar(df, x='Strike_Price', y=['CALLS_OI', 'PUTS_OI'],
                 labels={'value': 'Total Open Interest', 'variable': 'Option Type'},
                 orientation='v',
                 height=500,
                 # text='value',
                 # barmode='group',
                 color_discrete_sequence=[call_colors, put_colors])

    # Customize hover details to include strike price and set font size
    fig.update_traces(hovertemplate='Strike Price: %{x}<br>' +
                                    'Total OI: %{value}<br>' +
                                    '<extra></extra>',
                      hoverlabel=dict(font_size=14),  # Set font size for hover text
                      insidetextfont=dict(size=14, color='white')  # Set font size and color for the values
                      )

    # Add a solid white line for the current strike price
    fig.add_shape(type="line",
                  x0=current_strike_price,
                  y0=0,
                  x1=current_strike_price,
                  y1=min(max(CALLS_OI), max(PUTS_OI)),
                  line=dict(color="black", width=1, dash="solid")
                  )

    # Remove zoom
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=40),
        xaxis=dict(title_text='Strike Price', fixedrange=True,
                   title_font=dict(family='Arial'), tickfont=dict(size=14, family='Arial')),
        # Set x-axis title name and font size
        yaxis=dict(title_text='Total Open Interest', fixedrange=True,
                   title_font=dict(family='Arial'), tickfont=dict(size=14, family='Arial')),
        # Set y-axis title name and font size
        showlegend=False,
        font=dict(size=18, family='Calibri'),
        title=dict(text='CE/PE Total OI', x=0.4, y=None)  # Centered title
    )

    return fig


def fetch_last_value_by_name(data_dict, index_name):
    # Find the index corresponding to the given index name
    index_symbol = None
    for index, name in data_dict["indexSymbol"].items():
        if name == index_name:
            index_symbol = index
            break

    # Fetch the last value of the index
    if index_symbol is not None:
        last_value = data_dict["last"].get(index_symbol)
        return last_value
    else:
        return None


def plot_option_chain_analysis(value, exp_dates):
    derivative_df = od.nse_live_option_chain(value, exp_dates)

    # Convert relevant columns to integers
    int_columns = ['CALLS_Chng_in_OI', 'PUTS_Chng_in_OI', 'CALLS_OI', 'PUTS_OI']
    derivative_df[int_columns] = derivative_df[int_columns].astype(int)

    # Calculate total change in open interest for calls and puts
    call_chng_in_OI = derivative_df['CALLS_Chng_in_OI'].sum()
    puts_chng_in_OI = derivative_df['PUTS_Chng_in_OI'].sum()

    # Calculate total open interest for calls and puts
    call_OI = derivative_df['CALLS_OI'].sum()
    puts_OI = derivative_df['PUTS_OI'].sum()

    # Plot donut charts and line charts
    col1, col2 = st.columns(2)

    with col1:
        # Plot donut chart for change in open interest
        fig = oc_dial(['Put Change in OI', 'Call Change in OI'], [puts_chng_in_OI, call_chng_in_OI])
        st.pyplot(fig, use_container_width=True)

    with col2:
        # Plot donut chart for put-call ratio
        fig1 = oc_pcr(['Call OI', 'Put OI'], [call_OI, puts_OI])
        st.pyplot(fig1, use_container_width=True)

    index_mapping = {
        "NIFTY": "NIFTY 50",
        "BANKNIFTY": "NIFTY BANK",
        "FINNIFTY": "NIFTY FIN SERVICE",
        "MIDCPNIFTY": "NIFTY MID SELECT"
    }

    index_name = index_mapping.get(value)

    price_value = fetch_last_value_by_name(data_dict, index_name)
    st.write(value + ' : ' + str(price_value))

    fig = change_in_oi_bar_chart(derivative_df['CALLS_Chng_in_OI'], derivative_df['PUTS_Chng_in_OI'],
                                 derivative_df['Strike_Price'], price_value)

    st.plotly_chart(fig, use_container_width=True)

    fig = total_oi_bar_chart(derivative_df['CALLS_OI'], derivative_df['PUTS_OI'],
                             derivative_df['Strike_Price'], price_value)

    st.plotly_chart(fig, use_container_width=True)
