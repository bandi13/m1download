from account_info import account_info

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

DEBUGGING=False

def get_driver(headless):
    options = webdriver.ChromeOptions()

    # Put downloads in current directory
    prefs = {
        "download.default_directory": os.getcwd(),
        "download.directory_upgrade": True,
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)

    if headless == True:
        options.add_argument("--start-maximized");
        options.add_argument('--headless=new')

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)

    return driver

def login(username, password):
    driver.get("https://dashboard.m1.com/login")
    username_field = "/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/form/div[2]/div/div[1]/div/input"
    password_field = "/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/form/div[2]/div/div[2]/div/input"
    submit_button = "/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/form/div[4]/div/button"
    wait.until(EC.visibility_of_element_located((By.XPATH, username_field)))
    driver.find_element(By.XPATH, username_field).send_keys(username)
    driver.find_element(By.XPATH, password_field).send_keys(password)
    driver.find_element(By.XPATH, submit_button).click()

def do2FA(token):
    authcode_field = "/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div/form/div/div/input[1]"
    submit_button = "/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div/form/button"
    wait.until(EC.visibility_of_element_located((By.XPATH, authcode_field)))
    driver.find_element(By.XPATH, authcode_field).send_keys(token)
    driver.find_element(By.XPATH, submit_button).click()

def download_activity():
    # Wait for "Invest" menu option to load
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[2]/nav/div[2]/div[3]")))
    # Switch to "Activity" page
    driver.get("https://dashboard.m1.com/d/invest/activity")
    # Wait for "Download" button to load
    download_xpath = "/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[4]/button"
    wait.until(EC.visibility_of_element_located((By.XPATH, download_xpath)))

    download = driver.find_element(By.XPATH, download_xpath)
    download.click()

    time.sleep(5)

if __name__ == "__main__":
    driver = get_driver(not DEBUGGING)

    if DEBUGGING:
        wait = WebDriverWait(driver, 30)
    else:
        wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(0.5)

    account = account_info("account")

    login(account.get_username(), account.get_password())

    do2FA(account.get_otp())

    download_activity()

    # List all the files by time | reverse the order | print all but the first row of each file | reverse the order
    os.system("filter.sh Activity-* > ./M1Tx.csv")

    if not DEBUGGING:
        driver.quit()

