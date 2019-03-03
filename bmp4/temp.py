#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/2 11:33 
# @File : temp.py
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException


def firfoxtest():
    fireFoxOptions = webdriver.FirefoxOptions()

    firefox_profile = webdriver.FirefoxProfile()
    # Disable CSS
    firefox_profile.set_preference('permissions.default.stylesheet', 2)
    # Disable images
    firefox_profile.set_preference('permissions.default.image', 2)
    # Disable Flash
    firefox_profile.set_preference("plugin.state.flash", 0)

    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # Set the modified profile while creating the browser object
    fireFoxOptions.add_argument('-headless')
    fireFoxOptions.add_argument(("--proxy-server=http://" + '127.0.0.1:1080'))
    driver = webdriver.Firefox(firefox_profile=firefox_profile, options=fireFoxOptions)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 1)
    driver.get('https://voyeurhit.com/videos/hidden-cam-under-desk-caught-my-mom-masturbating/')
    download_url = driver.execute_script(
        "return window.pl3748.getConfig().playlistItem.allSources[1].file")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 2)
    print(download_url)
    # driver.quit()


def chrometest(times):
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-bundled-ppapi-flash")
    prefs = {"profile.managed_default_content_settings.images": 2}

    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--proxy-server=http://" + '127.0.0.1:1080')
    driver = webdriver.Chrome(options=chrome_options)

    # path_to_extension = sys.path[0]+r'\3.4.3_0'
    # path_to_extension = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User ' \
    #                     'Data\Default\Extensions\cfhdojbkjhnklbpkdaibdccddilifddb '
    # chrome_options.add_argument('load-extension=' + path_to_extension)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 3)
    driver.set_page_load_timeout(times)
    try:
        driver.get('https://voyeurhit.com/videos/hidden-cam-under-desk-caught-my-mom-masturbating/')
        driver.execute_script('return window.stop()')
        download_url = driver.execute_script(
            "return window.pl3748.getConfig().playlistItem.allSources[1].file")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 3.1)
        print(download_url)
    except TimeoutException:
        try:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 4)
            driver.execute_script('return window.stop()')
            download_url = driver.execute_script(
                "return window.pl3748.getConfig().playlistItem.allSources[1].file")
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 5)
            print(download_url)
        except TimeoutException:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 6)
        except WebDriverException:
            pass

    # driver.quit()


for i in range(5,10):
    print('水平不行啊：',i)
    chrometest(i)
