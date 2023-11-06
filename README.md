NOTE 7/11/23: I don't know whether this works anymore since I added the gui. The last time I made changes to this project was in June 2023. I made further changes since, however I'm setting what as already been pushed from private to public to add to my github portfolio.

I may improve this in the future.

# instagram-follow-statistics

This python script scrapes your profile's followers and following and then shows you who mutually follows you, who you don't follow back, and who doesn't follow you back.

This script works locally on you machine and only sends your Instagram login credentials to Instagram via the FireFox browser.

# How to use

1. Install selenium.
2. Change the your_username and your_password string variables to your Instagram username and password.
3. Run the program, don't touch the browser that opens, and view the report from the terminal after the script has finished running. Hopefully this runs for you zero no errors.

# How it works

1. The bot opens the browser and then logs into Instagram with the credentials you provided in the inputs from terminal. Password is hidden for security reasons.
2. The bot then goes to your instagram account page.
3. The bot scrapes the number of followers you have and then clicks on the followers. It then scrolls down to the bottom and scrapes the usernames of the people that follow you, then exits the follower page.
4. The bot repeats the process for following.
5. The bot exits the browser and a report is generated of who mutually follows you, who you don't follow back, and who doesn't follow you back.

# Note: 
- This program isn't perfect. The code can obviosuly be improved and works for my profile with roughly 200 following and followers.
- Not recommended for large profiles over 10K followers/following because the code uses a for loop that requires the bot to click Key.END to scroll down the list of followers and following.
- This code hasn't been tested throughly. Only on my profiles.
- XPATHS may change as the instagram inteface changes which means you may need to modify the XPATHS to where the buttons and data is stored.
