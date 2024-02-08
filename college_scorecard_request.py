# Dependencies
import requests
import pandas as pd
import datetime as dt
from api_key import api_key

# Make initial API call to retrieve total records
# Base URL
base_url = 'https://api.data.gov/ed/collegescorecard/v1/schools.json?'
initial_url = base_url + 'api_key=' + api_key
initial_result = requests.get(initial_url).json()
total_records = initial_result['metadata']['total']

# Calculate number of pages of data using 100 records per page
pages = list(range(1,(total_records//100 + 1)))

# Create year list to request five years of data
year_list = list(range(5))

# Create variable to store number of records on current page. One
# hundred pages for all pages except for the last page.
page_iterations = 100

# Workato, the automation/integration service this writer is using, requires 
# the function to be named 'main' and the parameter to be named 'input.' 
def main(input):
    # Base URL
    base_url = 'https://api.data.gov/ed/collegescorecard/v1/schools.json?'
    # API Key
    api_key = input['api_key']
    # Output Fields
    fields = 'id,' \
            'ope6_id,' \
            'ope8_id,' \
            'school.name,' \
            + str(input['data_year']) + '.earnings.10_yrs_after_entry.gt_threshold,' \
            + str(input['data_year']) + '.earnings.6_yrs_after_entry.gt_threshold,' \
            + str(input['data_year']) + '.earnings.8_yrs_after_entry.gt_threshold,' \
            + str(input['data_year']) + '.aid.median_debt.completers.overall'
    # Total Records Per Page
    per_page = '100'
    # Page Number
    page = str(input['page'])
    # Full URL
    url = base_url + 'api_key=' + api_key + '&fields=' + fields + '&per_page=' + per_page + '&page=' + page

    # API Request
    result = requests.get(url).json()
	
    # Create empty list to store results
    results_list = []
    
    # Loop through results
    for i in range(int(input['page_iterations'])):
        results_list.append({'UNITID': result['results'][(i)]['id'],
        'OPEID6': result['results'][(i)]['ope6_id'],
        'OPEID': result['results'][(i)]['ope8_id'],
        'INSTNM': result['results'][(i)]['school.name'],
        'GT_THRESHOLD_P10': result['results'][(i)][(str(input['data_year']) + '.earnings.10_yrs_after_entry.gt_threshold')],
        'GT_THRESHOLD_P6': result['results'][(i)][(str(input['data_year']) + '.earnings.6_yrs_after_entry.gt_threshold')],
        'GT_THRESHOLD_P8': result['results'][(i)][(str(input['data_year']) + '.earnings.8_yrs_after_entry.gt_threshold')],
        'GRAD_DEBT_MDN': result['results'][(i)][(str(input['data_year']) + '.aid.median_debt.completers.overall')],
        'DATA_YEAR': input['data_year']})

    # Create DataFrame
    df = pd.DataFrame(results_list)
    # Convert DataFrame to CSV
    csv = df.to_csv(index=False)
    
    # Workato requires a dictionary output.
    # Return CSV
    return {'csv': csv}

# Loop through year list to request five years of data
for year in year_list:
    # Define data year based on current year minus year_list index
    data_year = dt.datetime.now().year - year
    # Loop through pages to select page number in API request
    for page in pages:
        # Determine number of iterations for current page
        # Last page not divisible by 100 needs to be calculated
        if page == len(pages) and (total_records % 100 != 0):
            page_iterations = total_records % 100
        # Any other page or last page divisible by 100 is 100
        else:
            page_iterations = 100
        # Create input dictionary for main function
        input = {'data_year': data_year,
                 'page': page,
                 'page_iterations': page_iterations,
                 'api_key': api_key}
        # Print progress note to console
        print(f'Requesting page {page} for {data_year}')
        page_result = main(input)
        print(page_result)