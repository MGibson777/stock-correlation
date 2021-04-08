# IF TWO STOCKS ARE CORRELATED

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import datetime


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory":
                        r"C:\Users\thegi\PycharmProjects\URANIUM\\",
             "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(executable_path=r'C:\Users\thegi\PycharmProjects\URANIUM\chromedriver.exe', options = options)

#Independent First two and Dependent 2nd First predicts the 2nd 
stock_ticker = "VZ"
stock_ticker_2 = 'T'


from selenium.webdriver.common.keys import Keys
import time

driver.maximize_window()
driver.get(f"https://finance.yahoo.com/quote/{stock_ticker}/history?period1=1174262400&period2=1610409600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true")
time.sleep(5)


elem = driver.find_element_by_link_text('Download')
elem.click()

driver.get(f"https://finance.yahoo.com/quote/{stock_ticker_2}/history?period1=1174262400&period2=1610409600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true")
time.sleep(5)

elem = driver.find_element_by_link_text('Download')
elem.click()
driver.minimize_window()

# WORK WITH THE FILES
import pandas as pd


df = pd.read_csv(f"{stock_ticker}.csv")
df_2 = pd.read_csv(f"{stock_ticker_2}.csv")

df_merge_col = pd.merge(df, df_2, on='Date')

stock_ticker_prices = []
stock_ticker_2_prices = []
x = 0
for a in range(len(df_merge_col)):
    stock_ticker_prices.append(df_merge_col.iloc[x,5])
    stock_ticker_2_prices.append(df_merge_col.iloc[x,10])
    x = x +1

print(len(stock_ticker_prices))
print(len(stock_ticker_2_prices))

import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array(stock_ticker_prices).reshape((-1, 1))
y = np.array(stock_ticker_2_prices)

model = LinearRegression()
model.fit(x,y)

r_sq = model.score(x,y)
print('coefficient of determination:', r_sq)
print('intercept:', model.intercept_)
print('slope:', model.coef_)

#Predict Factor Y based on Price of Factor X
n = len(df)-1
stock_price = df.iloc[n,5]
u = ([(stock_price*0.5), (stock_price*0.8), (stock_price), (stock_price*1.2), (stock_price*1.5), (stock_price*2), (stock_price*2.5), (stock_price*3), (stock_price*5), (stock_price*10)])


z = np.array([(stock_price*0.5), (stock_price*0.8), (stock_price), (stock_price*1.2), (stock_price*1.5), (stock_price*2), (stock_price*2.5), (stock_price*3), (stock_price*5), (stock_price*10)]).reshape((-1,1))

y_pred = model.predict(z)
print(f"Year Data Going back from {df.iloc[0,0]} to present")
print('If Stock X went to price', u, sep='\n')
print('predicted response:', y_pred, sep='\n')

print(df_merge_col)

import os
os.remove(f'{stock_ticker}.csv')
os.remove(f'{stock_ticker_2}.csv')



