#------- DO NOT RUN --------- #
import pandas as pd
import requests

# Function -------------------------------------------------------------------------------------------------------------------------------------------------------------

imf_code = 'FILR_ON_PA'

def get_imf_dat(imf_code, freq ="A",database='IFS'):

    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
    key = f'CompactData/{database}/{freq}..{imf_code}' # adjust codes here

    # Navigate to series in API-returned JSON data
    data = (requests.get(f'{url}{key}').json()
            ['CompactData']['DataSet']['Series'])

    # Create pandas dataframe from the observations
    # attempt a)
    #data_list = [[data_n.get('@REF_AREA'), obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')]
    #             for data_n in data for obs in data_n['Obs']  ]
    # attempt b)
    data_list = []

    for country_data in data:

        try:
             for obs in country_data['Obs']:
        
                 try:
                     data_list_temp = [country_data.get('@REF_AREA'), obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')]
        
                     data_list.append(data_list_temp)
                 except:
                     next
        except:
            next
            
    

    df = pd.DataFrame(data_list, columns=['IMF_country_cod','date', imf_code])
     
    #df = df.set_index(pd.to_datetime(df['date']))['value'].astype('float')

    return(df)

## key = 'DataStructure/IFS' - Labor data 
#Labor Force, Persons, Number of: LLF_PE_NUM
#Labor Force, Persons, Percentage change, corresponding period previous year, Percent: LLF_PE_PC_CP_A_PT
#Labor Force, Persons, Percentage change, previous period, Percent: LLF_PE_PC_PP_PT
#Labor Markets, Employment, Index: LE_IX
#Labor Markets, Unemployment Rate, Percent: LUR_PT
#Labor Markets, Unemployment Rate, Percentage change, Corresponding period previous year, Percent: LUR_PC_CP_A_PT
#Labor Markets, Unemployment Rate, Percentage change, Previous period, Percent: LUR_PC_PP_PT
#Labor Markets, Wage Rates, Index: LWR_IX
#Labor Markets, Wage Rates, Percentage change, Corresponding period previous year, Percent: LWR_PC_CP_A_PT
#Labor Markets, Wage Rates, Percentage change, Previous period, Percent: LWR_PC_PP_PT

## Interest rate data
#Financial, Interest Rates Government Bond Yield, Per Cent Per Annum: FIGBY_PA
#Financial, Interest Rates, 3-Month Interbank Interest, Percent per annum: FII_3M_PA
#Financial, Interest Rates, Average Cost of Funds, Percent per Annum: FIACF_PA
#Financial, Interest Rates, Central Bank Borrowing Facility Rate: FIBFR_PA
#Financial, Interest Rates, Central Bank Certificates: FICB_PA
#Financial, Interest Rates, Certificates of Deposit, Percent per annum: FICD_PA
#Financial, Interest Rates, Corporate Paper Rate: FICPR_PA
#Financial, Interest Rates, Deposit Rate, Foreign Currency, Euro, Percent per Annum: FIDR_FX_EUR_PA
#Financial, Interest Rates, Deposit Rate, Foreign Currency, US Dollar, Percent per Annum: FIDR_FX_USD_PA
#Financial, Interest Rates, Deposit, Foreign Currency, Percent per Annum: FIDR_FX_PA                                         <---
#Financial, Interest Rates, Deposit, Overnight: FIDR_ON_PA                                                                   
#Financial, Interest Rates, Deposit, Percent per annum: FIDR_PA                                                              <---
#Financial, Interest Rates, Discount, Foreign Currency: FID_FX_PA                                                            <---           
#Financial, Interest Rates, Discount, Percent per annum: FID_PA                                                              <---
#Financial, Interest Rates, Eurosystem Deposit Facility Rate: FIDFR_PA
#Financial, Interest Rates, Government Bond Yields, Medium Term, Percent per annum: FIGBY_MT_PA
#Financial, Interest Rates, Government Bond Yields, Short- to Medium-Term, Percent per Annum: FIGBY_SM_PA
#Financial, Interest Rates, Government Securities, Government Bonds, Medium- to Long-term, Percent per annum: FIGB_MLT_PA
#Financial, Interest Rates, Government Securities, Government Bonds, Percent per annum: FIGB_PA                              <---
#Financial, Interest Rates, Government Securities, Government Bonds, Short-term, Percent per annum: FIGB_S_PA
#Financial, Interest Rates, Government Securities, Treasury Bills, 3-month, Percent per annum: FITB_3M_PA
#Financial, Interest Rates, Government Securities, Treasury Bills, Bond Equivalent, Percent per Annum: FITBBE_PA
#Financial, Interest Rates, Government Securities, Treasury Bills, Foreign Currency, Percent per Annum: FITB_FX_PA
#Financial, Interest Rates, Government Securities, Treasury Bills, Index: FITB_IX
#Financial, Interest Rates, Government Securities, Treasury Bills, Long-Term, Percent per Annum: FITB_L_PA
#Financial, Interest Rates, Government Securities, Treasury Bills, Percent per annum: FITB_PA                                <---
#Financial, Interest Rates, Key Repurchase Agreement Rate, Percent per annum: FIRAK_PA
#Financial, Interest Rates, Lending Rate, Foreign Currency, Euro, Percent per Annum: FILR_FX_EUR_PA
#Financial, Interest Rates, Lending Rate, Foreign Currency, Percent per Annum: FILR_FX_PA                        <---
#Financial, Interest Rates, Lending Rate, Foreign Currency, US Dollar, Percent per Annum: FILR_FX_USD_PA
#Financial, Interest Rates, Lending Rate, Overnight: FILR_ON_PA                                                     
#Financial, Interest Rates, Lending Rate, Percent per annum: FILR_PA                                             <---
#Financial, Interest Rates, London Eurodollar Deposit Rate, Three-Month, Percent per annum: FILED_3M_PA
#Financial, Interest Rates, London Interbank Offer Rate, One-Month, Percent per annum: FILIBOR_1M_PA
#Financial, Interest Rates, London Interbank Offer Rate, One-Year, Percent per annum: FILIBOR_1Y_PA
#Financial, Interest Rates, London Interbank Offer Rate, Overnight, Percent per Annum: FILIBOR_ON_PA
#Financial, Interest Rates, London Interbank Offer Rate, Six-Month, Percent per annum: FILIBOR_6M_PA
#Financial, Interest Rates, Monetary Policy-Related Interest Rate, Percent per annum: FPOLM_PA                   <---
#Financial, Interest Rates, Money Market, Foreign Currency: FIMM_FX_PA                                           <---
#Financial, Interest Rates, Money Market, Maximum, Percent per annum: FIMM_MAX_PA
#Financial, Interest Rates, Money Market, Minimum, Percent per annum: FIMM_MIN_PA
#Financial, Interest Rates, Money Market, Percent per annum: FIMM_PA                                             <---
#Financial, Interest Rates, Rate of Remuneration, Percent per Annum: FIRR_PA
#Financial, Interest Rates, Refinancing Rate, Percent per annum: FIR_PA                                          <---
#Financial, Interest Rates, Repurchase Agreement Rate, Percent per annum: FIRA_PA                                <---
#Financial, Interest Rates, Reverse Repurchase Agreement Rate: FIRAR_PA
#Financial, Interest Rates, Savings Rate, Foreign Currency, Percent per Annum: FISR_FX_PA                        <---
#Financial, Interest Rates, Savings Rate, Percent per annum: FISR_PA                                             <---
#Financial, Interest Rates, SDR Interest Rate, Percent per annum: FISDR_PA

## Economic activity
#Economic Activity, Industrial Production, Construction, Index: AIPCO_IX
#Economic Activity, Industrial Production, Construction, Percentage change, Corresponding period previous year, Percent: AIPCO_PC_CP_A_PT
#Economic Activity, Industrial Production, Construction, Percentage change, Previous period, Percent: AIPCO_PC_PP_PT
#Economic Activity, Industrial Production, Energy, Electricity Production, Index: AIPEE_IX
#Economic Activity, Industrial Production, Energy, Electricity Production, Percentage change, Corresponding period previous year, Percent: AIPEE_PC_CP_A_PT
#Economic Activity, Industrial Production, Energy, Electricity Production, Percentage change, Previous period, Percent: AIPEE_PC_PP_PT
#Economic Activity, Industrial Production, Index: AIP_IX
#Economic Activity, Industrial Production, Manufacturing, Index: AIPMA_IX
#Economic Activity, Industrial Production, Manufacturing, Percentage change, Corresponding period previous year, Percent: AIPMA_PC_CP_A_PT
#Economic Activity, Industrial Production, Manufacturing, Percentage change, Previous period, Percent: AIPMA_PC_PP_PT
#Economic Activity, Industrial Production, Mining, Index: AIPMI_IX
#Economic Activity, Industrial Production, Mining, Percentage change, Corresponding period previous year, Percent: AIPMI_PC_CP_A_PT
#Economic Activity, Industrial Production, Mining, Percentage change, Previous period, Percent: AIPMI_PC_PP_PT
#Economic Activity, Industrial Production, Percentage change, Corresponding period previous year, Percent: AIP_PC_CP_A_PT
#Economic Activity, Industrial Production, Percentage change, Previous period, Percent: AIP_PC_PP_PT
#Economic Activity, Oil Production, Crude, Index: AOMPC_IX
#Economic Activity, Oil Production, Crude, Percentage change, Corresponding period previous year, Percent: AOMPC_PC_CP_A_PT
#Economic Activity, Oil Production, Crude, Percentage change, Previous period, Percent: AOMPC_PC_PP_PT
#Economic Activity, Other Indicators, Tourism, Number of Visitors, Persons, Index: AOTV_PE_IX



# finding data  --------------------------------------------------------------------------------------------------------------------------------------------------------

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
key = 'Dataflow'  # Method with series information
search_term = 'CPI'  # Term to find in series names
series_list = requests.get(f'{url}{key}').json()['Structure']['Dataflows']['Dataflow']
# Use dict keys to navigate through results:
for series in series_list:
    if search_term in series['Name']['#text']:
        print(f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}")

# Finding the dimensions of the series ---------------------------------------------------------------------------------------------------------------------------------

key = 'DataStructure/CPI'  # Method / series
dimension_list = requests.get(f'{url}{key}').json()['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']
for n, dimension in enumerate(dimension_list):
    print(f"Dimension {n+1}: {dimension['@codelist']}")

# Finding the codes for each dimension

# Example: codes for third dimension, which is 2 in python
key = f"CodeList/{dimension_list[2]['@codelist']}"
code_list = requests.get(f'{url}{key}').json()['Structure']['CodeLists']['CodeList']['Code']
for code in code_list:
    print(f"{code['Description']['#text']}: {code['@value']}")


# Getting imf data  ----------------------------------------------------------------------------------------------------------------------------------------------------

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
key = 'CompactData/IFS/A..FPOLM_PA' # adjust codes here

e# Navigate to series in API-returned JSON data
data = (requests.get(f'{url}{key}').json()
        ['CompactData']['DataSet']['Series'])

print(data['Obs'][-1]) # Print latest observation


baseyr = data['@BASE_YEAR']  # Save the base year

# Create pandas dataframe from the observations
data_list = [[obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')]
             for obs in data['Obs']]

# Create pandas dataframe from the observations
data_list = [[data_n.get('@REF_AREA'), obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')]
             for data_n in data for obs in data_n['Obs']  ]


df = pd.DataFrame(data_list, columns=['IMF_country_cod','date', 'value'])
     
df = df.set_index(pd.to_datetime(df['date']))['value'].astype('float')

# Save cleaned dataframe as a csv file
#df.to_csv('UK_import_price_index.csv', header=True)

# 0) Setup -------------------------------------------------------------------------------------------------------------------------------------------------------------

# Interest rate dict

interest_rate_imf_codes = { 'FIDR_FX_PA':'Deposit, Foreign Currency' ,
                            'FIDR_PA':'Deposit',
                            'FID_FX_PA':'Discount, Foreign Currency',
                            'FID_PA':'Discount' ,
                            'FIGB_PA':'Government Securities, Government Bonds',
                            'FITB_PA':'Government Securities, Treasury Bills' ,
                            'FILR_FX_PA':'Lending Rate, Foreign Currency' ,
                            'FILR_PA':'Lending Rate' ,
                            'FPOLM_PA':'Monetary Policy-Related Interest Rate',
                            'FIMM_FX_PA':'Money Market, Foreign Currency',
                            'FIMM_PA':'Money Market' ,
                            'FIR_PA':'Refinancing Rate'  ,
                            'FIRA_PA':'Repurchase Agreement Rate',
                            'FISR_FX_PA':'Savings Rate, Foreign Currency',
                            'FISR_PA':'Savings Rate' }
 

# Transform keys and childs into list 
list_interest_rate_imf_codes = {'code': list(interest_rate_imf_codes.keys()),'label' : list(interest_rate_imf_codes.values())}

# Transform list into dataframe
df_interest_rate_imf_codes = pd.DataFrame( list_interest_rate_imf_codes)

# 1) Getting the data --------------------------------------------------------------------------------------------------------------------------------------------------

i=0
for code in df_interest_rate_imf_codes['code']:

    print(code)

    if i == 0:
        df = get_imf_dat(code)
    else:
    
        # get the data
        df_temp = get_imf_dat(code)

        # merge the data
        df = df.merge(df_temp,how = 'outer', on = ['IMF_country_cod','date'])
    
    i += 1

#df = df.set_index(pd.to_datetime(df['date']))['value'].astype('float')

# Save cleaned dataframe as a csv file
df.to_csv('./data/interest_rate.csv', header=True)
df_interest_rate_imf_codes.to_csv('./data/metadata_interest_rate.csv', header=True)


code = 'PCPI_IX'

df_temp = get_imf_dat(code,'A','CPI')


df_temp.to_csv('./data/CPI_A.csv', header=True)
