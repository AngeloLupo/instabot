import time
import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from settings import USERNAME, PASSWORD, PROFILE


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


def refuse_notifications(driver):
    try:
        refuse_notifications_button = find_elem_by_content(driver, 'button', 'Not Now')
        refuse_notifications_button.click()
        time.sleep(3)
    except NoSuchElementException:
        pass


def go_to_profile_from_home(driver):
    link_to_profile = find_elem_by_content(driver, 'a', PROFILE)
    link_to_profile.click()
    time.sleep(2)


def open_followers_modal_from_profile(driver):
    link_to_followers = driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a')
    link_to_followers.click()
    time.sleep(3)


def get_list_of_followers(driver):
    lists = driver.find_elements_by_tag_name('ul')
    list_of_followers = lists[2]
    last_follower = ''
    while last_follower != list_of_followers.find_elements_by_tag_name('li')[-1]:
        last_follower = list_of_followers.find_elements_by_tag_name('li')[-1]
        scroll_to_element(driver, last_follower)
        time.sleep(0.4)
    return list_of_followers.find_elements_by_tag_name('li')


def save_followers(follower_list):
    time_string = datetime.datetime.now().strftime('%Y%m%d%H%M')
    file = 'followers/{}'.format(time_string)
    with open(file, 'w') as f:
        for item in follower_list:
            f.write(str(item))


def process_followers(followers):
    items_list = followers.split("\\n")
    counter = 0
    pretty_followers = []
    while counter <= len(items_list)-1:
        username = items_list[counter]
        if items_list[counter+1] == 'Follow' or items_list[counter+1] == 'Following':
            pretty_followers.append([
                username,
                '',
                items_list[counter+1]
            ])
            counter = counter + 2
        else:
            pretty_followers.append(
                [
                    items_list[counter],
                    items_list[counter + 1],
                    items_list[counter + 2]
                ]
            )
            counter = counter + 3
    save_followers(pretty_followers)



def main():
    driver = get_driver()
    load_page(driver, 'https://www.instagram.com/accounts/login/', 2)
    login(driver)
    refuse_notifications(driver)
    go_to_profile_from_home(driver)
    open_followers_modal_from_profile(driver)
    followers = get_list_of_followers(driver)
    process_followers(followers)

main()
