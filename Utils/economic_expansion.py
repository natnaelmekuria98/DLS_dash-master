# DO NOT RUN ! 
# HHI to select language(or lang tree cut) => select country by t-index ( or income decile ) and ICL and HHI_{country}


# 0) Setup  ( Choosing a country )
country = "United States"

country_iso2 = 'US'

language = "English"

iso = "eng"

# Selection
# Consumer percentile 

# Dicl
dicl = pd.read_csv("../../../R codes/DICL network/data/dicl.csv", encoding = 'ISO8859-1')
# \R codes\DICL network\data

# IDEA!: Where the biggest variation of imports happens ( low or high HHI countries, low or high DICL countries, low or high T-index Countries)


# IDEA: expand language filtering by LP 
# IDEA: t-index calculus where is not internet users that determine the cut in the wealth distribuition, but make it customable


# Save t-index of countries with english speakers
t_index_selection = t_index_by_language_with_countries[ (t_index_by_language_with_countries['ISO_639']== iso) & (t_index_by_language_with_countries["year"] == 2017) &
                                                        (t_index_by_language_with_countries['iso2c']!= country_iso2)].copy()



t_index_selection.loc[:,'norm_t_index'] =  (t_index_selection.loc[:,'t_index'] - min(t_index_selection.loc[:,'t_index'] )) / (max(t_index_selection.loc[:,'t_index'] ) - min(t_index_selection.loc[:,'t_index'] ))

# IDEA: add entropy ( -sum{p(x)*log(p(x)) ) and Simpson Index ( sum{p(x)^a} ^ (1/(1-a)) where a = 2 for Simpson index) https://stats.stackexchange.com/questions/460564/how-is-the-herfindahl-hirschman-index-different-from-entropy
# IDEA: Less entropic/concentrated language are better for trade?
# IDEA: HHI for country, which is better a country in high or low HHI

# Save HHI by country

t_index_selection.loc[:,'HHI_by_country'] = [ HHI_country(selected_country)['ISO_HHI'].to_list()[0] for selected_country in t_index_selection['iso2c'] ]


# Save iso3 of each country

t_index_selection.loc[:,'iso3'] = [ gets_iso3_from_iso2(selected_country) for selected_country in t_index_selection['iso2c'] ]

# DICL ----------------------------------

def icl(iso,iso2):
    dicl.loc[(dicl["ISO3"]==iso) & (dicl['ISO3_2']==selected_country) ]

    return dicl.loc[(dicl["ISO3"]==iso) & (dicl["ISO3_2"]==iso2) ][['col','cnl','lp','cl']].mean(axis=1).values[0]

t_index_selection.loc[:,'ICL'] = [ icl("USA",selected_country) for selected_country in t_index_selection['iso3'] ]


t_index_selection.loc[:,'U'] = t_index_selection[['norm_t_index','HHI_by_country','ICL']].apply(lambda x: (x[0]+x[1]+x[2])/3 , axis=1)



fig = px.scatter_3d(t_index_selection , x='norm_t_index', y='HHI_by_country', z='ICL',hover_name ='country',color_continuous_scale=px.colors.sequential.Viridis,
              color='U')

# ISO Curves

X, Y, Z = np.mgrid[0:1:30j, 0:1:30j, 0:1:30j]
values =    (X + Y + Z)/3


fig.add_trace(go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=values.flatten(),
    caps= dict(x_show=False, y_show=False, z_show=False), 
    isomin=0,
    isomax=1,
    opacity=0.1, # max opacity
    #opacityscale=[[-0.5, 1], [-0.2, 0], [0.2, 0], [0.5, 1]],
    surface_count=21,
    colorscale='viridis',
    hoverinfo='skip'
    #reversescale=True
    ))

fig.layout['coloraxis']['colorbar']['x'] = 1.15

fig.show()




## LP_{country_i,country_j}
language_proximity_all(iso,"L1_Users")

## COL_{country_i,country_j} = Common Official Language

## CNL_{country_i,country_j} = Common Native Language

# DICL_{country_i,country_j} = LP + COL + CNL

# ---------------------------------------

# One nation One language ideas !!! CHECK GME PACKAGE https://www.usitc.gov/data/gravity/gme_docs/

# Gravity = ICL + DIST(distance) + CNTG (contiguous border) + CLNY(colonial relationship)

# SMCNTRY = EIA (Economic Integration Agreements) + EU (European Union Membership) + WTO ( Gatt and Wto membership)



hhi_rank






fig = go.Figure(data=go.Volume(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=values.flatten(),
    isomin=0,
    isomax=1,
    opacity=0.1, # max opacity
    #opacityscale=[[-0.5, 1], [-0.2, 0], [0.2, 0], [0.5, 1]],
    surface_count=21,
    colorscale='RdBu',
    reversescale=True,
    hoverinfo='skip'
    ))
fig.show()


t_index_selection , x='norm_t_index', y='HHI_by_country', z='ICL',hover_name ='country',color_continuous_scale=px.colors.sequential.Viridis,
              color='U'

fig.add_trace(go.Scatter3d(x=t_index_selection['norm_t_index'], y=t_index_selection['HHI_by_country'], z=t_index_selection['ICL'],
                                   mode='markers'))




X, Y, Z = np.mgrid[:1:20j, :1:20j, :1:20j]
vol = (X  + Y  + Z)/3


fig = go.Figure(data=go.Volume(
    x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
    value=vol.flatten(),

    opacity=0.2,
    surface_count=10,
    caps= dict(x_show=False, y_show=False, z_show=False), # no caps
    ))
fig.update_layout(scene_camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=0.1, y=2.5, z=0.1)
))

fig.show()


# Function

def market_expansion_metric(country_iso3,iso_639,year= 2018):

    # 0) Setup 

    ## gets iso 2 and contry name from iso3

    country_iso2 = pycountry.countries.get(alpha_3 = country_iso3).alpha_2
    country = pycountry.countries.get(alpha_3 = country_iso3).name

    iso_639
    ####
    country = "United States"

    country_iso2 = 'US'

    language = "English"

    iso = "eng"


    ####

    # Save t-index of countries with english speakers
    t_index_selection = t_index_by_language_with_countries[ (t_index_by_language_with_countries['ISO_639']== iso_639) & (t_index_by_language_with_countries["year"] == year) &
                                                        (t_index_by_language_with_countries['iso2c']!= country_iso2)].copy()


    # normalize the t-index
    t_index_selection.loc[:,'norm_t_index'] =  (t_index_selection.loc[:,'t_index'] - min(t_index_selection.loc[:,'t_index'] )) / (max(t_index_selection.loc[:,'t_index'] ) - min(t_index_selection.loc[:,'t_index'] ))

    # IDEA: add entropy ( -sum{p(x)*log(p(x)) ) and Simpson Index ( sum{p(x)^a} ^ (1/(1-a)) where a = 2 for Simpson index) https://stats.stackexchange.com/questions/460564/how-is-the-herfindahl-hirschman-index-different-from-entropy
    # IDEA: Less entropic/concentrated language are better for trade?
    # IDEA: HHI for country, which is better a country in high or low HHI

    # Save HHI by country

    t_index_selection.loc[:,'HHI_by_country'] = [ HHI_country(selected_country)['ISO_HHI'].to_list()[0] for selected_country in t_index_selection['iso2c'] ]


    # Save iso3 of each country

    t_index_selection.loc[:,'iso3'] = [ gets_iso3_from_iso2(selected_country) for selected_country in t_index_selection['iso2c'] ]

    # DICL ----------------------------------

    def icl(iso,iso2):
        dicl.loc[(dicl["ISO3"]==iso) & (dicl['ISO3_2']==selected_country) ]

        return dicl.loc[(dicl["ISO3"]==iso) & (dicl["ISO3_2"]==iso2) ][['col','cnl','lp','cl']].mean(axis=1).values[0]

    t_index_selection.loc[:,'ICL'] = [ icl(country_iso3,selected_country) for selected_country in t_index_selection['iso3'] ]

    # Utility function
    t_index_selection.loc[:,'U'] = t_index_selection[['norm_t_index','HHI_by_country','ICL']].apply(lambda x: (x[0]+x[1]+x[2])/3 , axis=1)


    return t_index_selection