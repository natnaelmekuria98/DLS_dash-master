# Network test/prod
import matplotlib.pyplot as plt
from pyvis.options import EdgeOptions


# load data - Don't know if this is the better way to do it 
exec(open("functions.py").read()) # Is better use from load_data import * ??? do I need __init__.py?
exec(open("load_data.py").read()) # Is better use from load_data import * ??? do I need __init__.py?
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 10)

#'''
# 0) preparing the data 

df_lics = pd.merge(LICs[['ISO_639','Language_Name','Country_Name','Country_Code',
                      'Area','All_Users','L1_Users', 'L2_Users','EGIDS']],
                TOLs[['ISO_639','Classification']], on ='ISO_639')

# get country most used language

users = "L1_Users"

df_lics_filtered_by_top_usage_within_country = df_lics.loc[df_lics.groupby('Country_Name', sort=False)[users].idxmax()]

# get top 50 users usage
top_n = df_lics_filtered_by_top_usage_within_country.nlargest(n=67, columns=[users]).Country_Code
# get language proximity for all languages

# a) first LP calculation version


for i in range(len(df_lics_filtered_by_top_usage_within_country.index)) :
#for iso in top_50 :

    iso = df_lics_filtered_by_top_usage_within_country['ISO_639'].iloc[i]

    country_code = df_lics_filtered_by_top_usage_within_country['Country_Code'].iloc[i]

    country_name = df_lics_filtered_by_top_usage_within_country['Country_Name'].iloc[i]

    if ( i == 0 ):
        df_lp = language_proximity_all(iso,users=users)

        df_lp = df_lp.loc[df_lp.groupby('Country_Code', sort=False)[users].idxmax()]


        df_lp['source'] = country_code

    else:
        df_temp = language_proximity_all(iso,users=users)

        df_temp = df_temp.loc[df_temp.groupby('Country_Code', sort=False)[users].idxmax()]

        df_temp['source'] = country_code

        df_lp = pd.concat([df_lp,df_temp], ignore_index=True)
   
    i += 1

    print(country_name + ' nrow : ' + str(len(df_lp.index) ) )


# Formatting
# obs.: Family names is from Country_Target

df_net_lp = df_lp[['source','Country_Code','L1_Users','Language_Name','distance','Family','Classification']]

# Using only top_n 
df_net_lp = df_net_lp[ df_net_lp['source'].isin(top_n) & df_net_lp['Country_Code'].isin(top_n) ]

# Column rename
df_net_lp.columns = ['Source','Target','L1_Users','Language_Name','weight','family','classification']


#df_net_lp['width'] = 10*df_net_lp.weight**2 


#df_net_lp['length'] = (1 - df_net_lp.weight ) * 150 + 500 

# Cleaning data with target == source
df_net_lp = df_net_lp.loc[ df_net_lp['Source'] != df_net_lp['Target'] ]

# Join country name with their respective code, source

df_net_lp = df_net_lp.merge(df_lics_filtered_by_top_usage_within_country[['Country_Code','Country_Name']], left_on = 'Source' , right_on = 'Country_Code').drop('Country_Code',axis='columns')

df_net_lp = df_net_lp.rename(columns={'Country_Name':'Country_Source'})

# Join country name with their respective code, target

df_net_lp = df_net_lp.merge(df_lics_filtered_by_top_usage_within_country[['Country_Code','Country_Name']], left_on = 'Target' , right_on = 'Country_Code').drop('Country_Code',axis='columns')

df_net_lp = df_net_lp.rename(columns={'Country_Name':'Country_Target'})

# Get first two names from family classification for each language

df_net_lp['family_branch'] = [ ",".join(filter(None,iso_class.split(',')[0:2])) for iso_class in df_net_lp['classification'] ]


# pyvis setup



df_net_lp_2 = df_net_lp

df_net_lp_2['group'] = list(pd.factorize(df_net_lp["family_branch"])[0])





df_net_lp_2.to_csv("./data/network_data.csv")

#'''


df_net_lp_2 = pd.read_csv("./data/network_data.csv",encoding = "ISO8859-1",index_col = 0)

import pyvis
from pyvis.network import Network
import math 

net = Network(height='100%', width='100%')
#net.show_buttons(filter_=['physics'])

#net.barnes_hut(gravity=-2000, central_gravity=0, spring_length=250, spring_strength=0.001, damping=0.09, overlap=.2)


# Normalization of L1 setup ( puts L1 values between 0 and 1 )
l1_max, l1_min = max(df_net_lp_2["L1_Users"]) , min(df_net_lp_2["L1_Users"])

l1_range = l1_max - l1_min

for row in df_net_lp_2[["Country_Target","L1_Users","Language_Name","group","family_branch"]].drop_duplicates().to_dict('records'):

    # normalize L1_Users
    l1_normalized = (row['L1_Users'] - l1_min) / l1_range

    # Add nodes 
    net.add_node(row['Country_Target'],value = 10*l1_normalized,
                 group = row['group'],title = 'Country : ' + row['Country_Target'] + '<br>Most Used Language(L1) : '+ row["Language_Name"] + '<br>L1_Users : ' + str(row["L1_Users"]) + '<br>Family-branch : ' + row['family_branch']     )
    

for row in df_net_lp_2.to_dict('records'):

    #if( row['weight'] != 1):

    #net.add_edge(row['Country_Target'],row["Country_Source"],value = (1-row['weight']),length = 300+150*row['weight']**2,color = {'opacity' :  (1-row['weight'])} )
    net.add_edge(row['Country_Target'],row["Country_Source"],value = ((math.cos(3*row['weight'])+1.5)/4),length = 300+150*row['weight']**2,
                    color = {'opacity' :  ((math.cos(3*row['weight'])+1.05)/3)}# ,
                    #title = 'Language Proximity between :<br>' + row['Country_Source'] + ' and<br>' + row['Country_Target']+ '<br>Is : ' + str(1-row['weight']) 
                    )


#num_actual_nodes = len(df_net_lp_2[["Country_Target","L1_Users","group"]].drop_duplicates().to_dict('records'))

#num_legend_nodes = len(df_net_lp_2['group'].unique())


#import math 

## Add Legend Nodes
#step = 75
#x_step = 200
#x = -450
#y = -250
#row_legend_size = 8

#column_legend_size = math.ceil(num_legend_nodes / row_legend_size)

#for row in df_net_lp_2[['group','family_branch']].drop_duplicates().to_dict('records'):

#    x = -450
#    y = -250

#    n_row = int(row['group']) - row_legend_size * math.floor(row['group']/row_legend_size)
#    n_row = int(n_row)
#    n_col = math.floor(row['group']/row_legend_size)
#    n_col = int(n_col)

#    y = int(f'{y+n_row*step}')
#    x = int(f'{x+n_col*x_step}')

#    #net.add_node(str(row)+'test',group = row,label = str(row)+'test', physics = False , x = x, y = f'{y+row*step}' )
#    net.add_node(row['family_branch'],value = 1,group = int(row['group']) ,fixed = True,  physics = False , x = x, y = y)

#    #net.add_node('teste',value = 10*l1_normalized,group = row['group'] ,  physics = False , x = x, y = f'{y+row*step}')

    
net.set_edge_smooth('curvedCW')


#net.toggle_physics(False)
net.show('example.html')


# not working
#net.set_options('var options = {"configure": {"enabled": true},	"nodes": {"font": {"strokeWidth": 5},"scaling": {"min": 2},"shadow": {"enabled": true}},"edges": {"color": {"inherit": true},        "smooth": {            "enabled": true,            "type": "curvedCW"        },		"color": {		  "inherit": true		},		"scaling": {		  "min": 0,		  "max": 3		},    },    "interaction": {        "dragNodes": true,        "hideEdgesOnDrag": false,        "hideNodesOnDrag": false    },    "physics": {        "enabled": true,        "stabilization": {            "enabled": true,            "fit": true,            "iterations": 1000,            "onlyDynamicEdges": false,            "updateInterval": 50        }    }};')


# Add this to example.html
'''
"nodes": {
		"font": {
		  "strokeWidth": 5
		},
		"scaling": {
		  "min": 2
		},
		"shadow": {
		  "enabled": true
		}
	},
    "edges": {
        "color": {
            "inherit": true
        },
        "smooth": {
            "enabled": true,
            "type": "curvedCW"
        },
		"color": {
		  "inherit": true
		},
		"scaling": {
		  "min": 0,
		  "max": 3
		},
    },


'''

test = """
var options = {
    "configure": {
        "enabled": true
    },
    "nodes": {
		"font": {
		  "strokeWidth": 5
		},
		"scaling": {
		  "min": 3,
		  "max": 30
		},
		"shadow": {
		  "enabled": true
		},
		"color": {
					"hover": {
								"border": '#2B7CE9',
								"background": '#D2E5FF'
							}
		
		}
	},
    "edges": {
        "color": {
            "inherit": true
        },
        "smooth": {
            "enabled": true,
            "type": "curvedCW"
        },
		"color": {
		  "inherit": true
		},
		"scaling": {
		  "min": 0,
		  "max": 3
		},
    },
	
    "interaction": {
		"tooltipDelay": 0,
        "dragNodes": true,
        "hideEdgesOnDrag": false,
        "hideNodesOnDrag": false
    },
    "physics": {
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "fit": true,
            "iterations": 1000,
            "onlyDynamicEdges": false,
            "updateInterval": 50
        }
    }
}

"""