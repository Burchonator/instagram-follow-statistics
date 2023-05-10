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

# fill the variables below with your instagram login credentials and run
your_username = str(input("Enter your username: "))
your_password = str(getpass("Enter your password (hidden): "))
print()

# OPENS BROWSER
browser = webdriver.Firefox()  # uses FireFox browser
browser.implicitly_wait(5)
browser.get("https://www.instagram.com/")  # opens instagram in browser

print("Logging into " + your_username + "...")

# LOGS INTO INSTAGRAM
sleep(1)
username_input = browser.find_element(By.NAME, "username")
password_input = browser.find_element(By.NAME, "password")
username_input.send_keys(your_username)
password_input.send_keys(your_password)
sleep(1)

login_button = browser.find_element(By.CSS_SELECTOR, "._acap")
login_button.click()
sleep(5)
print("...logged in")

# GO TO THE ACCOUNT PAGE
browser.get("https://www.instagram.com/" + str(your_username))
print("Opened account page")
sleep(3.5)

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
list_mutual_follow = []
for i in mutual_follow:
    list_mutual_follow.append(list_of_followers.pop(list_of_followers.index(i)))
    list_of_following.remove(i)


# remove the verified tag on the people in the list
def remove_verified_tag(listofpeople):
    for person in listofpeople:
        verified_tag = "\nVerified"
        if verified_tag in person:
            tag_index = person.index(verified_tag)
            index_of_person = listofpeople.index(person)
            listofpeople[index_of_person] = person[:tag_index]


remove_verified_tag(list_mutual_follow)
remove_verified_tag(list_of_followers)
remove_verified_tag(list_of_following)


def list_people(listofpeople):  # list the people in the list
    for i in listofpeople:
        print(" - " + str(i))


# MUTUALLY FOLLOW
print()
print(
    "There are "
    + str(len(list_mutual_follow))
    + " people who are mutual followers. These people are: "
)
list_people(list_mutual_follow)
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
