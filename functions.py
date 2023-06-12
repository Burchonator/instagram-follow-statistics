from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import csv
from selenium.common.exceptions import NoSuchElementException

# OPENS BROWSER
browser = webdriver.Firefox()  # uses FireFox browser
browser.implicitly_wait(5)
login_url = "https://www.instagram.com/"
browser.get(login_url)  # opens instagram in browser


def login_to_instagram(username, password):
    print("Logging into " + username + "...")

    username_element = browser.find_element(By.NAME, "username")
    password_element = browser.find_element(By.NAME, "password")
    if username_element and password_element:  # checks if the text boxes exist
        username_element.clear()
        password_element.clear()
        username_element.send_keys(username)
        password_element.send_keys(password)
    else:
        print(
            "Issue with username and password elements on instagram.",
            "Sending issue to the developer to get a fix on this issue.",
        )
    sleep(0.5)
    login_button = browser.find_element(By.CSS_SELECTOR, "._acap")
    if login_button:
        login_button.click()
    else:
        print(
            "Issue with login button element on instagram.",
            "Sending issue to the developer to get a fix on this issue.",
        )
    sleep(3)  # was 5

    login_unsuccessful = True
    logged_in = False
    try:
        incorrect_login_message = browser.find_element(
            By.XPATH, '//*[@id="slfErrorAlert"]'
        )
        login_unsuccessful = True
    except NoSuchElementException:
        login_unsuccessful = False

    if login_unsuccessful:
        print("Login was unsuccessful. Please try again.")
    else:
        logged_in = True
        print("Login Successful.")
    return logged_in


def check_valid_password_length(username, password):
    valid_creds = False
    if len(password) < 6:
        print(
            "Invalid password. Correct length of password is 6 characters or more."
        )
    else:
        print("Valid password")
        valid_creds = True
    return valid_creds
