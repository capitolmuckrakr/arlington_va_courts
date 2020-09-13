# coding: utf-8
from scrape_no_captcha_v2 import *
from random import random
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import datetime, os, sys

ENDPOINT_DB = os.environ['ENDPOINT_DB']
PGUSER = os.environ['PGUSER']
PGPASSWORD = os.environ['PGPASSWORD']
DB_NAME = os.environ['DB_NAME']
DB_URL = 'postgresql://' + PGUSER + ':' + PGPASSWORD + '@' + ENDPOINT_DB + '/' + DB_NAME

Browser = driver

def details_scraper(limitn,instancen):
    offset = int(limitn) * int(instancen)
    engine = create_engine(DB_URL)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    #sql to select only cases matching certain charges
    with open('bin/sql/case_nums_for_selected_charges.sql') as file:
        sql = text(file.read())
    result = conn.execute(sql,limitnum=limitn,offset=offset)
    case_nums = [x[0] for x in result]
    total_cases = len(case_nums)
    driver = Browser(True)
    loopcounter = 0
    file = 'data/case_details' + str(instancen) + '.tsv'
    case_details_file = open(file,'a',1)
    file = 'data/case_hearing_details' + str(instancen) + '.tsv'
    case_hearing_details_file = open(file,'a',1)
    file = 'data/case_service_details' + str(instancen) + '.tsv'
    case_service_details_file = open(file,'a',1)
    starttime = datetime.datetime.now()
    print(starttime)
    for casenum in case_nums:
        try:
            loopcounter+=1
            print("Checking case #{} of {}".format(loopcounter,total_cases))
            start_page(driver)
            terms(driver)
            search_setup_cases(driver)
            case_search(driver,casenum)
            results = case_details(driver)
            history = case_details_hearing_info(driver)
            hearing_info = case_details_info_items(history)
            hearing_info = [casenum + '\t' + x for x in hearing_info]
            new_results = []
            new_results.append(casenum)
            [new_results.append(x) for x in results]
            element = driver.find_element_by_id('serviceAndProcess')
            button = element.find_element_by_class_name('accordion-toggle')
            button.click()
            services = case_details_service_info(driver)
            if services:
                services_info = case_details_info_items(services)
                services_info = [casenum + '\t' + x for x in services_info]
                for x in services_info:
                    case_service_details_file.write(x + "\n")
            case_details_file.write("\t".join(new_results)+"\n")
            for x in hearing_info:
                case_hearing_details_file.write(x + "\n")
        except Exception as e:
            print(str(e))
        if (loopcounter % 3) == 0:
            sleep(int((random() * 10)//1))
        if (loopcounter % 25) == 0:
            sleep(int((random() * 100)//1))
        if (loopcounter % 600) == 0:
            sleep(int((random() * 30)//1))
    endtime = datetime.datetime.now()
    print(endtime)
    driver.close()
    case_details_file.close()
    case_hearing_details_file.close()
    case_service_details_file.close()

if __name__ == "__main__":
    (limitn, instancen) = sys.argv[1:3]
    details_scraper(limitn,instancen)