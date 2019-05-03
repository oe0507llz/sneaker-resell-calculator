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



def get_sizes_from_stockx(stockx_link, tax):
        stockx_sizes = []
        notification_list = []
        random_proxy = proxy_manager.random_proxy()
        proxies = random_proxy.get_dict()
 #       print(proxies)
        session = requests.Session()
        session.headers = {'User-Agent': ua.random}
  #      print(ua.random)

        #notification_list.append(stockx_link + '<br>')

#        try:
#            stockx_response = session.get(stockx_link, proxies=proxies)
#            print proxies
#        except:
        stockx_response = session.get(stockx_link)
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
                        taxedRetail = round(retailPrice * (1 + float(tax)), 2)
                        notification_list.append("<br>{} {} <br><br>Retail price is ${} while taxed price is ${}<br><br>".format(title, style_id, retailPrice, taxedRetail))
                        data_children = data['product']['children']
                        notification_list.append('''<table><tr><th style="width: 40px" align="center">Size</th><th style="width: 100px" align="center">Highest Bid</th><th style="width: 100px" align="center">Resell Gain</th><th style="width: 100px" align="center">Resell Profit</th></tr>''')
                        for child in data_children:
                                bid_size = data_children[child]['market']['highestBidSize']
                                highest_bid = data_children[child]['market']['highestBid']
                                resell_gain = round(highest_bid * 0.88, 2)
                                if bid_size and (resell_gain > taxedRetail):
                                        stockx_sizes.append(bid_size)
                                        resell_profit = round(resell_gain - taxedRetail, 2)
                                        notification_list.append('''<tr><td style="width: 40px" align="center">{}</td><td style="width: 100px" align="center">${}</td><td style="width: 100px" align="center">${}</td><td style="width: 100px" align="center">${}</td></tr>'''.format(bid_size, highest_bid, resell_gain, resell_profit))
        notification_list.append('</table>')
        if not windowPreloaded:
                stockx_sizes.append('all')
      #          print('window.Preloaded not found')
                notification_list.append("Try it again.")
        else:
            stockx_sizes.sort()
            if not all("1" in size for size in stockx_sizes):
                while "1" in stockx_sizes[0]:
                    size_tmp = stockx_sizes.pop(0)
                    stockx_sizes.append(size_tmp)
            stockx_sizes_string = 'Profitable sizes include: ' + ' '.join(stockx_sizes) + '<br><br>'
            notification_list.insert(1, stockx_sizes_string)
        return stockx_sizes, notification_list

notification_sum = []
def calculate(styleCode, tax):
    if 'stockx' in styleCode:
        #requests_response = requests.get(styleCode)
        #print(requests_response.text)
        stockx_link = styleCode
    else:
        search_response = requests.get('https://stockx.com/search?s={}'.format(styleCode))
       # print(search_response.text)
        search_soup = bs(search_response.text, 'lxml')
    stockx_sizes, notification_list = get_sizes_from_stockx(stockx_link, tax)
    return notification_list
