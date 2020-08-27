# coding: utf-8
from scrape_no_captcha_v2 import *
from nextdate import nextdate
from random import random
import datetime
#LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
#logger = logging.getLogger("arlington-court-scraper."+__name__)
#logger.setLevel(LOGLEVEL)

dates = nextdate(2020)
driver = driver(True)
loopcounter = 0
while True:
    try:
        loopcounter+=1
        courtdate = next(dates)
        enddate = datetime.date.today()
        enddate = enddate.strftime('%m/%d/%Y')
        if courtdate == enddate:
            break
        print("Checking cases for {}".format(courtdate))
        court_date = courtdate.split("/")
        filename = 'data/cases_' + court_date[2] + court_date[0] + court_date[1] + '.txt'
        if os.path.isfile(filename):
            print("Already saved",filename,"skipping")
            continue
        start_page(driver)
        terms(driver)
        search_setup(driver)
        date_search(driver,courtdate)
        sleep(5)
        pagecount = 0
        while results_next_page(driver):
            pagecount+=1
            print("advancing from page {} to next page".format(pagecount))
            sleep(waittime)
            
        cases = results(driver)
        print("Saving results to", filename)
        with open(filename,'w') as outfile:
            if cases:
                outfile.write(cases)
            else:
                outfile.write("No cases found, search this date again")
        sleep(2)
        if (loopcounter % 25) == 0:
            sleep(int((random() * 10)//1))
    except StopIteration:
        break
driver.close()
