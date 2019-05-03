import time
import datetime
import json

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
    try:
        login_button = find_elem_by_content(driver, 'div', 'Log in')
    except NoSuchElementException:
        login_button = find_elem_by_content(driver, 'div', 'Log In')
    login_button.click()
    time.sleep(4)


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
    time.sleep(4)


def open_followers_modal_from_profile(driver):
    # link_to_followers = driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a')
    link_to_followers = find_elem_by_href(driver, 'a', '/{}/followers/'.format(PROFILE))
    link_to_followers.click()
    time.sleep(3)


def get_list_of_followers(driver):
    lists = driver.find_elements_by_tag_name('ul')
    list_of_followers = lists[-1]
    last_follower = ''
    while last_follower != list_of_followers.find_elements_by_tag_name('li')[-1]:
        last_follower = list_of_followers.find_elements_by_tag_name('li')[-1]
        scroll_to_element(driver, last_follower)
        time.sleep(0.9)
    return list_of_followers.find_elements_by_tag_name('li')


def close_followers_modal(driver):
    close_button = driver.find_element_by_class_name('glyphsSpriteX__outline__24__grey_9')#
    close_button.click()
    time.sleep(1)


def open_following_modal_from_profile(driver):
    # link_to_followers = driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a')
    link_to_followers = find_elem_by_href(driver, 'a', '/{}/following/'.format(PROFILE))
    link_to_followers.click()
    time.sleep(3)


def get_list_of_following(driver):
    lists = driver.find_elements_by_tag_name('ul')
    list_of_following = lists[-1]
    last_following = ''
    while last_following != list_of_following.find_elements_by_tag_name('li')[-1]:
        last_following = list_of_following.find_elements_by_tag_name('li')[-1]
        scroll_to_element(driver, last_following)
        time.sleep(1)
    return list_of_following.find_elements_by_tag_name('li')


def save_follows(follows_list, directory, time_string=None):
    if not time_string:
        time_string = datetime.datetime.now().strftime('%Y%m%d%H%M')
    file = '{}/{}'.format(directory, time_string)
    dict_follows = {}
    for item in follows_list:
        dict_follows[item[0]] = [item[1], item[2]]

    json_follows = json.dumps(dict_follows)
    with open(file, 'w') as f:
        f.write(json_follows)
        f.close()


def process_follows(follows):

    pretty_follows = []

    for x in follows:
        s = x.text.split("\n")
        if len(s) == 2:
            pretty_follows.append(
                [
                    s[0],
                    '',
                    s[1]
                ]
            )
        else:
            pretty_follows.append(
                [
                    s[0],
                    s[1],
                    s[2]
                ]
            )
    return pretty_follows


def main():
    driver = get_driver()
    load_page(driver, 'https://www.instagram.com/accounts/login/', 2)

    login(driver)

    refuse_notifications(driver)

    go_to_profile_from_home(driver)

    time_string = datetime.datetime.now().strftime('%Y%m%d%H%M')

    open_followers_modal_from_profile(driver)
    followers = get_list_of_followers(driver)
    pretty_followers = process_follows(followers)
    save_follows(pretty_followers, 'followers', time_string)

    close_followers_modal(driver)

    open_following_modal_from_profile(driver)
    following = get_list_of_following(driver)
    pretty_following = process_follows(following)
    save_follows(pretty_following, 'following', time_string)


main()
