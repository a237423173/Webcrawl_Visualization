import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

url = "https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID=2330"
headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
res = requests.get(url, headers= headers)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "lxml")
data = soup.select_one("#txtFinDetailData")

dfs = pd.read_html(data.prettify())
df = dfs[0]

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        False

list_close = [float(df["年度股價(元)"]["收盤"][i]) for i in range(len(df["年度股價(元)"]["收盤"])) if isfloat(df["年度股價(元)"]["收盤"][i])]
list_year = [int(df["年度"]["年度"][i]) for i in range(len(df["年度"]["年度"])) if isint(df["年度"]["年度"][i])]
list_eps = [float(df["EPS(元)"]["稅後  EPS"][i]) for i in range(len(df["EPS(元)"]["稅後  EPS"])) if isfloat(df["EPS(元)"]["稅後  EPS"][i])]

data_input = pd.DataFrame({"year":list_year[0:30], "close_price":list_close[0:30], "eps":list_eps[0:30]})
data_input = data_input.reset_index(drop=True)
data_input.index = data_input.year

fig, ax1 = plt.subplots()
plt.title('TW2330')
plt.xlabel('Year')
ax2 = ax1.twinx()

ax1.set_ylabel('Close Price', color='blue')
ax1.plot(data_input.year, data_input.close_price, color='blue')

ax2.set_ylabel('EPS', color='red')
ax2.plot(data_input.year, data_input.eps, color='red')


plt.show()
