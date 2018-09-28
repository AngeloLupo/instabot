import time

from flask import Flask
from selenium import webdriver

from setting import USERNAME, PASSWORD

app = Flask(__name__)


def get_driver():
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)
    return driver


def load_page(driver, page, time_to_sleep):
    driver.get(page)
    time.sleep(time_to_sleep)


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def find_elem_by_content(driver, tag, content):
    xpath = "//{}[contains(text(), '{}')]".format(tag, content)
    return driver.find_element_by_xpath(xpath)


def login(driver):
    elems = driver.find_elements_by_tag_name('input')
    username = elems[0]
    username.send_keys(USERNAME)
    password = elems[1]
    password.send_keys(PASSWORD)
    login_button = find_elem_by_content(driver, 'button', 'login')
    login_button.click()


def main():
    driver = get_driver()
    load_page(driver, 'https://www.instagram.com/accounts/login/', 3)
    login(driver)


main()
