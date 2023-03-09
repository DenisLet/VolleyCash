import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

browser = webdriver.Chrome()
browser
browser.get("https://www.oddsportal.com/matches/handball/")

match_list = browser.find_elements(By.CSS_SELECTOR,".name a")

count = 0
for i in match_list:

   link = i.get_attribute("href")
   if "www" in link:
      print(link)
      count+=1
print(count)







time.sleep(3)
browser.quit()

