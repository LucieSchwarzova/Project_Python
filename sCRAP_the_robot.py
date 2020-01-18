#!/usr/bin/env python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import math
import operator
from datetime import datetime
import sqlite3
import random
import os
import time
import re

class DATART:
    '''
    Specific class for DATART eshop containing its web specific scraping methods under alligned terminology in
    order to be callable in the eshop class 
    '''
    
    def __init__(self, link, category):
        '''
        Define the empty generic eshop structure including the items that require web specific scraping  
        '''
        self.link = link
        self.category = category
        self.cat_link = []
        self.itms = []
        self.pgs = []
        self.urlspec = "/?startPos="
        self.pages = []
        self.products = []
               
        
    def get_catlink(self):
        '''
        Contruct the actual link for relevant category in DATART eshop  
        '''    
        self.cat_link = "{}/{}".format(self.link, self.category)
        
    def get_homesoupinfo(self, soup):
        '''
        Download the beautiful soup object from the first product page in selected category on DATART and extract available information
        '''    
        self.itms = int(soup.findAll("div",{'class','pagination-show-page'})[0].findAll('strong')[1].text)
        
        try: 
            self.pgs  = int(soup.findAll("a",{'class','button filter-attr'})[2].text)/1
        except:
            self.pgs = int(1) 
        
    def get_pages(self, souplist):
        
        self.pages = [None]*self.pgs
        for i in range(0,len(souplist)):
            self.pages[i] = page(souplist[i])
            
            
    def get_products(self, souplist):
        
        self.products = [None]*self.itms
        for i in range(0,len(souplist)):
            self.products[i] = product(souplist[i])
    
class page(DATART):
        
    def __init__(self, soup):
        '''
        Define the empty generic eshop structure including the items that require web specific scraping  
        '''
        self.soup = soup
        self.prodmod = self.soup.findAll('div', {'class':'category-page-item grid fly-parent wa-product-impression'})
             
    
class product(DATART):
    
    def __init__(self, soup):
        '''
        Define the empty generic eshop structure including the items that require web specific scraping  
        '''
        self.soup = soup
        self.title = []
        self.price = []
        self.currency = "CZK"
        self.get_title()
        self.get_price()
    
    
    def get_title(self):
        '''
        A method to extract product name from product module soup 
        '''
        self.title = self.soup.find('h3',{'class':'item-title'}).text.replace(u'\r', u'').replace(u'\n', u'').split(" (")[0]
     
    def get_price(self): 
        '''
        A method to extract product price from product module soup 
        '''
        self.price =  int(self.soup.find('span',{'class':'actual'}).text.split(":")[1].replace(u'\xa0', u'').split("Kč")[0])
           
    

class CZC:
    '''
    Specific clas for CZC eshop containing its web specific scraping methods under alligned terminology in
    order to be callable in the eshop class 
    '''
    
    def __init__(self, link, category):
        '''
        Define the empty generic eshop structure including the items that require web specific scraping  
        '''
 
        self.link = link
        self.category = category
        self.cat_link = []
        self.itms = []
        self.pgs = []
        self.urlspec = "?q-first="
        self.pages = []
        self.products = []
     
 
    def get_catlink(self):
        '''
        Contruct the actual link for relevant category in CZC eshop  
        '''
        self.cat_link = "{}/{}/produkty".format(self.link, self.category)
    
    def get_homesoupinfo(self,soup):
        '''
        Download the beautiful soup object from the first product page in selected category on CZC and extract available information
        '''    
        self.itms = int(str(soup.findAll('div',{'class','order-by-sum h-800'})).split(">")[1].split("<")[0].split(" ")[0].replace(u'\xa0', u''))
        self.pgs = math.ceil(self.itms/27)
 
    def get_pages(self, souplist):
 
        self.pages = [None]*self.pgs
        for i in range(0,len(souplist)):
            self.pages[i] = page(souplist[i])
    
 
    def get_products(self, souplist):
 
        self.products = [None]*self.itms
        for i in range(0,len(souplist)):
            self.products[i] = product(souplist[i])
     
    
class page(CZC):
    
    def __init__(self, soup):
        '''
        Define the empty generic eshop structure including the items that require web specific scraping  
        '''
        self.soup = soup
        self.prodmod = self.soup.findAll('div', {'class':'overflow'})

class product(CZC):

    def __init__(self, soup):
        '''
        Define the empty generic eshop structure including the items that require web specific scraping  
        '''
        self.soup = soup
        self.title = []
        self.price = []
        self.currency = "CZK"
        self.get_title()
        self.get_price()
    
    
    def get_title(self):
        '''
        A method to extract product name from product module soup 
        '''
        self.title = self.soup.find('a')['title'].split(",")[0].split(" +")[0]
     
    def get_price(self): 
        '''
        A method to extract product price from product module soup 
        '''
        price =self.soup.findAll('span',{'class':'price-vatin'})
        l=len(price)-1
        self.price = int(price[l].text.replace(u'\xa0', u'').split("Kč")[0])


# In[37]:


class eshop:
    '''
   The main class containing all infomation gathered from eshop page, including the information that 
   requires web-specific scraping methods. As a "bonus", it also backs up the soup objects of all product pages in a SQL database
    '''
    def __init__(self, link, category = "notebooky"):
       
        self.shop_name = link.split(".")[1].split("/")[0]
            
        if self.shop_name == "czc": # if we scrape CZC eshop, use the link and categroy to create object 
            #from the specific CZC class that has its own scraping methods defined bellow
            
            self.shop_obj = CZC(link, category)
            
        elif self.shop_name == "datart": #similar for Datart eshop
            
            self.shop_obj = DATART(link, category)
        
        else:
            print("Eshop {} out of scope".format(self.shop_name))
            self.shop_obj == []
            
        try: 
            self.robots_link = link + "/robots.txt"
            self.robots = requests.get(self.robots_link).text
        except: 
            print("Cannot reach robots.txt")
            
        self.cat_link = [] #link to to the first product page within category
        self.itms = [] #number of items in category
        self.pgs = [] # number of product pages in cateogory
        self.itmppg = [] #items per page
        self.urls = [] #list of URLs to all product pages within category
        self.allsoups = [] #list of BS objects for the urls list
        self.all_pages = [] #list of page objects from the BSs
        self.prd_modules = [] #list of product modules found in the product page BSs
        self.all_prds = []#list of product objects
        self.prd_data = {
                'product':[],
                'price':[]} 
        self.timestamp = []
        self.get_catlink()
        self.get_homesoup()
        self.leverage_soup()
        self.get_allsoups()
        self.get_pages()
        self.get_products()
        self.timestamp = datetime.now()
        self.output = pd.DataFrame(self.prd_data)
  

    def get_catlink(self):
        '''
        formulation of the main product page link requires eshop specific method -
        '''    
        self.shop_obj.get_catlink()
        self.cat_link = self.shop_obj.cat_link
        
    
    def get_homesoup(self):#generic method
        '''
        simplegeneric  request method 
        '''     
        try: 
            r = requests.get(self.cat_link)
            r.encoding='UTF-8'
            self.home_soup = BeautifulSoup(r.text,'lxml')
            print("Successfully requested the first {} homepage soup".format(self.shop_name))   
        
        except:
            print("Could not request the eshop main page or {} eshop".format(self.shop_name))
        
    def leverage_soup(self): 
        '''
        gathering initial information from the first product page via self.shop_obj 
        '''  
        try:
            self.shop_obj.get_homesoupinfo(self.home_soup)
        except:
            print("Could not run the e-shop specific information gathering method \n")
        self.pgs = self.shop_obj.pgs
        print("{} pages found\n".format(self.pgs))
        self.itms = self.shop_obj.itms
        print("{} items found\n".format(self.itms))

        self.itmppg = math.ceil(self.itms / self.pgs)
             
        self.urls = [None] * self.pgs
        
        self.urls[0] = self.cat_link
        
        for i in range(1,self.pgs):
            self.urls[i] = self.cat_link + self.shop_obj.urlspec + str(self.itmppg*i)
        
        print("Product page urls were generated")
    
    def get_allsoups(self):
        '''
        lists soup objects of all product pages within the category
        '''  
        self.allsoups = [None]*self.pgs
        
        for i in range(0,self.pgs):
            try:
                r = requests.get(self.urls[i])
                r.encoding='UTF-8'
                self.allsoups[i] = BeautifulSoup(r.text,'lxml')
                print( "{}th product page from {} eshop successfully requested \n".format(i +1,self.shop_name))
 
            except:
                print( "Could not request {}th product page from {} eshop \n".format(i+1,self.shop_name))
            
            time.sleep(random.randrange(0,300,1)/100) # in order not to be caught by web's robotic behavior deection systems
        
            
            
    def get_pages(self):
        '''
        creates eshop-specific list of page objects 
        '''
        self.shop_obj.get_pages(self.allsoups)
        self.pages = self.shop_obj.pages
        
        for i in range (0,self.pgs):
            self.prd_modules[((0+i)*self.itmppg):((1+i)*self.itmppg)] = self.pages[i].prodmod
        
        
    def get_products(self):
        '''
        Extrect the relevant information from the identified product modulesusingehop-specific methods
        '''
        self.shop_obj.get_products(self.prd_modules)
        self.all_prds = self.shop_obj.products
        self.prd_data['product'] = list(o.title for o in self.all_prds)
        self.prd_data['price'] = list(o.price for o in self.all_prds)
        
            


# In[38]:


class collect:
    '''
    This class contains method to collect the data from selected category and eshop. Some execution 
    parameters (period, iterations) can be also provided, while their default value is one, i.e. 
    one execution only, data is collected,not updated further. '''
    
    def __init__(self, link, category,period=1, iterations=1):
        print('You are about to start scraping the {} category. The page will be re-scanned every {} seconds, in total {} times'.format(category,period,iterations))
        self.timestamp = int(time.time())
        self.link = link
        self.category = category
        self.soup_tablename = 'soup'+str(self.timestamp)
        self.product_tablename  = 'product'+str(self.timestamp)
        self.request = []
        self.get_storage_ready()
        self.iterator(link, category, period,iterations)
        
        
                                            
    def get_storage_ready(self):                                   
       
        data_storage = sqlite3.connect('storage.db').cursor()
        data_storage.execute("""CREATE TABLE IF NOT EXISTS {}(
                                                            shop TEXT,
                                                            category TEXT,
                                                            product TEXT,
                                                            price INTEGER,
                                                            stamp INTEGER)""".format(self.product_tablename)) 
        
        data_storage.close()
        
        print("Current table for product data: {}".format(self.product_tablename)) 
        print("Current table for soups: {}".format(self.soup_tablename))                               
        print("Storage is ready. Data collection is about to start. The scraped data will be stored in *storage.db* database in your woking directory /n")
      
    
        
           
    def initiate_request(self):
        """ Request the link / category and scape all the requested information"""
        self.request = eshop(self.link,self.category)
           
    
    def iterator(self, link,category,period,iterations):
        
        self.initiate_request()
        self.data_upload()
        
        for i in range(iterations-1):
            print("{} iteration out of {} commited, next to be starter in {} mins \n".format(i+1,iterations, period/60))
            time.sleep(period) 
            self.initiate_request()
            self.timestamp = int(time.time())
            self.data_upload()
            print("{} iteration out of {} commited, next to be starter in {} mins \n".format(i,iterations, period/60))
               
    def data_upload(self):
        print("Data upload just started\n")
        try:
            data_storage = sqlite3.connect('storage.db')
            table = self.product_tablename
            link = self.link
            category = self.category
            time = self.timestamp
            
            for i in range(self.request.itms):
                price = self.request.output['price'][i]
                product = self.request.output['product'][i]
                data_storage = sqlite3.connect('storage.db')
                data_storage.execute( """INSERT INTO {}(shop, category, product, price, stamp)
                VALUES ('{}','{}','{}','{}','{}')""".format(table, link, category, product, price, time))
                data_storage.execute("""COMMIT""")
                print("Record {}/{} was added in the database\n".format(i+1,self.request.itms))
                data_storage.close()
            print("All changes successfully commited \n")
            
        except:
            print("An error occured in data upload")


# In[ ]:





# In[ ]:




