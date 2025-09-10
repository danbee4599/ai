from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time

def start():
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    driver.maximize_window()

    reject = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "W0wltc"))
    )
    reject.click()
    return driver



def scrape_website(driver, c):
        search = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )
        search.clear()
        search.send_keys(c + " careers")
        search.submit()

        website = WebDriverWait(driver, 10000).until(
            EC.element_to_be_clickable((By.XPATH, "(//h3)[1]"))
        )
        website.click()

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIGKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]"))
            ).click()
        except:
            pass

 
        try:
            try:
                S_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'search')]"))
                )
                S_button.click()
            except:
                pass
            while True:
                try:
                    button = WebDriverWait(driver,3).until(
                            EC.visibility_of_element_located((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'city')]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    button.click()
                    time.sleep(2)
                    html = driver.page_source
                    driver.back()
                    return html        
                except:
                    try:
                        driver.execute_script("window.scrollBy(0, 500)") 
                        at_bottom = driver.execute_script(
                        "return window.innerHeight + window.scrollY >= document.body.scrollHeight"
                        )
                        if at_bottom:
                            driver.back()
                            raise Exception
                    except:
                        driver.back()
                        raise Exception
        except:
            return driver.page_source

    

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    #for script_or_style in soup(["script", "style"]):
        #script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_content(cleaned_content, max_length=6000):
    return [
        cleaned_content[i : i + max_length] for i in range(0, len(cleaned_content), max_length)
    ]

