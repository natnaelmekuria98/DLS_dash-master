

## Plot facet Digital x Institutional Count ###################


# Data setup -----------------------------------------------------------------------------------------------------------------------------------------------------------

# Set year 

year = 2021


## Make groupping  for 3x3 matrix 
if ( year == 2022):
    # 2022 data
    no_x10_DLS = DLS_GLP_EGID_data[DLS_GLP_EGID_data["EGIDS"] != 'x10'].copy()
else:
    # 2021 data
    old_DLS = pd.read_csv('./data/dls/Old_results/received_run/numeric_adjusted_results.csv', encoding = 'ISO8859-1')

    old_DLS_GLP_EGID_data = old_DLS[["ISO_639","cluster","adjusted_total"]].merge(TOLs, on = "ISO_639")

    no_x10_DLS = old_DLS_GLP_EGID_data[old_DLS_GLP_EGID_data["EGIDS"] != 'x10'].copy()

    # Only for 2021 data
    no_x10_DLS = no_x10_DLS.rename(columns={"L1_Users": "L1"})

no_x10_DLS = DLS_GLP_EGID_data[DLS_GLP_EGID_data["EGIDS"] != 'x10'].copy()


mapping = { 'Still' : 'Non-Digital','Emerging':'Digital','Ascending':'Digital','Vital':'Digital' ,  'Thriving' :'Digital' }

##DLS_GLP_EGID_data['cluster_mapping'] = DLS_GLP_EGID_data.cluster.map(mapping)
no_x10_DLS['digital'] = no_x10_DLS.DLS_Level.map(mapping)

#old_DLS_GLP_EGID_data['cluster_mapping'] = old_DLS_GLP_EGID_data.cluster.map(mapping)

mapping = { 'x10':'Non-Institutional','9':'Non-Institutional','8b':'Non-Institutional','8a':'Non-Institutional','7':'Non-Institutional' ,
           '6b':'Non-Institutional','6a':'Non-Institutional','5':'Non-Institutional',  
           '4':'Institutional','3':'Institutional','2':'Institutional','1':'Institutional','0':'Institutional' }

no_x10_DLS['Institutional'] = no_x10_DLS.EGIDS.map(mapping)


df_long_temp = no_x10_DLS[['ISO_639','digital','Institutional']].drop_duplicates().groupby(['digital','Institutional']).count()['ISO_639']

df_long_temp = df_long_temp.unstack()

df_long_temp.fillna(0,inplace= True)

no_x10_DLS.groupby(['Institutional','digital','Area']).count()["ISO_639"]

# Plot setup -----------------------------------------------------------------------------------------------------------------------------------------------------------

fig_test = px.density_heatmap(no_x10_DLS,x = 'Institutional',y = "digital",category_orders = {"Institutional":['Non-Institutional', 'Institutional'],
                                                                                             "digital":['Non-Digital','Digital'][::-1]} ,
                               #marginal_x="histogram", marginal_y="histogram",
                               facet_col='Area', facet_col_wrap=2, color_continuous_scale='portland', 
                               title = "Digital X Institutional - Count ("+str(year)+")"#, text_auto=True
                               )

fig_test.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
fig_test.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))

#fig_test.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}},
#                             'colorscale': [[0.0, '#bababa'],
#                                            [0.0000000000000001, '#6a4a94'],
#                                            [0.1111111111111111,'#46039f'],
#                                            [0.2222222222222222,'#7201a8'],
#                                            [0.3333333333333333,'#9c179e'],
#                                            [0.4444444444444444,'#bd3786'], 
#                                            [0.5555555555555556,'#d8576b'],
#                                            [0.6666666666666666,'#ed7953'],
#                                            [0.7777777777777778,'#fb9f3a'],
#                                            [0.8888888888888888,'#fdca26'],
#                                            [1.0, '#d8e028']]}})

fig_test.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}}}})


# Annotations hack -----------------------------------------------------------------------------------------------------------------------------------------------------
#Are you able to improve the 2x2 by adding two things
#(1) adding Speaker totals into each quadrant;
# Speakers by quadrant 

iso_count_by_quadrant = no_x10_DLS.groupby(['Institutional','digital','Area']).count()[['ISO_639']].reset_index()

# Testing expand grid to deal with zero count values

col_expandgrid = expandgrid(no_x10_DLS.Institutional.unique(), no_x10_DLS.digital.unique(),no_x10_DLS.Area.unique() )

col_prior = pd.DataFrame.from_dict(col_expandgrid)
col_prior.rename(columns = {"Var1":"Institutional","Var2":"digital","Var3":"Area" },inplace = True)
# 2022
speakers_by_quadrant = no_x10_DLS.groupby(['Institutional','digital','Area']).sum()[['L1']].reset_index()

speakers_by_quadrant = col_prior.merge(speakers_by_quadrant,on = ['Institutional','digital','Area'],how= "left").fillna(0)

# 2021
#speakers_by_quadrant = no_x10_DLS.groupby(['Institutional','digital','Area']).sum()[['L1_Users']].reset_index()

#(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
#that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

# 2022
speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()
# 2021
#speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1_Users'] / speakers_by_quadrant['L1_Users'].sum()

# Merge groupping sum with counting sum 
speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant,how="left")
speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()

#fig_test.update_traces(texttemplate='%{z} <br> 12')

areas = ["Asia","Africa","Pacific","Europe","Americas"]

facet_coords = [["x","y5"],["x","y3"],["x","y"],["x2","y5"],["x2","y3"],]

# x = [0,1] => ["Non-Institutional", "Institutional"] 
Institutional = ["Non-Institutional", "Institutional"] 

# y = [0,1] => ["Non-Digital","Digital"]
digital = ["Non-Digital","Digital"]



plot_annot_coord = [[0,0],[0,1],[1,0],[1,1]]

for i in range(5):

    for j in range(4):
        
        if ( facet_coords[i][0] == 'x2'):
            fig_test.add_annotation({
                                     'font': {},
                                     'showarrow': False,
                                     #'bgcolor': 'white',
                                     'text': "" ,
                                     'x': plot_annot_coord[j][0] - .5*( plot_annot_coord[j][0] == 0 ) + .5*( plot_annot_coord[j][0] == 1  ) ,
                                     'xanchor': 'center',
                                     'xref': facet_coords[i][0], 
                                     'y': plot_annot_coord[j][1],
                                     'yanchor': 'bottom',
                                     'yref': facet_coords[i][1]
                                     })

        dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
                                    (speakers_by_quadrant['digital'] == digital[ plot_annot_coord[j][1]]) & # Filter by Digital value
                                    (speakers_by_quadrant['Area'] == areas[i] )] # Filter by Continent

        text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'

        fig_test.add_annotation({
                                 'font': {},
                                 'showarrow': False,
                                 #'bgcolor': 'white',
                                 'font': {'size': 10, 'color': 'white'},
                                 #'text': str(i) + "x: " + str(plot_annot_coord[j][0]) + " y: " + str(plot_annot_coord[j][1]) ,
                                 'text': text,  #  506 languages (7.09% of total languages)
                                 'x': plot_annot_coord[j][0] ,
                                 'xanchor': 'center',
                                 'xref': facet_coords[i][0], 
                                 'y': plot_annot_coord[j][1]-.30,
                                 'yanchor': 'bottom',
                                 'yref': facet_coords[i][1]
                                 })
        

############



fig_test.show()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Annotations added for all grouped 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
fig_test = px.density_heatmap(no_x10_DLS,x = 'Institutional',y = "digital",category_orders = {"Institutional":['Non-Institutional', 'Institutional'],
                                                                                             "digital":['Non-Digital','Digital'][::-1]} ,
                               #marginal_x="histogram", marginal_y="histogram",
                               #facet_col='Area', facet_col_wrap=2, 
                               color_continuous_scale='portland',
                               title = "Digital X Institutional - Count ("+str(year)+")"#, text_auto=True
                               )


fig_test.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
fig_test.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))


fig_test.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}}}})


# Annotations hack -----------------------------------------------------------------------------------------------------------------------------------------------------
#Are you able to improve the 2x2 by adding two things
#(1) adding Speaker totals into each quadrant;
# Speakers by quadrant 

iso_count_by_quadrant = no_x10_DLS.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

speakers_by_quadrant = no_x10_DLS.groupby(['Institutional','digital']).sum()[['L1']].reset_index()

#(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
#that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()

# Merge groupping sum with counting sum 
speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant)
speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()

#fig_test.update_traces(texttemplate='%{z} <br> 12')

areas = ["Africa","Europe","Americas","Pacific","Asia"]

facet_coords = [["x","y5"],["x","y3"],["x","y"],["x2","y5"],["x2","y3"],]

# x = [0,1] => ["Non-Institutional", "Institutional"] 
Institutional = ["Non-Institutional", "Institutional"] 

# y = [0,1] => ["Non-Digital","Digital"]
digital = ["Non-Digital","Digital"]



plot_annot_coord = [[0,0],[0,1],[1,0],[1,1]]


for j in range(4):
        
    dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
                                (speakers_by_quadrant['digital'] == digital[ plot_annot_coord[j][1]])  # Filter by Digital value
                                ] # Filter by Continent

    text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'

    fig_test.add_annotation({
                                'font': {},
                                'showarrow': False,
                                #'bgcolor': 'white',
                                'font': {'size': 10, 'color': 'white'},
                                #'text': str(i) + "x: " + str(plot_annot_coord[j][0]) + " y: " + str(plot_annot_coord[j][1]) ,
                                'text': text,  #  506 languages (7.09% of total languages)
                                'x': plot_annot_coord[j][0] ,
                                'xanchor': 'center',
                                'xref': 'x', 
                                'y': plot_annot_coord[j][1]-.20,
                                'yanchor': 'bottom',
                                'yref': 'y'
                                })
        

############



fig_test.show()



# One continent --------------------------------------------------------------------------------------------------------------------------------------------------------

fig_test_2 = px.density_heatmap(no_x10_DLS[no_x10_DLS["Area"]== 'Africa'],x = 'Institutional',y = "digital",category_orders = {"Institutional":['Non-Institutional', 'Institutional'],
                                                                                             "digital":['Non-Digital','Digital'][::-1]} ,
                               #marginal_x="histogram", marginal_y="histogram",
                               #facet_col='Area', facet_col_wrap=2, 
                               color_continuous_scale='portland',
                               title = "Digital X Institutional, Africa - Count ("+str(year)+")"#, text_auto=True
                               )


fig_test_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
fig_test_2.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))


fig_test_2.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}}}})


# Annotations hack -----------------------------------------------------------------------------------------------------------------------------------------------------
#Are you able to improve the 2x2 by adding two things
#(1) adding Speaker totals into each quadrant;
# Speakers by quadrant 

iso_count_by_quadrant = no_x10_DLS[no_x10_DLS["Area"]== 'Africa'].groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

speakers_by_quadrant = no_x10_DLS[no_x10_DLS["Area"]== 'Africa'].groupby(['Institutional','digital']).sum()[['L1']].reset_index()

#(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
#that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()

# Merge groupping sum with counting sum 
speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant)
speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()

#fig_test_2.update_traces(texttemplate='%{z} <br> 12')

areas = ["Africa","Europe","Americas","Pacific","Asia"]

facet_coords = [["x","y5"],["x","y3"],["x","y"],["x2","y5"],["x2","y3"],]

# x = [0,1] => ["Non-Institutional", "Institutional"] 
Institutional = ["Non-Institutional", "Institutional"] 

# y = [0,1] => ["Non-Digital","Digital"]
digital = ["Non-Digital","Digital"]



plot_annot_coord = [[0,0],[0,1],[1,0],[1,1]]


for j in range(4):
        
    dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
                                (speakers_by_quadrant['digital'] == digital[ plot_annot_coord[j][1]])  # Filter by Digital value
                                ] # Filter by Continent

    text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'

    fig_test_2.add_annotation({
                                'font': {},
                                'showarrow': False,
                                #'bgcolor': 'white',
                                'font': {'size': 10, 'color': 'white'},
                                #'text': str(i) + "x: " + str(plot_annot_coord[j][0]) + " y: " + str(plot_annot_coord[j][1]) ,
                                'text': text,  #  506 languages (7.09% of total languages)
                                'x': plot_annot_coord[j][0] ,
                                'xanchor': 'center',
                                'xref': 'x', 
                                'y': plot_annot_coord[j][1]-.2,
                                'yanchor': 'bottom',
                                'yref': 'y'
                                })
        

############



fig_test_2.show()




# Plot setup -----------------------------------------------------------------------------------------------------------------------------------------------------------

# OK, great. These are good.  I also need an analysis of the "Digital" languages, split into the 5 classification groups.
# I need this in total (for all digital languages) and then for the 2 quadrants (Digital/Non-Institutional, Digital/Institutional).
# Thanks.


####

# a) Splitting the adjusted score in to 5 groups -----------------------------------------------------------------------------------------------------------------------
import jenkspy

breaks = jenkspy.jenks_breaks(no_x10_DLS['adjusted_total'].to_list(), nb_class=5)

no_x10_DLS['adjusted_total_classes'] = pd.cut(no_x10_DLS['adjusted_total'],
                                   bins =  [0.0, 1.1252726022437, 4.27759844857043, 9.40865800865801, 17.5833333333333, 27.5],
                                   labels = [ '< 1.12', '1.12 - 4.28','4.28 - 9.41', '9.41 - 17.58', '17.58 - 27.5'] )

fig = px.scatter(no_x10_DLS[no_x10_DLS['digital'] != 'Non-Digital'], y = 'adjusted_total', x = 'EGIDS',
                 color ='adjusted_total_classes',category_orders = {"EGIDS":pd.CategoricalIndex(no_x10_DLS["EGIDS"]).categories})


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------


mapping = { 'still' : 'Non-Digital','emerging':'Digital','ascending':'Digital','vital':'Digital' ,  'thriving' :'Digital' }


fig_test = px.density_heatmap(no_x10_DLS[no_x10_DLS['digital'] != 'Non-Digital'],x = 'Institutional',
                                y = "adjusted_total_classes",category_orders = {"cluster":['still','emerging','ascending','vital', 'thriving'],
                                                                                             "adjusted_total_classes":[ '< 1.12', '1.12 - 4.28','4.28 - 9.41', '9.41 - 17.58', '17.58 - 27.5'][::-1]} ,
                               #marginal_x="histogram", marginal_y="histogram",
                               #facet_col='Area', facet_col_wrap=2, 
                               color_continuous_scale='portland', 
                               title = "Only Digital Languages Institutional - Count ("+str(year)+")"#, text_auto=True
                               )

fig_test.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
fig_test.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))

#fig_test.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}},
#                             'colorscale': [[0.0, '#bababa'],
#                                            [0.0000000000000001, '#6a4a94'],
#                                            [0.1111111111111111,'#46039f'],
#                                            [0.2222222222222222,'#7201a8'],
#                                            [0.3333333333333333,'#9c179e'],
#                                            [0.4444444444444444,'#bd3786'], 
#                                            [0.5555555555555556,'#d8576b'],
#                                            [0.6666666666666666,'#ed7953'],
#                                            [0.7777777777777778,'#fb9f3a'],
#                                            [0.8888888888888888,'#fdca26'],
#                                            [1.0, '#d8e028']]}})

fig_test.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}}}})


# Annotations hack -----------------------------------------------------------------------------------------------------------------------------------------------------
#Are you able to improve the 2x2 by adding two things
#(1) adding Speaker totals into each quadrant;
# Speakers by quadrant 

iso_count_by_quadrant = no_x10_DLS.groupby(['cluster']).count()[['ISO_639']].reset_index()

# 2022
speakers_by_quadrant = no_x10_DLS.groupby(['cluster']).sum()[['L1']].reset_index()
# 2021
#speakers_by_quadrant = no_x10_DLS.groupby(['Institutional','digital','Area']).sum()[['L1_Users']].reset_index()

#(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
#that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

# 2022
speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum() *100
# 2021
#speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1_Users'] / speakers_by_quadrant['L1_Users'].sum()

# Merge groupping sum with counting sum 
speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant)
speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum() *100

#fig_test.update_traces(texttemplate='%{z} <br> 12')

areas = ["Africa","Europe","Americas","Pacific","Asia"]

facet_coords = [["x","y5"],["x","y3"],["x","y"],["x2","y5"],["x2","y3"],]

# x = [0,1] => ["Non-Institutional", "Institutional"] 
Institutional = ["Non-Institutional", "Institutional"] 

# y = [0,1] => ["Non-Digital","Digital"]
digital = [ '< 1.12', '1.12 - 4.28','4.28 - 9.41', '9.41 - 17.58', '17.58 - 27.5']



plot_annot_coord = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4]]


for j in range(10):
        

    dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
                                    (speakers_by_quadrant['adjusted_total_classes'] == digital[ plot_annot_coord[j][1]])  # Filter by Digital value
                                    ] # Filter by Continent
    #dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
    #                            (speakers_by_quadrant['digital'] == digital[ plot_annot_coord[j][1]])  # Filter by Digital value
    #                            ] # Filter by Continent

    text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'

    fig_test.add_annotation({
                                'font': {},
                                'showarrow': False,
                                #'bgcolor': 'white',
                                'font': {'size': 10, 'color': 'white'},
                                #'text': str(i) + "x: " + str(plot_annot_coord[j][0]) + " y: " + str(plot_annot_coord[j][1]) ,
                                'text': text,  #  506 languages (7.09% of total languages)
                                'x': plot_annot_coord[j][0] ,
                                'xanchor': 'center',
                                'xref': 'x', 
                                'y': plot_annot_coord[j][1]-.2,
                                'yanchor': 'bottom',
                                'yref': 'y'
                                })


############



fig_test.show()