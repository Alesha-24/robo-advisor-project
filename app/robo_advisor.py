import requests
import json 
import os 
from dotenv import load_dotenv
import csv 
import plotly
import plotly.graph_objs as go

load_dotenv()

from datetime import date
from datetime import time 
from datetime import datetime

def to_usd(my_price):
    return f"${my_price:,.2f}"

today = datetime.now()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("Hello and welcome to this Financial Planning Software")


while True: 
    symbol = input("Please enter the ticker symbol for the stock data that you want or 'DONE': ")
    if symbol == "DONE":
        print("-------------------------")
        print("THANK YOU FOR INVESTING")
        print("-------------------------")
        exit()
        
    elif symbol.isalpha() and len(symbol) <=4:
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
        print(("URL:", request_url))
        response = requests.get(request_url)
        print(response.text)
        if "Error Message" in response.text:
            print("ERROR! That is an invalid ticker!")
            exit()
      #add something in such that risk tolerance changes the reccomendation 
        else: 
            parsed_response = json.loads(response.text)
            #print(parsed_response)
            #print(parsed_response.keys())
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

            if risk == "LOW"
                float(latest_close) >= 1.2 * float(recent_low): 
                    reccomendation = "BUY"
                else:
                    reccomendation = "DON'T BUY"
            elif risk == "MEDIUM"
            elif risk == "HIGH"
            
            
            file_name = "prices_" + symbol 
            print(file_name)
            csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name + ".csv" )

            with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
                writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
                writer.writeheader() # uses fieldnames set above
                for date in dates: 
                    daily_prices = tsd[date]
                    writer.writerow({
                        "timestamp": date, 
                        "open": to_usd(float(daily_prices["1. open"])),
                        "high": to_usd(float(daily_prices["2. high"])),
                        "low": to_usd(float(daily_prices["3. low"])),
                        "close": to_usd(float(daily_prices["4. close"])),
                        "volume": daily_prices["5. volume"]
                })
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

            for date in dates:
                line_data = [
                    {"date": date, "stock_price_usd": daily_prices["4. close"],
                    }]
            x_axis = []
            y_axis = []
            for x in line_data:
                x_coord = x["date"]
                y_coord = x["stock_price_usd"]
                x_axis.append(x_coord)
                y_axis.append(y_coord)
                
            plotly.offline.plot({
                "data": [go.Scatter(x= x_axis, y=y_axis)],
                "layout": go.Layout(title="Stock Prices")
            }, auto_open=True)


            print("----------------")
            print("GENERATING LINE GRAPH...")
            print(line_data) 
            print("PROCESSING NEXT REQUEST...")

    else: 
        print("Error - expecting a properly formed stock symbol like MSFT. Please try again")

#check low and high price difference
#to do = calcualte 52 week highs and lows 
#todo = add to the read me 
#todo = print graph of stock price over time
#REFINE RECCOMENDATION based on risk level 