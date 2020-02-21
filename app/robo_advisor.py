import requests
import json 
import os 
from dotenv import load_dotenv

def to_usd(my_price):
    return f"${my_price:,.2f}"

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("REQUESTING SOME SATA FROM THE INTERNET...")
print("Hello and welcome to this Financial Planning Software")

symbol = input("Please enter the ticker symbol for the stock data that you want: ")
if symbol.isalpha() and len(symbol) <=4: 
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}"
    print(("URL:", request_url))
    response = requests.get(request_url)
    print(response.text)
    #print(response.text)
    if "Error Message" in response.text:
        print("ERROR! That is an invalid ticker, please try again")
        exit()
    risk = input("What is your risk tolerance, please enter LOW, MEDIUM or HIGH: ")
else:
    print("Error - expecting a properly formed stock symbol like MSFT. Please try again")

parsed_response = json.loads(response.text)
print(parsed_response)
print(parsed_response.keys())
last_refreshed = (parsed_response["Meta Data"]["3. Last Refreshed"])
tsd = (parsed_response["Time Series (Daily)"])
date = list(tsd.keys())
latest_day = date[0]
latest_close = tsd[latest_day]["4. close"]

print("-------------------------")
print("SELECTED SYMBOL: ",symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: ", last_refreshed)
print("LATEST CLOSE: ", to_usd(float(latest_close)))
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")