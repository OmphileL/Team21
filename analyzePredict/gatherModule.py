import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver 
# Some utilities needed to work with the data
import json 
import datetime #for date formatting
from time import sleep #introduce delay for pulling data
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
 

def initialize_webdriver():
    # webdriver options help us with their configuration, 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument('--headless') #in this case we want the webdriver to run in the background (i.e. headless mode opens secret browser in background)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options) #create the driver
    return driver

# Take a datetime object and return the date as a string (yyyy-mm-dd)
def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

# Create a twitter search url given a username, start (since), and end (until) dates. 
def form_url(username, since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  username + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
    return p1 + p2

# Add a given number of days to the given date
def increment_day(date, i):
    return date + datetime.timedelta(days=i)


def pull_tweets(username = 'Eskom_SA', start = datetime.datetime(2018, 3, 7, 0, 0, 0), end = datetime.datetime(2018, 3, 9, 23, 59, 59)):
    
    days = (end - start).days + 1 # find the number of days between specified dates
    username = username.lower() # convert username to lowercase
    delay = 2  # time (s) to wait on each page load before reading the page
    tweet_selector = "[class='css-1dbjc4n r-my5ep6 r-qklmqi r-1adg3ll']" #used to identify tweets 
    
    y = []
    tweets_list = []
    for day in range(days):
     
        # Create twitter url between d1 and d2
        d1 = format_day(increment_day(start, 0))
        d2 = format_day(increment_day(start, 1))
        url = form_url(username, d1, d2)
        print(url)
        print(d1)
     
        # open (go to) url using webdriver
        driver = initialize_webdriver()
        driver.get(url)
        sleep(delay)
     
        try:
            # Find tweets in current view by css selector 
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
     
            # Scroll down the webpage and save tweets (and stop when you've reached the end of the page)
            scroll = True
            while scroll:
     
                # scrolling
                print('scrolling down to load more tweets')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
     
                # wait a bit for web elements (tweets) to load (sleep() waits for delay seconds )
                sleep(delay)
     
                # get newly loaded tweets (after scrolling) 
                more_tweets = driver.find_elements_by_css_selector(tweet_selector)
                if len(more_tweets) == len(found_tweets):
                    scroll = False
     
                # Update found tweets
                found_tweets = more_tweets
     
                # print and save tweets in a list
                #print("Printing tweets")
                for tweet in found_tweets:
                    try:
                        #print(tweet.text)
                        tweets_list.append({'date':d1, 'tweet':tweet.text})#.replace('\n', ' ')})
                    except StaleElementReferenceException as e:
                        print('lost element reference', tweet)
     
     
                y.append(len(tweets_list))
            #print('{} tweets found'.format(len(tweets_list)))
     
        except NoSuchElementException:
            print('no tweets on this day')
     
        # increment the start date by 1 day
        start = increment_day(start, 1)
    driver.delete_all_cookies()
    driver.__exit__
    driver.close()
    return pd.DataFrame(tweets_list)
