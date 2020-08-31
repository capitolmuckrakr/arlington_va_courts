# coding: utf-8
import re
from scrape_captcha import *
from time import sleep
from datetime import datetime

waittime = 5

def start_page(driver=driver):
    driver.implicitly_wait(1)
    driver.get("https://eapps.courts.state.va.us/ocis/landing/false")
    
def terms(driver=driver):
    try:
        #element = driver.find_element_by_id("acceptTerms")
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "acceptTerms")))
    except ElementClickInterceptedException:
        sleep(2)
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "acceptTerms")))
    sleep(1)
    element.click()

def search_setup(driver=driver,waittime=waittime):
    driver.find_element_by_id("searchBy").click()
    element = driver.find_element_by_css_selector("input[type='radio'][value='Hearing Date']").click()
    driver.find_element_by_id("searchBy").click()
    driver.find_element_by_id("courtLevelSelectBtn").click()
    driver.find_element_by_id("courtLevelLabel0").click()
    driver.find_element_by_id("courtLevelSelectBtn").click()
    driver.find_element_by_id("allCourtTitle").click()
    element = driver.find_element_by_id("courtSearch")
    element.send_keys("Arlington")
    driver.find_element_by_id("selectCourtSpan0").click()
    driver.find_element_by_id("applyCourtBtn").click()
    driver.implicitly_wait(waittime)

def search_setup_cases(driver=driver,waittime=waittime):
    driver.find_element_by_id("searchBy").click()
    element = driver.find_element_by_css_selector("input[type='radio'][value='Case Number']").click()
    driver.find_element_by_id("searchBy").click()
    driver.find_element_by_id("courtLevelSelectBtn").click()
    driver.find_element_by_id("courtLevelLabel0").click()
    driver.find_element_by_id("courtLevelSelectBtn").click()
    element = driver.find_element_by_id("courtSearch")
    driver.find_element_by_class_name("red-message").click()
    element.send_keys("Arlington")
    driver.find_element_by_id("selectCourtSpan0").click()
    driver.find_element_by_id("applyCourtBtn").click()
    driver.implicitly_wait(waittime)

def results(driver=driver):
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))
        result_list = element.text[43:][:-7]
        result_list = result_list.replace('\nCase','\tCase')
        result_list = result_list.replace('\nDefendant','\tDefendant')
        result_list = result_list.replace('\nComplainant','\tComplainant')
        result_list = result_list.replace('\nHearing','\tHearing')
        result_list = result_list.replace('\nAmended Charge','\tAmended Charge')
        result_list = result_list.replace('\nCharge','\tCharge')
        result_list = result_list.replace('\nResult','\tResult')
        return result_list
    except:
        return False

def results_next_page(driver=driver,waittime=waittime):
    try:
        driver.implicitly_wait(waittime)
        try:
            element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.ID, "loadMore")))
        except TimeoutException:
            #print("End of results")
            return False
        sleep(waittime)
        try:
            sleep(1)
            element.click()
        except StaleElementReferenceException:
            #print("End of results")
            return False
        except ElementClickInterceptedException:
            try:
                sleep(waittime)
                element.click()
            except StaleElementReferenceException:
                #print("End of results")
                return False
        return True
    except NoSuchElementException:
        #print("End of results")
        return False
    return True

def case_search(driver=driver,case = "GT20008944-00"):
    element = driver.find_element_by_id("caseNumberSearchField")
    element.send_keys(case)
    element.send_keys(Keys.ENTER)

def case_number(driver=driver):
    #Defendant Information
    return driver.find_element_by_id('caseNumberValue').text

def case_details_hearing_info(driver=driver):
    hearing_info_table = driver.find_element_by_id('hearingInfoTable')
    return hearing_info_table

def case_details_service_info(driver=driver):
    try:
        service_info_table = driver.find_element_by_id('serviceInfosTable')
    except NoSuchElementException:
        return False
    return service_info_table

def case_details_info_items(items):
    pattern = '\t\t\t'
    rows = []
    for row in items.find_elements_by_tag_name('tr'):
        try:
            rowval = ''
            for col in row.find_elements_by_tag_name('td'):
                if col.text:
                    rowval += col.text
                rowval += "\t"        
        except NoSuchElementException:
            pass
        #rowval = rowval.replace(pattern,'')
        rows.append(rowval)
    return rows

def case_details(driver=driver):
    #Defendant Information
    defendant_name = driver.find_element_by_id('defendantValue').text
    try:
        appealdatemessage = driver.find_element_by_id('appealDateMessage').text
    except NoSuchElementException:
        appealdatemessage = ''
    defendant_address = driver.find_element_by_id('addressValuespan').text
    defendant_gender = driver.find_element_by_id('genderValue').text
    defendant_race = driver.find_element_by_id('raceValue').text
    defendant_dob = driver.find_element_by_id('dateOfBirthValue').text
    defendant_attorney = driver.find_element_by_id('attorneyValue').text
    #Case/Charge Information
    defendant_status = driver.find_element_by_id('defendantStatusValue').text
    case_filed_date = driver.find_element_by_id('feildDateValue').text
    locality = driver.find_element_by_id('localityValue').text
    code_section = driver.find_element_by_id('codeSectionLink').text
    case_charge = driver.find_element_by_id('chargeValue').text
    case_type = driver.find_element_by_id('caseTypeValue').text
    case_class = driver.find_element_by_id('classValue').text
    offense_date = driver.find_element_by_id('offenseDateValue').text
    arrest_date = driver.find_element_by_id('arrestDateValue').text
    complainant = driver.find_element_by_id('complainantValue').text
    amended_code_section = driver.find_element_by_id('amendedCodeSectionValue').text
    amended_case_charge = driver.find_element_by_id('amendedChargeValue').text
    amended_case_type = driver.find_element_by_id('amendedCaseTypeValue').text
    amended_case_class = driver.find_element_by_id('amendedCclassValue').text
    #Appeal Information
    #Hearing Information
    #Disposition Information
    disposition = driver.find_element_by_id('dispositionValue').text
    try:
        disposition_message = driver.find_element_by_id('dispMessageId').text
    except NoSuchElementException:
        disposition_message = ''
    sentence_time = driver.find_element_by_id('sentenceTimeValue').text
    sentence_suspended = driver.find_element_by_id('sentenceSuspendedValue').text
    probation_type = driver.find_element_by_id('probationTypeValue').text
    probation_time = driver.find_element_by_id('probationTimeValue').text
    probation_starts = driver.find_element_by_id('probationStartsValue').text
    operator_license_suspension_time = driver.find_element_by_id('operatorLicenseSuspensionTimeValue').text
    restriction_effective_date = driver.find_element_by_id('restrictionEffectiveDateValue').text
    operator_license_restriction_codes = driver.find_element_by_id('operatorLicenseRestrictionCodesValue').text
    vasap = driver.find_element_by_id('vasapValue').text
    fine = driver.find_element_by_id('fineValue').text
    cost = driver.find_element_by_id('costValue').text
    cost_fine = driver.find_element_by_id('costFineValue').text
    fine_costs_paid = driver.find_element_by_id('fineAndCostsPaidValue').text
    fine_costs_paid_date = driver.find_element_by_id('fineAndCostsPaidDateValue').text
    #Service/Process
    case_detail_results = [defendant_name,defendant_address,defendant_gender,defendant_race,defendant_dob,defendant_attorney,defendant_status,case_filed_date,locality,code_section,case_charge,case_type,case_class,offense_date,arrest_date,complainant,amended_code_section,amended_case_charge,amended_case_type,amended_case_class,
    disposition,disposition_message,sentence_time,sentence_suspended,probation_type,probation_time,probation_starts,operator_license_suspension_time,restriction_effective_date,operator_license_restriction_codes,vasap,fine,cost,cost_fine,fine_costs_paid,fine_costs_paid_date
    ]
    return case_detail_results

def read_case_summaries(filepath):
    cases = []
    if os.path.isfile(filepath):
        with open(filepath) as file:
            for case in file.read().split("\n"):
                case_fields = case.split("\t")
                cases.append(case_fields)
            return cases
    else:
        return False
