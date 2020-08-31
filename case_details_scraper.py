# coding: utf-8
from scrape_no_captcha_v2 import *
from random import random
import datetime

case_nums = get_ipython().getoutput("cat data/cases_2020* | cut -d '#' -f2 | cut -d ':' -f2 | cut -d ' ' -f2 | cut -c 1-13 | grep -v 'GC' | sort | uniq")
case_nums = list(case_nums)
total_cases = len(case_nums)
driver = driver(True)
loopcounter = 0

case_details_file = open('data/case_details.tsv','a',1)
case_hearing_details_file = open('data/case_hearing_details.tsv','a',1)
case_service_details_file = open('data/case_service_details.tsv','a',1)

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
driver.close()
case_details_file.close()
case_hearing_details_file.close()
case_service_details_file.close()
