import requests
from bs4 import BeautifulSoup as bs
import time
import json
from proxymanager import ProxyManager
from fake_useragent import UserAgent
import datetime

#import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

#print("==============================")
#print(datetime.datetime.now())


me = "luozhou.li@gmail.com"
you = "monkeyfather101@gmail.com"



ua = UserAgent()
proxy_manager = ProxyManager('/home/ubuntu/flaskapp/proxies.txt')



def get_sizes_from_stockx(stockx_link):
        stockx_sizes = []
        notification_list = []
        random_proxy = proxy_manager.random_proxy()
        proxies = random_proxy.get_dict()
 #       print(proxies)
        session = requests.Session()
        session.headers = {'User-Agent': ua.random}
  #      print(ua.random)

        notification_list.append("===========================")
        notification_list.append(stockx_link)

        stockx_response = session.get(stockx_link)
        #stockx_response = session.get(stockx_link, proxies=proxies)
        #print(stockx_response.text)
        stockx_soup = bs(stockx_response.text, 'lxml')
   #     print(stockx_response.status_code)
        windowPreloaded = False
        #print(stockx_soup.findAll('script', {"type": "text/javascript"}))
        for stockx_script in stockx_soup.findAll('script', {"type": "text/javascript"}):
                if 'window.preLoaded' in stockx_script.text:
                        #print(stockx_script)
                        windowPreloaded = True
                        response_text_tmp = stockx_script.text.replace("window.preLoaded =", "")
                        response_text = response_text_tmp.replace(";", "")
                        data = json.loads(response_text)
                #       print(data)
                        #with open('stockx_response.json', 'w') as f:
                        #       f.write(data)
                        title = data['product']['name']
                        style_id = data['product']['styleId']
                        retailPrice = data['product']['retailPrice']
                        taxedRetail = round(retailPrice * 1.07, 2)
    #                    print("{} {} retail price is ${} while taxed price is ${}".format(title, style_id, retailPrice, taxedRetail))
                        notification_list.append("{} {} retail price is ${} while taxed price is ${}".format(title, style_id, retailPrice, taxedRetail))
                        data_children = data['product']['children']
                        for child in data_children.keys():
                                bid_size = data_children[child]['market']['highestBidSize']
                                highest_bid = data_children[child]['market']['highestBid']
                                resell_gain = round(highest_bid * 0.88, 2)
                                if bid_size and (resell_gain > taxedRetail):
                                        stockx_sizes.append(bid_size)
                                        resell_profit = round(resell_gain - taxedRetail, 2)
     #                                   print("Size {} highest bid is ${} while resell gain is ${} and resell profit is {}".format(bid_size, highest_bid, resell_gain, resell_profit))
                                        notification_list.append("Size {} highest bid is ${} while resell gain is ${} and resell profit is {}".format(bid_size, highest_bid, resell_gain, resell_profit))
        if not windowPreloaded:
                stockx_sizes.append('all')
      #          print('window.Preloaded not found')
                notification_list.append("StockX window.Preloaded not found")
        return stockx_sizes, notification_list

notification_sum = []
def calculate(styleCode):
    if 'stockx' in styleCode:
        #requests_response = requests.get(styleCode)
        #print(requests_response.text)
        stockx_link = styleCode
    else:
        search_response = requests.get('https://stockx.com/search?s={}'.format(styleCode))
       # print(search_response.text)
        search_soup = bs(search_response.text, 'lxml')
    stockx_sizes, notification_list = get_sizes_from_stockx(stockx_link)
    return notification_list
