from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def get_driver():
  # Set options to make browsing easier
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")

  driver = webdriver.Chrome(options=options)
  driver.get("https://quotes.toscrape.com/login/")
  return driver

def clean_text(text):
  """ Extract only the temperature from text """
  """ Extract goodreads page url from webpage """
  return float(text.split(":")[1].strip())
  

def main():
  driver = get_driver()
  
  # Find and fill in username and password
  driver.find_element(by="id", value="username").send_keys("admin")
  time.sleep(2)
  driver.find_element(by="id", value="password").send_keys("admin" + Keys.RETURN)
  time.sleep(2)
  
  # Click on Home link and wait 2 seconds
  driver.find_element(by="xpath", value="/html/body/nav/div/a").click()
  time.sleep(2)
  
  # Scrape the temperature value
  text = driver.find_element(by="xpath", value="/html/body/div[1]/div/h1[2]").text
  return clean_text(text)

print(main())