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

## Feature
* Proxy (Northern California)
* AWS cloud database
* AWS cloud server

## Version
#### Cloud
* Google Chrome: google-chrome-stable-66.0.3359.117-1.x86_64 
* Firefox: 52.8.0
* ChromeDriver: 2.38.552522
* GeckoDriver: 0.20.1
* Selenium: 3.12.0
* Python: 3.6

## Installation 
#### Windows
1. Download Git from https://git-scm.com/download/win
2. Clone the repo <br>
*git clone https://github.com/comp-journalism/fb-trends.git*
3. To activate the virtual environment <br>
*.\Scripts\Activate*
4. Install pip <br>
https://pip.pypa.io/en/stable/installing/
5. Get Python frameworks, libraries, software and resources. <br>
*python -m pip install awesome_package (more info at https://github.com/vinta/awesome-python)*
6. Get AP Scheduler <br>
*pip install apscheduler*
7. Get pyvirtualdisplay <br>
*pip3.5 install pyvirtualdisplay*
8. Get Selenium Webdriver <br>
*python -m pip install -U selenium*
9. Get pymysql <br>
*install pymysql*

#### Linux (AWS Red Hat Fedora) 
1. Install git <br>
*yum install git*
2. Clone repo <br>
*git clone https://github.com/comp-journalism/fb-trends.git*
3. *cd fb-trends*
4. Now you can run your code on the cloud! :thumbsup:
##### Firefox on Linux
1. Download geckodriver at https://github.com/mozilla/geckodriver/releases
2. Extract the downloaded file <br>
*tar xvzf filename.tar.gz*
3. Add geckodriver to PATH <br>
*export PATH=$PATH:/path/to/geckodriver*
4. Install Firefox <br>
*yum install firefox*
5. Install pyvirtualdisplay <br>
*pip install pyvirtualdisplay selenium*
6. Install Xvfb <br>
*sudo yum install Xvfb*

## Common Errors
* Q: selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary <br> A: https://askubuntu.com/questions/708581/have-installed-chrome-on-ubuntu-however-cannot-find-where-to-run-it
* Q: selenium.common.exceptions.WebDriverException: Message: 'chromedriver.exe' executable may have wrong permissions. Please see https://sites.google.com/a/chromium.org/chromedriver/home <br>
A: sudo chmod 777 chromedriver.exe
* Q: selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally <br>
A: https://stackoverflow.com/questions/22558077/unknown-error-chrome-failed-to-start-exited-abnormally-driver-info-chromedri
* Q: ModuleNotFoundError: No module named 'pyvirtualdisplay'<br>
A: https://github.com/timgrossmann/InstaPy/issues/10
* Q: No package xvfb available. No package xserver-xephyr available <br>
A: https://serverfault.com/questions/344793/install-xvfb-via-yum-yum-repository-for-xvfb
* Q: ModuleNotFoundError: No module named 'pyvirtualdisplay'<br>
A: https://github.com/timgrossmann/InstaPy/issues/727 <br>
pip install pyvirtualdisplay -U
* Q: ModuleNotFoundError: No module named 'pymysql'<br>
A: Pip install pymysql
* Q: How to get root access on cloud <br>
A: Sudo su

