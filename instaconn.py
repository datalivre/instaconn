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

    def __init__(self, username, password, driver):
        self.username = username
        self.password = password
        self.driver = driver

    def login(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username')))
        finally:
            user_pass_list = [self.driver.find_element_by_name(field) for field in [
                'username', 'password']]
            actions = ActionChains(self.driver).click(user_pass_list[0]).send_keys(
                self.username).click(user_pass_list[1]).send_keys(self.password).send_keys(Keys.RETURN)
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
                        default='files/instaconn.properties', required=False,
                        help='arquivo de propriedades')
    arguments = parser.parse_args()
    args_file = get_args(arguments.file)
    driver = webdriver.Chrome(executable_path=args_file['chromedriver_path'])
    driver.get(args_file['login_url'])
    try:
        instaconn = InstaConn(
            args_file['username'], args_file['password'], driver)
        instaconn.login()
        instaconn.home()
        input("Pressione uma tecla para sair.")
    except KeyboardInterrupt:
        exit(errno.EPERM)
    finally:
        print('Bye')
        instaconn.quit_browser()
