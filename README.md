# Facebook Trends
Shin Lee's Northwestern University MMSS Senior Thesis

## Project
### This code collects Trending Topic data from Facebook Using Selenium
<dl>
  <dt>The Code Collects the Following</dt>
  <dd>1. Trending Topics (Category, Title, Description, TrendLink, Ranking, ScrapeID, Timestamp, Source)</dd>
  <dd>2. Each Trending Topics Tabs (Category, Title, Description, Unique URL, Ranking, ScrapeID, Timestamp, Source, Published Date, Time Since published) </dd>
  <dt>The Code Computes the Following</dt>
  <dd>1. Jaccard Similarites including average, min, max, and standard deviation</dd>
  <dd>2. Gets the cumulative new Trending Topics </dd>
  <dd>3. Compares the number of cumulative new Trending Topics between two CSV (per category and overall)</dd>
  <dd>4. Gets total unique URLs from Trending Topic Tabs (per category and overall) </dd>
  <dd>5. Ranks the news sources by number of articles </dd>

</dl>

## Installation 

## Common Errors
* Q: selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary A: https://askubuntu.com/questions/708581/have-installed-chrome-on-ubuntu-however-cannot-find-where-to-run-it
* selenium.common.exceptions.WebDriverException: Message: 'chromedriver.exe' executable may have wrong permissions. Please see https://sites.google.com/a/chromium.org/chromedriver/home
sudo chmod 777 chromedriver.exe"
selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally
https://stackoverflow.com/questions/22558077/unknown-error-chrome-failed-to-start-exited-abnormally-driver-info-chromedri
ModuleNotFoundError: No module named 'pyvirtualdisplay'
https://github.com/timgrossmann/InstaPy/issues/10
No package xvfb available. No package xserver-xephyr available
https://serverfault.com/questions/344793/install-xvfb-via-yum-yum-repository-for-xvfb
ModuleNotFoundError: No module named 'pyvirtualdisplay'
https://github.com/timgrossmann/InstaPy/issues/727
pip install pyvirtualdisplay -U
selenium.common.exceptions.WebDriverException: Message: 'chromedriver.exe' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home
 name 'MySQLdb' is not defined
selenium.common.exceptions.WebDriverException: Message: chrome not reachable
ModuleNotFoundError: No module named 'pymysql'
Pip install pymysql
TypeError: not enough arguments for format string

