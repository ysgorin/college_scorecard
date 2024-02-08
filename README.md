# College Scorecard Data Import

## Project Overview
This developer was tasked with creating an automation to import [College Scorecard Data](https://collegescorecard.ed.gov/data/) into a data warehouse using the automation tool, [Workato](https://www.workato.com/).

At the time of this writing, Workato's HTTP app did not support API names that have periods in their name. For example, '2021.earnings.10_yrs_after_entry.gt_threshold' In Workato, that API name would be processed as 'gt_threshold' which is nested in '10_yrs_after_entry' which is nested in 'earnings' which is nested in '2021.'

This developer used Workato's Python snippets app to make the API request and convert the data into a CSV for use in later automation steps.

The Python executable, [College Scorecard Request](college_scorecard_request.py), is the complete process of the API request. In practice, only the function is used in the Python executable step as the for loops and input parameter defintions are in earlier automation steps.

Technologies used: Python