# Utility scrip to merge all numeric_adjusted_results by date

import os

# List all files in the folder with numeric_adjusted_results
numeric_adjustes_results_files = os.listdir('./data/dls/numeric_adjusted_results')

# Get the path for all the files
numeric_adjustes_results_files = [ f"./data/dls/numeric_adjusted_results/{file_name}" for file_name in numeric_adjustes_results_files ]

# Get the files 
all_numeric_adjustes_results = pd.concat(map(pd.read_csv, numeric_adjustes_results_files), ignore_index=True)


# Formatting the data 
all_numeric_adjustes_results['ISO_639'] = all_numeric_adjustes_results['ISO_639'].astype('str')
all_numeric_adjustes_results['cluster'] = all_numeric_adjustes_results['cluster'].astype('str')
all_numeric_adjustes_results['date'] = pd.to_datetime(all_numeric_adjustes_results['date'])


# Cleaning the data
# TODO: REMOVE WRONG ISO IN R SCRIPT, !!!!!!!!!!!!IMPORTANT!!!!!!!!!!!!
all_numeric_adjustes_results = all_numeric_adjustes_results.loc[[(len(iso)== 3) for iso in all_numeric_adjustes_results["ISO_639"] ] ]

# Save into a csv
all_numeric_adjustes_results.to_csv('./data/dls/all_numeric_adjusted_results.csv')