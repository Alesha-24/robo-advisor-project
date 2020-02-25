# Alesha Gulamhusein - OPIM 243: Robo Advisor Project  
The purpose of this document is to help you install and use the robo-adivsor-project. This project serves as an online financial advisor system which is desinged to help you make stock investment decisions. 

## Functionality 
### Information Input 
The system will first prompt you to input a stock symbol (e.g. "TSLA", "MSFT", "C", etc.). It will then prompt you to input your risk tolerance, either LOW, MEDIUM or HIGH, for investing that particular stock in order to generate a tailored reccommendation. The system will allow you to generate a reccomendation for multiple stock tickers at once - however please note that it will produce the reccomendation for each stock before prompting you to enter additional stock tickers. When you are finished entering data please type 'DONE'.

### Data Validation 
So as to ensure to provide you with the most accurate information the system also has a built-in two step data validation process which verifies that there is available for the stock ticker entered. 

### Information Output 
The program provide ouptut in three forms. 

First it will print out summary statistics of the stock along with a reccomendation as to whether or not to buy it and justification for that reccomendation. The reccomendation will be based upon two calculations; the frist will compare the latest closing price to the lowest price over the past 100 days, the second will compare the latest closing price to the average closing price over the past 52-weeks. The first calculation will vary depending on the risk level you entered for the stock, such that a greater level of risk averseness will require greater capital gains for the reccomendation to be in favour of buying the stock. 

```sh
-------------------------
SELECTED TICKER:  AAPL
-------------------------
REQUESTING STOCK MARKET DATA...
REQUEST AT:  2020 / 2 / 24    21 : 45
-------------------------
LATEST DAY:  2020-02-24
LATEST CLOSE:  $298.18
52 WEEK AVERAGE CLOSE: $232.64
100 DAY HIGH:  $327.85
52 WEEK HIGH: $327.85
100 DAY LOW:  $215.13
52 WEEK LOW: $169.50
-------------------------
RECOMMENDATION: BUY / DON'T BUY
RECOMMENDATION REASON: (REASON)
```

The second form of output will be a CSV file that has record historical stock data for the past 100 days. Each stock that you choose to analyse will have a unique CSV file that will be named with the stock ticker symbol and stored in the data folder within the project repository.

The third form of output will be a line graph that displays the trend in your chosen stock's closing price over the last 100 days. 

## Set Up
Use GitHub.com to first fork and then download or 'clone' the project repository onto your computer.  It is helpful to choose an easily accessible download location like the Desktop.  


After cloning the repository you can then use GitHub Desktop Software to access  the project repository or naivagte their using the command-line below:

```sh
 cd ~/Desktop/robo-adivsor/app
```

## Environment Set Up

Create and activate a new Anaconda virtual environment:

```sh
conda create -n shopping-env python=3.7 # (first time only)
conda activate shopping-env
```

From within this virtual environment, you can run the Python script from the command-line:

```sh
python shopping_cart.py
```
