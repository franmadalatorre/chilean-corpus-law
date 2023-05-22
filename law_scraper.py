### Law scraper

## Imports
import time 
import pandas as pd 
import numpy as np
from tqdm import tqdm
import os

from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager


def format_text(content):
    ## This function will receive the text scraped from an url and format it.

    text = [phrase for phrase in content.split("\n")] # Separating by line-break
    processed = [t.strip().replace('"',"") for t in text if len(t.strip()) > 1] # Striping big blank spaces, " symbols and blank spaces with lenght = 1.
    law_number = processed[0].split(" ")[-1].replace(".","") # Obtaining the law number

    return law_number,processed

def scrape_law(num_law, dataset):
    
    ## Definimos url
    url = f'https://www.bcn.cl/leychile/navegar?idLey={num_law}'
    
    try:
        ## Obtenemos la data de la url con el driver
        driver.get(url) 

        ## Damos 5 segundos para permitir que se cargue la página correctamente
        time.sleep(5)

        # Con find_element podemos encontrar elementos del HTML. En este caso, el texto de la LEY está en un div con id = 'read-norma', así que lo buscamos y extraemos el texto de ese elemento.
        content = driver.find_element(By.ID, "read-norma").text
        
        ## Formatting text
        _, text = format_text(content)
    
    except:
        text = np.nan

    # Saving the number of the law and text in a DataFrame
    df_aux = pd.DataFrame({'Num_law':num_law,'text':[text]})

    # Concatenating the extracted law to the dataset
    dataset = pd.concat([dataset,df_aux])

    return dataset



if __name__ == '__main__':

    # Until which law to scrape
    MAX_LAW_NUMBER = 6000

    # start by defining the options 
    options = webdriver.ChromeOptions() 
    options.headless = True # it's more scalable to work in headless mode 
    # normally, selenium waits for all resources to download 
    # we don't need it as the page also populated with the running javascript code. 
    options.page_load_strategy = 'none' 
    # this returns the path web driver downloaded 
    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 
    # pass the defined options and service objects to initialize the web driver 
    driver = Chrome(options=options, service=chrome_service) 
    driver.implicitly_wait(5)


    ## Creating the .csv file to save all of the scraped laws in case it does not exists
    if not os.path.exists('dataset.csv'):
        dataset = pd.DataFrame(columns=["Num_law",'text'])
        dataset.to_csv('dataset.csv')

    else:
        # Loading the dataset
        dataset = pd.read_csv('dataset.csv',index_col=0)
        
        # To only retrieve laws that are not already in the dataset
        iterator = [num_law for num_law in np.arange(1,MAX_LAW_NUMBER) if num_law not in dataset['Num_law'].values]

    ## Scraping loop
    for law in tqdm(iterator,desc = 'Retrieving laws'):

        # This function returns the dataset including the new law
        dataset = scrape_law(law,dataset)

        # Saving the dataset each 50 laws, to avoid time by saving the file every iteration 
        if law % 50:
            dataset.to_csv('dataset.csv')


    driver.close()





