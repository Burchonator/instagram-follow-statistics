print(
    """
  _____           _                                   
 |_   _|         | |                                  
   | |  _ __  ___| |_ __ _  __ _ _ __ __ _ _ __ ___   
   | | | '_ \/ __| __/ _` |/ _` | '__/ _` | '_ ` _ \  
  _| |_| | | \__ \ || (_| | (_| | | | (_| | | | | | | 
 |_____|_| |_|___/\__\__,_|\__, |_|  \__,_|_| |_| |_| 
 |  ____|  | | |            __/ |                     
 | |__ ___ | | | _____     |___/                      
 |  __/ _ \| | |/ _ \ \ /\ / /                        
 | | | (_) | | | (_) \ V  V /                         
 |_|__\___/|_|_|\___/ \_/\_/_   _                     
  / ____| |      | | (_)   | | (_)                    
 | (___ | |_ __ _| |_ _ ___| |_ _  ___ ___            
  \___ \| __/ _` | __| / __| __| |/ __/ __|           
  ____) | || (_| | |_| \__ \ |_| | (__\__ \           
 |_____/ \__\__,_|\__|_|___/\__|_|\___|___/           

 Showing you who you mutually follow, who you don't 
 follow back, and who doesn't follow you back.

 Created by: Mitchell Burcheri
 Date Created: 9/5/2023                                              
"""
)

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

# fill the variables below with your instagram login credentials and run

print("Loading...")
print()

logged_in = False

# OPENS BROWSER
browser = webdriver.Firefox()  # uses FireFox browser
browser.implicitly_wait(5)
login_url = "https://www.instagram.com/"
browser.get(login_url)  # opens instagram in browser


def collect_user_login():
    valid_creds = False
    while valid_creds == False:
        print("Please login")
        your_username = str(input("Enter your username: "))
        your_password = str(getpass("Enter your password (hidden): "))
        if len(your_password) < 6:
            print(
                "Invalid password. Correct length of password is 6 characters or more."
            )
        else:
            valid_creds = True
        print()
    return your_username, your_password


def login_to_website(input_username, input_password):
    print("Logging into " + input_username + "...")

    username_element = browser.find_element(By.NAME, "username")
    password_element = browser.find_element(By.NAME, "password")
    if username_element and password_element:  # checks if the text boxes exist
        username_element.clear()
        password_element.clear()
        username_element.send_keys(input_username)
        password_element.send_keys(input_password)
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


username = ""
while logged_in == False:
    username, password = collect_user_login()  # collect user input
    login_to_website(username, password)  # login to instagram
    login_unsuccessful = True
    try:
        incorrect_login_message = browser.find_element(
            By.XPATH, '//*[@id="slfErrorAlert"]'
        )
        login_unsuccessful = True
    except NoSuchElementException:
        login_unsuccessful = False

    if login_unsuccessful:
        print("Login was unsuccessful. Please try again.")
        print()
    else:
        logged_in = True
        print("Login Successful.")
        print()
    # sleep(10000)


# GO TO THE ACCOUNT PAGE
sleep(4)
browser.get("https://www.instagram.com/" + str(username))
print("Opened account page")
sleep(4)

# BEGIN SCRAPING
print("Scraping followers...")

# SCRAPE THE NUMBER OF FOLLOWERS
number_of_followers = int(
    browser.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span",
    ).text
)  # records the number of followers that is listed on the page


# LOOK FOR THE FOLLOWERS LINK AND CLICK LINK
TIMEOUT = 5  # seconds
WebDriverWait(browser, TIMEOUT).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))
).click()
sleep(3)

# SCROLL DOWN TO VIEW ALL FOLLOWERS
scrolling_spot = browser.find_element(
    By.XPATH,
    "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]",
)
scrolling_spot.click()
for i in range(number_of_followers):
    ActionChains(browser).send_keys(Keys.END).perform()
    sleep(0.1)


# SCRAPE THE FOLLOWERS INTO A LIST USING THE NUMBER OF FOLLOWERS
list_of_followers = []
for follower_number in range(number_of_followers):
    list_of_followers.append(
        browser.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div["
            + str(follower_number + 1)
            + "]/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a/span/div",
        ).text
    )
sleep(5)

# EXIT OUT OF THE FOLLOWERS LIST
exit_button = browser.find_element(
    By.XPATH,
    "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button",
)
exit_button.click()
print("Scraped followers. Now scraping following...")
sleep(3.5)

# SCRAPE THE NUMBER OF FOLLOWING
number_of_following = int(
    browser.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span",
    ).text
)  # records the number of followers that is listed on the page


# LOOK FOR THE FOLLOWERS LINK AND CLICK LINK
TIMEOUT = 5  # seconds
WebDriverWait(browser, TIMEOUT).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]"))
).click()
sleep(3)

# SCROLL DOWN TO VIEW ALL FOLLOWING
scrolling_spot = browser.find_element(
    By.XPATH,
    "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]",
)
scrolling_spot.click()
sleep(3)
for i in range(number_of_following):
    ActionChains(browser).send_keys(Keys.END).perform()
    sleep(0.1)

# SCRAPE THE FOLLOWING INTO A LIST USING THE NUMBER OF FOLLOWING
list_of_following = []
for following_number in range(number_of_following):
    list_of_following.append(
        browser.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div["
            + str(following_number + 1)
            + "]/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a/span/div",
        ).text
    )

browser.close()
print("...Finished scraping")
print()

# SCRAPING COMPLETE

# LIST THE STATISTICS

# print(list_of_followers)
# print(list_of_following)

print("Listing statistics")
print("-------------------")

# add people who mutually follow you to a list and remove them from the other lists
mutual_follow = list(set(list_of_followers) & set(list_of_following))
list_of_mutual = []
for i in mutual_follow:
    list_of_mutual.append(list_of_followers.pop(list_of_followers.index(i)))
    list_of_following.remove(i)


# remove the verified tag on the people in the list
def remove_verified_tag(listofpeople):
    for person in listofpeople:
        verified_tag = "\nVerified"
        if verified_tag in person:
            tag_index = person.index(verified_tag)
            index_of_person = listofpeople.index(person)
            listofpeople[index_of_person] = person[:tag_index]


remove_verified_tag(list_of_mutual)
remove_verified_tag(list_of_followers)
remove_verified_tag(list_of_following)


def list_people(listofpeople):  # list the people in the list
    for person in listofpeople:
        # print(" - " + str(i))
        print(str(person))


# MUTUALLY FOLLOW
print()
print(
    "There are "
    + str(len(list_of_mutual))
    + " people who are mutual followers. These people are: "
)
list_people(list_of_mutual)
print()

# FOLLOWERS YOU DON'T FOLLOW
print(
    "There are "
    + str(len(list_of_followers))
    + " people you don't follow back. These people are: "
)
list_people(list_of_followers)
print()

# PEOPLE WHO DON'T FOLLOW YOU BACK
print(
    "There are "
    + str(len(list_of_following))
    + " people that don't follow you back. These people are: "
)
list_people(list_of_following)
print()

with open("results.csv", "w") as results_csv:
    writer = csv.writer(results_csv)
    i = 0
    while list_of_mutual[i] or list_of_followers[i] or list_of_following[i]:
        line_to_write = ""
        if list_of_mutual[i]:
            line_to_write += str(list_of_mutual[i])
        line_to_write += ","
        if list_of_followers[i]:
            line_to_write += str(list_of_followers[i])
        line_to_write += ","
        if list_of_following[i]:
            line_to_write += str(list_of_following[i])
        i += 1
        writer.writerow(line_to_write)
