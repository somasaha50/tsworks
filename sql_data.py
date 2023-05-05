import yfinance as yf
import pandas as pd
import configparser
import sqlite3


# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

conn = sqlite3.connect('financial_data.db')

# Loop through the companies in the configuration file
for company in config.sections():
    ticker = config[company]['ticker']
    period = config[company]['period']

    # Download the financial data
    data = yf.download(ticker, period=period)
    data['company'] = company
    data = data.reset_index().rename(columns={'Date': 'date'})
    data = data[['company', 'date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    # Create a table for the company in the database
    table_name = f'{company}_data'
    data.to_sql(table_name, conn, if_exists='replace', index=False)

    print(f'Downloaded {len(data)} rows for {ticker} and saved to database')

    # Save the data to a CSV file
    filename = f'{ticker}.csv'
    data.to_csv(filename)

    print(f'Downloaded {len(data)} rows for {ticker} and saved to {filename}')


# Close the database connection
conn.close()


