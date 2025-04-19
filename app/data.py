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
        start_date = pd.Timestamp('2020-05-01')
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

# Initialize quarterly chart
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

        # Aggregated data by quarter, getting the average of 'btc_closing_price'
        df_quarterly_agg = df_quarterly.groupby(df_quarterly['Date'].dt.to_period('Q'))['btc_closing_price'].mean()

        # Plot the aggregated data
        plt.figure(figsize=(10, 6))
        df_quarterly_agg.plot(kind='line', marker='o', markersize=6, linewidth=2)
        plt.title('BTC Closing Price per Quarter')
        plt.xlabel('Quarter')
        plt.ylabel('BTC Closing Price')
        plt.grid(True)

        # Save plot to a BytesIO object and encode it as base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # HTML template with plot embedded
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quarterly BTC Closing Prices</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">Quarterly BTC Closing Prices (May 2020 to March 2025)</h1>
            <img src="data:image/png;base64,{plot_url}" alt="Quarterly BTC Closing Price">
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
