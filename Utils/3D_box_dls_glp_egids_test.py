# testing new 3d box with mean surface cutting plot

# Base Code

# Make 3D box
# Obs.: Custom data os used to get ISO data for clickevent and Area for hover
from numpy import ndarray
from numpy.core.multiarray import asarray
from load_data import DLS_GLP_EGID_data


fig_3dbox = px.scatter_3d(DLS_GLP_EGID_data, x='GLP', y='EGIDS', z='adjusted_total',
                    color=color, log_x=True, hover_name = "Language_Name", custom_data = ["ISO_639","Area"],
                    category_orders = {"EGIDS":pd.CategoricalIndex(DLS_GLP_EGID_data["EGIDS"]).categories}, height=800,
                    labels={
                                    "GLP": "Gross Language Product",
                                    "EGIDS": "EGIDS",
                                    "adjusted_total": "Digital Language Support Score"
                                })

# Set 3D box hover 
fig_3dbox.update_traces(hovertemplate='<b>%{hovertext}</b><br><br>Area = %{customdata[1]}<br>GLP = %{x}<br>EGIDS = %{y}<br>Digital Language<br>Support Score = %{z}<extra></extra>')

# Set click mode
fig_3dbox.update_layout(clickmode='event+select')

# Padding formatting
fig_3dbox.update_layout(margin=dict(l=20,
                                    r=25,
                                    b=30,
                                    t=30,
                                    pad=4
                                    )
                            )


# Example

x_glp = DLS_GLP_EGID_data["GLP"]
y_EGIDS = DLS_GLP_EGID_data["EGIDS"]
z_adjusted_total = DLS_GLP_EGID_data["adjusted_total"]
color_Area = DLS_GLP_EGID_data["Area"]
X_2, Y_2 = np.meshgrid([max(x_glp),100], [min(y_EGIDS),max(y_EGIDS)])

layout = go.Layout(width = 700, height =700,
                             title_text='Chasing global Minima')
fig = go.Figure(data=[go.Surface(x = X_2, y = Y_2, z=[[12,12],[12,12],[12,12],
                                                      [12,12],[12,12],[12,12],
                                                      [12,12],[12,12],[12,12],
                                                      [12,12],[12,12],[12,12],
                                                      [12,12]], colorscale = 'Blues')], layout=layout)

fig.add_scatter3d(x=x_glp, y=y_EGIDS, z = z_adjusted_total, mode='markers', 
                  marker=dict(size=2, color=["green","blue","yellow","red","black"]))



fig = px.scatter_3d(DLS_GLP_EGID_data, x='GLP', y='EGIDS', z='adjusted_total',log_x= True,
                    color=color, hover_name = "Language_Name", custom_data = ["ISO_639","Area"],
                    category_orders = {"EGIDS":pd.CategoricalIndex(DLS_GLP_EGID_data["EGIDS"]).categories}, height=800,
                    labels={
                                    "GLP": "Gross Language Product",
                                    "EGIDS": "EGIDS",
                                    "adjusted_total": "Digital Language Support Score"
                                })


fig.add_surface(x = X_2, y = Y_2, z=[[12,12],[12,12]], colorscale = 'Blues')

fig.show()


# Density plot with 3D volume plots ############################




x_glp = DLS_GLP_EGID_data["GLP"]


numbers_of_dls_bins = 6

# create X GLP space
x_glp_space = np.geomspace(1, max(x_glp), numbers_of_dls_bins+1)

# create Y EGIDS space
#y_egids_space = DLS_GLP_EGID_data["EGIDS"].unique().sort_values().tolist()

y_egids_space = np.asarray(np.linspace(1,13,   13), dtype=np.float32)

# Create Z DLS space
z_dls_space = np.linspace(0, 28,  numbers_of_dls_bins+1)

# Create mesh grid
#X_3, Y_3, Z_3 = np.meshgrid(x_glp_space, y_egids_space, z_dls_space)

X_f, Y_f, Z_f = np.meshgrid(x_glp_space[1::], y_egids_space[1::], z_dls_space[1::])

# Get DLS GLP EGID data separated
df_temp = DLS_GLP_EGID_data[["GLP","EGIDS","adjusted_total"]]

# Transform EGIDS to Integer
df_temp['EGIDS'] = pd.factorize(DLS_GLP_EGID_data["EGIDS"],sort=True)[0]



# Value egids flatten len = 12*99*99 = 117612
values_egids = []
counter = 0
for i_y_n in range(1,len(y_egids_space)):
           
    # values 
    ## upper bound
    y_n_upper = y_egids_space[i_y_n]
    ## lower bound
    y_n_lower = y_egids_space[i_y_n - 1]

    # Interval 
    #y_interval = pd.Interval(left=y_n_lower, right=y_n_upper,closed="left")

    # Filtering bin
    df_y_filtered = df_temp[ (df_temp["EGIDS"] >= y_n_lower) & (df_temp["EGIDS"]< y_n_upper)]


    values_glp = []

    for i_x_n in range(1,len(x_glp_space)):

        # values 
        ## upper bound
        x_n_upper = x_glp_space[i_x_n]
        ## lower bound
        x_n_lower = x_glp_space[i_x_n - 1]

        # Interval 
        #x_interval = pd.Interval(left=y_n_lower, right=y_n_upper,closed="left")

        # Filtering bin
        df_x_filtered = df_y_filtered[ (df_y_filtered["GLP"]>= x_n_lower) & (df_y_filtered["GLP"] < x_n_upper)]
        
        values_dls_temp = []

        counter += numbers_of_dls_bins

        # Counting x_n_upper,y_n_upper,
        if (len(df_x_filtered)!= 0):

            z_count = df_x_filtered['adjusted_total'].value_counts(bins= z_dls_space) 
            
            values_dls_temp = z_count.values
            #values_dls_temp = np.asarray(np.append(values_dls_temp,0), dtype=np.float32)
            #print(da)
        else: 
            values_dls_temp = np.asarray((numbers_of_dls_bins)*[0], dtype=np.float32)
        
        if ( len(values_dls_temp) == 0 ):
            values_dls_temp = np.asarray((numbers_of_dls_bins)*[0], dtype=np.float32)
    
        #if (len(values_dls_temp)!= 99 ):

        values_glp.append(values_dls_temp)


    values_egids.append(values_glp)
   
    
values = np.asarray(values_egids)



fig_volume = go.Figure(data=go.Volume(
    x=np.asarray(np.log(X_f.flatten()+.00000001), dtype=np.float32 ),
    y=Y_f.flatten(),
    z=np.asarray(Z_f.flatten(), dtype=np.float32 ),
    value=np.asarray(np.log(values.flatten()+.00000001), dtype=np.float32 ),
    isomin=0,
    #cmax = 0,
    #cmin = -18,
    isomax=6,
    opacity=0.1, # max opacity
    #opacityscale=[[-18.42, 0], [0, 1], [1, 1], [5, 1]],
    surface_count=21,
    colorscale='RdBu',
    #category_orders = {"EGIDS":pd.CategoricalIndex(DLS_GLP_EGID_data["EGIDS"]).categories}
    ))
fig_volume.show()
fig_volume.update_yaxes(type='category')
fig_volume.layout.scene.yaxis = {'categoryarray': ['x10', '9', '8b', '8a', '7', '6b', '6a', '5', '4', '3', '2', '1', '0'],
                                   'categoryorder': 'array',
                                   'title': {'text': 'EGIDS'}}

fig_volume.update_layout({'height': 800,
               'legend': {'title': {'text': 'Area'}, 'tracegroupgap': 0},
               'margin': {'t': 60},
               'scene': {'domain': {'x': [0.0, 1.0], 'y': [0.0, 1.0]},
                         'xaxis': {'title': {'text': 'Gross Language Product'}, 'type': 'log'},
                         'yaxis': {'categoryarray': array(['x10', '9', '8b', '8a', '7', '6b', '6a', '5', '4', '3', '2', '1', '0'],
                                                          dtype=object),
                                   'categoryorder': 'array',
                                   'title': {'text': 'EGIDS'}},
                         'zaxis': {'title': {'text': 'Digital Language Support Score'}}},
               'template': '...'})






fig = px.scatter_3d(DLS_GLP_EGID_data, x='GLP', y='EGIDS', z='adjusted_total',#log_x= True,
                    color=color, hover_name = "Language_Name", custom_data = ["ISO_639","Area"],
                    category_orders = {"EGIDS":pd.CategoricalIndex(DLS_GLP_EGID_data["EGIDS"]).categories}, height=800,
                    labels={
                                    "GLP": "Gross Language Product",
                                    "EGIDS": "EGIDS",
                                    "adjusted_total": "Digital Language Support Score"
                                })


fig.add_volume(x=np.asarray(np.log(X_f.flatten()+.00000001), dtype=np.float32 ),
                y=Y_f.flatten(),
                z=np.asarray(Z_f.flatten(), dtype=np.float32 ),
                value=np.asarray(np.log(values.flatten()+.00000001), dtype=np.float32 ),
                #isomin=-0.5,
                #isomax=0.5,
                opacity=0.1, # max opacity
                opacityscale=[[-18.42, 0], [0, 1], [1, 1], [5, 1]],
                surface_count=26,
                colorscale='RdBu')

fig.show()