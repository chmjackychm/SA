from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pandas import ExcelWriter

import pandas as pd
import numpy as np
import re
import math
import time
import csv

booking_1 = 'http://www.booking.com/searchresults.html?aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmcgV1c19tZIgBAZgBMbgBBsgBDNgBA-gBAfgBAqgCAw&sid=da04d20bdc59442c370a7a57fb3ab1aa&dcid=4&class_interval=1&dest_id=186&dest_type=country&dtdisc=0&group_adults=2&group_children=0&hlrd=0&hyb_red=0&inac=0&label_click=undef&nflt=ht_id%3D201%3B&nha_red=0&no_rooms=1&postcard=0&redirected_from_city=0&redirected_from_landmark=0&redirected_from_region=0&review_score_group=empty&room1=A%2CA&sb_price_type=total&score_min=0&src_elem=sb&ss=Saudi%20Arabia&ss_all=0&ss_raw=saudi%20arbia&ssb=empty&sshis=0&order=class'
base = 'http://www.booking.com/searchresults.html?aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmcgV1c19tZIgBAZgBMbgBBsgBDNgBA-gBAfgBAqgCAw&sid=da04d20bdc59442c370a7a57fb3ab1aa&dcid=4&class_interval=1&dest_id=186&dest_type=country&group_adults=2&group_children=0&hlrd=0&label_click=undef&nflt=ht_id%3D201%3B&no_rooms=1&order=class&review_score_group=empty&room1=A%2CA&sb_price_type=total&score_min=0&src_elem=sb&ss=Saudi%20Arabia&ss_raw=saudi%20arbia&ssb=empty&rows=15&offset='
booking_rest = [base + str((i - 1) * 15) for i in range(2, 47)]
booking_rest.append(booking_1)



# hotels = driver.find_elements_by_class_name("sr-hotel__title   ")
# name = hotels[0].text.split('\n')[0]
# city = hotels[0].text.split('\n')[-1]

hotel_lists = pd.DataFrame()

driver = webdriver.Firefox()

i = 1
for link in booking_rest:

    driver.get(link)
    hotels = driver.find_elements_by_class_name("sr-hotel__title   ")
    hotel = [hotel.text.split('\n')[0] for hotel in hotels]
    city = [hotel.text.split('\n')[-1] for hotel in hotels]
    hotel_list = pd.DataFrame({'name':hotel,'city':city})
    hotel_lists = hotel_lists.append(hotel_list)
    print(i)
    i += 1
writer = ExcelWriter("C:/Users/jchen5/Downloads/SA/SA city.xlsx", engine='xlsxwriter')
hotel_lists.to_excel(writer, index=False, sheet_name='raw')
writer.save()
print("Done!")


driver = webdriver.Firefox()
driver.get(booking_1)
hotels = driver.find_elements_by_class_name("sr-hotel__title   ")
