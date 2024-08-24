from bs4 import BeautifulSoup #pip install bs4
import requests
import numpy as np
import csv
from datetime import datetime 

Link = "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1311&_nkw=xiaomi+14+ultra&_sacat=0&_odkw=m1+xiaomi&_osacat=0"

def get_prices_by_link(link):
    # get source
    r = requests.get(link)
    # parse source
    page_parse = BeautifulSoup(r.text, 'html.parser')
    # print(page_parse)
    # find all list items from search results
    search_results = page_parse.find("ul", {"class":"srp-results"}).find_all("li", {"class":"s-item"})
    
    item_prices = []
    
    for result in search_results:
        price_as_text = result.find("span", {"class":"s-item__price"}).text
        if "to" in price_as_text:
            continue 
        price = float(price_as_text[1:].replace(",",""))
        item_prices.append(price)
    return item_prices

def remove_outliers(prices, m=2):
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def get_average(prices):
    return np.mean(prices)

def save_to_file(prices):
    fields = [datetime.today().strftime("%B-%d-%Y"), np.around(get_average(prices), 2)]
    with open("prices.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == "__main__":
    prices = get_prices_by_link(Link)
    prices_without_outliers = remove_outliers(prices)
    save_to_file(prices_without_outliers)
