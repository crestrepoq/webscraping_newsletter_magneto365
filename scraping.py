import requests
from bs4 import BeautifulSoup
import re
from re import search
import numpy as np
import pandas as pd
import json
import math

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

enlace = 'https://bit.ly/3sznxto'

def parser_url(url):
    '''
    input: url of interest
    output: html with urls of jobs
    '''
    url = requests.get(url)
    soup = BeautifulSoup(url.content, 'html.parser')
    split_html = list(soup.children)
    return split_html

def parser_html(current_driver):
    '''
    input: hmtl element
    output: html with urls of jobs
    '''
    source = current_driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    split_html = list(soup.children)
    return split_html

def url_jobs(url_parser):
    '''
    Input: html with beautifulsoup format = class 'bs4.element.Tag'
    Output: list with url jobs 
    '''
    urls_jobs = list()
    for link in url_parser.find_all(class_="outline"):
        link_job = link.get('href')
        urls_jobs.append(link_job)
    print('Cantidad de vacantes',len(urls_jobs))
    return urls_jobs

def num_pags(url):
    pages = list()
    parser_link = parser_url(url)[2]
    for link in parser_link.find_all(class_="page-link"):
        number_page = link.text
        pages.append(number_page)
    return int(pages[-2])

# pag_one =  parser_url(enlace)[2] #genera una lista de 6 elementos donde elemento 3 o [2] es el del html de interes
# jobs = url_jobs(pag_one)

# print(jobs)

driver = webdriver.Chrome(executable_path=r'C:/Users/Cristian Restrepo/Documents/Anaconda/pkgs/python-3.7.6-h60c2a47_2/chromedriver.exe')
driver.get(enlace)

num_pages = num_pags(enlace) + 1
for i in range(1,num_pages):
    if i == 1:
        pag_one =  parser_url(enlace)[2]
        jobs = url_jobs(pag_one)
    else:
        element = driver.find_element_by_xpath("//a[@class='page-link'][@rel='next']")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)
        page = parser_html(driver)[0]
        jobs_page = url_jobs(page)
        print(jobs_page)
        jobs.extend(jobs_page)
        print(len(jobs))

print(len(jobs))

# file = open('jobs.html', 'w')
# file.write(driver.page_source)
# file.close()

driver.close()