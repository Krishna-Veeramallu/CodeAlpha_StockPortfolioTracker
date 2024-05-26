import urllib.request
import json

# Set up Alpha Vantage API
API_KEY = 'your_alpha_vantage_api_key'
BASE_URL = 'https://www.alphavantage.co/query'

# Portfolio dictionary to store stock data
portfolio = {}

def get_stock_data(symbol):
    url = f"{BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}"
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
        data_json = json.loads(data)
        if 'Time Series (1min)' in data_json:
            return data_json['Time Series (1min)']
        else:
            print(f"Error retrieving data for {symbol}")
            return None

def add_stock(symbol, quantity):
    data = get_stock_data(symbol)
    if data:
        portfolio[symbol] = {
            'quantity': quantity,
            'data': data
        }
        print(f"Added {quantity} shares of {symbol} to the portfolio.")
    else:
        print(f"Failed to add {symbol} to the portfolio.")

def remove_stock(symbol):
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Removed {symbol} from the portfolio.")
    else:
        print(f"{symbol} is not in the portfolio.")

def track_portfolio():
    for symbol, info in portfolio.items():
        latest_price = float(next(iter(info['data'].values()))['1. open'])
        total_value = latest_price * info['quantity']
        print(f"{symbol}: {info['quantity']} shares at ${latest_price:.2f} each. Total value: ${total_value:.2f}")

def main():
    while True:
        print("\nPortfolio Management")
        print("1. Add stock")
        print("2. Remove stock")
        print("3. Track portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            quantity = int(input("Enter quantity: "))
            add_stock(symbol, quantity)
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ").upper()
            remove_stock(symbol)
        elif choice == '3':
            track_portfolio()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()