from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

G_GORM_URL = ("https://docs.google.com/forms/d/e/1FAIpQLSdSNsxrImTGuz1xoZbNbANXYNIvIkCHkz8YndnKzDjVi7-U3w/viewform?usp=sf_link")
Zillow_URL = "https://appbrewery.github.io/Zillow-Clone/"


# TODO 1: Find address, price/month, and property link for each of properties on the listing
response = requests.get(url="https://appbrewery.github.io/Zillow-Clone/")
Zillow_webpage = response.text

soup = BeautifulSoup(Zillow_webpage, "html.parser")

# Find all the addresses
all_addresses_elements = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.getText().replace("\n", " ").replace("|", "").strip() for address in all_addresses_elements]
# print(f"\n After clean-up, now the {len(all_addresses_elements)} addresses look like this: \n")
# print(all_addresses)

# Find all the links
all_links_elements = soup.select(".StyledPropertyCardDataWrapper a")
all_links = [link.get("href") for link in all_links_elements]
# print(f"The {len(all_links_elements)} links look like this: \n")
# print(all_links)

# Find all the prices
all_price_elements = soup.select(".StyledPropertyCardDataWrapper span")
all_prices = [price.getText().replace("/mo", "").split("+")[0] for price in all_price_elements if "$" in price.text]
# print(f"The {len(all_price)} links look like this: \n")
# print(all_price)

# TODO 2: To fill in the G-form via Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for index in range(len(all_addresses)):
    try:
        driver.get(G_GORM_URL)
        # Wait the G-form being loaded
        time.sleep(2)
        input_addr_property = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        input_addr_property.send_keys(all_addresses[index])
    except NoSuchElementException:
        print("Address input not found")
    except ElementClickInterceptedException:
        print("Address input not interactable")

    try:
        time.sleep(1)
        input_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        input_price.send_keys(all_prices[index])
    except NoSuchElementException:
        print("Price input not found")
    except ElementClickInterceptedException:
        print("Price input not interactable")

    try:
        time.sleep(1)
        input_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        input_link.send_keys(all_links[index])
    except NoSuchElementException:
        print("Link input not found")
    except ElementClickInterceptedException:
        print("Link input not interactable")

    # Submit the respose
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    # Submit another response
    time.sleep(1)
    submit_another = driver.find_element(By.CSS_SELECTOR, ".c2gzEf a")
    submit_another.click()

    time.sleep(1)




