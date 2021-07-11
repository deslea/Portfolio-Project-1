# This file is a portfolio project by Deslea Selmes for the 
# Codecademy Pro Data Analysis Career Path. It is a limited-
# guidance project with basic defined outcomes (data extraction
# and analysis) of a provided csv dataset (pretty clean, no nulls),
# to be written in Python on your own environment (mine is VS Code).
# No starting code was provided, and no analysis questions - part
# of the task is to self-define questions/analysis tasks that may be
# of use to a client (who is not defined). The dataset contains 
# basic data about a set of customers of medical insurance.

# I have positioned this as a short analysis for a hypothetical 
# client, the marketing department. They intend to run a feelgood
# advertorial campaign providing quit-smoking resources to current
# and prospective customers. They want to know the impact of 
# quitting smoking on premiums, and also information to target
# the advertorials (smoking rates among, for instance, women
# with children) and regional variations.

# Much of this analysis would be better done in SQL but this was
# outside the parameters of the project.

import csv

# CSV fields are age: n, sex: male/female, bmi: float, children: n (0 for none), 
# smoker: yes/no, region: str, charges: float (not limited to 2 dec)

insurance_raw = []

with open('insurance.csv') as csvfile:
    input_file = csv.reader(csvfile)
    for row in input_file:
        insurance_raw.append(row)

# Clean up data types
# Build per-variable lists for ease of single-factor analysis

def get_data(selector, lst):
    for ea in insurance_raw:
        if ea[0] == 'age':
            continue
        elif selector == 'age':
            lst.append(int(ea[0]))
        elif selector == 'sex':
            lst.append(ea[1])
        elif selector == 'bmi':
            lst.append(float(ea[2]))
        elif selector == 'chn':
            lst.append(int(ea[3]))
        elif selector == 'smoker':
            lst.append(ea[4])
        elif selector == 'region':
            lst.append(ea[5])
        elif selector == 'charges':
            lst.append(float(ea[6]))

lst_age = []
lst_sex = []
lst_bmi = []
lst_chn = []
lst_smoker = []
lst_region = []
lst_charges = []
get_data('age', lst_age)
get_data('sex', lst_sex)
get_data('bmi', lst_bmi)
get_data('chn', lst_chn)
get_data('smoker', lst_smoker)
get_data('region', lst_region)
get_data('charges', lst_charges)

# Build dictionary for deeper analysis

custDict = {}
i = 0
while i < len(lst_age):
    custDict[i] = {'age': lst_age[i], 'sex': lst_sex[i], 'bmi': lst_bmi[i], 'chn': lst_chn[i], 'smoker': lst_smoker[i], 'region': lst_region[i], 'charges': lst_charges[i]}
    i += 1

#print(custDict)

# Analysis Questions:
# Number/% of smokers in the set
# Number/% of smokers separated by gender
# Number/% of smokers among people with children (total and separated by gender)
# Number/% of smokers by region (total and separated by gender)
# Difference in average insurance cost between smokers and non-smokers
# Dataset has no nulls and no provision for nonbinary. Total = m+f.

# slice data by gender and smoker status

female_smokers = []
male_smokers = []
female_nonsmokers = []
male_nonsmokers = []

for ea in custDict:
    my_customer_id = ea
    my_customer_info = custDict[ea]
    my_customer_smoker = my_customer_info['smoker']
    my_customer_sex = my_customer_info['sex']
    if my_customer_smoker == 'yes':
        if my_customer_sex == 'male':
            male_smokers.append(my_customer_info)
        else:
            female_smokers.append(my_customer_info)
    else:
        if my_customer_sex == 'male':
            male_nonsmokers.append(my_customer_info)
        else:
            female_nonsmokers.append(my_customer_info)

# Get overall population figures

num_customers = len(custDict)
num_customers_m = len(male_smokers) + len(male_nonsmokers)
num_customers_f = len(female_smokers) + len(female_nonsmokers)
num_smokers_m = len(male_smokers)
num_smokers_f = len(female_smokers)
num_smokers = num_smokers_m + num_smokers_f
num_nonsmokers_m = len(male_nonsmokers)
num_nonsmokers_f = len(female_nonsmokers)
num_nonsmokers = num_nonsmokers_m + num_nonsmokers_f
percent_smokers = str(round((num_smokers/num_customers * 100), 2)) + '%'
percent_smokers_m = str(round((num_smokers_m/num_customers_m * 100), 2)) + '%'
percent_smokers_f = str(round((num_smokers_f/num_customers_f * 100), 2)) + '%'

# Results
print("\nCustomer Breakdown:\n")
print("All Customers:", num_customers)
print("All Males:", num_customers_m)
print("All Females:", num_customers_f)
print("Smoking Males:", num_smokers_m)
print("Smoking Females:", num_smokers_f)
print("\nCommentary:\n")
print("Smokers make up", percent_smokers, "of the customers analysed.")
print("Male smokers make up", percent_smokers_m, "of male customers.")
print("Female smokers make up", percent_smokers_f, "of female customers.\n")

# Extract insurance pricing difference and slice by whether or not children
total_charges_s = 0
total_charges_ns = 0
smokers_nochildren_m = 0
smokers_nochildren_f = 0

for ea in male_smokers:
    total_charges_s += ea['charges']
    if ea['chn'] == 0:
        smokers_nochildren_m += 1

for ea in female_smokers:
    total_charges_s += ea['charges']
    if ea['chn'] == 0:
        smokers_nochildren_f += 1

for ea in male_nonsmokers:
    total_charges_ns += ea['charges']

for ea in female_nonsmokers:
    total_charges_ns += ea['charges']

avg_charges_ns = round(total_charges_ns/num_nonsmokers)
avg_charges_s = round(total_charges_s/num_smokers)
str_avg_charges_ns = str('$' + str(avg_charges_ns))
str_avg_charges_s = str('$' + str(avg_charges_s))
avg_charges_diff = avg_charges_s - avg_charges_ns
str_avg_charges_diff = str('$' + str(avg_charges_diff))
smokers_withchildren_m = num_smokers_m - smokers_nochildren_m
smokers_withchildren_f = num_smokers_f - smokers_nochildren_f
smokers_children_percent_m = str(round(smokers_withchildren_m/num_smokers_m * 100)) + '%'
smokers_children_percent_f = str(round(smokers_withchildren_f/num_smokers_f * 100)) + '%'

# Results

print("Smokers pay on average " + str_avg_charges_s + " for medical insurance. This is " + str_avg_charges_diff + " more than nonsmokers.")
print(smokers_children_percent_m + " of male smokers have children and " + smokers_children_percent_f + " of female smokers have children.")

# Slice into regions

smoker_regions = {'northeast': 0, 'northwest': 0, 'southeast': 0, 'southwest': 0}
nonsmoker_regions = {'northeast': 0, 'northwest': 0, 'southeast': 0, 'southwest': 0}

def divide_regions(lst, smoker):
    if smoker == 'TRUE':
        add_to = smoker_regions
    else:
        add_to = nonsmoker_regions
    for ea in lst:
        if ea['region'] == 'northeast':
            add_to['northeast'] += 1
        elif ea['region'] == 'northwest':
            add_to['northwest'] += 1
        if ea['region'] == 'southeast':
            add_to['southeast'] += 1
        elif ea['region'] == 'southwest':
            add_to['southwest'] += 1       

divide_regions(male_smokers, 'TRUE')
divide_regions(female_smokers, 'TRUE')
divide_regions(male_nonsmokers, 'FALSE')
divide_regions(female_nonsmokers, 'FALSE')     

#regions (all)
northeast_s = smoker_regions['northeast']
northwest_s = smoker_regions['northwest']
southeast_s = smoker_regions['southeast']
southwest_s = smoker_regions['southwest']
northeast_ns = nonsmoker_regions['northeast']
northwest_ns = nonsmoker_regions['northwest']
southeast_ns = nonsmoker_regions['southeast']
southwest_ns = nonsmoker_regions['southwest']

region_percent = lambda i, ii: round(i/(i + ii) * 100)

# Result
print('\nRegional Breakdown:')
print("Smokers in the Northeast make up", + region_percent(northeast_s, northeast_ns), "percent of customers there.")
print("Smokers in the Northwest make up", + region_percent(northwest_s, northwest_ns), "percent of customers there.")
print("Smokers in the Southeast make up", + region_percent(southeast_s, southeast_ns), "percent of customers there.")
print("Smokers in the Southwest make up", + region_percent(southwest_s, southwest_ns), "percent of customers there.")