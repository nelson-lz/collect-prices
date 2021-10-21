import requests
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver import Firefox
options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9222")
driverc = webdriver.Chrome(options = options)
#drivef = Firefox(executable_path="/usr/local/bin/geckodriver")

url = "https://www.stock.com.py/default.aspx"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
categorias = soup.findAll('a', attrs={"class": "collapsed"})
for cat in categorias:
    print(cat.text)

driverc.get(url)

driverc.quit()