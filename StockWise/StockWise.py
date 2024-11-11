import streamlit as st  # streamlit library
import pandas as pd  # pandas library
import yfinance as yf  # yfinance library
import datetime  # datetime library
from datetime import date
from plotly import graph_objs as go  # plotly library
from plotly.subplots import make_subplots
from prophet import Prophet  # prophet library
from prophet.plot import plot_plotly
import time  # time library
from streamlit_option_menu import option_menu  # select_options library
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="StockWise", layout="wide", initial_sidebar_state="expanded")

def add_meta_tag():
    meta_tag = """
        <head>
            <meta name="google-site-verification" content="QBiAoAo1GAkCBe1QoWq-dQ1RjtPHeFPyzkqJqsrqW-s" />
        </head>
    """
    st.markdown(meta_tag, unsafe_allow_html=True)

# Main code
add_meta_tag()

# Sidebar Section Starts Here
today = date.today()  # today's date
st.write('''# StockWise ''')  # title
st.sidebar.image("Images/StockWiseLogo1.png", width=250, use_column_width=False)  # logo
st.sidebar.write('''# StockWise ''')

with st.sidebar: 
    selected = option_menu("Utilities", ["Stocks Performance Comparison", "Real-Time Stock Price", "Stock Prediction", 'About'])

start = st.sidebar.date_input('Start', datetime.date(2022, 1, 1))  # start date input
end = st.sidebar.date_input('End', datetime.date.today())  # end date input
# Sidebar Section Ends Here

# Read CSV file
stock_df = pd.read_csv("StockWiseTickersData.csv")

# Stock Performance Comparison Section Starts Here
if selected == 'Stocks Performance Comparison':  # if user selects 'Stocks Performance Comparison'
    st.subheader("Stocks Performance Comparison")
    tickers = stock_df["Company Name"]
    # Dropdown for selecting assets
    dropdown = st.multiselect('Pick your assets', tickers)

    with st.spinner('Loading...'):  # Spinner while loading
        time.sleep(2)

    dict_csv = pd.read_csv('StockWiseTickersData.csv', header=None, index_col=0).to_dict()[1]  # Read CSV file
    symb_list = []  # List for storing symbols
    for i in dropdown:  # For each asset selected
        val = dict_csv.get(i)  # Get symbol from CSV file
        symb_list.append(val)  # Append symbol to list

    def relativeret(df):  # Function for calculating relative return
        rel = df.pct_change()  # Calculate relative return
        cumret = (1 + rel).cumprod() - 1  # Calculate cumulative return
        cumret = cumret.fillna(0)  # Fill NaN values with 0
        return cumret  # Return cumulative return

    if len(dropdown) > 0:  # If user selects at least one asset
        df = relativeret(yf.download(symb_list, start, end))['Adj Close']  # Download data from yfinance
        raw_df = relativeret(yf.download(symb_list, start, end))
        raw_df.reset_index(inplace=True)  # Reset index

        closingPrice = yf.download(symb_list, start, end)['Adj Close']  # Download data from yfinance
        volume = yf.download(symb_list, start, end)['Volume']
        
        st.subheader('Raw Data {}'.format(dropdown))
        st.write(raw_df)  # Display raw data
        chart = ('Line Chart', 'Area Chart', 'Bar Chart')  # Chart types
        # Dropdown for selecting chart type
        dropdown1 = st.selectbox('Pick your chart', chart)
        with st.spinner('Loading...'):  # Spinner while loading
            time.sleep(2)

        st.subheader('Relative Returns {}'.format(dropdown))
                
        if dropdown1 == 'Line Chart':  # If user selects 'Line Chart'
            st.line_chart(df)  # Display line chart
            # Display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)  # Display line chart

            # Display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)  # Display line chart

        elif dropdown1 == 'Area Chart':  # If user selects 'Area Chart'
            st.area_chart(df)  # Display area chart
            # Display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.area_chart(closingPrice)  # Display area chart

            # Display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.area_chart(volume)  # Display area chart

        elif dropdown1 == 'Bar Chart':  # If user selects 'Bar Chart'
            st.bar_chart(df)  # Display bar chart
            # Display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.bar_chart(closingPrice)  # Display bar chart

            # Display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.bar_chart(volume)  # Display bar chart

        else:
            st.line_chart(df, width=1000, height=800, use_container_width=False)  # Display line chart
            # Display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)  # Display line chart

            # Display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)  # Display line chart

    else:  # If user doesn't select any asset
        st.write('Please select at least one asset')  # Display message
# Stock Performance Comparison Section Ends Here
    
# Real-Time Stock Price Section Starts Here
elif selected == 'Real-Time Stock Price':  # If user selects 'Real-Time Stock Price'
    st.subheader("Real-Time Stock Price")
    tickers = stock_df["Company Name"]  # Get company names from CSV file
    # Dropdown for selecting company
    a = st.selectbox('Pick a Company', tickers)

    with st.spinner('Loading...'):  # Spinner while loading
        time.sleep(2)

    dict_csv = pd.read_csv('StockWiseTickersData.csv', header=None, index_col=0).to_dict()[1]  # Read CSV file
    symb_list = []  # List for storing symbols

    val = dict_csv.get(a)  # Get symbol from CSV file
    symb_list.append(val)  # Append symbol to list

    if "button_clicked" not in st.session_state:  # If button is not clicked
        st.session_state.button_clicked = False  # Set button clicked to false

    def callback():  # Function for updating data
        st.session_state.button_clicked = True  # Set button clicked to true
        
    if st.button("Search", on_click=callback) or st.session_state.button_clicked:  # Button for searching data
        if a == "":  # If user doesn't select any company
            st.write("Click Search to Search for a Company")
            with st.spinner('Loading...'):  # Spinner while loading
                time.sleep(2)
        else:  # If user selects a company
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)  # Reset index
            st.subheader('Raw Data of {}'.format(a))  # Display raw data
            st.write(data)  # Display data

            def plot_raw_data():  # Function for plotting raw data
                fig = go.Figure()  # Create figure
                fig.add_trace(go.Scatter(  # Add scatter plot
                    x=data['Date'], y=data['Open'], name="stock_open"))  # X-axis: date, Y-axis: open
                fig.add_trace(go.Scatter(  # Add scatter plot
                    x=data['Date'], y=data['Close'], name="stock_close"))  # X-axis: date, Y-axis: close
                fig.layout.update(  # Update layout
                    title_text='Line Chart of {}'.format(a), xaxis_rangeslider_visible=True)  # Title, X-axis: rangeslider
                st.plotly_chart(fig)  # Display plotly chart

            def plot_candle_data():  # Function for plotting candle data
                fig = go.Figure()  # Create figure
                fig.add_trace(go.Candlestick(x=data['Date'],  # Add candlestick plot
                                             open=data['Open'],
                                             high=data['High'],  # Y-axis: high
                                             low=data['Low'],  # Y-axis: low
                                             close=data['Close'], name='market data'))  # Y-axis: close
                fig.update_layout(  # Update layout
                    title='Candlestick Chart of {}'.format(a),  # Title
                    yaxis_title='Stock Price',  # Y-axis: title
                    xaxis_title='Date')  # X-axis: title
                st.plotly_chart(fig)  # Display plotly chart

            chart = ('Candle Stick', 'Line Chart')  # Chart types
            # Dropdown for selecting chart type
            dropdown1 = st.selectbox('Pick a chart type', chart)

            with st.spinner('Loading...'):  # Spinner while loading
                time.sleep(2)

            if dropdown1 == 'Candle Stick':  # If user selects 'Candle Stick'
                plot_candle_data()  # Plot candle data
            else:  # If user selects 'Line Chart'
                plot_raw_data()  # Plot raw data

            # Display closing price of selected asset
            st.write("### Closing Price of {}".format(a))
            st.line_chart(data['Close'])  # Display line chart
    else:  # If button is not clicked
        st.write("Click the Search button to get the stock data")  # Display message
# Real-Time Stock Price Section Ends Here

# Stock Prediction Section Starts Here
elif selected == 'Stock Prediction':  # If user selects 'Stock Prediction'
    st.subheader("Stock Prediction")

    tickers = stock_df["Company Name"]  # Get company names from CSV file
    a = st.selectbox('Pick a Company', tickers)

    with st.spinner('Loading...'):  # Spinner while loading
        time.sleep(2)

    dict_csv = pd.read_csv('StockWiseTickersData.csv', header=None, index_col=0).to_dict()[1]  # Read CSV file
    symb_list = []  # List for storing symbols
    val = dict_csv.get(a)  # Get symbol from CSV file
    symb_list.append(val)  # Append symbol to list

    if a == "":  # If user doesn't select any company
        st.write("Enter a Stock Name")  # Display message
    else:  # If user selects a company
        data = yf.download(symb_list, start=start, end=end)
        data.reset_index(inplace=True)  # Reset index
        st.subheader('Raw Data of {}'.format(a))  # Display raw data
        st.write(data)  # Display data

        def plot_raw_data():  # Function for plotting raw data
            fig = go.Figure()  # Create figure
            fig.add_trace(go.Scatter(  # Add scatter plot
                x=data['Date'], y=data['Open'], name="stock_open"))  # X-axis: date, Y-axis: open
            fig.add_trace(go.Scatter(  # Add scatter plot
                x=data['Date'], y=data['Close'], name="stock_close"))  # X-axis: date, Y-axis: close
            fig.layout.update(  # Update layout
                title_text='Time Series Data of {}'.format(a), xaxis_rangeslider_visible=True)  # Title, X-axis: rangeslider
            st.plotly_chart(fig)  # Display plotly chart

        plot_raw_data()  # Plot raw data
        n_years = st.slider('Years of prediction:', 1, 4)  # Slider for selecting years of prediction
        period = n_years * 365  # Calculate number of days

        # Predict forecast with Prophet
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})  # Rename columns

        m = Prophet()  # Create object for Prophet
        m.fit(df_train)  # Fit data to Prophet
        future = m.make_future_dataframe(periods=period)  # Create future dataframe
        forecast = m.predict(future)  # Predict future dataframe

        # Show and plot forecast
        st.subheader('Forecast Data of {}'.format(a))  # Display forecast data
        st.write(forecast)  # Display forecast data

        st.subheader(f'Forecast plot for {n_years} years')  # Display message
        fig1 = plot_plotly(m, forecast)  # Plot forecast
        st.plotly_chart(fig1)  # Display plotly chart

        st.subheader("Forecast components of {}".format(a))  # Display message
        fig2 = m.plot_components(forecast)  # Plot forecast components
        st.write(fig2)  # Display plotly chart

        # Calculate and display accuracy metrics
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]  # Filter forecast data
        forecast = forecast[forecast['ds'].isin(data['Date'])]  # Include only actual dates

        # Merge actual data with forecasted data
        merged_data = pd.merge(data[['Date', 'Close']], forecast, left_on='Date', right_on='ds', how='inner')

        # Calculate accuracy metrics
        mae = mean_absolute_error(merged_data['Close'], merged_data['yhat'])
        mse = mean_squared_error(merged_data['Close'], merged_data['yhat'])
        rmse = mse ** 0.5

        st.subheader('Accuracy Metrics')
        st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
        st.write(f"Mean Squared Error (MSE): {mse:.2f}")
        st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
# Stock Prediction Section Ends Here

# About Section Starts Here
elif selected == 'About':  # If user selects 'About'
    st.subheader("About StockWise")
    st.write("StockWise is a comprehensive tool for analyzing and predicting stock prices.")
    st.write("Developed using Streamlit, Prophet, and various other libraries, StockWise provides insights into stock performance, real-time data, and future predictions.")
    st.write("For more information or inquiries, please contact support@stockwise.com")
# About Section Ends Here
