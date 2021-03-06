from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


# https://selenium-python.readthedocs.io/installation.html
# https://www.youtube.com/watch?v=Xjv1sY630Uc

def main():
    user_name = input('Enter instagram username: ')
    pw = input('Enter instagram password:   ')

    wait_duration = 10  # seconds
    PATH = "C:\\Program Files (x86)\\ChromeDriver\\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    # An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying to find any element (
    # or elements) not immediately available. The default setting is 0 (zero). Once set, the implicit wait is set for
    # the life of the WebDriver object.
    driver.implicitly_wait(wait_duration)  # seconds

    driver.get("https://www.instagram.com/")

    user_name_input = driver.find_element_by_name('username')
    password_input = driver.find_element_by_name('password')

    user_name_input.send_keys(user_name)
    password_input.send_keys(pw, Keys.ENTER)

    driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()  # Do you want to save info? => no
    driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()  # Notifications => no

    driver.find_element_by_link_text(user_name).click()  # Go to profile page

    class_name = 'isgrP'

    driver.find_element_by_css_selector(f'a[href="/{user_name}/followers/"]').click()
    follower_set = get_user_set(driver, class_name)

    driver.back()

    driver.find_element_by_css_selector(f'a[href="/{user_name}/following/"]').click()
    following_set = get_user_set(driver, class_name)

    file = open("onlyfans.txt", "w")
    res = list(follower_set.difference(following_set))
    res.sort()

    for user in res:
        file.write(user + "\n")

    file.close()

    file = open("disloyals.txt", "w")
    res = list(following_set.difference(follower_set))
    res.sort()

    for user in res:
        file.write(user + "\n")

    file.close()

    file = open("mutuals.txt", "w")
    res = list(following_set.intersection(follower_set))
    res.sort()

    for user in res:
        file.write(user + "\n")

    file.close()

    time.sleep(10)
    print('finish')

    driver.quit()

    # Getting the size and height of an element
    # e = driver.find_element_by_xpath("//someXpath")
    # location = e.location
    # size = e.size
    # w, h = size['width'], size['height']

def get_user_set(driver, class_name):
    ul = driver.find_element_by_css_selector(f'.{class_name} ul')
    height = ul.size['height']
    prev_height = 0

    driver.execute_script(f"list = document.querySelector('.{class_name} ul');")

    check_freq = 0.1
    check_duration = 3

    while prev_height < height:
        driver.execute_script("list.scrollIntoView(false);")
        for i in range(int(check_duration / check_freq)):
            if height != ul.size['height']:
                break
            time.sleep(check_freq)

        prev_height = height
        height = ul.size['height']

    users = driver.find_elements_by_css_selector(f'div.{class_name} ul li span a')

    return set([user.text for user in users])


if __name__ == '__main__':
    main()
    
