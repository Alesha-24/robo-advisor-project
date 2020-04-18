import pytest 
import os 
from app.robo_advisor import get_response1, get_response2, calculate_recent_high, calculate_recent_low, write_to_csv, risk_calc, recc_reason, to_usd 

CI_ENV = os.environ.get("CI") == "true" # expect default environment variable setting of "CI=true" on Travis CI, see: https://docs.travis-ci.com/user/environment-variables/#default-environment-variables
@pytest.mark.skipif(CI_ENV==True, reason="to avoid configuring credentials on, and issuing requests from, the CI server")

def test_get_response1():
    symbol = "TSLA"
    _, parsed_response = get_response1(symbol)
    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol

def test_get_response2():
    symbol = "TSLA"
    parsed_response_2 = get_response2(symbol)
    assert isinstance(parsed_response_2, dict)
    assert "Meta Data" in parsed_response_2.keys()
    #assert "Weekly Adjusted Prices and Volumes" in parsed_response_2
    assert parsed_response_2["Meta Data"]["2. Symbol"] == symbol

def test_calculate_recent_high():
    tsd = {'2020-04-17': {'1. open': '179.5000', '2. high': '180.0000', '3. low': '175.8700', '4. close': '178.6000', '5. volume': '52273542'},
           '2020-04-16': {'1. open': '174.3000', '2. high': '177.2800', '3. low': '172.9000', '4. close': '177.0400', '5. volume': '50479610'}, 
           '2020-04-15': {'1. open': '171.2000', '2. high': '173.5700', '3. low': '169.2400', '4. close': '171.8800', '5. volume': '40940833'}, 
           '2020-04-14': {'1. open': '169.0000', '2. high': '173.7500', '3. low': '168.0000', '4. close': '173.7000', '5. volume': '52874338'}, 
           '2020-04-13': {'1. open': '164.3500', '2. high': '165.5700', '3. low': '162.3000', '4. close': '165.5100', '5. volume': '41905264'}, 
           '2020-04-09': {'1. open': '166.3600', '2. high': '167.3700', '3. low': '163.3300', '4. close': '165.1400', '5. volume': '51431775'}
           }
    dates = list(tsd.keys())
    assert calculate_recent_high(tsd,dates) == "180.0000"

def test_calculate_recent_low():
    tsd = {'2020-04-17': {'1. open': '179.5000', '2. high': '180.0000', '3. low': '175.8700', '4. close': '178.6000', '5. volume': '52273542'},
           '2020-04-16': {'1. open': '174.3000', '2. high': '177.2800', '3. low': '172.9000', '4. close': '177.0400', '5. volume': '50479610'}, 
           '2020-04-15': {'1. open': '171.2000', '2. high': '173.5700', '3. low': '169.2400', '4. close': '171.8800', '5. volume': '40940833'}, 
           '2020-04-14': {'1. open': '169.0000', '2. high': '173.7500', '3. low': '168.0000', '4. close': '173.7000', '5. volume': '52874338'}, 
           '2020-04-13': {'1. open': '164.3500', '2. high': '165.5700', '3. low': '162.3000', '4. close': '165.5100', '5. volume': '41905264'}, 
           '2020-04-09': {'1. open': '166.3600', '2. high': '167.3700', '3. low': '163.3300', '4. close': '165.1400', '5. volume': '51431775'}
           }
    dates = list(tsd.keys())
    assert calculate_recent_low(tsd,dates) == "162.3000"

# def test_write_to_csv():
#     csv_filepath = os.path.join(os.path.dirname(__file__), "example_reports", "temp_prices.csv")
#     tsd = {'2020-04-17': {'1. open': '179.5000', '2. high': '180.0000', '3. low': '175.8700', '4. close': '178.6000', '5. volume': '52273542'},
#            '2020-04-16': {'1. open': '174.3000', '2. high': '177.2800', '3. low': '172.9000', '4. close': '177.0400', '5. volume': '50479610'}, 
#            '2020-04-15': {'1. open': '171.2000', '2. high': '173.5700', '3. low': '169.2400', '4. close': '171.8800', '5. volume': '40940833'}, 
#            '2020-04-14': {'1. open': '169.0000', '2. high': '173.7500', '3. low': '168.0000', '4. close': '173.7000', '5. volume': '52874338'}, 
#            '2020-04-13': {'1. open': '164.3500', '2. high': '165.5700', '3. low': '162.3000', '4. close': '165.5100', '5. volume': '41905264'}, 
#            '2020-04-09': {'1. open': '166.3600', '2. high': '167.3700', '3. low': '163.3300', '4. close': '165.1400', '5. volume': '51431775'}
#            }
#     dates = ['2020-04-17', '2020-04-16', '2020-04-15', '2020-04-14', '2020-04-13', '2020-04-09', '2020-04-08', '2020-04-07']
#     if os.path.isfile(csv_filepath):
#         os.remove(csv_filepath)
#     assert os.path.isfile(csv_filepath) == False # just making sure the test was setup properly
#     result = write_to_csv(tsd, csv_filepath, dates)
#     # EXPECTATIONS
#     assert result == True
#     assert os.path.isfile(csv_filepath) == True

def test_risk_calc():
    #ensuring that the function is calculating risk level appropriately
    latest_close = 22
    recent_low = 18
    avg_52_week = 20
    risk = "LOW"
    assert risk_calc(recent_low, latest_close, avg_52_week, risk) == "BUY"
    risk = "MEDIUM"
    assert risk_calc(recent_low, latest_close, avg_52_week, risk) == "BUY"
    risk = "HIGH"
    assert risk_calc(recent_low, latest_close, avg_52_week, risk) == "BUY"

    latest_close = 19
    recent_low = 18
    avg_52_week = 20
    risk = "LOW"
    assert risk_calc(recent_low, latest_close, avg_52_week, risk) == "DON'T BUY"
    risk = "MEDIUM"
    assert risk_calc(recent_low, latest_close, avg_52_week, risk) == "DON'T BUY"
    risk = "HIGH"
    assert risk_calc(recent_low, latest_close, avg_52_week, risk) == "DON'T BUY"

def test_recc_reason():
    risk = "LOW" 
    recc = "BUY"
    assert recc_reason(risk, recc) == "The stock's latest close price was 1.20 times higher than the lowest price in the past 100 days. Also, the latest close price was greater than the average close price over the past 52 weeks. Therefore, this stock seems profitable and our reccommendation is to buy it."
    risk = "MEDIUM" 
    recc = "BUY"
    assert recc_reason(risk, recc) == "The stock's latest close price was 1.12 times higher than the lowest price in the past 100 days. Also, the latest close price was greater than the average close price over the past 52 weeks. Therefore, this stock seems profitable and our reccomemndation is to buy it." 
    risk = "HIGH" 
    recc = "BUY"
    assert recc_reason(risk, recc) == "The stock's latest close price was 1.07 times higher than the lowest price in the past 100 days. Also, the latest close price was greater than the average close price over the past 52 weeks. Therefore, this stock seems profitable and our reccommendation is to buy it."
    recc = "DON'T BUY"
    assert recc_reason(risk, recc) == "This stock has not shown signfnicant growth potential and the market seems to be quite volatile. Therefore, we advise not to buy this stock at this time."
 
def test_to_usd(): 
    # it should apply USD formatting
    assert to_usd(2.40) == "$2.40"

    # it should display two decimal places
    assert to_usd(2.4) == "$2.40"

    # it should round to two places
    assert to_usd(2.4000003) == "$2.40"

    # it should display thousands separators
    assert to_usd(1234567890.5555555) == "$1,234,567,890.56"