from scrape_no_captcha_v2 import *
from random import random
import datetime

casenum = "GT20013174-00"
case_nums = [casenum]
case_details_file = open('data/case_details.tsv','w',1)
case_hearing_details_file = open('data/case_hearing_details.tsv','w',1)
case_service_details_file = open('data/case_service_details.tsv','w',1)

driver = driver(True)

starttime = datetime.datetime.now()
for casenum in case_nums:
    try:
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
            case_hearing_details_file.write(casenum + '\t' + x + "\n")
    except Exception as e:
        print(str(e))

endtime = datetime.datetime.now()

case_details_file.close()
case_hearing_details_file.close()
case_service_details_file.close()
