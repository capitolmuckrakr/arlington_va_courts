# coding: utf-8

import os, csv, datetime

def nextdate(year=2020):
    HOME = os.environ.get('HOME')
    csv_dir = HOME + '/Downloads'
    csv_filename = csv_dir + '/VA_court_weekends_holidays.csv'
    invalid_dates = []
    with open(csv_filename, "r") as filing_csv:
        reader = csv.reader(filing_csv)
        next(reader)
        for row in reader:
            invalid_date = row[:3]
            invalid_date = datetime.date(int(invalid_date[0]),int(invalid_date[1]),int(invalid_date[2]))
            invalid_dates.append(invalid_date)
    courtdate = datetime.date(year,1,1)
    enddate = datetime.date(year,12,31)
    while courtdate < enddate:
        if not courtdate in invalid_dates:
            yield courtdate.strftime('%m/%d/%Y')
        courtdate = courtdate + datetime.timedelta(days=1)
