from selenium import webdriver
import re
import os
import csv
import openpyxl
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

chrome_options = webdriver.ChromeOptions()  
#chrome_options.add_argument('--headless')     
service = Service(executable_path=r"Your_Path/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

wb = openpyxl.Workbook()
ws = wb.active

xpath_exist = '//*[@id="__next"]/div/div/div[5]/div[3]/main/header/div[1]/div[1]/div[1]'
csv_file_path = f'cars.csv'
# Function to check if an element exists
def check_element_exists(driver, xpath_exist):
    try:
        driver.find_element(By.XPATH, xpath_exist)
        return True
    except NoSuchElementException:
        return False
if os.path.exists(csv_file_path):
    os.remove(csv_file_path)
for i in range(1,20):
    if check_element_exists(driver, xpath_exist) == True:
        break
    else:
        url = f'https://www.autoscout24.hu/lst/audi/rs4?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&fregto=2002&ocs_listing=include&page={i}&powertype=kw&search_id=1lp5nzyo8ej&sort=standard&source=listpage_pagination&ustate=N%2CU'
        driver.get(url)
        if i == 1:
            cookie_path = '//*[@id="as24-cmp-popup"]/div/div[3]/button[2]'
            cookie = driver.find_element(By.XPATH, cookie_path)
            cookie.click()

        change_car = 'audi-rs4'
        xpath = '//*[@id="__next"]/div/div/div[5]/div[3]/main'
        element = driver.find_element(By.XPATH, xpath)
        links = element.find_elements(By.TAG_NAME, 'a')
        href_values = [link.get_attribute('href') for link in links]
        audi_links = [href for href in href_values if change_car in href]
        data = element.text.split('\n')

        date_pattern = re.compile(r'^\d+ \/\ \d+$')

        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            row_data = []
            for item in data:
                if 'Megosztás' in item:
                        continue
                if 'Kedvencek közé' in item:
                        continue
                if '+ További járművek a kereskedésből' in item:
                        continue
                if date_pattern.search(item):
                    continue
                if 'Audi RS4' in item:
                    if row_data:
                        csv_writer.writerow(row_data)
                    row_data = [item]
                if 'Vissza' in item:
                    break
                else:
                    row_data.append(item)
            if row_data:
                csv_writer.writerow(row_data)
        column_name = "Link"
        xlsx_file_path = 'links.xlsx'
        if i == 1:
            ws.append([column_name])
            for href in audi_links:
                ws.append([href])
        else:
             for href in audi_links:
                ws.append([href])

        wb.save(xlsx_file_path)

        print(f"Data from {url} has been saved to {xlsx_file_path}")
driver.quit()
