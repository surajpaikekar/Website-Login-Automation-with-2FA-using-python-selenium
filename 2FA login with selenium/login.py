#############################################################
import time
from datetime import date, timedelta, datetime
from lxml import etree, html
from requests_futures.sessions import FuturesSession
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import sys
import imaplib
import base64
import email
import re
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tqdm.notebook import tqdm
import logging
from pathlib import Path
logging.basicConfig(filename='login_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_chrome_driver():
    try:
        login_url = "your login URL"
        
        chrome_options = Options()  
        chrome_options.add_argument('--headless')  
        chrome_options.add_argument('--disable-gpu')  
        # Handle Content Security Policy (CSP) Restrictions
        # chrome_options.add_argument('--disable-web-security')
        # chrome_options.add_argument('--allow-running-insecure-content')
        # use stable driver
        #driver = webdriver.Chrome(options =chrome_options) 
        driver = webdriver.Chrome(ChromeDriverManager().install(), options =chrome_options)

        driver.set_window_size(1200, 800) 
        driver.get(login_url)
        time.sleep(5)
        return driver
    
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        # sys.exit(1)
    except TimeoutException as e:
        print(f"Timeout waiting for element: {e}")
        # sys.exit(1)
    except Exception as e:
        print(f"Error in get_chrome_driver: {e}")
        # sys.exit(1)

def get_verification_code():

    """
        2FA Code : This code fetched the recent OTP from your Email.
    """
    try:
        imap_url = 'imap.gmail.com'
        # this is done to make SSL connnection with  
        con = imaplib.IMAP4_SSL(imap_url)  

        username = 'your Gmail ID'
        password = 'your Gmail App Password, for example-fjdhbfjbjdjbf' ## This should not be you actual Gmail Password. You need to create new Gmail App password in Gmail securty Tab

        # calling login method from SSL connection
        con.login(username, password)   

        # calling fuction to check for email under this label 
        con.select('Inbox') 
        result, data = con.search(None, 'FROM','Domain Email ID from which you are expecting Email OTP')
        ids = data[0]    # get the first item   
        id_list = ids.split()  
        latest_email_id = id_list[-1]   # get latest email

        result, data = con.fetch(latest_email_id, "(RFC822)") 
        raw_email = data[0][1]
        ## Get Verification code using regular expression
        email_message = {
            part.get_content_type(): part.get_payload()
            for part in email.message_from_bytes(raw_email).walk()
        }

        verification_code = re.findall('\d+', email_message["text/html"])[2]
        print(verification_code)

        return verification_code
    
    except Exception as e:
        print(f"Error in get_verification_code: {e}")
        # sys.exit(1)

def login(driver):   
    try:
        """
        Login Function: This function will fetch the OTP from the Email for the 2FA 
        """

        driver.find_element(By.ID, "loginFormAndStuff:username").click()
        driver.find_element(By.ID, "loginFormAndStuff:username").clear()
        driver.find_element(By.ID, "loginFormAndStuff:username").send_keys('website username') 
        driver.find_element(By.ID, "loginFormAndStuff:inputPassword").click()
        driver.find_element(By.ID, "loginFormAndStuff:inputPassword").clear()
        driver.find_element(By.ID, "loginFormAndStuff:inputPassword").send_keys('website password') 
        driver.find_element(By.ID, "loginFormAndStuff:submitLoginWith").click()

        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "otppswd")))

        driver.find_element(By.ID, "otppswd").click()
        driver.find_element(By.ID, "otppswd").clear()
        time.sleep(4)
        
        # Recieving the Actual OTP from Gmail.
        verification_code = get_verification_code()
        time.sleep(1)

        driver.find_element(By.ID, "otppswd").send_keys(verification_code)
        driver.find_element(By.ID, "submit-btn").click()
        time.sleep(3)

        """
            Selenium Automation : After successfull login, moving forward to desired webpage [ Finding button and clciking them ]
        """
        element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "Actual XPATH")))
        element.click()
        time.sleep(3)
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "Actual XPATH")))
        element.click()
        time.sleep(5)
        return driver
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
   
    except TimeoutException as e:
        print(f"Timeout waiting for element: {e}")
       
    except Exception as e:
        print(f"Error in proda_login: {e}")
    

driver  = get_chrome_driver()
driver.set_window_size(1200, 800) ## setting window size for web browser to help to find all the Tabs and buttons 
driver  = login(driver)
print(f"Main driver initialized: ")
logging.info(f"Main driver initialized:")

# #### output cookies, sessions and user agent #######
cookies_list =  driver.get_cookies()
selenium_user_agent = driver.execute_script("return navigator.userAgent;")
logging.info(f"user agent: {selenium_user_agent}")


"""
    You can use these updated cookies and current sessions after successfuly fetching them from updated driver. 
    For instance you can use them in creating new Web Drivers or Multi-threading (Parallel processing) 

"""

