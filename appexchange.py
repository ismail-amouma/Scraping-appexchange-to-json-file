from asyncio.windows_events import NULL
from tkinter import E
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
import pandas as pd
import concurrent.futures
import json
final_list=[]
service = ChromeService(executable_path=ChromeDriverManager().install())
driver= webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://appexchange.salesforce.com/consulting")

button=WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH,'//button[@id="onetrust-accept-btn-handler"]'))).click()
select = Select(driver.find_element(By.ID, 'select_country'))
select.select_by_visible_text("Netherlands")
apply_button=driver.find_element(By.XPATH,"//button[@id='appx_btn_filter_apply']").click()
time.sleep(10)
total_links=int(int(driver.find_element(By.XPATH,'//*[@id="total-items-store"]').text)/28)
for i in range(total_links+1):
    try:
        see_more=WebDriverWait(driver, 50).until(
                                    EC.element_to_be_clickable((By.XPATH,'//button[@id="appx-load-more-button-id"]')))              
        driver.execute_script("arguments[0].click();", see_more)
    except:
        pass
links=driver.find_elements(By.XPATH,'//a[@class="appx-tile appx-tile-consultant tile-link-click"]')
links_list=[link.get_attribute('href') for link in links]
driver.quit()
switch = {
        "Jan" : 1,
        "Feb" : 2,
        "Mar" : 3,
        "Apr" : 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
}
def date_format_changer(date):

    spliteddate=date.replace(",","").split()
    year=spliteddate[2]
    mount=spliteddate[0]
    day=spliteddate[1]
    return year+"-"+str(switch.get(mount))+"-"+day+"T00:00:00.000Z"

def get_data(link):
        partner_details=[]
        Saleforce_expertise=[]
        industry_expertise=[]
        reviews=[]
        driver= webdriver.Chrome(service=service)
        driver.maximize_window()
        driver.get(link)
        try:
            button=WebDriverWait(driver, 120).until(
                                        EC.element_to_be_clickable((By.XPATH,'//button[@id="onetrust-accept-btn-handler"]'))).click()
        except:
            pass
        Partner=driver.find_element(By.XPATH,'//h1[@id="consulting-header-bar-title-id"]').text
        dic1={}
        dic1['Partner']=Partner
        try:
            About_infos=driver.find_elements(By.XPATH,'//div[@class="appx-extended-detail-subsection-label-description"]/div')
            for i in range(len(About_infos)):
                if About_infos[i].text=="Headquarters":
                    dic1['Headquarters']=About_infos[i+1].text
        except:
            dic1['Headquarters']=NULL
        try:
            a=driver.find_element(By.XPATH,'(//span[@class="appx-summary-bar_facts-value"])[2]').text
        except:
            a=NULL
        dic1['Projects Completed']=a
        try:
            b=driver.find_element(By.XPATH,'(//span[@class="appx-summary-bar_facts-value"])[3]').text
        except:
            b=NULL
        dic1['Certified Experts']=b
        try:
            c=driver.find_element(By.XPATH,'(//span[@class="appx-summary-bar_facts-value"])[3]').text
        except:
            c=NULL
        dic1['Founded']=c
        partner_details.append(dic1)
        button=driver.find_element(By.XPATH,'(//a[@class="slds-tabs_default__link"])[2]')
        driver.execute_script("arguments[0].click();", button)

        time.sleep(15)
        def get_table(id,list):
            Expertise=driver.find_elements(By.XPATH,f'//ul[@id="{id}"]/li')
            num_spec=driver.find_elements(By.XPATH,f'//*[@id="{id}"]/li/section/div/h3/button/span/span[2]')
            numbers=[int(number.text.split()[0]) for number in num_spec]
            data=[[expertie.get_attribute("psa-title"),expertie.get_attribute("psa-level")] for expertie in Expertise ]
            buttons=driver.find_elements(By.XPATH,f'//*[@id="{id}"]/li/section/div/h3/button')
            for button in buttons:
                driver.execute_script("arguments[0].click();", button)
            specializations=driver.find_elements(By.XPATH,f'//ul[@id="{id}"]/li/section/div/ul')
            specialization_list=[]
            for specilazation in specializations:
                specialization_list.extend(specilazation.text.splitlines())
            for count,number in enumerate(numbers,start=0):
                for j in range(number):
                    dica={}
                    dica['Expertise']=data[count][0]
                    dica['Specialization']=specialization_list[count+j]
                    dica['Level']=data[count][1]
                    list.append(dica)
        try:
            get_table("appx_accordion_products",Saleforce_expertise)
        except:
            Saleforce_expertise=NULL
        try:
            get_table("appx_accordion_industry",industry_expertise)
        except:
            industry_expertise=NULL
        dic1["salesforce_expertises"]=Saleforce_expertise
        dic1["industry_expertises"]=industry_expertise
        try:
            buttons=driver.find_elements(By.XPATH,'//*[@id="appx_accordion_certifications"]/li/section/div/h3/button')
            for button in buttons:
                driver.execute_script("arguments[0].click();", button)
            certis=driver.find_elements(By.XPATH,'//*[@id="appx_accordion_certifications"]/li/section/div/h3/button/span/span[1]')
            totals=driver.find_elements(By.XPATH,'//*[@id="appx_accordion_certifications"]/li/section/div/h3/button/span/span[2]')
            certi_list=[certi.text for certi in certis]
            total_list=[total.text.split()[0] for total in totals]
            total_type=driver.find_element(By.XPATH,'(//h2[@class="slds-text-heading_small"])[2]').text.split()[1].replace('(','').replace(')','')
            dic1["certification_total"]=total_type
            certis_types=driver.find_elements(By.XPATH,'//ul[@id="appx_accordion_certifications"]/li/section/div/ul')
            certification_type=[]
            for count,info in enumerate(certis_types,start=0):
                d={}
                d["Type"]=certi_list[count]
                d["certification_type_total"]=total_list[count]
                numbers=info.find_elements(By.TAG_NAME,"li")
                certification=[]
                for number in numbers:
                    dico={}
                    spans=number.find_elements(By.TAG_NAME,'span')
                    span_list=[span.text for span in spans]
                    dico["name"]=span_list[0]
                    dico["total "]=span_list[1]
                    certification.append(dico)
                    d["certification"]=certification
                certification_type.append(d)
            dic1["certifications"]=[{"certification_type": certification_type}]
        except:
            dic1["certifications"]=[{"certification_type": NULL}]

        button=driver.find_element(By.XPATH,'(//a[@class="slds-tabs_default__link"])[3]')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(15)
        try:
            total_review=driver.find_element(By.XPATH,'(//*[@id="reviewContainer"]/c-appx-questionnaire-base-container/span/div/c-appx-questionnaire-response-header/div/c-appx-questionnaire-response-stats/div/div/div[1])[1]').text.split()[0]
            dic1["review_total"]=total_review
            while True:
                try:
                    button=driver.find_element(By.XPATH,'//button[@class="slds-button slds-button_neutral"]')
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(4)
                except:
                    break
            showmore=driver.find_elements(By.XPATH,'//a[@class="slds-text-link_reset"]')
            for s in showmore:
                driver.execute_script("arguments[0].click();", s)
            commants=driver.find_elements(By.XPATH,'//div[@class="appx-review-content"]/p[3]')
            average_rating=driver.find_element(By.XPATH,'(//*[@id="reviewContainer"]/c-appx-questionnaire-base-container/span/div/c-appx-questionnaire-response-header/div/c-appx-questionnaire-response-rating/div/div/div[2]/div[1])[1]').text
            dic1["average_rating"]=average_rating
            reviws_deatil=driver.find_elements(By.XPATH,'//*[@class="appx-review-details"]')
            Dates=driver.find_elements(By.XPATH,'//a[@class="appx-create-new-comment"]')
            reviws_info_l=[]
            for review in reviws_deatil:
                x=review.text.splitlines()
                y=[NULL]*8
                for i in range(len(x)):
                    if x[i]=="Product Area":
                        y[1]=x[i+1].split(",")
                    elif x[i]=="Industry":
                        y[3]=x[i+1]
                    elif x[i]=="Project Length (months)":
                        y[5]=x[i+1]
                    elif x[i]=="Country":
                        y[7]=x[i+1]
                reviws_info_l.append(y)
            dates2=[date_format_changer(date.text) for date in Dates[0::2]]

            commant=[c.text for c in commants]
            for i in range(int(total_review)):
                dic={}
                dic["Product Area"]=reviws_info_l[i][1]
                dic["Industry"]=reviws_info_l[i][3]
                dic["Project Lenght"]=reviws_info_l[i][5]
                dic["Country"]=reviws_info_l[i][7]
                dic["Date"]=dates2[i]
                dic["Comment"]=' '.join(commant[i].splitlines())
                reviews.append(dic)
            dic1["reviews"]=reviews
        except:
            dic1["review_total"]=NULL
            dic1["average_rating"]=0
            dic1["reviews"]=NULL
        final_list.append(dic1)
        driver.quit()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(get_data, links_list)

with open('appex.json', 'w',encoding="latin1") as f:
    json.dump(final_list, f)



