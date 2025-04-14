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
                        "value": "000DF5EED53F0347110122295069DFCAB1252A260D6DE6CCDDCB7B47AB17E9D9899837247337E4EAB4BDEC824DBA99DC8A4A76D5E00F68E6B5EA256F24E3744061039EBF9AE87E0DFE6AABC2B110D089AFE3FAECAF1E59DD31D1C90765193D40A29FC8F4D989A0A5698E3036E731D5CF0864529592752F4EC1820D50EE5BB742C9CFF244D3F331FEB4DDFC186A0F32C9E2E6E38361EB714B0047FA5838D9859E9D668CBF1692A27A24616E6F6F250E418D423C4792B1D5B33C8502616A449503DB662100759779BF09A36AFD6DE975638355E84F8CA38939ED33611CBE61AC66B0D6C78E92081058DC53E8D63148C8545CDF55506899525E4904C17A08504F4D7F1D8F569493FB755ECFC055203AD928F65AAC6E6FA3AB0128E90F3B6CDEE71ACE7C4CFEF7826AB8AFB23A13613D73582F9506621385A8C939C6D2D95C122A601C8FC500461446B41E41D41DABC5B8BA56"})
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
