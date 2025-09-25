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
from pypdf import PdfReader


class File:
    def __init__(self, file):
        self.file = file
    def read_file(self):
        df = pd.read_excel(self.file, 0, index_col = None)
        df[["Name", "Industry"]]
        companies_txt = []
        for i in df.itertuples():
            if i.Sector == "Healthcare":
                companies_txt.append(i.Name)
        return companies_txt

class Driver:
    def __init__(self):
        pass
    def launch(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.google.com/")
        self.driver.maximize_window()
        reject = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "W0wltc"))
        )
        reject.click()
        return self.driver

class Find_website:
    def __init__(self, company_name, driver):
        self.company_name = company_name
        self.driver = driver
    def search(self):
        self.driver.back()
        search = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
        search.clear()
        search.send_keys(self.company_name + " careers")
        search.submit()
        website = WebDriverWait(self.driver, 10000).until(
            EC.element_to_be_clickable((By.XPATH, "(//h3)[1]"))
        )
        website.click()

class Remove_pop_ups:
    def __init__(self, driver):
        self.driver = driver
    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIGKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]"))
            ).click()
        except:
            pass

class Scroll_down:
    def __init__(self, driver):
        self.driver = driver
    def scroll(self):
        try:
            try:
                S_button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'search')]"))
                )
                S_button.click()
            except:
                pass
            try:
                button = WebDriverWait(self.driver,3).until(
                        EC.visibility_of_element_located((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'city')]"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                button.click()
                time.sleep(2)
                return self.driver.page_source      
            except:
                try:
                    self.driver.execute_script("window.scrollBy(0, 500)") 
                    at_bottom = self.driver.execute_script(
                    "return window.innerHeight + window.scrollY >= document.body.scrollHeight"
                    )
                    if at_bottom:
                        raise Exception
                except:
                    raise Exception
        except:
            return self.driver.page_source



class Pdf_take:
    def __init__(self, path):
        self.path = path
        self.reader = PdfReader(path)
    def read(self):
        self.text = ""
        for p in self.reader.pages:
            self.text += p.extract_text()
        return self.text()



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
        return self.cleaned_content

class Final_file:
    def __init__(self, company_name, final_text):
        self.company_name = company_name
        self.final_text = final_text
        self.file_name = self.company_name.replace(" ", "_")
        with open(f"{self.file_name}.txt", "w", encoding="utf-8") as f:
            f.write(final_text)



companies = File(r"C:\Users\82105\Downloads\facilities_task (1).xlsx").read_file()
driver = Driver().launch()
for c in companies:
    Find_website(c, driver).search()
    Remove_pop_ups(driver).accept_cookies()
    source_code = Scroll_down(driver).scroll()
    final_text = Parse(source_code).clean()
    Final_file(c, final_text)
