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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C7C9719FBE3424EF126C036084BA3B31B6BD4F5CAF5C956FD22A39BE1984E7B7F4F025CC53F8BD46EBF9E211A7BD25C861F02545D53D5D7EBBA404340FD5FC32CE7516DC2D2A4535FAAEB10DC14A78F18EACCBC3591EF2DF51AD1DA4F067C772A21C3A03DCE6A8A2F5A49FFA00658AF7E6E8B196EE5B9C9EFF2CBEB65CCF2808F58B92F05A0F243902C50A4FC7E0922ACF343CE411B9C79579D9ECD43AC705AE80F925A55B09D230FD6D0E3E27007A5E57908B202A5D97BBB1595B67FCC82A4A6F56E5739F262F26BC131E1471CF98126E395CB0D83F7949AAB58B6EA6A0CF59E02794DBC332AF91B732943AB96323C9EE3C145EA82A1DC3520C536EA1870A95A2BC15C427343F22939ABB9FA5C5420963DAE2C23D0B6B585439F17EF46DB69C8E04C1149EAD2D0911D3A5AA8C62778DB20AB5251F328A07CEA9991B1CE1F6C33401446CA265F75A6F49256C9BC39411"})
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
