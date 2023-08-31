import pandas as pd
import numpy as np

# This script complements dls_polytomous with data for languages with no data 


# Grid expand
lang_and_dates_expand_grid = np.array([(x, y) for x in TOLs['ISO_639'] for y in dls_polytomous.date.unique()])

df_lang_and_dates_expand_grid = pd.DataFrame.from_records(x)

# Rename dataframe
df_lang_and_dates_expand_grid.rename(columns={0: "ISO_639", 1: "date"},inplace = True)

# Merge all languages
dls_polytomous = pd.merge(dls_polytomous,df_lang_and_dates_expand_grid,on = ['ISO_639','date'],how='right')

# Replace NaN
dls_polytomous.fillna(0,inplace = True)

# Set float as int 
dls_polytomous = dls_polytomous.astype({"encoding" : "int32",
                                        "content" : "int32",
                                        "localized" : "int32",
                                        "surface" : "int32",
                                        "meaning" : "int32",
                                        "speech" : "int32",
                                        "assistant" : "int32"})

dls_polytomous.to_csv("./data/dls/dls_polytomous.csv", encoding = "ISO8859-1",index = False)