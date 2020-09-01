# coding: utf-8
from scrape_no_captcha_v2 import *

case_files = os.listdir('data')

os.chdir('data')

for x in case_files:
    if x in ['selected_charges.txt','selected_cases.txt']:
        continue
    with open(x) as case_file:
        cases_by_day  = []
        for line in case_file:
            cases_by_day.append(line)
        cases = format_case_summaries(cases_by_day)
        newfile = 'formatted_' + x
        with open(newfile,'w') as formatted_cases:
            for record in cases:
                formatted_cases.write(record)
