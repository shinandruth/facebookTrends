# fb_trends.py

import time
import csv
import datetime
import os
import configparser
import random

from pyvirtualdisplay import Display
from urllib.request import urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from time import gmtime, strftime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


link = "http://www.facebook.com"

#----------------SET chrome_driver_name TO LOCATION OF YOUR CHROME DRIVER--------------------------
chrome_driver_name = ""
#--------------------------------Config File---------------------------------
config = configparser.ConfigParser()
config.read("config.ini")
config_type = "PUPPET"

fb_username = config[config_type]["USERNAME"]
fb_password = config[config_type]["PASSWORD"]
per_unit = int(config[config_type]["INTERVAL"])
filename = config[config_type]["FILENAME"]
#--------------------------------DB Connection---------------------------------
db = pymysql.connect(host="fb-scrape-db.c0lrs8fl8ynt.us-east-2.rds.amazonaws.com",
                     user="",
                     password="",
                     db="fb_scrape_db",
                     charset="utf8mb4")
cursor = db.cursor()
#--------------------------------Scrape Functions---------------------------------

'''
init_driver()
Initiates the webdriver
'''
def init_driver():
    chrome_options = webdriver.ChromeOptions()
    #-----headless----
    # display = Display(visible=0, size=(800,600))
    # display.start()
    chrome_options.add_argument("--headless")
    #-----------------
    chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_driver = chrome_driver_name
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    #------Firefox--------
    # Optional: the commented out below code is to use Selenium with Firefox
    # driver = webdriver.Firefox(firefox_options=options)
    # driver = webdriver.Firefox()
    # driver.set_window_size(1124,850)
    #---------------------
    driver.wait = WebDriverWait(driver, 5)
    return driver

'''
log_in(driver, username, pw)
Login to facebook
Prints error message if login failed
'''
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

'''
click_icons(icon_ids)
Clicks through the all the icons and initiates the data collection
'''
def click_icons(icon_ids):
    global scrapeID
    icons = driver.find_elements_by_class_name("_1o7n")
    index =  0
    outer_list = []
    outer_tab = []
    length = len(icon_ids)
    for icon in icons:
        if index < length:
            icon.click()
            time.sleep(2)
            ts = datetime.datetime.now()
            category = icon_name(index)
            get_trending(icon_ids[index], outer_list, outer_tab, category, ts)
            index += 1
    scrapeID += 1
    return outer_list, outer_tab

'''
load_icon_html()
Clicks through the icons to load the HTML element for each Trending Topic category
'''
def load_icon_html():
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_class_name("_1o7n"))
    icons = driver.find_elements_by_class_name("_1o7n")
    top = icons[0]
    politics = icons[1]
    politics.click()
    top.click()
    count = 0
    for icon in icons:
        driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_1o7n")))
        icon.click()
        count += 1
'''
get_icon_id()
Gets the Icon IDs for Trending Topic's Categories
'''
def get_icon_id():
    classes = driver.find_elements_by_class_name("_5my7")
    icon_ids = []
    for c in classes:
        icon_ids.append(c.get_attribute("id"))
    if len(icon_ids) < 5:
        driver.refresh()
        load_icon_html()
        icon_ids = get_icon_id()
    return icon_ids

'''
icon_name(index)
Creates icon name (Trending Topic Category) for documentation purposes
'''
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

'''
hover(i)
Hovers over element i
'''
def hover(i):
    hover = ActionChains(driver).move_to_element(i)
    hover.perform()

'''
new_tab(link, category, scrapeID, t)
Gets the tab information for each tab
'''
def new_tab(link, category, scrapeID, t):
    time.sleep(random.randint(10,15))
    outer_l, l = [], []
    rank = 1
    arg = "window.open(\'" + link + "\', 'new_window')"
    driver.execute_script(arg)
    driver.switch_to.window(driver.window_handles[1])
    try:
        driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_c-_")))
        element_to_hover_over = driver.find_element_by_class_name("_c-_")
        hover(element_to_hover_over)
        title = driver.find_element_by_class_name("_c-_").text
        source = driver.find_element_by_class_name("_2ieq").text
        e = driver.find_element_by_tag_name("abbr")
        p_date = e.get_attribute("title")
        ts = driver.find_element_by_class_name("timestampContent").text
        description = driver.find_element_by_class_name("_15ly").text
        link = driver.find_element_by_class_name("_6015").get_attribute("href")
        l.append(t)
        l.append(scrapeID)
        l.append(category)
        l.append(rank)
        l.append(title)
        l.append(source)
        l.append(p_date)
        l.append(ts)
        l.append(description)
        l.append(link)
        outer_l.append(l)
        description = "None"
        p_date = "None"
        ts = "None"
        mini_news_box = driver.find_element_by_class_name("_cw9")
        mini_news = mini_news_box.find_elements_by_tag_name("li")
        for mini in mini_news:
            rank += 1
            l = []
            hover_over = mini.find_element_by_class_name("_6079")
            hover(hover_over)
            source = mini.find_element_by_class_name("_607a").text
            title = mini.find_element_by_class_name("_6079").text
            link = mini.find_element_by_class_name("_607b").get_attribute("href")
            l.append(t)
            l.append(scrapeID)
            l.append(category)
            l.append(rank)
            l.append(title)
            l.append(source)
            l.append(p_date)
            l.append(ts)
            l.append(description)
            l.append(link)
            outer_l.append(l)
    except TimeoutException:
        pass
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return outer_l
'''
get_trendings(id, outer_list, outer_tab, category, ts)
Gets trending and tabs information.
Note: new_tab() is called in this function
'''
def get_trending(id, outer_list, outer_tab, category, ts):
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_class_name("_5myl"))
    current = driver.find_element_by_id(id)
    box = current.find_element_by_class_name("_5myl")
    articles = box.find_elements_by_class_name("_5my2")
    count = 1
    for article in articles:
        temp_list = []
        one_tab = []
        title = article.find_element_by_class_name("_5v0s")
        description = article.find_element_by_class_name("_3-9y")
        source = article.find_element_by_class_name("_1oic")
        link = article.find_element_by_class_name("_4qzh").get_attribute("href")
        temp_list.append(category)
        temp_list.append(title.text)
        temp_list.append(description.text)
        temp_list.append(source.text[2:])
        temp_list.append(link)
        temp_list.append(count)
        temp_list.append(scrapeID)
        temp_list.append(ts.isoformat())
        outer_list.append(temp_list)
        count += 1
        single_tab = new_tab(link, catergory, scrapeID, ts.isoformat())
        outer_tab.append(single_tab)
    return outer_list, outer_tab

'''
scrape_job()
APScheduler's job - all task to scrape Facebook trends and tabs.
'''
def scrape_job():
    print( datetime.datetime.now())
    time.sleep(10)
    driver.refresh()
    load_icon_html()
    time.sleep(2)
    icon_ids = get_icon_id()
    list_of_list, list_of_tab = click_icons(icon_ids)
    with open(filename+".csv", "a",  newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(list_of_list)
    with open("tabs_"+filename+".csv", "a",  newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for a in list_of_tab:
            writer.writerows(a)

if __name__ == "__main__":
    scrapeID = 0
    driver = init_driver()
    log_in(driver, fb_username, fb_password)
    with open(filename+".csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "title", "description", "source", "trendlink", "rank", "scrapeid", "timestamp"]) #Scrap ID
    with open("tabs_"+filename+".csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "scrapeid", "type", "rank", "title", "source", "publishedDate", "timeSince", "description", "url"]) #Scrap ID
    sched = BlockingScheduler()
    job = sched.add_job(scrape_job, "interval", minutes=per_unit, misfire_grace_time=30)
    job.modify(next_run_time=datetime.datetime.now())

    sched.start()
    try:
        time.sleep(1)
    except (KeyboardInterrupt, Exception):
        sched.shutdown()
    driver.quit()
