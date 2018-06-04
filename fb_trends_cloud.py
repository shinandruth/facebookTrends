#fb_trends_cloud.py

import time
import csv
import datetime
import os
import configparser
import random
import pymysql.cursors

from urllib.request import urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from time import gmtime, strftime
from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

link = "http://www.facebook.com"
os.environ["LANG"] = "en_US.UTF-8"

#----------------SET chrome_driver_name/gecko_driver TO LOCATION OF YOUR CHROME DRIVER--------------------------
chrome_driver = "/home/ec2-user/selenium_env/chromedriver"
gecko_driver = "/home/ec2-user/selenium_env/geckodriver"
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
    display = Display(visible=0, size=(1366,768))
    display.start()
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("start-maximized")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument("--disable-setuid-sandbox")
    # chrome_options.add_argument('--disable-extensions')
    # driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
    #----------------Firefox--------------
    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = False

    firefox_options = webdriver.FirefoxOptions()
    #firefox_options.add_argument("start-maximized")
    firefox_options.add_argument("--headless")
    #firefox_options.add_argument('--disable-gpu')
    #firefox_options.add_argument('--no-sandbox')
    #firefox_options.add_argument("--disable-setuid-sandbox")
    #firefox_options.add_argument('--disable-extensions')
    driver = webdriver.Firefox(capabilities=cap, executable_path=gecko_driver, firefox_options=firefox_options)
    #-------------------------------------
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
        print("log in success")
    except Exception:
        print("Username, password, and/or log in button not found at", link)
        driver.refresh()

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
        load_icon_html(driver)
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
    driver.get_screenshot_as_file('/home/ec2-user/selenium_env/google.png')
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
def get_trending(id, outer_list, outer_tab, catergory, ts):
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
        temp_list.append(catergory)
        temp_list.append(title.text)
        temp_list.append(description.text)
        temp_list.append(link)
        temp_list.append(count)
        temp_list.append(scrapeID)
        temp_list.append(ts)
        temp_list.append(source.text[2:])
        outer_list.append(temp_list)
        if count == 1:
            single_tab = new_tab(link, catergory, scrapeID, ts)
            outer_tab.append(single_tab)
        count += 1
    return outer_list, outer_tab

'''
scrape_job()
APScheduler's job - all task to scrape Facebook trends and tabs.
'''
def scrape_job():
    print(datetime.datetime.now())
    time.sleep(5)
    driver.refresh()
    load_icon_html()
    time.sleep(2)
    icon_ids = get_icon_id()
    list_of_list, list_of_tab = click_icons(icon_ids)
    with db.cursor() as cursor:
        sql_trends = "INSERT INTO TRENDS_ONLY_CLOUD(Category, Title, Description, TrendLink, Ranking, ScrapeID, TS, Source)  VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        cursor.executemany(sql_trends, list_of_list)
        sql_tabs = "INSERT INTO TABS_CLOUD(TS, ScrapeID, Category, Ranking, Title, Source, PublishedDate, TimeSince, Description, URL)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql_tabs, list_of_tab)
    db.commit()
    print("----------------------finished one scrape------------------------------")

if __name__ == "__main__":
    driver = init_driver()
    log_in(driver, fb_username, fb_password)
    scrapeID = 0
    sched = BlockingScheduler()
    job = sched.add_job(scrape_job, "interval", minutes=per_unit, misfire_grace_time=30)
    job.modify(next_run_time=datetime.datetime.now())
    sched.start()
    try:
        time.sleep(1)
    except (KeyboardInterrupt, Exception):
        sched.shutdown()
    db.close()
    driver.quit()
