from account_info import account_info

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver(headless):
    if headless == True:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    else:
        driver = webdriver.Chrome()

    return driver

def login(username, password):
    driver.get("https://dashboard.m1.com/login")
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div/form/div[2]/div/div[1]/div/input")))
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div/form/div[2]/div/div[1]/div/input").send_keys(username)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div/form/div[2]/div/div[2]/div/input").send_keys(password)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div/form/div[4]/div/button").click()

def do2FA(token):
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div[2]/div/div/form/div/div/input")))
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div/div/form/div/div/input").send_keys(token)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div/div/form/button").click()

if __name__ == "__main__":
    driver = get_driver(False)

    wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(0.5)

    account = account_info("account")

    login(account.get_username(), account.get_password())

    do2FA(account.get_otp())

# Comment this out to leave the browser window open
#   driver.quit()

