from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from dateutil.parser import parse
import pandas as pd
import time

import streamlit as st
import os
# from PIL import Image
import google.generativeai as genai


st.title('Latest news from Competitors')
days = st.number_input("Input how many days of news should be checked: ")
submit = st.button("Generate")

API_KEY = "AIzaSyC7oy_8IcwQkQneHijxroFiLQm0kMzylzo"


titles, source, dates, descriptions, company = [], [], [], [], []
max_attempts = 5
thirty_days_ago = datetime.now() - timedelta(days)

def get_gemini_response(question):
    # print(question)
    genai.configure(api_key=API_KEY) 
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"The following text has the date, company name, title and link for some news of interest of our competitors. Now I need you to present this data like a professional news reporting with covering all news not necessarily in order and then at the end write the Dates, clickable Titles with respective links as hyperlinks in a list with the heading: <Explore more>. Make sure to do hyperlinks so that people can click on links if they want to read more about any news. Here is all the data: {question}"
    # print(prompt)
    response = model.generate_content(prompt)
    return response.text


def MICROCHIP():
    global titles, source, dates, descriptions 

    for attempt in range(max_attempts):
        try:
            URL = "https://www.microchip.com/en-us/about/news-releases#" 
            options = webdriver.ChromeOptions()

            driver = webdriver.Chrome(options)
            driver.get(URL)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[@id='DataTables_Table_1']/tbody[@class='striped-bg']/tr"))
            )
            news = driver.find_elements(By.XPATH, "//table[@id='DataTables_Table_1']/tbody[@class='striped-bg']/tr")
            # news = []
            # for i in range(2):  
            #     table_id = f"DataTables_Table_{1-i}"
            #     news_items = driver.find_elements(By.XPATH, f"//table[@id='{table_id}']/tbody[@class='striped-bg']/tr")
            #     news.extend(news_items)

            temp_titles, temp_source, temp_dates, temp_descriptions, company_name = [], [], [], [], []

            for item in news:
                title = item.find_element(By.XPATH, ".//a").get_attribute('innerHTML')
                date_element = item.find_elements(By.XPATH, ".//td")
                date = date_element[1].text
                link = item.find_element(By.XPATH, ".//a").get_attribute('href')
                description = "NA"

                if(item == news[0]):
                    first_news_date = parse(date)

                if(parse(date) >= thirty_days_ago):
                    temp_titles.append(title)
                    temp_source.append(link)
                    temp_dates.append(parse(date))
                    temp_descriptions.append(description) 
                    company_name.append("Microchip")
                else:
                    break
            
            if(first_news_date < thirty_days_ago): 
                break

            if temp_titles:
                titles.extend(temp_titles)
                source.extend(temp_source)
                dates.extend(temp_dates)
                descriptions.extend(temp_descriptions)
                company.extend(company_name)
                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed, retrying... Error: {str(e)}")
        finally:
            driver.quit()

def NXP():
    global titles, source, dates, descriptions  # Ensure we're modifying global variables

    for attempt in range(max_attempts):
        try:
            URL = "https://www.nxp.com/company/about-nxp/newsroom:NEWSROOM"
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options)

            driver.get(URL)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='news-briefs']/ul/li/a"))
            )

            button = driver.find_element(By.XPATH, "//div[@id='news-briefs']/ul/li/a")
            driver.execute_script("arguments[0].click();", button)

            news = driver.find_elements(By.XPATH, "//div[@id='retrieved-results']/ul/li")  

            first_news_date = ""

            # Temporary lists to hold this attempt's news
            temp_titles, temp_source, temp_dates, temp_descriptions, company_name = [], [], [], [], []
            for item in news:
                title = item.find_element(By.XPATH, ".//span").get_attribute('innerHTML')
                date = item.find_element(By.XPATH, ".//div/div").get_attribute('innerHTML')
                link = item.find_element(By.XPATH, ".//h3/a").get_attribute('href')
                description = item.find_element(By.XPATH, ".//p/span").get_attribute('innerHTML')

                if(item == news[0]):
                    first_news_date = parse(date)

                if(parse(date) >= thirty_days_ago):
                    temp_titles.append(title)
                    temp_source.append(link)
                    temp_dates.append(parse(date))
                    temp_descriptions.append(description) 
                    company_name.append("NXP")
                else:
                    break
            
            if(first_news_date < thirty_days_ago): 
                break

            # If we reach here, no exceptions were thrown, so break the loop
            if temp_titles:
                titles.extend(temp_titles)
                source.extend(temp_source)
                dates.extend(temp_dates)
                descriptions.extend(temp_descriptions) 
                company.extend(company_name)
                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed, retrying... Error: {str(e)}")
        finally:
            # Close the driver after each attempt to ensure a fresh start
            driver.quit()

def STM():
    global titles, source, dates, descriptions 

    for attempt in range(max_attempts):
        try:
            URL = "https://newsroom.st.com/all-news/browse"
            options = webdriver.ChromeOptions()

            driver = webdriver.Chrome(options)
            driver.get(URL)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='grid-start']//div[@class='column-12--mobile-small column-4--tablet margin-bottom--1 no-padding--mobile']"))
            )

            news = driver.find_elements(By.XPATH, "//div[@id='grid-start']//div[@class='column-12--mobile-small column-4--tablet margin-bottom--1 no-padding--mobile']")

            temp_titles, temp_source, temp_dates, temp_descriptions, company_name = [], [], [], [], []
            for item in news:
                title = item.find_element(By.XPATH, ".//div[@class='stn-card__title']/h4").get_attribute('innerHTML')
                date_element = item.find_element(By.XPATH, ".//div[@class='stn-card__date']")
                span_date_element = date_element.find_element(By.XPATH, ".//span")
                span_date = span_date_element.get_attribute('innerHTML')
                remaining_date = date_element.text[len(span_date):]  
                date = span_date + remaining_date
                link = item.find_element(By.XPATH, ".//a").get_attribute('href')
                description = "NA"

                if(item == news[0]):
                    first_news_date = parse(date)

                if(parse(date) >= thirty_days_ago):
                    temp_titles.append(title)
                    temp_source.append(link)
                    temp_dates.append(parse(date))
                    temp_descriptions.append(description) 
                    company_name.append("STM")
                else:
                    break
            
            if(first_news_date < thirty_days_ago): 
                break

            if temp_titles:
                titles.extend(temp_titles)
                source.extend(temp_source)
                dates.extend(temp_dates)
                descriptions.extend(temp_descriptions) 
                company.extend(company_name)
                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed, retrying... Error: {str(e)}")
        finally:
            driver.quit()

def ESPRESSIF():
    global titles, source, dates, descriptions 

    for attempt in range(max_attempts):
        try:
            URL = "https://www.espressif.com/en/company/newsroom/news" 
            options = webdriver.ChromeOptions()

            driver = webdriver.Chrome(options)
            driver.get(URL)

            news = driver.find_elements(By.XPATH, "//div[@id='block-system-main']/div/div/div/div/ul/li")

            temp_titles, temp_source, temp_dates, temp_descriptions, company_name = [], [], [], [], []
            for item in news:
                title = item.find_element(By.XPATH, ".//div[@class='views-field views-field-title']/span/a").get_attribute('innerHTML')
                date = item.find_element(By.XPATH, ".//div[@class='views-field views-field-field-date']/div/span").get_attribute('innerHTML')
                link = item.find_element(By.XPATH, ".//div[@class='views-field views-field-title']/span/a").get_attribute('href')
                description = item.find_element(By.XPATH, ".//div[@class='views-field views-field-body']/div").get_attribute('innerHTML')

                if(item == news[0]):
                    first_news_date = parse(date)

                if(parse(date) >= thirty_days_ago):
                    temp_titles.append(title)
                    temp_source.append(link)
                    temp_dates.append(parse(date))
                    temp_descriptions.append(description) 
                    company_name.append("Expressif")
                else:
                    break
            
            if(first_news_date < thirty_days_ago): 
                break

            if temp_titles:
                titles.extend(temp_titles)
                source.extend(temp_source)
                dates.extend(temp_dates)
                descriptions.extend(temp_descriptions) 
                company.extend(company_name)
                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed, retrying... Error: {str(e)}")
        finally:
            driver.quit()

def SILICON_LABS():
    global titles, source, dates, descriptions  

    for attempt in range(max_attempts):
        try:
            URL = "https://news.silabs.com/" 
            options = webdriver.ChromeOptions()

            driver = webdriver.Chrome(options)
            driver.get(URL)

            news = driver.find_elements(By.XPATH, "//div[@id='wd_featurebox-teaser_1382_tab_content']/div/div/div/div")

            temp_titles, temp_source, temp_dates, temp_descriptions, company_name = [], [], [], [], []
            for item in news:
                title = item.find_element(By.XPATH, ".//div[@class='wd_content_wrapper']/div[@class='wd_title']/a").get_attribute('innerHTML')
                date = item.find_element(By.XPATH, ".//div[@class='wd_content_wrapper']/div[@class='wd_content-header']/div[@class='wd_date']").text
                link = item.find_element(By.XPATH, ".//div[@class='wd_content_wrapper']/div[@class='wd_title']/a").get_attribute('href')
                description = item.find_element(By.XPATH, ".//div[@class='wd_content_wrapper']/div[@class='wd_summary']/p").get_attribute('innerHTML')

                if(item == news[0]):
                    first_news_date = parse(date)

                if(parse(date) >= thirty_days_ago):
                    temp_titles.append(title)
                    temp_source.append(link)
                    temp_dates.append(parse(date))
                    temp_descriptions.append(description) 
                    company_name.append("Silicon Labs")
                else:
                    break
            
            if(first_news_date < thirty_days_ago): 
                break

            if temp_titles:
                titles.extend(temp_titles)
                source.extend(temp_source)
                dates.extend(temp_dates)
                descriptions.extend(temp_descriptions) 
                company.extend(company_name)
                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed, retrying... Error: {str(e)}")
        finally:
            driver.quit()


if submit and days:
    try:
        MICROCHIP()
    except Exception as e:
        print(f"Could not fetch news from MICROCHIP: {str(e)}")

    # time.sleep(0.5)
    print(1)

    try:
        NXP()
    except Exception as e:
        print(f"Could not fetch news from NXP: {str(e)}")

    # time.sleep(0.5)
    print(2)

    try:
        STM()
    except Exception as e:
        print(f"Could not fetch news from STM: {str(e)}")

    # time.sleep(0.5)
    print(3)

    try:
        ESPRESSIF()
    except Exception as e:
        print(f"Could not fetch news from ESPRESSIF: {str(e)}")

    # time.sleep(0.5)
    print(4)

    try:
        SILICON_LABS()
    except Exception as e:
        print(f"Could not fetch news from SILICON LABS: {str(e)}")
    print(5)

    dict = {'DATE': dates, 'COMPANY': company, 'TITLE': titles, 'SOURCE LINK': source, 'DESCRIPTION': descriptions}
    print(dict)
    df = pd.DataFrame(dict)

    if not df.empty:
        df = df.sort_values(
            by="DATE",
            ascending=False
        )
        print(df.head(49))
    else:
        print("No news found.")


    search_words = ['Security', 'IoT', 'Microcontroller', 'security', 'MCU', 'matter', 'smart home', 'PSA', 'FIPS', 'Common Criteria']

    matched_news = []
    for index, row in df.iterrows():
        for word in search_words:
            if word in row['TITLE'] or word in row['DESCRIPTION']:
                matched_news.append(f"Date: {row['DATE']}, Company: {row['COMPANY']}, Headline: {row['TITLE']}, Description: {row['DESCRIPTION']}, Source Link: {row['SOURCE LINK']}\n")
                break

    matched_news_string = '\n'.join(matched_news)
    
    final_response = get_gemini_response (matched_news_string)
    st.subheader("News of interest:")
    st.write("\n", final_response)

    

