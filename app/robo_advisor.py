import requests
import json 
import os 
from dotenv import load_dotenv
import csv 

load_dotenv()

from datetime import date
from datetime import time 
from datetime import datetime

def to_usd(my_price):
    return f"${my_price:,.2f}"

today = datetime.now()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("REQUESTING SOME SATA FROM THE INTERNET...")
print("Hello and welcome to this Financial Planning Software")


while True: 
    symbol = input("Please enter the ticker symbol for the stock data that you want or 'DONE': ")
    if symbol == "DONE":
        print("-------------------------")
        print("THANK YOU FOR INVESTING")
        print("-------------------------")
        
        
    elif symbol.isalpha() and len(symbol) <=4:
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
        print(("URL:", request_url))
        response = requests.get(request_url)
        print(response.text)
        if "Error Message" in response.text:
            print("ERROR! That is an invalid ticker, please try again")
            exit()
      #add something in such that risk tolerance changes the reccomendation 
        else: 
            parsed_response = json.loads(response.text)
            print(parsed_response)
            print(parsed_response.keys())
            last_refreshed = (parsed_response["Meta Data"]["3. Last Refreshed"])
            tsd = (parsed_response["Time Series (Daily)"])
            dates = list(tsd.keys())
            latest_day = dates[0]
            latest_close = tsd[latest_day]["4. close"]

            high_prices = []
            low_prices = []
            
            for  date in dates:
                    high_price = tsd[date]["2. high"]
                    low_price = tsd[date]["3. low"]
                    high_prices.append(high_price)
                    low_prices.append(low_price)
            recent_high = max(high_prices)
            recent_low = max(low_prices)
            
            risk = input("What is your risk tolerance, please enter LOW, MEDIUM or HIGH: ")
            
            if float(latest_close) >= 1.2 * float(recent_low): 
                reccomendation = "BUY"
            else:
                reccomendation = "DON'T BUY"
            
            #add something else in 
            print("-------------------------")
            print("SELECTED SYMBOL: ",symbol)
            print("-------------------------")
            print("REQUESTING STOCK MARKET DATA...")
            print("REQUEST AT: ", today.year, "/", today.month, "/", today.day, "  ", today.hour, ":", today.minute)
            print("-------------------------")
            print("LATEST DAY: ", last_refreshed)
            print("LATEST CLOSE: ", to_usd(float(latest_close)))
            print("RECENT HIGH: ", to_usd(float(recent_high)))
            #recent high = highest price over last 100 days of trading data 
            print("RECENT LOW: ", to_usd(float(recent_low)))
            print("-------------------------")
            print("RECOMMENDATION:", reccomendation, "!")
            print("RECOMMENDATION REASON: TODO")
            print("-------------------------")
            #need to write data to CSV file 
            print("WRITING DATA TO") #csv_file_path)
            print("-------------------------")
            print("PROCESSING NEXT REQUEST...")

    else: 
        print("Error - expecting a properly formed stock symbol like MSFT. Please try again")


#check low and high price difference
#to do = calcualte 52 week highs and lows s

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=["city", "name"])
    writer.writeheader() # uses fieldnames set above
    writer.writerow({"city": "New York", "name": "Yankees"})
    writer.writerow({"city": "New York", "name": "Mets"})
    writer.writerow({"city": "Boston", "name": "Red Sox"})
    writer.writerow({"city": "New Haven", "name": "Ravens"})

#way ton incorporate multiple stock into analysis 


#todo = print grapph of stock price over time