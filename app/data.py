from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def display_table():
    # Path to your CSV file
    file_path = r"C:\Users\Ev\Desktop\TRG Week 20\CryptoAnalysis.csv"
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)

    # Remove rows with any NaN values
    df_cleaned = df.dropna()

    # Reformat the 'Date' column to MM/DD/YYYY if it exists
    if 'Date' in df_cleaned.columns:
        df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], dayfirst=True)

        # Format the 'Date' column to American standard MM/DD/YYYY
        df_cleaned['Date'] = df_cleaned['Date'].dt.strftime('%m/%d/%Y')

        # Filter data to start from 04/30/2020
        start_date = pd.Timestamp('2020-04-30')
        df_cleaned = df_cleaned[df_cleaned['Date'] >= start_date.strftime('%m/%d/%Y')]

    # Convert the dataframe to an HTML table
    html_table = df_cleaned.to_html(classes='table table-striped', index=False)
    
    # HTML template with the table embedded
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crypto Analysis</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">Crypto Analysis</h1>
            {html_table}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

@app.route('/quarterly')
def quarterly_data():
    # Path to your CSV file
    file_path = r"C:\Users\Ev\Desktop\TRG Week 20\CryptoAnalysis.csv"
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)

    # Remove rows with any NaN values
    df_cleaned = df.dropna()

    # Reformat the 'Date' column to MM/DD/YYYY if it exists
    if 'Date' in df_cleaned.columns:
        df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], dayfirst=True)

        # Aggregate the data by quarter (3 months)
        df_cleaned['Quarter'] = df_cleaned['Date'].dt.to_period('Q')

        # Filter the data to show only desired months: May 2020, Aug 2020, etc.
        df_quarterly = df_cleaned[df_cleaned['Date'].dt.month.isin([5, 8, 11, 2])]
        
        # We want to show data up to March 2025
        end_date = pd.Timestamp('2025-03-31')
        df_quarterly = df_quarterly[df_quarterly['Date'] <= end_date]

        # Aggregated data by quarter, getting the average of all closing prices
        df_quarterly_agg = df_quarterly.groupby(df_quarterly['Quarter'])[[
            'btc_closing_price', 'eth_closing_price', 'usdt_closing_price', 'xrp_closing_price', 
            'bnb_closing_price', 'sol_closing_price', 'usdc_closing_price', 'doge_closing_price', 
            'ada_closing_price', 'trx_closing_price']].mean()

        # Scale down BTC closing prices by a factor (e.g., divide by 10000)
        df_quarterly_agg['btc_closing_price'] = df_quarterly_agg['btc_closing_price'] / 100

        # Plot the aggregated data
        plt.figure(figsize=(12, 8))
        
        # Plot each cryptocurrency with distinct colors and markers
        df_quarterly_agg['btc_closing_price'].plot(kind='line', marker='o', markersize=6, linewidth=2, label='BTC Closing Price', color='b')
        df_quarterly_agg['eth_closing_price'].plot(kind='line', marker='s', markersize=6, linewidth=2, label='ETH Closing Price', color='g')
        df_quarterly_agg['usdt_closing_price'].plot(kind='line', marker='^', markersize=6, linewidth=2, label='USDT Closing Price', color='r')
        df_quarterly_agg['xrp_closing_price'].plot(kind='line', marker='d', markersize=6, linewidth=2, label='XRP Closing Price', color='c')
        df_quarterly_agg['bnb_closing_price'].plot(kind='line', marker='v', markersize=6, linewidth=2, label='BNB Closing Price', color='m')
        df_quarterly_agg['sol_closing_price'].plot(kind='line', marker='p', markersize=6, linewidth=2, label='SOL Closing Price', color='y')
        df_quarterly_agg['usdc_closing_price'].plot(kind='line', marker='x', markersize=6, linewidth=2, label='USDC Closing Price', color='orange')
        df_quarterly_agg['doge_closing_price'].plot(kind='line', marker='H', markersize=6, linewidth=2, label='DOGE Closing Price', color='pink')
        df_quarterly_agg['ada_closing_price'].plot(kind='line', marker='*', markersize=6, linewidth=2, label='ADA Closing Price', color='purple')
        df_quarterly_agg['trx_closing_price'].plot(kind='line', marker='D', markersize=6, linewidth=2, label='TRX Closing Price', color='brown')
        
        plt.title('Quarterly Crypto Closing Prices (May 2020 to March 2025)')
        plt.xlabel('Quarter')
        plt.ylabel('Closing Price')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.grid(True)

        # Save plot to a BytesIO object and encode it as base64
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # HTML template with plot embedded
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quarterly Crypto Closing Prices</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">Quarterly Crypto Closing Prices (BTC, ETH, USDT, XRP, BNB, SOL, USDC, DOGE, ADA, TRX) (May 2020 to March 2025)</h1>
            <img src="data:image/png;base64,{plot_url}" alt="Quarterly Crypto Closing Prices">
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
