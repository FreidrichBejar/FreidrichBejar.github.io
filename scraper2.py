from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

last_name = input("Enter Last Name: ")

service = Service(executable_path=r"C:\Users\bejar.ft\Desktop\VSCode\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://idbop.mylicense.com/verification/")
name_input = driver.find_element(By.ID, 't_web_lookup__last_name')
name_input.send_keys(last_name + Keys.ENTER)

first_name = []
middle_name = []
last_name = []
license_num = []
license_type = []
status = []
orig_date = []
expiry = []
renewed = []

list_id = []

for i in range (3, 43, 1):
    list_id.append(f'//*[@id="datagrid_results__ctl{i}_name"]')

for item in list_id:
    driver.switch_to.window(driver.window_handles[0]) 
    link = driver.find_element(By.XPATH, item)
    link.click()

    driver.switch_to.window(driver.window_handles[1]) 
    name_details = driver.find_elements(By.XPATH, '//*[@id="_ctl27__ctl1_first_name"]')
    for info in name_details:
        first_name.append(info.find_element(By.XPATH, '//*[@id="_ctl27__ctl1_first_name"]').text)
        middle_name.append(info.find_element(By.XPATH, '//*[@id="_ctl27__ctl1_m_name"]').text)
        last_name.append(info.find_element(By.XPATH, '//*[@id="_ctl27__ctl1_last_name"]').text)
        license_num.append(info.find_element(By.XPATH, '//*[@id="_ctl36__ctl1_license_no"]').text)
        license_type.append(info.find_element(By.XPATH, '//*[@id="_ctl36__ctl1_license_type"]').text)
        status.append(info.find_element(By.XPATH, '//*[@id="_ctl36__ctl1_status"]').text)
        orig_date.append(info.find_element(By.XPATH, '//*[@id="_ctl36__ctl1_issue_date"]').text)
        expiry.append(info.find_element(By.XPATH, '//*[@id="_ctl36__ctl1_expiry"]').text)
        renewed.append(info.find_element(By.XPATH, '//*[@id="_ctl36__ctl1_last_ren"]').text)

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="btn_close"]')))

    close_btn = driver.find_element(By.XPATH, '//*[@id="btn_close"]')
    close_btn.click()
    print(first_name)

    WebDriverWait(driver, 240)

dict = {
    'First Name' : first_name, 
    'Middle Name' : middle_name, 
    'Last Name' : last_name,
    'License Number' : license_num,
    'License Type' : license_type,
    'Status' : status,
    'Original Issued Date' : orig_date,
    'Expiration Date': expiry,
    'Renewal Date' : renewed
    }


df = pd.DataFrame(dict)
df.to_csv('IDBOP_Data', sep=',', encoding='utf-8')


# driver.quit()