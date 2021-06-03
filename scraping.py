import requests
from bs4 import BeautifulSoup
import re
from re import search
import numpy as np
import pandas as pd
import json
import math
import pickle

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

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

enlaces = {#'ingenierias':'https://bit.ly/3b6o1Bm'
            #,'software_informatica_y_telecomunicaciones':'https://bit.ly/2OjFnBB'
            #,'economia_estadistica_y_matematicas':'https://bit.ly/3rgPtkB'
            #,'recursos_humanos':'https://bit.ly/3e11pnv'
            #,'mercadeo_y_publicidad':'https://bit.ly/3uOClWQ'
            #,'ventas':'https://bit.ly/384XAtX'
            'comunicacion_y_periodismo':'https://bit.ly/37HsWX6'
            ,'servicio_al_cliente':'https://bit.ly/3baJlpr'
            ,'diseno_arquitectura_artes_graficas_y_afines':'https://bit.ly/3r8yf9O'
            ,'compras_y_comercio':'https://bit.ly/3b9OFcx'
            ,'derecho_asesoria_afines':'https://bit.ly/3raFle5'
            ,'administracion_oficina':'https://bit.ly/3uLVvfY'
            ,'produccion_operarios_manufactura':'https://bit.ly/2PrBKu9'
            ,'call_center_telemercadeo_bpo':'https://bit.ly/3sznxto'
            ,'hoteleria_y_Turismo':'https://bit.ly/3aLR2Rs'
            ,'bodega_logistica_y_transporte':'https://bit.ly/3qhQPeF'
            ,'mantenimiento_y_reparaciones':'https://bit.ly/3rclGu9'
            ,'medicina_sector_salud_y_ciencias':'https://bit.ly/2MFnYTJ'
            ,'deportes_y_recreacion':'https://bit.ly/2OgcmXL'
            ,'gastronomia_bebidas_alimentos_y_restaurantes':'https://bit.ly/3069MGo'
            ,'servicios_generales_aseo_seguridad':'https://bit.ly/304zkDN'
            ,'otras':'https://bit.ly/2R2e2VZ'} #'call_center_telemercadeo_bpo':'https://bit.ly/3sznxto'

all_jobs = {}

for categoria,enlace in enlaces.items():

    driver = webdriver.Chrome(executable_path=r'C:/Users/Cristian Restrepo/Documents/Anaconda/pkgs/python-3.7.6-h60c2a47_2/chromedriver.exe')
    driver.get(enlace)

    dict_jobs = dict()

    num_pages = num_pags(enlace) + 1
    for i in range(1,num_pages):
        if i == 1:
            pag_one =  parser_url(enlace)[2]
            jobs = url_jobs(pag_one)
            job_dict = {}
            for i in jobs:
                job = {}
                job[i] = categoria
                job_dict.update(job)
            dict_jobs.update(job_dict)
            print(i)
            #dict_jobs[categoria] = jobs

        else:
            element = driver.find_element_by_xpath("//a[@class='page-link'][@rel='next']")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(3)
            page = parser_html(driver)[0]
            jobs_page = url_jobs(page)
            print(jobs_page)
            job_dict = {}
            for i in jobs_page:
                job = {}
                job[i] = categoria
                job_dict.update(job)
            dict_jobs.update(job_dict)
            print(i)
            #dict_jobs[categoria].extend(jobs_page)
        
        #dict_jobs.update(job_dict)
        print(dict_jobs)
        print(len(dict_jobs))
    
    all_jobs.update(dict_jobs)
    #all_jobs = dict(all_jobs.items() + dict_jobs.items())
    #print(len(all_jobs))

    driver.close()

    file_to_write = open("jobs_magneto.pickle", "wb")

    pickle.dump(all_jobs, file_to_write)

print(len(all_jobs))

# file_name = "jobs_magneto.pkl"

# open_file = open(file_name, "wb")
# pickle.dump(all_jobs, open_file)
# open_file.close()

# open_file = open(file_name, "rb")
# loaded_list = pickle.load(open_file)
# open_file.close()

# print(loaded_list)


# def save_obj(obj, name ):
#     with open('obj/'+ name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)



# def load_obj(name ):
#     with open('obj/' + name + '.pkl', 'rb') as f:
#         return pickle.load(f)