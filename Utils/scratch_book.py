#### Scratch book ####






# Scatter plot for investigating High GLP per capita but low egids

temp = DLS_GLP_EGID_data[DLS_GLP_EGID_data["GLP"]>0]

temp['GLP_per'] = temp['w_GDP_lang_GHS_kummu'] / temp['L1']

temp['GLP_per'].fillna(0,inplace=True)

temp.sort_values(by=["EGIDS"], ascending=False, inplace=True)

fig_GLP_per_cap = px.box(temp[temp['GLP_per']>0], y="GLP_per", color="EGIDS",#symbol = 'Region_Name',
                            hover_name = 'Language_Name', points="all" )


fig_GLP_per_cap.show()


# Scatter plot for most spoken languages on each country

GLPs.loc[GLPs.groupby('Country_Code', sort=False)['All_Users'].idxmax()]


idx = GLPs.groupby('Country_Code')['All_Users'].transform(max) == GLPs['All_Users']


temp2 = GLPs[idx]

temp2 = temp2[temp2["GLP_vanila"]>0]

temp2['GLP_per'] = temp2['GLP_vanila'] / temp2['L1_Users']

temp2['GLP_per'].fillna(0,inplace=True)


temp2 = temp2.merge(LICs[["ISO_639","Language_Name","Country_Code","Country_Name","EGIDS"]],on = [ 'ISO_639','Country_Code'] )



temp2.sort_values(by=["EGIDS"], ascending=False, inplace=True)




fig_GLP_per_cap = px.box(temp2[temp2['GLP_per']>0], y="GLP_per", color="EGIDS",#symbol = 'Region_Name',
                            hover_name = 'Country_Name_y', points="all" )


fig_GLP_per_cap.show()

test = LICs.loc[LICs.groupby('Country_Code', sort=False)['All_Users'].idxmax()]


test['Country_Code']


households_consumption = wbdata.get_dataframe({"NE.CON.PRVT.CD":"household_consu"})

test2 = get_imf_dat("FIGB_PA")

len(test2['IMF_country_cod'].unique())


# IMF FD index

imf_fd = pd.read_excel('./data/IMF/FD Index Database (Excel).xlsx')


imf_fd = imf_fd.loc[imf_fd.groupby('code', sort=False)['year'].idxmax()]

LICs_first_lang = LICs.loc[LICs.groupby('Country_Code', sort=False)['All_Users'].idxmax()]


LICs_first_lang = LICs_first_lang.merge(imf_fd, left_on = "iso_3",right_on = "code")

LICs_first_lang["EGIDS"] = pd.Categorical(LICs_first_lang["EGIDS"],['x10','9','8b','8a','7','6b','6a','5','4','3','2','1','0'], ordered = True)

fig = px.box(LICs_first_lang, x = 'Area', y="FM", color="EGIDS",#symbol = 'Region_Name',
                            hover_name = 'Country_Name', points="all" ,category_orders = {"EGIDS":pd.CategoricalIndex(DLS_GLP_EGID_data["EGIDS"]).categories[::-1]})


#fig.update_traces(
#    hovertemplate="<br>".join([
#        "colx: %{x}",
#        "coly: %{y}",
#        "col1: %{hover_name}"
#    ])
#)

fig.show()

################################### Economic data ###########################################
# ### Economic data                                                                         #
#                                                                                           #
# # GLP and Consumption                                                                     #
# GLP, GLP ALL, GLP w v1, GLP w v2, HHCP                                                    #
#                                                                                           #
# # Investment                                                                              #
# Interest Rates                                                                            #
#                                                                                           #
# # Trade                                                                                   #
# Currency                                                                                  #
#                                                                                           #
#                                                                                           #
#                                                                                           #
#############################################################################################


LICs_and_currencies = LICs_selected_language


## net work ##############

import pyvis
from pyvis.network import Network
import math 


net = Network(height='100%', width='100%')

# [ Country_Code , Language_Name , Country_Name , Region_Name , Area, L1_Users , L1_percentage_of_country_L1, Currency_Code, Currency_Name ]
for row in LICs_and_currencies.drop_duplicates().to_dict('records'):

    # normalize L1_Users
    l1_normalized = (row['L1_Users'] - l1_min) / l1_range

    # Add nodes 
    net.add_node(row['Country_Target'],value = 10*l1_normalized,
                 group = row['group'],title = 'Country : ' + row['Country_Target'] + '<br>Most Used Language(L1) : '+ row["Language_Name"] + '<br>L1_Users : ' + str(row["L1_Users"]) + '<br>Family-branch : ' + row['family_branch']     )
    

for row in LICs_and_currencies.to_dict('records'):

    #if( row['weight'] != 1):

    #net.add_edge(row['Country_Target'],row["Country_Source"],value = (1-row['weight']),length = 300+150*row['weight']**2,color = {'opacity' :  (1-row['weight'])} )
    net.add_edge(row['Country_Target'],row["Country_Source"],value = ((math.cos(3*row['weight'])+1.5)/4),length = 300+150*row['weight']**2,
                    color = {'opacity' :  ((math.cos(3*row['weight'])+1.05)/3)}# ,
                    #title = 'Language Proximity between :<br>' + row['Country_Source'] + ' and<br>' + row['Country_Target']+ '<br>Is : ' + str(1-row['weight']) 
                    )


net.set_edge_smooth('curvedCW')


#net.toggle_physics(False)
net.show('example.html')





## Lines in map ########

fig = go.Figure(data=go.Scattergeo(
    locations = ['BRA','ARG','USA'],
    #lat = [40.7127, 51.5072],
    #lon = [-74.0059, 0.1275],
    mode = 'lines',
    line = dict(width = 2, color = 'blue'),
))

fig.update_layout(
    title_text = 'London to NYC Great Circle',
    showlegend = False,
    geo = dict(
        resolution = 50,
        showland = True,
        showlakes = True,
        landcolor = 'rgb(204, 204, 204)',
        countrycolor = 'rgb(204, 204, 204)',
        lakecolor = 'rgb(255, 255, 255)',
        projection_type = "equirectangular",
        coastlinewidth = 2,
        #lataxis = dict(
        #    range = [20, 60],
        #    showgrid = True,
        #    dtick = 10
        #),
        #lonaxis = dict(
        #    range = [-100, 20],
        #    showgrid = True,
        #    dtick = 20
        #),
    )
)

fig.show()