# -*- coding: utf-8 -*- 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from random import randrange
from playsound import playsound
from datetime import datetime
import io
import json

allGood = True  # Changes to False if something went wrong
counter = 0     # Number of written comments

class InstaBot():

    def __init__(self):
        self.driver = webdriver.Chrome()
        
    # Wait for element to load
    def waitFor(self, xpath):
        maxWait = 60
        try:
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.driver, maxWait).until(element_present)
        except:
            print("Waited too long for element to load :/")
            nextButton = self.driver.find_element_by_css_selector('.coreSpriteRightPaginationArrow')
            nextButton.click()
            sleep(5)

    # Login using given username and password
    def login(self, login, password):
        self.driver.get("https://www.instagram.com/")

        bot.waitFor('//*[@id="loginForm"]/div/div[1]/div/label/input')
        loginInput = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        loginInput.send_keys(login)

        bot.waitFor('//*[@id="loginForm"]/div/div[2]/div/label/input')
        passwordInput = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        passwordInput.send_keys(password)

        bot.waitFor('//*[@id="loginForm"]/div/div[3]/button')
        loginButton = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        loginButton.click()

    # Search for given hashtag and click on the last photo
    def search(self, hashtag):
        bot.waitFor('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        searchInput = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        searchInput.send_keys(hashtag)

        bot.waitFor('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]')
        firstResult = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]')
        firstResult.click()

        bot.waitFor('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
        firstPhoto = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
        firstPhoto.click()

    # Close the current photo
    def close(self):
        bot.waitFor('/html/body/div[4]/div[3]/button')
        closeButton = self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button')
        closeButton.click()

    # Like, follow, and comment post
    def comment(self, secondsBetween, compliments, emojis, ads, advertisedProfile, like, follow, comment, blacklist):
        bot.waitFor('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/*[name()="svg"]')
        heartSvg = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/*[name()="svg"]')
        label = heartSvg.get_attribute("aria-label")

        # Check if already followed
        notFollowed = False
        try:
            self.driver.find_element_by_xpath('//button[normalize-space()="Obserwowanie"]')
        except:
            notFollowed = True

        # Check for profiles from blacklist
        shouldntSkip = True
        for x in range(len(blacklist)):
            foundSomeone = True
            try:
                profile = '//a[normalize-space()="' + blacklist[x] + '"]'
                self.driver.find_element_by_xpath(profile)
            except:
                foundSomeone = False
            if foundSomeone:
                shouldntSkip = False
                break

        # If not already liked and not already followed, and not on blacklist, than like, follow and comment
        if label == u"Lubię to!" and notFollowed and shouldntSkip:
            if like:
                bot.waitFor('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                heartButton = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                heartButton.click()

            if follow:
                sleep(2)
                bot.waitFor('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                follow = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                follow.click()

            bot.waitFor('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[2]/button')
            commentButton = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[2]/button')
            commentButton.click()

            # Check if input element exists
            inputFound = True
            try:
                commentInput = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
            except:
                print("Could not find the input element")
                inputFound = False
            
            # Needed for emojis
            JS_ADD_TEXT_TO_INPUT = """
            var elm = arguments[0], txt = arguments[1];
            elm.value += txt;
            elm.dispatchEvent(new Event('change'));
            """

            # Comment text
            text = compliments[randrange(len(compliments))] + " " + emojis[randrange(len(emojis))] + " " + ads[randrange(len(ads))] + " " + advertisedProfile

            # If input element exists than write a comment
            if inputFound and comment:
                self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, commentInput, text)
                commentInput.send_keys(" ")
                sleep(3)
                sendButton = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/button')
                sendButton.click()

            global counter
            global allGood

            # Check for "cannot comment any more" notification
            allGood = False
            try:
                self.driver.find_element_by_css_selector('.JBIyP')
            except:
                # If everything is good than play a sound, print the time and print a comment
                allGood = True
                playsound('sounds/good.wav')
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time)
                if comment:
                    print(text)
                counter+=1
                sleep(secondsBetween-5)
        # Skipping a post
        else:
            playsound('sounds/skip.wav')
            print('Skipped')
            
        # Load next post if everything went fine
        if allGood:
            nextButton = self.driver.find_element_by_css_selector('.coreSpriteRightPaginationArrow')
            nextButton.click()
        # Play the sound when something is wrong
        else:
            playsound('sounds/bad.wav')


with io.open('settings.json', encoding="utf8") as data:
    settings = json.load(data)

login = settings["login"]
password = settings["password"]
numberOfComments = settings["numberOfComments"]
secondsBetween = settings["secondsBetween"]
hashtag = settings["hashtag"]
compliments = settings["compliments"]
emojis = settings["emojis"]
ads = settings["ads"]
advertisedProfile = settings["advertisedProfile"]
like = settings["like"]
follow = settings["follow"]
comment = settings["comment"]
blacklist = settings["blacklist"]

bot = InstaBot()
bot.login(login, password)
bot.search(hashtag)

while counter<numberOfComments:
    bot.comment(secondsBetween, compliments, emojis, ads, advertisedProfile, like, follow, comment, blacklist)
    if not allGood:
        break

playsound("sounds/end.wav")
print("\n############ END ############\nSuccessfully written " + str(counter) + " comments\n")
