import os

def field_size(index):
    HOME = os.environ['HOME']
    longest_field_length = 0
    longest_field_val = ''
    file_dir = HOME + '/scripts/arlington_va_courts/data'
    os.chdir(file_dir)
    case_files = os.listdir()
    for x in case_files:
        if x in ['selected_charges.txt','selected_cases.txt','scraped_originals']:
            continue
        with open(x) as file:
            for line in file:
                field = line.split("\t")[index]
                fieldlength = len(field)
                if fieldlength > longest_field_length:
                    longest_field_length = fieldlength
                    longest_field_val = field
    print(longest_field_val,longest_field_length)
