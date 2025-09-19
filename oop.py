import pandas as pd
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


df = pd.read_excel(r"C:\Users\82105\Downloads\facilities_task (1).xlsx", 0, index_col = None)
df[["Name", "Industry"]]

companies_txt = []
for i in df.itertuples():
    if i.Sector == "Healthcare":
        companies_txt.append(i.Name)

driver = webdriver.Chrome()
driver.get("https://www.google.com/")
driver.maximize_window()
reject = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "W0wltc"))
)
reject.click()

class Scrape_website:
    def __init__(self, company_name):
        self.company_name = company_name
    def search(self):
        search = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
        search.clear()
        search.send_keys(self.company_name + " careers")
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
                    return driver.page_source
                    driver.back()      
                except:
                    try:
                        driver.execute_script("window.scrollBy(0, 500)") 
                        at_bottom = driver.execute_script(
                        "return window.innerHeight + window.scrollY >= document.body.scrollHeight"
                        )
                        if at_bottom:
                            raise Exception
                    except:
                        raise Exception
        except:
            return driver.page_source
            driver.back()

class Parse:
    def __init__(self, source_code):
        self.source_code = source_code
    def clean(self):
        self.soup1 = BeautifulSoup(self.source_code, "html.parser")
        self.body_content = self.soup1.body
        if self.body_content:
            self.the_body_content = self.body_content
        self.soup2 = BeautifulSoup(self.the_body_content, "html.parser")
        self.cleaned_content = self.soup2.get_text(separator="\n")
        self.cleaned_content = "\n\n".join(
            line.strip() for line in self.cleaned_content.splitlines() if line.strip()
        )

company_objects = {}
source_codes_list = {}
source_codes_objects = {}
for k in companies_txt:
    company_objects[k] = Scrape_website(k)
    source_codes_list[k] = company_objects[k].search()
    source_codes_objects[k] = Parse(source_codes_list[k])
    final_text = source_codes_objects[k].clean()
    file_name = k.replace(" ", "_")
    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        f.write(final_text)



