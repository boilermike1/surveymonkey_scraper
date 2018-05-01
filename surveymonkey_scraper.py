from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pandas as pd
import numpy as np

chromedriver = "/home/boilermike1/Documents/ds/packages/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

def survey_monkey_scraper(extension, filename = None):
    '''Scrapes survey data from SurveyMonkey into a dataframe. Must import selenium and setup chromedriver'''
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://www.surveymonkey.com/results/{}/browse/'.format(extension))
    time.sleep(3)
    resp_button = driver.find_element_by_css_selector('a.respondent-goto-menu-btn')
    resp_button.click()
    num_resp = driver.find_element_by_css_selector('input.goto-number-text.sm-input').get_attribute('value')
    num_resp = int(num_resp)
    q_columns_list = list()
    resp_list = list()
    for i in range(num_resp):
        if i > 0:
            resp_button = driver.find_element_by_css_selector('a.respondent-goto-menu-btn')
            resp_button.click()
        time.sleep(1)
        resp_num_input = driver.find_element_by_css_selector('input.goto-number-text.sm-input')
        resp_num_input.click()
        resp_num_input.clear()
        resp_num_input.send_keys(i+1)
        resp_num_input.send_keys(Keys.ENTER)
        time.sleep(2)
        q_containers = driver.find_elements_by_css_selector('div.response-question-container')
        for col,entry in enumerate(q_containers):
            if len(q_containers[col].text) > 2:
                resp_list.append(q_containers[col].text)
    df_output = survey_monkey_cleaner(resp_list, num_resp)
    if filename == None:
        pass
    else:
        survey_monkey_to_excel(df_output, filename)
    return df_output

def survey_monkey_cleaner(resp_list, num_resps):
    num_qs = len(resp_list) // num_resps
    col_list = list()
    ans_list = list()
    for i in resp_list[0:num_qs]:
        col_list.append(i.split(sep = '\n')[0] + ' - '
                        + i.split(sep = '\n')[1])
    for j in resp_list:
        ans_list.append(' - '.join(j.split(sep = '\n')[2:]))
    resp_df = pd.DataFrame(columns = col_list)
    for k in range(num_resps):
        resp_df.loc[k] = ans_list[k*num_qs:k*num_qs+num_qs]
    return resp_df

def survey_monkey_to_excel(df, filename):
    df.to_excel(filename)
