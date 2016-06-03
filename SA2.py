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

booking_1 = 'http://www.booking.com/searchresults.html?aid=356980&label=gog235jc-country-XX-sa-sa-unspec-us_il-com-L%3Axu-O%3AwindowsS7-B%3Achrome-N%3Ayes-S%3Abo-U%3Ac&sid=da04d20bdc59442c370a7a57fb3ab1aa&dcid=4&class_interval=1&dest_id=186&dest_type=country&dtdisc=0&first_filter_suggestion_clicked=2&group_adults=2&group_children=0&hlrd=0&hyb_red=0&inac=0&label_click=undef&nflt=ht_id%3D204%3B&nha_red=0&no_rooms=1&postcard=0&redirected_from_city=0&redirected_from_landmark=0&redirected_from_region=0&review_score_group=empty&room1=A%2CA&sb_price_type=total&score_min=0&ss=saudi%20arabia&ss_all=0&ss_raw=saudi%20ara&ssb=empty&sshis=0&order=class_asc'
base = 'http://www.booking.com/searchresults.html?aid=356980&label=gog235jc-country-XX-sa-sa-unspec-us_il-com-L%3Axu-O%3AwindowsS7-B%3Achrome-N%3Ayes-S%3Abo-U%3Ac&sid=da04d20bdc59442c370a7a57fb3ab1aa&dcid=4&class_interval=1&dest_id=186&dest_type=country&first_filter_suggestion_clicked=2&group_adults=2&group_children=0&hlrd=0&label_click=undef&nflt=ht_id%3D204%3B&no_rooms=1&order=class_asc&review_score_group=empty&room1=A%2CA&sb_price_type=total&score_min=0&ss=saudi%20arabia&ss_raw=saudi%20ara&ssb=empty&rows=15&offset='
booking_rest = [base + str((i - 1) * 15) for i in range(2, 35)]

booking_rest.append(booking_1)

name_list = []
star_list = []
#star_text_list = []
address_list = []
room_list = []
#room_text_list = []
link_list = []

i = 1
for link in booking_rest:

    driver = webdriver.Firefox()
    driver.get(link)

    hotels = driver.find_elements_by_class_name("hotel_image")

    for hotel in hotels:
        hotel.click()
        driver.implicitly_wait(5)
        time.sleep(1)
        driver.switch_to_window(driver.window_handles[1])
        link_list.append(driver.current_url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            name = soup.find('span', {'class': 'fn'}).text.strip()
        except:
            name = ""

        print(i,name)
        i += 1

        try:
        #    star_text = soup.find('span', {'class': 'hp__hotel_ratings__stars'}).text
            star = ''.join(re.findall("(\d+)",soup.find('span', {'class': 'hp__hotel_ratings__stars'}).text))
        except:
        #   star_text= ""
            star = ""
        try:
            address = soup.find('span', {'class': 'hp_address_subtitle jq_tooltip'}).text.strip()
        except:
            address = ""
        try:
        #    room_text = soup.find('p', {'class': 'summary hotel_meta_style'}).text.split('\n')[2]
            room = ''.join(re.findall("(\d+)",soup.find('p', {'class': 'summary hotel_meta_style'}).text.split('\n')[2]))
        except:
        #    room_text = ""
            room = ""

        name_list.append(name)
        star_list.append(star)
        address_list.append(address)
        room_list.append(room)
        #star_text_list.append(star_text)
        #room_text_list.append(room_text)

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        driver.switch_to_window(driver.window_handles[0])

    driver.close()

#hotel = pd.DataFrame({'name': name_list, 'address': address_list, 'star': star_list, 'room': room_list,'room_text':room_text_list,'star_text':star_text_list})
hotel = pd.DataFrame({'name': name_list, 'address': address_list, 'star': star_list, 'room': room_list})

writer = ExcelWriter("C:/Users/jchen5/Downloads/SA/SA total star category 3.xlsx", engine='xlsxwriter')
hotel.to_excel(writer, index=False, sheet_name='raw')
writer.save()
print("Done!")


# hotel_w_link = pd.DataFrame({'name': name_list, 'address': address_list, 'star': star_list, 'room': room_list,'room_text':room_text_list,'star_text':star_text_list,'link':link_list})
# writer2 = ExcelWriter("C:/Users/jchen5/Downloads/SA/SA total star category with link.xlsx", engine='xlsxwriter')
# hotel_w_link.to_excel(writer2, index=False, sheet_name='raw')
# writer2.save()
# print("Done too!")
