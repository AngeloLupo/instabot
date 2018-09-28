import time

from flask import Flask
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from settings import USERNAME, PASSWORD, PROFILE

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


def find_elem_by_href(driver, tag, content):
    xpath = '//{}[@href="{}"]'.format(tag, content)
    return driver.find_element_by_xpath(xpath)


def login(driver):
    elems = driver.find_elements_by_tag_name('input')
    username = elems[0]
    username.send_keys(USERNAME)
    password = elems[1]
    password.send_keys(PASSWORD)
    login_button = find_elem_by_content(driver, 'button', 'Log in')
    login_button.click()
    time.sleep(3)

    try:
        disable_notifications_button = find_elem_by_content(driver, 'button', 'Not Now')
        disable_notifications_button.click()
        time.sleep(3)
    except NoSuchElementException:
        pass

    link_to_profile = find_elem_by_content(driver, 'a', PROFILE)
    link_to_profile.click()
    time.sleep(2)

    link_to_followers = driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a')
    link_to_followers.click()
    time.sleep(3)

    lists = driver.find_elements_by_tag_name('ul')
    list_of_followers = lists[2]
    last_follower = ''
    while last_follower != list_of_followers.find_elements_by_tag_name('li')[-1]:
        last_follower = list_of_followers.find_elements_by_tag_name('li')[-1]
        scroll_to_element(driver, last_follower)
        time.sleep(0.4)
    list_of_followers = list_of_followers.find_elements_by_tag_name('li')


def main():
    driver = get_driver()
    load_page(driver, 'https://www.instagram.com/accounts/login/', 2)
    login(driver)


main()
