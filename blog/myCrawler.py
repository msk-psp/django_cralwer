#!/usr/bin/python
# -*- coding: euc-kr -*-
import requests
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
from urlparse import urlparse

def spider(item_name,site_name):
    #url_item_name = parse.quote(item_name.decode(encoding='UTF-8').encode('euc-kr'))
    urls = {'11st': ("http://search.11st.co.kr/SearchPrdAction.tmall?method=getTotalSearchSeller&kwd="),
        'auction': ("http://search.auction.co.kr/search/search.aspx?keyword="),
        'naver': "https://search.shopping.naver.com/search/all.nhn?query="}
    print(urls[site_name])
    if(site_name =='naver'):
        resp = requests.get(urls[site_name]+urllib.unquote(item_name).decode('euc-kr'))
    else:
        resp = requests.get(urls[site_name]+item_name)

    resp.raise_for_status()

    if(site_name == 'naver'):
        resp.encoding = 'utf-8'
    else:
        resp.encoding='euc-kr'

    plain_text = resp.text

    soup = BeautifulSoup(plain_text, 'lxml')

    #for link in soup.select('div.list_info p.info_tit a') :
    data = {}
    count = -1;
    if(site_name == '11st'):
        mytag = soup.find_all(True, {"class": ["sale_price", "list_info"]})
        mytag2 = soup.find_all(True, {"class": ["photo_wrap"]}, "a")
        for link in mytag:
            if(link.find('a')):
                count+=1
                href = link.find('a').get('href')        # to get product href
                product_name = link.find('a').string        # to get prouct name
                encoded_name = str(product_name).decode('utf8')
#                data[count] = str(href) + ", " + str(product_name)  # add into dict$
                data[count] = str(href) + ", " + str(encoded_name).strip()  # add into dict$
            else:
                product_price = link.string                             # to get pr$
                if(product_price):
                    data[count] = data[count] +", " + str(product_price).replace(",",".")
        count=0
        for link2 in mytag2:
            if(link2.img):
                data[count] = data[count] + ", " + str(link2.img.get('data-original'))
                count+=1

    elif (site_name == 'auction'):
        mytag = soup.find_all('div', {"class": ["list_view"]})
        for link in mytag:
            count+=1
            print(link.find_all('src'))
            if(link.find('a').get('href')):
                href = link.find('a').get('href')
            else:
                href =""
            if(link.find('div', {'class':'item_title'})):
                product_name = link.find('div', {'class':'item_title'}).get_text()
            else:
                product_name = ""
            if(link.find('div', {'class':'item_price'})):
                product_price = str(link.find('div', {'class':'item_price'}).get_text()).replace(",",".")
            else:
                product_price = ""
            if(link.find('a').img.get('data-original')):
                product_img = link.find('a').img.get('data-original')
            elif(link.find('a').img):
                product_img = link.find('a').img["src"]
                print(product_img)

            #print("href ",link.find('a').get('href'))
            #print("src ",link.find('a').img.get('data-original'))
            #print(link.find('div', {'class':'item_price'}).get_text())
            #print(link.find('div', {'class':'item_title'}).get_text())
            data[count] = str(href) + "," + str(product_name).strip() + "," +str(product_price).strip()+","+ str(product_img).strip()
           # print(data[count])


    else:
        mytag = soup.find_all('li', {"class": ["ad _itemSection","_model_list _itemSection","_exception _itemSection","_itemSection"]})
        for link in mytag:
            count += 1
            if(link.find('a').img):
                href = link.find('a').get('href')
                product_img = link.find('a').img.get('data-original')
                #print(link.find('a').get('href'))
                #print(link.find('a').img.get('data-original'))
            if(link.find('div', {'class':"info"})):
                product_name = link.find('div',{'class':"info"}).a.get('title')
                product_price =  str(link.find('div',{'class':"info"}).find('em').get_text()).replace(",",".")
                #print(link.find('div',{'class':"info"}).a.get('title'))
                #print(link.find('div',{'class':"info"}).find('em').get_text())
            data[count] = str(href) + "," + str(product_name).strip() + "," + str(product_price).strip() + "," + str(product_img).strip()
        print(data[count])
    resp.close()
    return data

