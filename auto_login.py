# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", 
                        "value": "00B2B63C9D46598DAC41E86FF54167583EB8A0DDAE954DFD125D1BE78651E5D52A00FCCBBFB29A4F073BCBBF925C2F3203FAADA362DA40BF7BCC30C34FC6FC7816C343E6EEF229F90C90B68C610DDA5C5467517812F69C344174BBEDE3C7ED3A0B59426672575C9C234DCE23F8D4F519D0654CE00ACB43DA30ABBEFC8A097738F04090B41D01675F34339AFE8A0114472FCCF1F7438DDF73ED75302B031ED37C456F67E1816D9F16B826537A2146BA2749ADFFF04B2D5F79AF41D28E504CC8C35E16DCDE4151E03CC5C47A7CA58A5AA3BFDA3E654FEA30FB00DCB49A6F13AEEF3F3206BD5A8F4F6D30FB446857FD58513415724780C222E52D669621BCE2483CC76B35D229160A94600425833FADD563C7398A194CF918E699CC42E8CD304263C43DDDBA744B6F438C64FC55EA2EBA4A3F0F0972C840ED84E4DC45918DA10544B4C0739C4A9C072A5FB0EA11BAD64AF08D"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
