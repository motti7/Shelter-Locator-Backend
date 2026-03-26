# to opening browser
from selenium import webdriver

# to open chrome with driver
from selenium.webdriver.chrome.service import Service

# to find elements in the page
from selenium.webdriver.common.by import By

# to wait for elements to load
from selenium.webdriver.support.ui import WebDriverWait

# to install and setting  up chrome deiver
from webdriver_manager.chrome import ChromeDriverManager

import csv

import time


SCRAPING_URL = "https://www.petah-tikva.muni.il/Emergency/Pages/Receivers.aspx"
PTK_CSV = "shelters_ptk.csv"



# This script scrapes the shelters data from the Peta Tikva municipality website and saves it to a CSV file.
def script_ptk_shelters():
    
    # download ChromeDriver 
    service = Service(ChromeDriverManager().install())
    # open Chrome browser
    driver = webdriver.Chrome(service=service)
    # navigate to the Peta Tikva emergency shelters page
    driver.get(SCRAPING_URL)
    # wait for the page to load
    wait = WebDriverWait(driver, 15)


    shelters_data = []
    # we will loop through the pages of the shelters tables and for each table we extract the relevant data of each shelter, and saving it in the shelters data list
    while True:

        # wait for the table to be present
        time.sleep(2)  
    
        tables = driver.find_elements(By.TAG_NAME, 'table')

        # we now that the shelters table is the fourth one (index 3)
        table = tables[3]  

        # we saving all the table rows into a selenium object
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # skip the header row
        for row in rows[1:]:

            # get all the columns in the row
            cols = row.find_elements(By.TAG_NAME, 'td')


            # we taking all the relavant columns as a strings  
            address = cols[2].text.strip()

            shelter_type = cols[3].text.strip()
            if not shelter_type:
                shelter_type = "סוג מקלט: לא זמין"

            place_name = cols[4].text.strip()
            if not place_name:
                place_name = "שם מקום: לא זמין"


            # append the data to our list
            shelters_data.append([address, shelter_type, place_name])

        # try to find the "next" button and click it
        try:
            next_button = driver.find_element(By.XPATH, "//a[@title='הבא']")
            next_button.click()
        # in the last iteration, there will be no "next" button, so we break the loop
        except:
            break  


    # save the data to a CSV file
    with open(PTK_CSV, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['כתובת', 'סוג מקלט', 'שם מקום'])
        writer.writerows(shelters_data)

    # close the browser
    driver.quit()

    print(f"end, saved {len(shelters_data)} rows to {PTK_CSV}")