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
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div/form/div[2]/div/div[1]/div/input")))
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div/form/div[2]/div/div[1]/div/input").send_keys(username)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div/form/div[2]/div/div[2]/div/input").send_keys(password)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div/form/div[4]/div/button").click()

def do2FA(token):
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div[2]/div/div/form/div/div/input")))
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div/div/form/div/div/input").send_keys(token)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/div/div/form/button").click()

def download_activity(dividends_only):
    # Wait for "Invest" menu option to load
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/nav/div[2]/div[2]")))
    # Switch to "Activity" page
    driver.get("https://dashboard.m1.com/d/invest/activity")
    # Wait for "Download" button to load
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[4]/a/span/div")))
    download = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[4]/a/span/div")
    next_button = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[1]/div/button[2]")

    if dividends_only:
        # Click on "Activity type"
        driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[3]/div[1]").click()
        # Hover over "Dividends"
        hoverable = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div/div[3]")
        ActionChains(driver).move_to_element(hoverable).perform()
        time.sleep(0.1)
        # Click on "Only"
        driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div/div[3]/label/a/span").click()
        time.sleep(0.1)

    page = 1
    while next_button.is_enabled():
        print("Downloading page {}".format(page))
        page = page + 1
        download.click()
        next_button.click()
        time.sleep(1)

if __name__ == "__main__":
    driver = get_driver(not DEBUGGING)

    wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(0.5)

    account = account_info("account")

    login(account.get_username(), account.get_password())

    do2FA(account.get_otp())

    download_activity(True)

    # List all the files by time | reverse the order | print all but the first row of each file | reverse the order
    os.system("ls -1t Activity-* | tac | xargs -I{} sh -c 'tail -n +2 \"{}\"' | tac > ./M1Tx.csv")

    if not DEBUGGING:
        driver.quit()

