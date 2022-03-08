from asyncore import read
import csv
import json
from textwrap import indent

folder = 'stack-overflow-developer-survey-2021'

with open(f'{folder}/survey_results_public.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = ['ResponseId', 'MainBranch', 'Employment', 'Country', 'US_State', 'UK_Country', 'EdLevel', 'Age1stCode', 'LearnCode', 'YearsCode', 'YearsCodePro', 'DevType', 'OrgSize', 'Currency', 'CompTotal', 'CompFreq', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith', 'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith', 'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith', 'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'OpSys', 'NEWStuck', 'NEWSOSites', 'SOVisitFreq', 'SOAccount', 'SOPartFreq', 'SOComm', 'NEWOtherComms', 'Age', 'Gender', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth', 'SurveyLength', 'SurveyEase', 'ConvertedCompYearly']
    trans_i = header.index('Trans')
    gender_i = header.index('Gender')
    country_i = header.index('Country')
    state_i = header.index('US_State')

    res = {

        "count_trans": 0,
        "count_gnc": 0,
        "sample": 0,

        "count_trans_ny": 0,
        "count_gnc_ny": 0,
        "sample_ny": 0,

        "count_trans_ca": 0,
        "count_gnc_ca": 0,
        "sample_ca": 0,

        "trans_results": {
            '% Trans USA': 0,
            '% Trans NY': 0,
            '% Trans CA': 0
        },

        "gnc_results": {
            '% nc USA': 0,
            '% nc NY': 0,
            '% nc CA': 0
        },

        "trans_umbrella": {
            '% USA': 0,
            '% NY': 0,
            '% CA': 0
        }

    }

    for row in reader:

        if (row[country_i] == "United States of America"): # Checks to see if living in USA

            if (row[state_i] == 'California'):
                res['sample_ca'] += 1 
            if (row[state_i] == 'New York'):
                res['sample_ny'] += 1 

            if (row[gender_i] == 'Non-binary, genderqueer, or gender non-conforming'):
                if (row[state_i] == 'California'):
                    res['count_gnc_ca'] += 1 
                if (row[state_i] == 'New York'):
                    res['count_gnc_ny'] += 1 
                res['count_gnc'] += 1

            if (row[trans_i] == "Yes"):
                if (row[state_i] == 'California'):
                    res['count_trans_ca'] += 1 
                if (row[state_i] == 'New York'):
                    res['count_trans_ny'] += 1 
                res['count_trans'] += 1
            
            res['sample'] += 1

    res['trans_results']['% Trans USA'] = round((res['count_trans'] / res['sample'])*100, 2)
    res['trans_results']['% Trans CA'] = round((res['count_trans_ca'] / res['sample_ca'])*100, 2)
    res['trans_results']['% Trans NY'] = round((res['count_trans_ny'] / res['sample_ny'])*100, 2)

    res['gnc_results']['% nc USA'] = round((res['count_gnc'] / res['sample'])*100, 2)
    res['gnc_results']['% nc CA'] = round((res['count_gnc_ca'] / res['sample_ca'])*100, 2)
    res['gnc_results']['% nc NY'] = round((res['count_gnc_ny'] / res['sample_ny'])*100, 2)

    res['trans_umbrella']['% USA'] = res['trans_results']['% Trans USA'] + res['gnc_results']['% nc USA']
    res['trans_umbrella']['% CA'] = res['trans_results']['% Trans CA'] + res['gnc_results']['% nc CA']
    res['trans_umbrella']['% NY'] = res['trans_results']['% Trans NY'] + res['gnc_results']['% nc NY']

    with open('data.json', 'w') as outfile:
        
        outfile.write( json.dumps(res, indent=4) )

    print (res)