import requests

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()
high, low, close = [], [], []

# extracting data to lists
for i in data['Time Series (5min)']:
    high.append(float(data['Time Series (5min)'][i]['2. high']))
    low.append(float(data['Time Series (5min)'][i]['3. low']))
    close.append(float(data['Time Series (5min)'][i]['4. close']))


# reversing the lists
high = high[::-1]
low = low[::-1]
close = close[::-1]

atr_peroid = 7
multiplier = 3
length = len(high)

# basic upper and lower bands
basic_upper_band, basic_lower_band = length*[0], length*[0]

for i in range(length):
    basic_upper_band[i] = (high[i])+(low[i])/2 + atr_peroid*multiplier
    basic_lower_band[i] = (high[i])+(low[i])/2 - atr_peroid*multiplier


# Final Upper Band
final_upper_band, final_lower_band = length*[0], length*[0]
for i in range(length):
    if i == 0:
        final_upper_band[i] = 0
    else:
        if (basic_upper_band[i] < final_upper_band[i - 1]) or (close[i - 1] > final_upper_band[i - 1]):
            final_upper_band[i] = basic_upper_band[i]
        else:
            final_upper_band[i] = final_upper_band[i - 1]


# final lower band
for i in range(length):
    if i == 0:
        final_lower_band[i] = 0
    else:
        if (basic_lower_band[i] > final_lower_band[i - 1]) or (close[i - 1] < final_lower_band[i - 1]):
            final_lower_band[i] = basic_lower_band[i]

        else:
            final_lower_band[i] = final_lower_band[i - 1]


# SuperTrend
supertrend = length * [0]

for i in range(length):

    if i == 0:
        supertrend[i] = 0

    elif (supertrend[i - 1] == final_upper_band[i - 1]) and (close[i] <= final_upper_band[i]):
        supertrend[i] = final_upper_band[i]

    elif (supertrend[i - 1] == final_upper_band[i - 1]) and (close[i] > final_upper_band[i]):
        supertrend[i] = final_lower_band[i]

    elif (supertrend[i - 1] == final_lower_band[i - 1]) and (close[i] >= final_lower_band[i]):
        supertrend[i] = final_lower_band[i]

    elif (supertrend[i - 1] == final_lower_band[i - 1]) and (close[i] < final_upper_band[i]):
        supertrend[i] = final_upper_band[i]


print(supertrend)
