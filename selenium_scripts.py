# LIBRARIES USED:
# SELENIUM

import time
import csv

from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

link = "http://www.facebook.com"
response = urlopen("http://www.facebook.com")
page_source = response.read()

fb_username = "computational.journalism.lab@gmail.com"
fb_password = "D66bkPphJ8D3bVzq"

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def log_in(driver, username, pw):
    driver.get(link)
    try:
        email = driver.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password = driver.wait.until(EC.presence_of_element_located((By.NAME, "pass")))
        log_button = driver.wait.until(EC.presence_of_element_located((By.ID, "u_0_2")))
        email.send_keys(username)
        password.send_keys(pw)
        log_button.click()
        icon = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2md")))
        icon.click()
    except TimeoutException:
        print("Username, password, home page icon, and/or log in button not found at", link)

def see_more_btn():
    try:
        see_more_btn = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_5my9")))
        see_more_btn.click()
    except TimeoutException:
        print("see more btn not found")

def click_icons(icon_ids):
    icons = driver.find_elements_by_class_name("_1o7n")
    index =  0
    list_of_categories = []
    for icon in icons:
        data = [[] for _ in range(4)]
        icon.click()
        list_of_categories.append(get_trending(icon_ids[index], data))
        time.sleep(3)
        index += 1
    return list_of_categories

def load_icon_html():
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_class_name("_1o7n"))
    icons = driver.find_elements_by_class_name("_1o7n")
    for icon in icons:
        icon.click()
        time.sleep(3)

def get_icon_id():
    ids =[]
    classes = driver.find_elements_by_css_selector("div._5my7")
    for c in classes:
        ids.append(c.get_attribute("id"))
    return ids

def get_trending(id, list_of_list):
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_class_name("_5myl"))
    current = driver.find_element_by_id(id)
    box = current.find_element_by_class_name("_5myl")
    articles = box.find_elements_by_class_name("_5my2")
    count = 1
    for article in articles:
        title = article.find_element_by_class_name("_5v0s")
        description = article.find_element_by_class_name("_3-9y")
        source = article.find_element_by_class_name("_1oic")
        link = article.find_element_by_class_name("_4qzh").get_attribute("href")
        count += 1
        list_of_list[0].append(title.text)
        list_of_list[1].append(description.text)
        list_of_list[2].append(source.text[1:])
        list_of_list[3].append(link)
    return list_of_list


# open a csv file with append, so old data will not be erased
# with open(‘facebook_trends.csv’, ‘a’) as csv_file:
#  writer = csv.writer(csv_file)
#  writer.writerow([name, price, datetime.now()])

if __name__ == "__main__":
    driver = init_driver()
    log_in(driver, fb_username, fb_password)
    load_icon_html()
    icon_ids = get_icon_id()
    print(click_icons(icon_ids))
    #time.sleep(5)
    #driver.quit()
