from selenium import webdriver
from utils import extracting_channel_videos

page_url = input('Please enter your YouTube URL: ')

driver = webdriver.Chrome()
extracting_channel_videos(page_url, driver)

driver.quit()
