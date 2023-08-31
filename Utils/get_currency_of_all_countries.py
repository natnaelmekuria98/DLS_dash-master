# Get currency for all countries 
from babel.numbers import get_territory_currencies,get_currency_name


countries_df = LICs[['Country_Code','Country_Name']].drop_duplicates()

countries_df['Currency_Code'] = countries_df['Country_Code'].apply(lambda x : get_territory_currencies(x)[0] )

countries_df['Currency_Name'] = countries_df['Currency_Code'].apply(lambda x : get_currency_name(x, count=None, locale='en_US_POSIX') )



countries_df.to_csv("./data/currencies_by_country.csv")