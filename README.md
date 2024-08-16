# Zillow_Web_Scraping_And_Auto_Data_Entry

### Objective
Develop a comprehensive Python script that scrapes real estate data from a Zillow-clone website, processes the data, and enters it into a Google Form using Selenium. This project integrates web scraping, data cleaning, and automated data entry to create a structured dataset.

### Step-by-Step Guide

#### Step 1: Set Up Your Google Form

1. **Create a New Google Form**:
   - Navigate to [Google Forms](https://docs.google.com/forms/).
   - Create a new form with the following three short-answer questions:
     1. Property Price
     2. Property Address
     3. Property Link

2. **Get the Form Link**:
   - Click on the "Send" button and copy the link to the form. This link will be used to programmatically submit data.

#### Step 2: Scrape Data from Zillow-Clone Website

1. **Visit the Zillow-Clone Website**:
   - Go to [Zillow-Clone](https://appbrewery.github.io/Zillow-Clone/) and examine the structure of the web page to identify the data elements.

2. **Scrape Listings with BeautifulSoup**:
   - Use the `requests` library to get the HTML content and `BeautifulSoup` to parse the data.

   ```python
   import requests
   from bs4 import BeautifulSoup

   url = "https://appbrewery.github.io/Zillow-Clone/"
   response = requests.get(url)
   soup = BeautifulSoup(response.content, "html.parser")

   listings = soup.find_all("div", class_="list-card-info")

   links = [listing.find("a")["href"] for listing in listings]
   prices = [listing.find("div", class_="list-card-price").text for listing in listings]
   addresses = [listing.find("address", class_="list-card-addr").text for listing in listings]
   ```

3. **Clean Up the Data**:
   - Process the scraped data to remove unnecessary characters and formatting.

   ```python
   cleaned_prices = [price.replace("$", "").replace("+", "").split("/")[0] for price in prices]
   cleaned_addresses = [address.replace("\n", "").replace("|", "").strip() for address in addresses]
   ```

#### Step 3: Automated Data Entry with Selenium

1. **Set Up Selenium**:
   - Install Selenium and set up a WebDriver (e.g., ChromeDriver).

   ```bash
   pip install selenium
   ```

   ```python
   from selenium import webdriver
   from selenium.webdriver.common.by import By
   from selenium.webdriver.common.keys import Keys

   driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
   ```

2. **Fill Out the Google Form**:
   - Use Selenium to open the Google Form and fill it out for each listing.

   ```python
   form_url = "your_google_form_url"
   driver.get(form_url)

   for price, address, link in zip(cleaned_prices, cleaned_addresses, links):
       price_field = driver.find_element(By.XPATH, '//*[@id="your_price_field_xpath"]')
       address_field = driver.find_element(By.XPATH, '//*[@id="your_address_field_xpath"]')
       link_field = driver.find_element(By.XPATH, '//*[@id="your_link_field_xpath"]')

       price_field.send_keys(price)
       address_field.send_keys(address)
       link_field.send_keys(link)

       submit_button = driver.find_element(By.XPATH, '//*[@id="your_submit_button_xpath"]')
       submit_button.click()

       driver.get(form_url)  # Navigate back to the form for the next entry
   ```

3. **Generate Google Sheet from Form Responses**:
   - After submitting all entries, click on the "Sheet" icon in Google Forms to create a Google Sheet with the collected data.

### Prerequisites
- Python 3.x
- `requests`, `beautifulsoup4`, and `selenium` libraries (install using `pip install requests beautifulsoup4 selenium`)
- Google Chrome and ChromeDriver (or another WebDriver of your choice)

### Notes
- Ensure to handle exceptions and errors such as network issues, incorrect data extraction, and form submission errors.
- Securely store and manage sensitive data, such as form URLs and any necessary credentials.
- Be mindful of Google's and the target website's terms of service regarding web scraping and automated actions.

By following this guide, you will create a robust Python script capable of scraping real estate data, processing it, and entering it into a Google Form to generate a structured Google Sheet. This project will enhance your skills in web scraping, data cleaning, and automation.
