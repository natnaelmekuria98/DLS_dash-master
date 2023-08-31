from dash import dcc, html
import dash_bootstrap_components as dbc

# Page Layout Output ---------------------------------------------------------------------------------------------------------------------------------------------------

layout = html.Div([
                   # First Row -----------------------------------------------------------------------------------------------------------------------------------------
                   dbc.Row([
                            #html.input()
                            html.Div([
                                      # Carousel-Indicators ------------------------------------------------------------------------------------------------------------
                                      html.Div([
                                                html.Button(type = "button", className = "active", **{"aria-label":"Slide 1","aria-current":"true",
                                                                                                      "data-bs-target":"#carouselHomeIndicators", "data-bs-slide-to":"0"}),
                                                html.Button(type = "button", **{"aria-label":"Slide 2","aria-current":"false",
                                                                                "data-bs-target":"#carouselHomeIndicators", "data-bs-slide-to":"1"}),
                                                html.Button(type = "button", **{"aria-label":"Slide 3","aria-current":"false",
                                                                                "data-bs-target":"#carouselHomeIndicators", "data-bs-slide-to":"2"}),
                                               ],className="carousel-indicators"),
                                      # Carousel-inner (Content) -------------------------------------------------------------------------------------------------------
                                      html.Div([
                                                # First Carousel content -----------------------------------------------------------------------------------------------
                                                html.Div([
                                                          # Carousel Row -----------------------------------------------------------------------------------------------                                                     
                                                          dbc.Row([ 
                                                                    # First Col ----------------------------------------------------------------------------------------
                                                                    dbc.Col([
                                                                             html.Img(src="./assets/images/home/3dbox.svg")
                                                                              ],md = 6, style = {"display": "flex",
                                                                                                "height": "10%",
                                                                                                "width": "500px",
                                                                                                "flex-direction": "column",
                                                                                                "justify-content": "center",
                                                                                                #"margin-left": "auto",
                                                                                                #"margin-right": "auto"
                                                                                                }),
                                                                    # Second Col ---------------------------------------------------------------------------------------
                                                                    dbc.Col([
                                                                             html.H1("Digital Language Support"),
                                                                             html.Li("Index created to measure Languages level of digital support"),
                                                                             html.Li("482 softwares languages support considered (more planned)"),
                                                                             html.Li("3917 languages with at least one software support"),
                                                                             html.Li("Software has seven possible classfications based on linguistic\
                                                                                      functions (content, encoding, surface, meaning, localized, speech, assistant)"),
                                                                             html.Li("Planned to be updated regularly (weekly basis)"),
                                                                             # See data button
                                                                             dbc.Button("See data",href="/language-page/dls",color="primary",
                                                                                        style = {'width': '100px','color': '#000',
                                                                                                 'background-color': '#bfb5ff',
                                                                                                 'border-color': '#bfb5ff',
                                                                                                 #'align-self': 'center',
                                                                                                 'margin-top': '5%',
                                                                                                 'margin-right': '10%',
                                                                                                 'margin-left': '10%'}
                                                                                        )
                                                                             ],md = 6, style = {"display": "flex",
                                                                                                "height": "10%",
                                                                                                "width": "500px",
                                                                                                "flex-direction": "column",
                                                                                                "justify-content": "center",
                                                                                                #"margin-left": "auto",
                                                                                                #"margin-right": "auto"
                                                                                                })
                                                                    ],
                                                                      className = "w-100",
                                                                      style = {'max-width': '81%','min-height': '600px',
                                                                               'padding-top': '6%',
                                                                               'margin-left': 'auto','margin-right': 'auto',
                                                                               'justify-content': 'center'}
                                                                      ),
                                                         #html.Img(src='/assets/images/home/dls_car.svg', style = {'width': '100%'})
                                                         ],className="carousel-item active"),
                                                # Second Carousel content ----------------------------------------------------------------------------------------------
                                                html.Div([
                                                          # Carousel Row -----------------------------------------------------------------------------------------------                                                     
                                                          dbc.Row([ 
                                                                    # First Col ----------------------------------------------------------------------------------------
                                                                    dbc.Col([
                                                                             html.H1("Language Economics"),
                                                                             html.Li("Economic data grouped by language"),
                                                                             html.Li("Estimation of Language Gross Domestic Product  (Gross  Language Product) \
                                                                                      without or with geographic data"),
                                                                             html.Li("Use of international trade data to show trends in export/import by \
                                                                                      grouped by language(planned)"),
                                                                             html.Li("Wealth distribution data associated with languages (planned)"),
                                                                             
                                                                             # See data button
                                                                             dbc.Button("See data",href="/language-page/economics",
                                                                                        style = {'width': '100px','color': '#000',
                                                                                                 'background-color': '#bfb5ff',
                                                                                                 'border-color': '#bfb5ff',
                                                                                                 'align-self': 'flex-end',
                                                                                                 'margin-top': '5%',
                                                                                                 'margin-right': '10%',
                                                                                                 'margin-left': '10%'}
                                                                                        )
                                                                             ],md = 6, style = {"display": "flex",
                                                                                                "height": "10%",
                                                                                                "width": "500px",
                                                                                                "flex-direction": "column",
                                                                                                "justify-content": "center",
                                                                                                #"margin-left": "auto",
                                                                                                #"margin-right": "auto"
                                                                                                }),
                                                                    # Second Col ---------------------------------------------------------------------------------------
                                                                    dbc.Col([
                                                                             html.Img(src="./assets/images/home/cpi.svg"),
                                                                             html.P("* - Consumer Price Index of all Countries that speaks english",
                                                                                    style = {"align-self": "center"}),
                                                                             ],md = 6, style = {"display": "flex",
                                                                                               "height": "10%",
                                                                                               "width": "500px",
                                                                                               "flex-direction": "column",
                                                                                               "justify-content": "center",
                                                                                               #"margin-left": "auto",
                                                                                               #"margin-right": "auto"
                                                                                               }),
                                                                             
                                                                    
                                                                    ],
                                                                      className = "w-100",
                                                                      style = {'max-width': '81%','min-height': '600px',
                                                                               'padding-top': '6%',
                                                                               'margin-left': 'auto','margin-right': 'auto',
                                                                               'justify-content': 'center'}
                                                                      ),
                                                         #html.Img(src='/assets/images/home/dls_car.svg', style = {'width': '100%'})
                                                         ],className="carousel-item"),
                                                
                                                # Third Carousel content -----------------------------------------------------------------------------------------------
                                                html.Div([
                                                          # Carousel Row -----------------------------------------------------------------------------------------------                                                     
                                                          dbc.Row([ 
                                                                    # First Col ----------------------------------------------------------------------------------------
                                                                    dbc.Col([
                                                                             html.H1("Language Analytics"),
                                                                             html.Li("Language Concentration Index "),
                                                                             html.Li("Language Internet User Purchase Power Index"),
                                                                             html.Li("Countries Languages and proximity"),   
                                                                             # See data button
                                                                             dbc.Button("See data",href="/language-page/economics",
                                                                                        style = {'width': '100px','color': '#000',
                                                                                                 'background-color': '#bfb5ff',
                                                                                                 'border-color': '#bfb5ff',
                                                                                                 'align-self': 'flex-end',
                                                                                                 'margin-top': '5%',
                                                                                                 'margin-right': '10%',
                                                                                                 'margin-left': '10%'}
                                                                                        ),
                                                                             html.Img(src="./assets/images/glp_togo/togo_tem_gdp.svg",
                                                                                      style = {'width': '60%',
                                                                                               'align-self': 'center'})
                                                                             ],md = 4, style = {"display": "flex",
                                                                                                "height": "10%",
                                                                                                #"width": "500px",
                                                                                                "flex-direction": "column",
                                                                                                "justify-content": "center",
                                                                                                #"margin-left": "auto",
                                                                                                #"margin-right": "auto"
                                                                                                }),
                                                                    # Second Col ---------------------------------------------------------------------------------------
                                                                    dbc.Col([
                                                                             html.Img(src="./assets/images/lang_tree/lang_tree_with_L1_bars.svg"),
                                                                             ],md = 4, style = {"display": "flex",
                                                                                               "height": "10%",
                                                                                               #"width": "500px",
                                                                                               "flex-direction": "column",
                                                                                               "justify-content": "center",
                                                                                               #"margin-left": "auto",
                                                                                               #"margin-right": "auto"
                                                                                               }),
                                                                    # Third Col ----------------------------------------------------------------------------------------
                                                                    dbc.Col([
                                                                             html.Img(src="./assets/images/glp_togo/2_togo_overlaps.svg",
                                                                                      style = {'width': '100%',
                                                                                               'align-self': 'center'}),
                                                                             html.H1("Socio-Economic Data"),
                                                                             html.Li("Variety of data related to a country or a language"),
                                                                             html.Li("Maps and Analytics build in geographical data"),
                                                                             
                                                                             ],md = 4, style = {"display": "flex",
                                                                                               "height": "10%",
                                                                                               #"width": "500px",
                                                                                               "flex-direction": "column",
                                                                                               "justify-content": "center",
                                                                                               #"margin-left": "auto",
                                                                                               #"margin-right": "auto"
                                                                                               }),
                                                                    
                                                                    ],
                                                                      className = "w-100",
                                                                      style = {'max-width': '81%','min-height': '600px',
                                                                               'padding-top': '1%', 'max-height': '70vh',
                                                                               'margin-left': 'auto','margin-right': 'auto',
                                                                               'justify-content': 'center'}
                                                                      ),
                                                         #html.Img(src='/assets/images/home/dls_car.svg', style = {'width': '100%'})
                                                         ],className="carousel-item"),
                                                ],className="carousel-inner"),
                                      # carousel-control (next and prev button) ----------------------------------------------------------------------------------------
                                      ## Prev Button
                                      html.Button([
                                              html.Span(className= "carousel-control-prev-icon", **{"aria-hidden": "true"}),
                                              html.Span(["Previous"],className= "visually-hidden")

                                              ],className="carousel-control-prev", type = "button",
                                                **{"data-bs-slide":"prev","data-bs-target":"#carouselHomeIndicators"}  ),
                                      ## Next Button
                                      html.Button([
                                              html.Span(className= "carousel-control-next-icon", **{"aria-hidden": "true"}),
                                              html.Span(["Next"],className= "visually-hidden")
                                              ],className="carousel-control-next", type = "button",
                                                **{"data-bs-slide":"next","data-bs-target":"#carouselHomeIndicators"}  )
                                      #  
                                      ],className="carousel slide carousel-dark",
                                        id= "carouselHomeIndicators",
                                        style = {"padding-right": "0px", "padding-left": "0px"},
                                        **{"data-bs-ride": "carousel"}
                                        ),

                            ], style = {"margin-top": "0px", "margin-left": "0rem",
                                        "margin-right": "0rem", "padding-right": "1px"}), 
                   # Second Row -----------------------------------------------------------------------------------------------------------------------------------------
                   dbc.Row([
                            # First Col ---------------------------------------------------------------------------------------------------------------------------------
                            dbc.Col([],md = 4),
                            # Second Col --------------------------------------------------------------------------------------------------------------------------------
                            dbc.Col([
                                     html.Div([
                                               html.H1([html.B(["Intelligence"]) ]),
                                               html.P(["Derivation's unique analytical platform offers unrivalled access \
                                                        to decision-support information regarding the world's living languages. \
                                                        A broad range of graphical and statistical options provides unlimited \
                                                        insight into language populations, maps, dialects, endangerment, trends, \
                                                        usage and more in every corner of the world. Our tools enable organisations \
                                                        to make better decisions regarding expansion and localisation, based upon \
                                                        the world's most authoritative, comprehensive and up-to-date language data."],
                                                      style = {'text-align': 'justify'})
                                               ])
                                     ],md = 4)
                            ],style = {"background-color": "rgb(52 194 255 / 11%)",
                                       "box-shadow": "0 1px 3px 0 rgb(0 0 0 / 20%)",
                                       "border-top": "1px solid rgba(207,215,230,0.5)",
                                       "padding": "3rem 2rem","margin-top": "0px"}), 

                            # Third Col ---------------------------------------------------------------------------------------------------------------------------------
                            dbc.Col([],md = 4),
                        

                       ], id = "landing_page",
                        style = {"margin-left": "0rem",
                                 "margin-right": "0rem",
                                 #"padding": "0rem .73rem 2rem 0rem"
                                 })

## First Row -------------------------------------------------------------------------------------------------------------------------------------------
first_row = dbc.Container([
        dbc.Col([
                html.H1("Understand the global Digital Language Divide, easily and efficiently.",
                        style={"margin-top": "80px"}),
                html.P(
                    "The gap between digital and non-digital languages is referred to as the Digital \
                        Language Divide and, for languages that are non-digital, this means no hardware\
                        or software support (e.g., no keyboards, no operating systems, no fonts), without\
                        which there is no content of any kind. Given 50% of the world’s languages are\
                        non-digital and less than 1% are considered fully digital, it’s a critical \
                        humanitarian and technological issue facing billions of people across the \
                        planet. For the first time ever, using the Derivation : Intelligence platform,\
                        linguists, researchers and companies can measure and visualize the Digital \
                        Language Divide impact - comparing & contrasting individual languages.",
                    className="col-lg-10 mx-auto text-white text-center mt-sm-5 mt-3",
                ),
            ],className="mx-auto",lg=10
        ),
    ],
)

## Explore digital language -------------------------------------------------------------------------------------------------------------------------------------------
second_Section = html.Section(
    className="container mt-100",
    children=[
        # First Row -------------------------------------------------------------------------------------------------------------
        html.H2(
            className="heading mb-3",
            children=[
                "Focus on the Digital Language Support of every language and every country.",
                # html.Br(className="d-none d-md-block"),
                # " support intelligence tool",
            ],
        ),
        html.P(
            className="text-muted",
            children=[
                "It's important to understand that digital equality does not exist across all \
                languages: around 50% of the world’s living languages are digitally supported,\
                albeit to varying degrees, and 50% are not digitally supported (at all).\
                For speakers, readers and signers of digitally weaker languages, it can mean \
                being forced to operate in a different language or face exclusion from vital\
                access to digital language content.   The Derivation : Intelligence platform \
                enables attention to focus on exactly which languages are (and are not) supported\
                and to what degree in various aspects of digital technology.",
                html.Br(),
                # "visualization and language data infographics to enable every language to display its unique strengths and potential",
            ],
        ),
        # Second Row ------------------------------------------------------------------------------------------------------------
        html.Div(
            className="row gx-lg-5",
            children=[
                # First column -----------------------------------------------------------------------------------------------------
                html.Div(
                    className="col-md-6",
                    children=[
                        html.Div(
                            className="dls-card",
                            children=[
                                html.H3(
                                    className="mb-4",
                                    children=["What is Digital Language Support ('DLS')?"],
                                ),
                                html.P(
                                    className="text-muted",
                                    children=[
                                        "DLS is an innovative suite of objective metrics that classifies \
                                        the extent to which a language is (or is not) supported in the digital\
                                        era.  It measures the language-specific capabilities of hardware or \
                                        software support, including keyboards, operating systems, fonts, voice\
                                        assistants and more."
                                    ],
                                ),
                                # html.Button(
                                #     type='button',
                                #     className='btn btn-theme px-3',
                                #     **{
                                #         'data-bs-toggle': 'modal',
                                #         'data-bs-target': '#dlsModal'
                                #     },
                                #     children=[
                                #         html.H5(
                                #             className="mb-0",
                                #             children=[
                                #                 html.I(
                                #                     className="fa-solid fa-arrow-right"
                                #                 )
                                #             ],
                                #         )
                                #     ],
                                # ),
                                html.Img(
                                    src="/assets/images/dls-vector.svg",
                                    className="img-fluid",
                                    alt="dls vector",
                                ),
                            ],
                        )
                    ],
                ),
                # Second column ----------------------------------------------------------------------------------------------------
                html.Div(
                    className="col-md-6",
                    children=[
                        html.Div(
                            className="dls-card",
                            children=[
                                html.H3(
                                    className="mb-4",
                                    children=["Why is DLS important to companies?"],
                                ),
                                html.P(
                                    className="text-muted",
                                    children=[
                                        "In simple terms, thousands of languages struggle to thrive in an \
                                        increasingly digitally-biased world.   To address the language \
                                        inequalities impacting billions of people, requires a comprehensive \
                                        and granular understanding of which languages possess what digital \
                                        strengths and weaknesses."
                                    ],
                                ),
                                # html.Button(
                                #     type='button',
                                #     className='btn btn-theme px-3',
                                #     **{
                                #         'data-bs-toggle': 'modal',
                                #         'data-bs-target': '#globalStateModal'
                                #     },
                                #     children=[
                                #         html.H5(
                                #             className="mb-0",
                                #             children=[
                                #                 html.I(
                                #                     className="fa-solid fa-arrow-right"
                                #                 )
                                #             ],
                                #         )
                                #     ],
                                # ),
                                html.Img(
                                    src="/assets/images/globalState-vector.svg",
                                    className="img-fluid",
                                    alt="dls vector",
                                ),
                            ],
                        )
                    ],
                ),
            ],
        ),
    ],
)

## DLS distribution analysis -------------------------------------------------------------------------------------------------------------------------------------------
third_Section = html.Section(
    className="container mt-100",
    children=[
        html.Div(
            className="row align-items-center",
            children=[
                # First column -----------------------------------------------------------------------------------------------------
                html.Div(
                    className="col-lg-6",
                    children=[
                        html.H2(
                            className="heading mb-4 d-lg-none ",
                            children="DLS distribution analysis"
                        ),
                        html.Img(
                            className="img-fluid",
                            src="/assets/images/lang_tree/lang_tree_with_L1_bars.svg",
                            alt="chart images"
                        )
                    ]
                ),
                # Second column ----------------------------------------------------------------------------------------------------
                html.Div(
                    className="col-lg-6 mt-5 mt-lg-0",
                    children=[
                        html.H2(
                            className="heading mb-4 d-lg-block",
                            children="DLS distribution analysis"
                        ),
                        html.P(
                            className="text-muted analytics-text mb-0",
                            children="Derivation’s unique analytical platform offers unrivalled access to decision-support information regarding the world’s living languages. A broad range of graphical and statistical options provides unlimited insight into language populations, maps, dialects, endangerment, trends, usage and more in every corner of the world. Our tools enable organisations to make better decisions regarding expansion and localisation, based upon the world’s most authoritative, comprehensive and up-to-date language data."
                        ),
                        # html.A(
                        #     href="#",
                        #     className="btn btn-theme mt-3 mt-md-5",
                        #     children="Read More"
                        # )
                    ]
                )
            ]
        )
    ]
)

font_color = '#FCF4F5'


# Global Trends -------------------------------------------------------------------------------------------------------------------------------------------
fourth_Section = html.Section([
    dbc.Container([
        # First Row -------------------------------------------------------------------------------------------------------------
        dbc.Row([
            # First column -----------------------------------------------------------------------------------------------------
            dbc.Col([
                html.H2(
                    className="heading mb-4 d-lg-block",
                    children="Global Trends. Local Insight.",
                    style={"color": font_color}
                ),
                html.P(
                    className="analytics-text mb-0",
                    children="Focus on trends with global, regional and country-level analysis. \
                                Harness data in tabular, graphical and statistical format.",
                    style={"color": font_color}
                ),
                # html.A(
                #     href="#",
                #     className="btn btn-theme mt-3 mt-md-5",
                #     children="Read More"
                # )
            ], className="mt-5 mt-lg-0", lg=6
            ),
            # Second column ----------------------------------------------------------------------------------------------------
            dbc.Col([
                html.Img(
                    className="img-fluid",
                    src="/assets/images/home/world_map_dls.svg",
                    alt="chart images",
                    style={"height": "270px", "border-radius": "5px"}
                )
            ], className="col-lg-4",
            ),
        ], className="align-items-center",
        style={"display": "flex",
               "justify-content": "space-evenly"}
        ),
        # Second Row ------------------------------------------------------------------------------------------------------------
        dbc.Row([
            # First column -----------------------------------------------------------------------------------------------------
            dbc.Col([
                html.Img(
                    className="img-fluid",
                    src="/assets/images/home/column.svg",
                    alt="chart images",
                    style={"border-radius": "5px"}
                ),
            ], lg=6
            ),
            # Second column ----------------------------------------------------------------------------------------------------
            dbc.Col([
                    html.H2(
                        className="heading mb-4 d-lg-block",
                        children="Powerful Language Comparison",
                        style={"color": font_color}
                    ),
                    html.P(
                        className="analytics-text mb-0",
                        children="Deep dive into single or multiple languages, including powerful comparison tools. A range of 2D graphs and dynamic 3D visualization.",
                        style={"color": font_color}
                    ),
                    # html.A(
                    #     href="#",
                    #     className="btn btn-theme mt-3 mt-md-5",
                    #     children="Read More"
                    # )
                    ], className="mt-20 mt-lg-0",
                    lg=5
                    )
            ], className="align-items-center mt-5",
            style={"display": "flex",
                "justify-content": "space-evenly"}
            ),
        # Third Row ------------------------------------------------------------------------------------------------------------
        dbc.Row([
            # First column -----------------------------------------------------------------------------------------------------
            dbc.Col([
                html.H2(
                    className="heading mb-4 d-lg-block",
                    children="Advanced Digital Language Analysis",
                    style={"color": font_color}
                ),
                html.P(
                    className="analytics-text mb-0",
                    children="The world’s most advanced Digital Language Divide tool, based upon the most complete digital language support dataset.  Unique analysis techniques including 2x2 matrices.",
                    style={"color": font_color}
                ),
                # html.A(
                #     href="#",
                #     className="btn btn-theme mt-3 mt-md-5",
                #     children="Read More"
                # )
            ],className="mt-5 mt-lg-0",lg=6,
            ),
            # Second column ----------------------------------------------------------------------------------------------------
            dbc.Col([
                html.Img(
                    className="img-fluid",
                    src="/assets/images/home/matrix_example.svg",
                    alt="chart images",
                    style={"height": "320px", "border-radius": "5px"}
                    )
                ],lg=5
            ),
            ],className="align-items-center mt-5",
            style={"display": "flex",
                   "justify-content": "space-evenly"}
        )
    ])
],
className="mt-100",
style={"padding": "50px",
       "background": "linear-gradient(0deg, #D34B55, #DF6A3F )"}
)

## Powerful Language Comparison -------------------------------------------------------------------------------------------------------------------------------------------
# fifth_Section = html.Section([
#         dbc.Container([ 
        
#         ])
#     ],className="mt-0"
# )

# ## Advanced Digital Language Analysis -------------------------------------------------------------------------------------------------------------------------------------------
# sixth_Section = html.Section([
#     dbc.Container([
        
#     ])
# ], className="mt-0"
# )

## Features and Benefits -------------------------------------------------------------------------------------------------------------------------------------------
seventh_Section = html.Section(
    className="container mt-100",
    children=[
        html.H2(className="heading", children="Features and Benefits"),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-xl-6",
                    children=[
                        html.H4(
                            className="fw-bold mt-40 mb-4",
                            children="DLS dataset:",
                        ),
                        html.Ul(
                            className="feature-list",
                            children=[
                                html.Li(
                                    children="Unique global dataset based upon more than 140 data sources (2021)"
                                ),
                                html.Li(
                                    children="Summarized 5-point digital support category for 7,000+ living languages"
                                ),
                                html.Li(
                                    children="Granular language component scores for language-specific comparison"
                                ),
                                html.Li(
                                    children="ISO 639 encoded to enable simple integration and analysis with other datasets"
                                ),
                            ],
                        ),
                        html.H4(
                            className="fw-bold mt-40 mb-4",
                            children="DLS visualization tool:",
                        ),
                        html.Ul(
                            className="feature-list",
                            children=[
                                html.Li(
                                    children="Visual and dynamic presentation of the DLS dataset for superior analysis"
                                ),
                                html.Li(
                                    children="Access to global, regional and language-specific charts and tables"
                                ),
                                html.Li(
                                    children="Unique comparison tool enabling side-by-side analysis of multiple languages"
                                ),
                                html.Li(
                                    children="Powerful and flexible “beta” software with many user-defined options."
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="col-xl-6 mt-5 mt-xl-0",
                    children=[
                              html.Div(className='langScale-block', children=[
                                html.Div(className='chartArrow', children=[
                                  html.Span(className='mb-0 fw-semibold', children='Weaker'),
                                  html.Span(className='mb-0 fw-semibold', children='Stronger')
                                ]),
                                html.Div(className='bar-flex justify-content-md-center', children=[
                                    html.Div(children=[
                                        html.H5(className='text-center d-xl-block', children='Unknown'),
                                        html.H5(className='text-center d-xl-none', children='Unk'),
                                        html.Span(className='bar-merger single border-bottom-0'),
                                        html.Button(
                                            type='button',
                                            className='btn scale-bar bar-1',
                                            children=[
                                                html.Div(children=[
                                                    html.Span(children='Unclassified')
                                                ]),
                                                html.Div(children='U')
                                            ]
                                        )
                                    ]),
                                    html.Div(children=[
                                        html.H5(className='text-center', children='Unsupported'),
                                        html.Span(className='bar-merger single border-bottom-0'),
                                        html.Button(
                                            type='button',
                                            className='btn scale-bar bar-2',
                                            children=[
                                                html.Div(children=[
                                                    html.Span(children='Still')
                                                ]),
                                                html.Div(children='S')
                                            ]
                                        )
                                    ]),
                                    html.Div(children=[
                                        html.H5(className='text-center', children='Partial Support'),
                                        html.Span(className='bar-merger border-bottom-0'),
                                        html.Div(className='d-flex', children=[
                                            html.Div(className='', children=[
                                                html.Div(className='d-flex', children=[
                                                    html.Button(
                                                        type='button',
                                                        className='btn scale-bar bar-4',
                                                        children=[
                                                            html.Div(children=[
                                                                html.Span(children='Emerging')
                                                            ]),
                                                            html.Div(children='E')
                                                        ]
                                                    )
                                                ])
                                            ]),
                                            html.Div(children=[
                                                html.Div(className='d-flex', children=[
                                                    html.Button(
                                                        type='button',
                                                        className='btn scale-bar bar-6',
                                                        children=[
                                                            html.Div(children=[
                                                                html.Span(children='Ascending')
                                                            ]),
                                                            html.Div(children='A')
                                                        ]
                                                    )
                                                ])
                                            ]),
                                        html.Div(className='', children=[
                                            html.Div(className='d-flex', children=[
                                                html.Button(
                                                    type='button',
                                                    className='btn scale-bar bar-9',
                                                    children=[
                                                        html.Div(children=[
                                                            html.Span(children='Vital')
                                                        ]),
                                                        html.Div(children='V')
                                                    ]
                                                )
                                            ])
                                        ])
                                    ])
                                    ]),
                                    html.Div(children=[
                                    html.H5(className='text-center', children='Supported'),
                                    html.Span(className='bar-merger single border-bottom-0'),
                                    html.Div(className='d-flex', children=[
                                        html.Button(
                                            type='button',
                                            className='btn scale-bar bar-14',
                                            children=[
                                                html.Div(children=[
                                                    html.Span(children='Thriving')
                                                ]),
                                                html.Div(children='T')
                                            ]
                                        )
                                    ])
                                    ])
                                ]),
                                html.P(
                                    className='text-theme fw-semibold fst-italic text-center mt-4',
                                    children='Languages are classified and grouped using the global Digital Language Support ("DLS") scale'
                                )
                              ])
                    ]),
            ],
        ),
    ],
)

# Footer -----------------------------------------------------------------------------------------------------------------------------------------------------------
footer = html.Footer(
    className="mt-100",
    children=[
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="d-md-flex justify-content-md-between text-center",
                    children=[
                        html.P(
                            className="mb-0",
                            children="Copyright © 2021–2023. Derivation LLC. All Rights Reserved.",
                        ),
                        html.Div(
                            className="mt-2 mt-md-0",
                            children=[
                                html.A(
                                    className="text-white me-3",
                                    href="https://derivation.co/about-us/",
                                    children="About",
                                ),
                                html.A(
                                    className="text-white",
                                    href="https://derivation.co/contact/",
                                    children="Support",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Page Layout -----------------------------------------------------------------------------------------------------------------------------------------------------------
layout = html.Div([
    # first_row,
    second_Section,
    # third_Section,
    fourth_Section,
    # fifth_Section,
    # sixth_Section,
    seventh_Section,
    footer
])
