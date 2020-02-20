import requests
import json 
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("REQUESTING SOME SATA FROM THE INTERNET...")
print("Hello and welcome to this Financial Planning Software")

symbol = input("Please enter the ticker symbol for the stock data that you want: ")
if symbol.isalpha() and len(symbol) <=4: 
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    print(("URL:", request_url))
    response = requests.get(request_url)
    #print(response.text)
    if "Error Message" in response.text:
        print("ERROR! That is an invalid ticker, please try again")
        exit()
    print(response.status_code)
    risk = input("What is your risk tolerance, please enter LOW, MEDIUM or HIGH: ")
else:
    print("Error - expecting a properly formed stock symbol like MSFT. Please try again")

parsed_response = json.loads(response.text)
print(parsed_response)


print("-------------------------")
print("SELECTED SYMBOL: ",symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")