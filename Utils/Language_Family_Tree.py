# Language family tree


TOLs[["ISO_639","Language_Name","Region_Name","Area","L1_Users","Classification"]]


# Making languages first level, Language name to first branch of the family tree
Lang_First_level = TOLs[["Language_Name"]][0:100]

Lang_First_level = Lang_First_level.rename(columns={'Language_Name':'source'})

# addind first branch 
Lang_First_level['target'] =  [ string.split(',')[-1] for string in TOLs['Classification'][0:100] ]


# Making the families names branchs 

for i in range(len(Lang_First_level['source'])):

    if i == 0:
        ## Split the family name into its componets
        source = TOLs['Classification'][i].split(',')

        ## Shift family name to match its parents 
        target = source[:-1]

        # Insert all languages roots ( DONT KNOW WHAT VAULE )
        target.insert(0,"Roots")

        # Make data frame 
        family_branch_tree = pd.DataFrame(data= { 'source' : source, 'target' : target })
    else:
        ## Split the family name into its componets
        source = TOLs['Classification'][i].split(',')

        ## Shift family name to match its parents 
        target = source[:-1]

        # Insert all languages roots ( DONT KNOW WHAT VAULE )
        target.insert(0,"Roots")

        # Make data frame 
        family_branch_tree_temp = pd.DataFrame(data= { 'source' : source, 'target' : target })
        
        # Append data
        family_branch_tree = family_branch_tree.append(family_branch_tree_temp)



# Append all levels 
family_branch_tree_final = family_branch_tree.append(Lang_First_level)




import pyvis
from pyvis.network import Network
import math 

net = Network(height='100%', width='100%')
#net.show_buttons(filter_=['physics'])

#net.barnes_hut(gravity=-2000, central_gravity=0, spring_length=250, spring_strength=0.001, damping=0.09, overlap=.2)


# Normalization of L1 setup ( puts L1 values between 0 and 1 )
#l1_max, l1_min = max(df_net_lp_2["L1_Users"]) , min(df_net_lp_2["L1_Users"])

#l1_range = l1_max - l1_min

# Adding Nodes
# NOTE: I'll not use this, a dataframe is better, but for now is this
all_nodes = family_branch_tree_final.stack().tolist()

all_nodes = list(set(all_nodes))

for node in all_nodes:    

    # Add nodes 

    net.add_node(node,value = 1
                 #group = row['group'],
                 #title = 'Country : ' + row['Country_Target'] + '<br>Most Used Language(L1) : '+ row["Language_Name"] + '<br>L1_Users : ' + str(row["L1_Users"]) + '<br>Family-branch : ' + row['family_branch']
                 )
    print(node)
   
    
# Adding edges
for row in family_branch_tree_final.to_dict('records'):

    #if( row['weight'] != 1):

    #net.add_edge(row['Country_Target'],row["Country_Source"],value = (1-row['weight']),length = 300+150*row['weight']**2,color = {'opacity' :  (1-row['weight'])} )
    net.add_edge(row['source'],row["target"],value = 1,
                    #color = {'opacity' :  ((math.cos(3*row['weight'])+1.05)/3)}# ,
                    #title = 'Language Proximity between :<br>' + row['Country_Source'] + ' and<br>' + row['Country_Target']+ '<br>Is : ' + str(1-row['weight']) 
                    )


#net.set_edge_smooth('curvedCW')


#net.toggle_physics(False)
net.show('example.html')



## Networkx text

import networkx as nx
import matplotlib as plt
import pygraphviz
import _graphvis

G = nx.from_pandas_edgelist(family_branch_tree_final)

pos = nx.nx_agraph.graphviz_layout(G, prog="twopi", args="")
plt.figure(figsize=(8, 8))
nx.draw(G, pos, node_size=20, alpha=0.5, node_color="blue", with_labels=False)
plt.axis("equal")
plt.show()

#--global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz
#-global-option=build_ext --global-option="-L/opt/lib/mygviz/" --global-option="-R/opt/lib/mygviz/"  pygraphviz

## Plotly dendrogram

import plotly.figure_factory as ff
import numpy as np
np.random.seed(1)

X = np.random.rand(15, 12) # 15 samples, with 12 dimensions each
fig = ff.create_dendrogram(X)
fig.update_layout(width=800, height=500)
fig.show()



X = TOLs['ISO_639'][0:200]

linkage_array =[]

import time



i = 0 
for x in X:
    loop_time = time.time()
    print( "{0:.2%}".format(i/len(X)) )
    temp = [ language_proximity(x,y) for y in X ]
    linkage_array.append(temp)
    print("--- %s seconds ---" % (time.time() - loop_time))
    i += 1
    #if ( i == 5):
    #    break

linkage_array_array = np.asarray(linkage_array)

fig = ff.create_dendrogram(linkage_array_array,labels = TOLs['Language_Name'][0:210].to_list())
fig.update_layout(width=1600, height=800)
fig.show()


fig.write_html("dendrogram_test.html")

#fig = ff.create_dendrogram(,distfun = language_proximity_all)




#################################### I'm here #################################################

# Notes: Construct polar Coordinates plot from already available dendrogram data. get_polar converts x,y to r, theta. 
# Probably will need to add fig.add_scatterpolar or fig.add_scatterpolargl 
 
# printing unique_combination list
print(unique_combinations)

# transforming normal dendrogram to polar coordenates
import math

def get_polar_old(coord):
    x = coord[0]
    y = coord[1]

    r = math.sqrt(x**2 + y**2)
    theta = math.degrees(math.atan(y/x))

    return  r,  theta

def get_polar_radialized_x(coord):
    x = coord[0]

    max_x = coord[2]
    min_x = coord[3]

    r = y
    #theta =  360*(x-min_x) / (max_x-min_x)
    
    theta =  360*(x) / (max_x)
    
    return  theta

def get_polar_radialized_y(coord):
    
    y = coord[1]
    max_y = coord[4]
    min_y = coord[5]
    
    # Slope
    if ( min_y == 0 ):
        

        r =  -1*y + (max_y)
    else:
        m = (min_y/-max_y)

        r =  m*y + (min_y)

    return  r




fig_polar = go.Figure()

# get the max,min X values ( Full circle )
for i in range(len(fig.data)):
    if i == 0:
        max_X_temp = max(fig.data[i]['x'])
        min_X_temp = min(fig.data[i]['x'])
        max_Y_temp = max(fig.data[i]['y'])
        min_Y_temp = min(fig.data[i]['y'])
    else:
        max_X_temp = max(np.append(fig.data[i]['x'],max_X_temp))
        min_X_temp = min(np.append(fig.data[i]['x'],min_X_temp))
        max_Y_temp = max(np.append(fig.data[i]['y'],max_Y_temp))
        min_Y_temp = min(np.append(fig.data[i]['y'],min_Y_temp))
        print(np.array(fig.data[i]['x'],max_X_temp))

# theta = [ (2/max(X)) * np.pi * x for x in X ]

def smoothsegment(seg, Nsmooth=10):
    return np.concatenate([[seg[0]], np.linspace(seg[1], seg[2], Nsmooth), [seg[3]]])


# Loop for creating the plot with the dendrogram radial projection        
for i in range(len(fig.data)):
        

    cart_coord = pd.DataFrame({'x' : smoothsegment(fig.data[i]['x']) , "y" : smoothsegment(fig.data[i]['y']) ,"max_x" : max_X_temp, "min_x" : min_X_temp,
                               "max_y" : max_Y_temp  , "min_y" : min_Y_temp})


    print( str(i) + " : " + str([ get_polar_radialized_x(x) for x in np.array(cart_coord) ]) )
    #polar_coord = cart_coord.apply(get_polar,axis=1)

    # tranformed theta is g: [min(X),max(X)] ------> [0,2*pi] where X is the space of all X in the plot 

    #polar_coord = /(max_X_temp-min_X_temp)

    fig_polar.add_trace(go.Scatterpolar(
            #r = cart_coord['y'].values,
            r = [ get_polar_radialized_y(y) for y in np.array(cart_coord) ],
            # Theta = 2*pi*(x-min(x)) / (max(x)-min(x))
            theta = [ get_polar_radialized_x(x) for x in np.array(cart_coord) ],
            #width=[20,15,10,20,15,30,15,],
            mode = 'lines',
            marker = dict(color = fig.data[i].marker.color),
            name = 'Branch' + str(i),
            #line_color = 'peru'
        ))


# Transform tick vals

tick_text = fig.layout.xaxis.ticktext
transformed_tick_vals  = [  360*(x) / max(fig.layout.xaxis.tickvals ) for x in fig.layout.xaxis.tickvals  ],

fig_polar.update_layout(
    title = 'Mic Patterns',
    showlegend = False,
    #polar_radialaxis = dict(#mirror= 'allticks',
    #                     rangemode= 'tozero',
    #                     showgrid= False,
    #                     showline= True,
    #                     showticklabels= True,
    #                     tickmode= 'array',
    #                     ticks= 'outside',
    #                     ticktext= ['Ghotuo', 'Alumu-Tesu', 'Ari', 'Ankave', 'Ambrak', 'Abu�\x80\x99',
    #                                        'Miniafia Oyan', 'Aranadan', 'Amal', 'Albanian, Arbëreshë'],
    #                     tickvals= [.3, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0,
    #                                  75.0, 85.0, 95.0]),
    polar_angularaxis = dict(#mirror= 'allticks',
                         #rangemode= 'tozero',
                         showgrid= False,
                         showline= True,
                         showticklabels= True,
                         tickmode= 'array',
                         ticks= 'outside',
                         #rotation = 90,
                         #tickangle = [.3, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0,
                         #             75.0, 85.0, 95.0],
                         ticktext= tick_text,
                         tickvals= transformed_tick_vals[0])
)

fig_polar.show()



fig_polar.layout.


Y = 5*[2]
X = range(100)



plt.plot(X, Y)
plt.show()

r = 2

g = 1

y_x = [ math.asin(i) for i in y ]

r = np.arange(0, 2, 0.01)

r = 100*[1.5]

theta = [ (2/max(X)) * np.pi * x for x in X ]

test = [ [2*math.cos(n_t), 2*math.sin(n_t)]  for n_t in theta ]


fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

new_r = [ x[0] for x in test]

new_theta = [ x[1] for x in test]

ax.plot(theta, r)
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()




#### sunburst
family_branch_tree_final.groupby('target').sum()

pre_test = family_branch_tree_final.drop_duplicates()

T = 66
test = dict(source = pre_test["source"][0:T].to_list(),
            target = pre_test["target"][0:T].to_list(),
            value = pre_test["value"][0:T].to_list() )


fig_sun = px.sunburst(test,names="source",parents="target",values="value")

fig_sun.show()

data2 = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=9*[1])

fig2 = px.sunburst(
    data2,
    names='character',
    parents='parent',
    values='value',
)
fig2.show()