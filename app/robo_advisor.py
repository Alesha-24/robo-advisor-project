import requests
import json 
import os 
from dotenv import load_dotenv
import csv 
import plotly
import plotly.graph_objs as go
import statistics

load_dotenv()

from datetime import date
from datetime import time 
from datetime import datetime

def get_response1(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
    response = requests.get(request_url)
    return response

def get_response2(symbol):
    request_52 = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
    response_52 = requests.get(request_52)
    return response_52

def calculate_recent_high(tsd):
    high_prices = []
    for  date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(high_price)
    recent_high = max(high_prices)
    return recent_high

def calculate_recent_low(tsd):
    low_prices = []
    for  date in dates:
        low_price = tsd[date]["3. low"]
        low_prices.append(low_price)
    recent_low = min(low_prices)
    return recent_low

def write_to_csv(csv_file_path):
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for date in dates: 
            daily_prices = tsd[date]
            writer.writerow({
                "timestamp": date, 
                "open": to_usd(float(daily_prices["1. open"])),
                "high": to_usd(float(daily_prices["2. high"])),
                "low": to_usd(float(daily_prices["3. low"])),
                "close": to_usd(float(daily_prices["4. close"])),
                "volume": daily_prices["5. volume"]})
    return True 

def risk_calc(risk):
    if risk == "LOW" and float(latest_close) >= 1.2 * float(recent_low) and float(latest_close) > avg_52_week :
        recc = "BUY"
    elif risk == "MEDIUM" and float(latest_close) >= 1.12 * float(recent_low) and float(latest_close) > avg_52_week :
        recc = "BUY"
    elif risk == "HIGH" and  float(latest_close) >= 1.07 * float(recent_low) and float(latest_close) > avg_52_week :
        recc = "BUY"
    else:
        recc = "DON'T BUY"
    return recc     

def recc_reason(risk, recc):
    if risk == "LOW" and recc == "BUY": 
        reccomendation_reason = "The stock's latest close price was 1.20 times higher than the lowest price in the past 100 days. Also, the latest close price was greater than the average close price over the past 52 weeks. Therefore, this stock seems profitable and our reccommendation is to buy it."
    elif risk == "MEDIUM" and recc == "BUY": 
        reccomendation_reason = "The stock's latest close price was 1.12 times higher than the lowest price in the past 100 days. Also, the latest close price was greater than the average close price over the past 52 weeks. Therefore, this stock seems profitable and our reccomemndation is to buy it." 
    elif risk == "HIGH" and  recc == "BUY": 
        reccomendation_reason = "The stock's latest close price was 1.07 times higher than the lowest price in the past 100 days. Also, the latest close price was greater than the average close price over the past 52 weeks. Therefore, this stock seems profitable and our reccommendation is to buy it."
    else:
        reccomendation_reason = "This stock has not shown signfnicant growth potential and the market seems to be quite volatile. Therefore, we advise not to buy this stock at this time."
    return reccomendation_reason    

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}"
 
if __name__ == "__main__":

    today = datetime.now()

    API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

    print("-------------------------")
    print("HELLO AND WELCOME TO THIS STOCK ANALYSIS AND INVESTMENT RECCOMENDATION PROGRAM")
    print("-------------------------")

    while True: 
        symbol = input("Please enter the ticker symbol for the stock data that you want, or if you have finished please type 'DONE': ")
        if symbol == "DONE":
            print("-------------------------")
            print("THANK YOU FOR INVESTING")
            print("-------------------------")
            exit()
            
        elif symbol.isalpha() and len(symbol) <=4:
            response = get_response1(symbol)
            if "Error Message" in response.text:
                print("ERROR! That is an invalid ticker!")
                exit()
            else: 
                parsed_response = json.loads(response.text)
                last_refreshed = (parsed_response["Meta Data"]["3. Last Refreshed"])
                tsd = (parsed_response["Time Series (Daily)"])
                dates = list(tsd.keys())
                latest_day = dates[0]
                latest_close = tsd[latest_day]["4. close"]
                
                response_52 = get_response2(symbol)
                parsed_response_52 = json.loads(response_52.text)
                tsw = (parsed_response_52["Weekly Adjusted Time Series"])
                weeks = list(tsw.keys())
                
                recent_high = calculate_recent_high(tsd)
                recent_low = calculate_recent_low(tsd)
                
                close_prices = []
                highs_52 = []
                lows_52 = []
                for week in weeks:
                    if len(close_prices) < 52 :
                        close = float(tsw[week]["5. adjusted close"])
                        high = tsw[week]["2. high"]
                        low = tsw[week]["3. low"]
                        close_prices.append(close)
                        highs_52.append(high)
                        lows_52.append(low)
            
                high_52_week = max(highs_52)
                low_52_week = min(lows_52)
                avg_52_week = statistics.mean(close_prices)
                
                risk = input("What is your risk tolerance for this stock, please enter LOW, MEDIUM or HIGH: ")
                recc = risk_calc(risk)
                reccomendation_reason = recc_reason(risk, recc)
    
                file_name = "prices_" + symbol 
                csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name + ".csv" )
                write_to_csv(csv_file_path)
                
                formatted_time = datetime.now().strftime("%m/%d/%Y, %r")

                print("-------------------------")
                print("SELECTED TICKER: ",symbol)
                print("-------------------------")
                print("REQUESTING STOCK MARKET DATA...")
                print("REQUEST AT: ", formatted_time)
                print("-------------------------")
                print("LATEST DAY: ", last_refreshed)
                print("LATEST CLOSE: ", to_usd(float(latest_close)))
                print("52 WEEK AVERAGE CLOSE:", to_usd(float(avg_52_week)))
                print("100 DAY HIGH: ", to_usd(float(recent_high)))
                print("52 WEEK HIGH:", to_usd(float(high_52_week)))
                print("100 DAY LOW: ", to_usd(float(recent_low)))
                print("52 WEEK LOW:", to_usd(float(low_52_week)))
                print("-------------------------")
                print("RECOMMENDATION:", recc, "!")
                print("RECOMMENDATION REASON: ", reccomendation_reason)
                print("-------------------------")
                print("WRITING DATA TO", csv_file_path)
                print("-------------------------")
                x =[]
                y = []
                for date in dates:
                    x.append(date)
                    y.append(tsd[date]["4. close"])
                
                plot_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{symbol.upper()}_chart.html")
                plotly.offline.plot({
                    "data": [go.Scatter(x=x, y=y)],
                    "layout": go.Layout(title=f"Daily Close Price of {symbol.upper()} Stock", yaxis_title = "Price ($)", xaxis_title = "Date")
                    }, filename=plot_file_path, auto_open=True)
                
                print("GENERATING LINE GRAPH...")
                print("-------------------------")
                print("READY TO PROCESS NEXT REQUEST")
            
        else: 
            print("Error - expecting a properly formed stock symbol like MSFT. Please try again")





        