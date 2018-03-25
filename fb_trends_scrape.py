# LIBRARIES USED:
# SELENIUM, APSCHEDULER
# pip install apscheduler

##fix currently problem

import time
import csv
import datetime

from urllib.request import urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from time import gmtime, strftime

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
per_unit = 1
filename = "1min_test"

def init_driver():
    driver = webdriver.Firefox()
    driver.set_window_size(1124,850)
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
    except TimeoutException:
        print("Username, password, and/or log in button not found at", link)

def see_more_btn():
    try:
        see_more_btn = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_5my9")))
        see_more_btn.click()
    except TimeoutException:
        print("see more btn not found")

def click_icons(icon_ids):
    global scrapeID
    icons = driver.find_elements_by_class_name("_1o7n")
    index =  0
    outer_list = []
    length = len(icon_ids)
    #print("id length:", length)
    #print("icon_ids: ", icon_ids)
    for icon in icons:
        if index < length:
            icon.click()
            ts = datetime.datetime.now()
            category = icon_name(index)
            get_trending(icon_ids[index], outer_list, category, ts)
            index += 1
    scrapeID += 1
    return outer_list

def load_icon_html():
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_class_name("_1o7n"))
    icons = driver.find_elements_by_class_name("_1o7n")
    for icon in icons:
        driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_1o7n")))
        icon.click()

def get_icon_id():
    classes = driver.find_elements_by_css_selector("div._5my7")
    icon_ids = []
    for c in classes:
        icon_ids.append(c.get_attribute("id"))
    return icon_ids

def icon_name(index):
    if index == 0:
        return "Top Trends"
    elif index == 1:
        return "Politics"
    elif index == 2:
        return "Science and Technology"
    elif index == 3:
        return "Sports"
    elif index == 4:
        return "Entertainment"
    else:
        return "Error: Could not find icon name"

def get_trending(id, outer_list, catergory, ts):
    t = ts.strftime("%c")
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_class_name("_5myl"))
    current = driver.find_element_by_id(id)
    box = current.find_element_by_class_name("_5myl")
    articles = box.find_elements_by_class_name("_5my2")
    count = 1
    for article in articles:
        temp_list = []
        title = article.find_element_by_class_name("_5v0s")
        description = article.find_element_by_class_name("_3-9y")
        source = article.find_element_by_class_name("_1oic")
        link = article.find_element_by_class_name("_4qzh").get_attribute("href")
        temp_list.append(catergory)
        temp_list.append(title.text)
        temp_list.append(description.text)
        temp_list.append(source.text[2:])
        temp_list.append(link)
        temp_list.append(count)
        temp_list.append(scrapeID)
        temp_list.append(t)
        outer_list.append(temp_list)
        count += 1
    return outer_list

def scrape_job():
    print("current run:", datetime.datetime.now())
    icon = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2md")))
    icon.click()
    driver.refresh()
    load_icon_html()
    driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_5my7")))
    icon_ids = get_icon_id()
    #print("got icon_ids")
    list_of_list = click_icons(icon_ids)
    #print("got click_icons")
    with open(filename+".csv", "a",  newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(list_of_list)

if __name__ == "__main__":
    scrapeID = 0
    driver = init_driver()
    log_in(driver, fb_username, fb_password)
    with open(filename+".csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "title", "description", "source", "uniquelink", "rank", "scrapeid", "timestamp"]) #Scrap ID
        sched = BlockingScheduler()
        job = sched.add_job(scrape_job, "interval", minutes=per_unit, misfire_grace_time=30) #max_runs
        print("scrape started at:", datetime.datetime.now())
        sched.start()
        try:
            time.sleep(1)
        except (KeyboardInterrupt, Exception):
            sched.shutdown()
    #time.sleep(5)
    driver.quit()
