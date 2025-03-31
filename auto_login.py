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
                        "value": "00277D17885357CFC8CC8461590EB7F2EEF78062222118785D6A77E6B772D6AD501B2406D15BF69663B1118090EBF43838F541CE1BDAD0E5F8F465845FA2C14BCE093DE8A51057B036BF81698C425C4228BDE3204CC4E16073733E02AE1DC0A81E72FD476B3FA1595FEEADF5B80BEC39DEA7CA729029BDCBDA1A3AA4ACA75C4948AC991E31562AEEF5A09E80057C6BE789FF9675D7DE753FAEB47D2472136E2D7232DA63E0526C317768A1411C643DCED2FEF9D3D208095AF055D7BCA65EF41384E892F08B75BFE2E4223BB70C3D6B5FFEBC8DA13A12096DE9E8B6B4468DA540B139EF92FA5B3131C64DEB8CE5B0CD9A7C12BF50B2B55828F659250F007C98ABFF281149BB877B961E205CE5C0A375E7DCCBD4999B8F7F72B9EFA0F5094432388BD6389C17E12066925CD544DBE845C3792F04E100E234E6CF58786CE49D8D1065F7EF871D2607205A51AA74EBDDB2FF48
                        "})
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
