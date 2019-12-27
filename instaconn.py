# _*_ coding:utf-8 _*_
# @author Robert Carlos                 #
# email robert.carlos@linuxmail.org     #
# 2019-Dec (CC BY 3.0 BR)               #

import argparse
import errno
from sys import exit

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from packs.get_args import get_args


class InstaConn:

    def __init__(self, username, password, location_url, driver):
        self.username = username
        self.password = password
        self.location_url = location_url
        self.driver = driver

    def login(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username')))
        finally:
            username_field = self.driver.find_element_by_name('username')
            password_field = self.driver.find_element_by_name('password')
            username_field.clear()
            password_field.clear()
            actions = ActionChains(self.driver).click(username_field).send_keys(
                self.username).click(password_field).send_keys(self.password).send_keys(Keys.RETURN)
            actions.perform()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[contains(text(), "Agora não")]')))
        finally:
            try:
                self.driver.find_element_by_xpath(
                    '//button[contains(text(), "Agora não")]').click()
            except Exception:
                self.driver.find_element_by_link_text('Agora não').click()

    def home(self):
        self.driver.find_element_by_xpath(
            f"//a[contains(@href,'/{self.username}')]").click()

    def quit_browser(self):
        self.driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Robo de automação")
    parser.add_argument('-f', action='store', dest='file',
                        default='instaconn.properties', required=False,
                        help='arquivo de propriedades')
    arguments = parser.parse_args()
    args_file = get_args(arguments.file)
    driver = webdriver.Chrome(executable_path=args_file['chromedriver_path'])
    driver.get(args_file['login_ig'])
    try:
        instaconn = InstaConn(
            args_file['username'], args_file['password'],
            args_file['location_url'], driver)
        instaconn.login()
        instaconn.home()
        input("Pressione uma tecla para sair.")
    except KeyboardInterrupt:
        print('Bye')
        exit(errno.EPERM)
    finally:
        instaconn.quit_browser()
