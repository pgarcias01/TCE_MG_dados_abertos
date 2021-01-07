from selenium import webdriver
from selenium.webdriver.remote.utils import load_json
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
import zipfile
import json
from multiprocessing import Pool

class Spider():

    def __init__(self) -> None:
        config = self.load_config('../config.json')
        self.link = config['link']
        self.driver_path = config['driver_path']
        self.max_process = config['max_process']
        self.parent_dir = config['parent_dir']
        driver = webdriver.Chrome(self.driver_path)
        driver.get(self.link)
        html = driver.page_source
        soup = BeautifulSoup(html)
        anos = soup.find('select', {'id': 'formulario:j_idt63'})
        self.anos = [item.text for item in anos.find_all('option')]
        driver.close()


    def load_config(self,filepath):
        """Load a json file."""
        with open(filepath, "r", encoding='utf8') as fp:
            obj = json.load(fp)
        return obj

    def wait_for_downloads(self,path):
        while any([filename.endswith(".crdownload") for filename in 
                os.listdir(path)]):
            time.sleep(2)

    def unzip(self,dir_name):
        extension = ".zip"
        os.chdir(dir_name) # change directory from working dir to dir with files
        if len(os.listdir(dir_name))>0:
            for item in os.listdir(dir_name): # loop through items in dir
                if item.endswith(extension): # check for ".zip" extension
                    file_name = os.path.abspath(item) # get full path of files
                    zip_ref = zipfile.ZipFile(file_name) # create zipfile object
                    zip_ref.extractall(dir_name) # extract file to dir
                    zip_ref.close() # close file
                    os.remove(file_name) # delete zipped file

    def extract_data(self,ano):
        if ano in os.listdir(self.parent_dir):
            pass
        
        else:
            path = os.path.join(self.parent_dir, ano)
            os.mkdir(path) 
            chromeOptions = webdriver.ChromeOptions()
            prefs = {"download.default_directory" : path}
            chromeOptions.add_experimental_option("prefs",prefs)
            driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chromeOptions)
            driver.get(self.link)
            driver.find_element_by_xpath('//*[@id="formulario:j_idt49"]/span[1]').click()
            select = Select(driver.find_element_by_id('formulario:j_idt63'))
            select.select_by_value(ano)

            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:arquivoAnoExercicio"]'))
            WebDriverWait(driver, 10).until(element_present)

            html_page = driver.page_source
            soup_page = BeautifulSoup(html_page)
            rows = len(soup_page.find('tbody',{'class':'ui-datatable-data ui-widget-content'}).find_all('tr'))
            for file in range(rows):
                driver.find_element_by_xpath(f'//*[@id="formulario:checkboxDT:{file}:j_idt71"]').click()
                self.unzip(path)
                time.sleep(1)
                self.wait_for_downloads(path)
            self.unzip(path)
            driver.close()

if __name__ == "__main__":
    spider = Spider()
    with Pool(spider.max_process) as p:
        p.map(spider.extract_data, spider.anos)