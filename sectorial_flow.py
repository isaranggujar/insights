import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from equity_market import equity_market_data

nse = equity_market_data.NSE()
df = nse.indices_data()
indices_to_drop = [0, 15]
df = df.drop(indices_to_drop)

# Convert relevant columns to numeric type
df['percentChange'] = pd.to_numeric(df['percentChange'])
df['advances'] = pd.to_numeric(df['advances'])
df['declines'] = pd.to_numeric(df['declines'])

# Calculate positive and negative percent changes
positive_values = df['percentChange'][df['percentChange'] >= 0].sum()
negative_values = abs(df['percentChange'][df['percentChange'] < 0].sum())

# Calculate total advances and declines
advances = df['advances'].sum()
declines = df['declines'].sum()

# Data to represent long and short positions
labels = ['Bullish', 'Bearish']
values = [positive_values, negative_values]

# Data to represent advances and declines
labels1 = ['Advances', 'Declines']
values1 = [advances, declines]

# Data to represent symbols with percentage change
index_list = df['indexSymbol'].tolist()
percent_change_list = df['percentChange'].tolist()


def sentiment_chart():
    custom_colors = ['#08bdbd', '#d36135']
    fig = plt.figure(figsize=(4, 4))
    plt.pie(values, colors=custom_colors, autopct='%1.1f%%',
            startangle=90, wedgeprops=dict(width=0.4))
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.gca().add_artist(centre_circle)
    plt.title('Sentiment Dial', y=1.1)
    plt.axis('equal')
    plt.subplots_adjust(bottom=0.4)
    return fig


def ratio_chart():
    custom_colors = ['#08bdbd', '#d36135']
    fig = plt.figure(figsize=(4, 4))
    plt.pie(values1, colors=custom_colors, autopct='%1.1f%%',
            startangle=90, wedgeprops=dict(width=0.4))
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.gca().add_artist(centre_circle)
    plt.title('A/D Ratio', y=1.1)
    plt.axis('equal')
    plt.subplots_adjust(bottom=0.4)
    return fig


def create_bar_graph():
    # Precompute color list
    color_list = ['#08bdbd' if v >= 0 else '#d36135' for v in percent_change_list]

    # Create bar chart
    fig = go.Figure(go.Bar(x=index_list, y=percent_change_list, marker_color=color_list))

    # Customize hover details
    hover_text = [f"{index}: {value}%" for index, value in zip(index_list, percent_change_list)]
    fig.update_traces(hoverinfo='text', hovertext=hover_text)

    # Update layout
    fig.update_layout(
        title=dict(text='Sectorial Flow', x=0.5),  # Centered title
        margin=dict(l=40, r=40, b=40, t=60),
        xaxis=dict(title='Indices', tickmode='array', tickvals=list(range(len(index_list))),
                   ticktext=index_list, tickangle=270, tickfont=dict(size=14, family='Arial'), fixedrange=True),
        yaxis=dict(title='% Change', fixedrange=True),
        dragmode=False,
        showlegend=False,
        height=600
    )

    # Display the bar chart in Streamlit
    return fig


def sectorial_flow():
    # Create two columns
    col1, col2 = st.columns(2)

    # Add content to the first column
    with col1:
        data = {"Category": labels,
                "Values": values
                }

        fig = sentiment_chart()
        st.pyplot(fig, use_container_width=True)
        fig = pd.DataFrame(data)
        st.write(fig)

    with col2:
        data = {"Category": labels1,
                "Values": values1
                }

        fig = ratio_chart()
        st.pyplot(fig, use_container_width=True)
        fig = pd.DataFrame(data)
        st.write(fig)

    fig = create_bar_graph()
    st.plotly_chart(fig, use_container_width=True)
