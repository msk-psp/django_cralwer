#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect

#try:
#    from urllib.parse import urlparse
#except ImportError:
#    try:
#        from urlparse import urlparse
#    except ImportError:
#        import urllib.parse
#from urlparse import urlparse

import urllib
from urlparse import urlparse

from .models import Post
from .myCrawler import spider
from .forms import PostForm
from .forms import NameForm
# Create your views here.
def post_shop_list(request):
    products = []
    url_item_name = urllib.quote(product_name.encode('euc-kr'))

    posts = spider(url_item_name)
    for key, value in posts.items():
        product = value.split(',')
        #product = [href,name,price,img_src]
        print(product)
        product_entry = {
            'key': key,
            'name': product[1],
            'href': product[0],
            'price': str(product[2]).replace(".",","),
            'img' : product[-1]
        }
	products.append(product_entry)

    return render(request, 'blog/post_list.html',{'products' : products})

def my_post_new(request):
    if request.method == 'POST':
        form = NameForm()
        form = NameForm(request.POST)
        if(form.is_valid()):
            text = form.cleaned_data['product_name']
            products = []

            url_item_name = urllib.quote(text.encode('euc-kr'))
            posts = spider(url_item_name,"11st")
            elevn_st_products = get_products(posts)

            posts = spider(url_item_name,"auction")
            auc_products = get_products(posts)

            posts = spider(url_item_name,"naver")
            naver_products = get_products(posts)

            args = {'elevn_st': elevn_st_products, 'auction': auc_products, 'naver': naver_products, 'text': text}
            return render(request,'blog/post_edit.html',args)
    else:
        form = NameForm()
    form = NameForm(request.POST)
    return render(request, 'blog/post_edit.html', {'form': form})


def get_products(posts):
    products = []
    for key, value in posts.iteritems():
        product = value.split(',')
        product_entry = {
            'key': key,
            'name': product[1],
            'href': product[0],
            'price': str(product[2]).replace(".",","),
            'img' : product[-1]
        }
        products.append(product_entry)
    return products



