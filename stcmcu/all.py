import time
import logging
from random import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

account_list = {
# Accounts
"<Username>" : "<Passwd>",
}

f = open('website.txt', encoding='utf-8')
webpage = []
for line in f:
    webpage.append(line.strip())
f.close

logging.basicConfig(filename='all.log', encoding='utf-8', level=logging.INFO,
format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y/%m/%d %a %H:%M:%S')
logging.info('Script launched')

for account in account_list:
    my_username = account
    my_password = account_list[account]
    logging.info('Account: %s', my_username)

    try:
        launch_options = webdriver.ChromeOptions()
        launch_options.add_argument('--incognito')
        driver = webdriver.Chrome(options=launch_options)
        logging.info('Webdriver launched')

        driver.get("https://www.stmcu.com.cn/")
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "登录").click()
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "账号密码登录").click()
        time.sleep(1)
        driver.find_element(By.ID, "username").send_keys(my_username)
        driver.find_element(By.ID, "password").send_keys(my_password)
        driver.find_element(By.CSS_SELECTOR, ".an_lan").click()
        time.sleep(1)
        logging.info('%s login successful', my_username)

        driver.get("https://www.stmcu.com.cn/User/UserCenter")
        time.sleep(1)
        points_read = driver.find_element(By.CLASS_NAME, "zt_r").text
        logging.info('Checking initial points: %s', points_read)
        initial_points = int(points_read)

        rd = [randrange(1400) for j in range(100)]
        js = ''
        count = 0

        logging.info('Download loop starting')
        for i in rd:
            js = 'window.open("' + webpage[i] + '");'
            driver.execute_script(js)
            time.sleep(1)
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])  
            try:
                download_btn = driver.find_element(By.XPATH, '//*[@id="down_load_btn"]')  
            except NoSuchElementException:
                logging.warning('Invalid URL. Skipping')
            else:
                download_btn.click()
                count += 1
                logging.info('%d files fetched', count)
                if count >= 30:
                    time.sleep(1)
                    driver.get("https://www.stmcu.com.cn/User/UserCenter")
                    time.sleep(1)
                    cur_points_read = driver.find_element(By.CLASS_NAME, "zt_r").text
                    cur_points = int(cur_points_read)
                    award_points = cur_points - initial_points
                    if award_points >= 297:
                        logging.info('Account %s gained %d - %d = %d points',
                        my_username, cur_points, initial_points, award_points)
                        break
                else:
                    time.sleep(2)
        logging.info('Webdriver quitting')
        driver.quit()
    except:
        logging.critical("Unexpected error or browser closed by user")
        driver.quit()
        quit(1)
quit(0)