# TRG Week 20

## Analysis of the Top Ten Cryptocurrencies

- Link To Dataset : https://www.kaggle.com/datasets/albertobircoci/top10-cryptocurrencies-03-2025

### 1st Commit

- Initiated data.py and associated files to load the HTML dataframe for cleaning.

### 2nd Commit

- Dropped all rows containing NaN values to show clear comparison between crytocurrencies.

- Formatted the Date values to align with the American standard.

### 3rd Commit

- The first row of value is dated 04/10/2020. The last row is dated 03/31/2025.

- Adjust code so the first row is dated 05/01/2020.

- Show aggregated data of the "btc_closing_price" per month, every 3 months. Show May 2020 data, August 2020, and so on. Make sure we show the last month, March 2025. Place the pricing on the y axis and the monthly tickers on the x axis.

- Shown on /quarterly route.

### 4th Commit

- Add "eth_closing_price" and "usdt_closing_price" columns as separately colored lines in the same route and plot.

### 5th Commit

- Add "xrp_closing_price" "bnb_closing_price" "sol_closing_price" "usdc_closing_price" "doge_closing_price" "ada_closing_price" "trx_closing_price" columns as separately colored lines on the same route and plot.

- Scaled "btc_closing_price" down by 100 to show better variance amongst the ten cryptocurrencies.