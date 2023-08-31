# dotenv
import os

import dash
import dash_bootstrap_components as dbc
import flask
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
from dotenv import load_dotenv
from flask_login import (LoginManager, UserMixin, current_user, login_user,
                         logout_user)
from flask_sqlalchemy import SQLAlchemy
#import psycopg2 #psycopg2-2.9.3
from sqlalchemy import Table, create_engine
#import orjson
#from shapely import wkb
from werkzeug.security import check_password_hash, generate_password_hash

from functions import *
from load_data import *
from pages import (Home,
                   Digital_Language_Support_Academic,
                   Digital_Language_Support_global,
                   Digital_Language_Support_languages,
                   lang_divide,
                #    digital_institutional_matrix,
                   unauthorized_access,
                   unauthorized_access_ac_co)

from flask import jsonify, request, redirect
import stripe


# For local database. Used to run user management database locally
if __name__ == '__main__':
    import warnings
    import sqlite3
    from sqlalchemy.sql import select

import gc

#gc.set_debug(gc.DEBUG_LEAK)
gc.enable()


#from collections import defaultdict
#from gc import get_objects
#before = defaultdict(int)
#after = defaultdict(int)
#for i in get_objects():
#    before[type(i)] += 1 
#bootstrap-table.min.js:10 Uncaught TypeError: Cannot set properties of undefined (setting 'BootstrapTable')

###### DEBUG LOGGER NOT USE ON PROD ######
# import logging

# logger = logging.getLogger(__name__)
# root_logger = logging.getLogger()
# root_logger.setLevel(logging.INFO)
# sh = logging.StreamHandler()
# formatter = logging.Formatter(
#     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# sh.setFormatter(formatter)
# #sh.setFormatter(CsvFormatter())
# root_logger.addHandler(sh)

######

# 1) Set app style ------------------------------------------------------------------------------------------------------------------------------------------------------

FONT_AWESOME_64 = {"rel": "stylesheet",
                   "href": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
                   "integrity": "sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==",
                   "crossorigin": "anonymous",
                   "referrerpolicy": "no-referrer"
                   }

# Stylesheet
bootstrap_table_css = "https://unpkg.com/bootstrap-table@1.20.0/dist/bootstrap-table.min.css"

# Scripts 
# NOTE: jQuery has to be loaded before bootstrap_table_js ( see "Q: Can I use jQuery with Dash?" https://dash.plotly.com/faqs)
# WARNING: jQuery has limited functions with dash
bootstrap_jQuery = { "src": "https://code.jquery.com/jquery-3.6.0.slim.min.js",
                     "integrity": "sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=",
                     "crossorigin":"anonymous"}

bootstrap_bundle = { "src": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js",
                     "integrity": "sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe",
                     "crossorigin":"anonymous"}
# bootstrap_table_js = "https://unpkg.com/bootstrap-table@1.20.0/dist/bootstrap-table.min.js"

# 2) App setup (Flask-Login and stripe) ---------------------------------------------------------------------------------------------------------------------------------

## 2.1) Start flask server
server = flask.Flask(__name__)

# Force HTTPS redirect
if 'DYNO' in os.environ:
    @server.before_request
    def before_request():
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

## 2.2) Create app
app = dash.Dash(__name__, server=server,
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    FONT_AWESOME_64,
                ],
                external_scripts=[
                    'https://www.googletagmanager.com/gtag/js?id=G-XSE8FXPJF4',
                    'https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-MML-AM_CHTML',
                    bootstrap_jQuery,
                    bootstrap_bundle
                ],
                suppress_callback_exceptions=True,
                assets_folder="./assets",
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                ]
                )



## 2.3) Getting env variables 
load_dotenv()

## 2.4) Check if is production or development
# NOTE: This is necessary because the user database uses a free tier for heroku postgres.This tier has only \
#       one credential, is not recommended to share a high level credential of a database.
if __name__ == '__main__':
    # Configuring server for user persistence ( once logged, the users stays logged in even after\
    #  closing the page) and database interaction. 
    # server.config.update(SECRET_KEY=os.urandom(12))
    server.config.update(SECRET_KEY="test")
    server.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite')
    server.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False)

    warnings.filterwarnings("ignore")
    #conn = sqlite3.connect('data.sqlite')
    engine = create_engine('sqlite:///instance/data.sqlite')
    
else:
    # Configuring server for user persistence ( once logged, the users stays logged in even after\
    #  closing the page) and database interaction.     
    server.config.update(SECRET_KEY=os.getenv('SECRET_KEY'))
    server.config.update(SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'))
    server.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False)

    # Create engine and initialize
    engine = create_engine(os.getenv('DATABASE_URL'))

# Set session cookie to be secure.
server.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
## 2.5) Initialize database with app
db = SQLAlchemy()
db.init_app(server)

## 2.6) Create users class for interacting with users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(355), unique=True, nullable = False)
    account_type = db.Column(db.String(20), nullable = False)
    # stripe_id = db.Column(db.String(255), unique=False)
    # account_interval = db.Column(db.String(20), nullable = False)

    
## 2.7) Create User class with UserMixin
class Users(UserMixin, Users):
    pass    

## 2.8) Create table 
Users_tbl = Table('users', Users.metadata)

## 2.9) Flask-Login config

# Setup the LoginManager for the server
# The login manager lets the Dash app do things like load a user from an ID\
#  and validate the user in the login process.
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

## 2.10) Stripe Setup

stripe_keys = {
    "secret_key": os.getenv('STRIPE_SECRET_KEY'),
    "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY"),
    "endpoint_secret" : os.getenv("STRIPE_ENDPOINT_SECRET"),
}


stripe.api_key = stripe_keys["secret_key"]

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = stripe_keys["endpoint_secret"]

@app.server.route('/webhook', methods=['POST'])
def webhook():

    # print(stripe_keys)

    event = None    
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    # print([sig_header])
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    # if event['type'] == 'payment_intent.succeeded':
    if event['type'] == 'customer.subscription.updated':
        payment_intent = event['data']['object']

        # Connect to database
        # print('Connecting to database')
        conn = engine.connect()
        # Create a query
        # print('Creating query')
        # print(payment_intent.customer)
        # print(payment_intent.plan.interval)
        # stmt = Users_tbl.update().where(Users_tbl.c.stripe_id == payment_intent.customer).values(account_interval = payment_intent.plan.interval)
        stmt = Users_tbl.update()#.values(account_interval = payment_intent.plan.interval)
        # Execute the query
        # print('Executing query')
        conn.execute(stmt)
        # Commit
        # print('Commiting')
        conn.commit()
        # Close the connection
        # print('Closing connection')
        conn.close()

        # ... handle payment_intent.succeeded event
    # ... handle other event types
    # else:
        # print('Unhandled event type {}'.format(event['type']))
    
    # Handle delete event
    if event['type'] == 'customer.subscription.deleted':
        payment_intent = event['data']['object']

        # Connect to database
        # print('Connecting to database')
        conn = engine.connect()
        # Create a query
        # print('Creating query')
        # print(payment_intent.customer)
        # print(payment_intent.plan.interval)
        # stmt = Users_tbl.update().where(Users_tbl.c.stripe_id == payment_intent.customer).values(account_interval = None)
        stmt = Users_tbl.update()#.values(account_interval = None)
        # Execute the query
        # print('Executing query')
        conn.execute(stmt)
        # Commit
        # print('Commiting')
        conn.commit()
        # Close the connection
        # print('Closing connection')
        conn.close()



        # print(payment_intent)
        # ... handle payment_intent.succeeded event


    return jsonify(success=True)


# 3) Layouts -----------------------------------------------------------------------------------------------------------------------------------------------------------

## 3.1) Login Layout ---------------------------------------------------------------------------------------------------------------------------------------------------

### 3.1.1) Login creation -------------------------------------------------------------------------------------------------------------------------------------------------

create = html.Div([
        dbc.Row([
                dbc.Col([html.A([
                    html.Img(src="/assets/images/derivation-logo.png")
                ], href="/", className="logo mt-3 d-block"),
                dcc.Loading([
                    html.Div([
                        # Title ------------------------------------------
                        dbc.Row([
                                html.H3('Create User Account'),
                                ],className="mb-2"),
                        dcc.Location(id='create_user', refresh=True),
                        # Username ---------------------------------------
                        dbc.Row([
                                html.Label("Username", className="form-label"),
                                dbc.Input(
                                    id="username",
                                    type="text",
                                    placeholder="user name",
                                    maxLength=15)
                                ],className="mb-2"),
                        # Password ---------------------------------------
                        dbc.Row([
                                html.Label("Password", className="form-label"),
                                dbc.Input(
                                    id="password",
                                    type="password",
                                    placeholder="password"
                                ),
                                ],className="mb-2"),
                        # Email ------------------------------------------
                        dbc.Row([
                                html.Label("E-mail", className="form-label"),
                                dbc.Input(
                                    id="email",
                                    type="email",
                                    placeholder="email",
                                    maxLength=50
                                ),
                                ],className="mb-2"),
                        # Account Type -----------------------------------  
                        dbc.Row([
                                html.Label("Type", className="form-label"),
                                dbc.Select(
                                    options=[
                                        {"label": "Academic", "value": "academic"},
                                        {"label": "Commercial",
                                            "value": "commercial"}
                                    ], id="account_type"),
                                ],className="mb-2"),
                        # Submit Button -----------------------------------
                        dbc.Row([
                                dbc.Button(
                                    'Create User',
                                    id='submit-val',
                                    className="btn btn-theme",
                                    n_clicks=0),
                                ],className="mb-2"),
                        html.Hr(),
                        # Login Button ------------------------------------
                        html.Div(id='container-button-basic')
                    ],id = "create-user-div")

                ],id="loading-1",  type="default")
                    
                ],
                    md=4,
                    className="px-4 px-lg-5 py-5"
                ),
                dbc.Col([
                        html.Img(
                            src="/assets/images/login-right-vector.svg",
                            className="img-fluid log-topRight",
                            alt="login vector"
                        ),
                        html.Img(
                            src="/assets/images/login-left-vector.svg",
                            className="img-fluid log-bottomLeft",
                            alt="login vector"
                        ),
                        html.Div(
                            className="login-container",
                            children=[
                                html.H1(
                                    [
                                        html.Span("Welcome to"),
                                        " Derivation : Intelligence"
                                    ],
                                    style={"font-size": "8vh !important"}
                                )
                            ])
                    ],
                    md=8,
                    className="login-bg"
                )
            ],
            className="align-items-stretch h-100"
        )
    ],
    className="ps-sm-3 auth-page"
)

### 3.1.2) Login login ----------------------------------------------------------------------------------------------------------------------------------------------------

login = html.Div([
        dbc.Row([
                dbc.Col([
                        html.A(href="/", className="logo mt-3 d-block", children=[
                            html.Img(src="/assets/images/derivation-logo.png"),
                        ]),
                        html.Div(
                            className="login-form",
                            children=[
                                html.H5(
                                    "The world’s most advanced Digital Language Divide tool, based upon the most complete digital language support dataset.",
                                    className="fw-normal login-text",
                                    style={"align-text": "justify"}
                                ),
                                html.Form(
                                    className="w-100 mt-2",
                                    children=[
                                        html.Div(
                                            className="mb-4",
                                            children=[
                                                html.Label(
                                                    "Username", className="form-label"),
                                                dcc.Input(
                                                    className="form-control",
                                                    id="uname-box",
                                                    value="",
                                                    type="text",
                                                    placeholder=""
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className="mb-4",
                                            children=[
                                                html.Label(
                                                    "Password", className="form-label"),
                                                dcc.Input(
                                                    className="form-control",
                                                    id="pwd-box",
                                                    value="",
                                                    type="password",
                                                    placeholder=""
                                                )
                                            ]
                                        ),
                                        html.Button(
                                            "Login",
                                            type="button",
                                            id="login-button",
                                            className="btn btn-theme mt-2 d-block"
                                        )
                                    ]
                                ),
                                dcc.Location(id='url_login', refresh=True)
                            ]
                        )
                    ],
                    md=4,
                    className="px-4 px-lg-5 py-5"
                ),
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/images/login-right-vector.svg",
                            className="img-fluid log-topRight",
                            alt="login vector"
                        ),
                        html.Img(
                            src="/assets/images/login-left-vector.svg",
                            className="img-fluid log-bottomLeft",
                            alt="login vector"
                        ),
                        html.Div(
                            className="login-container",
                            children=[
                                html.H1(
                                    [
                                        html.Span("Welcome to"),
                                        " Derivation : Intelligence"
                                    ],
                                    style={"font-size": "8vh !important"}
                                )
                            ]
                        )
                    ],
                    md=8,
                    className="login-bg"
                )
            ],
            className="align-items-stretch h-100"
        )
    ],
    className="ps-sm-3 auth-page"
)

### 3.1.3) Login success --------------------------------------------------------------------------------------------------------------------------------------------------

success = html.Div([dcc.Location(id='url_login_success', refresh=True)
            , html.Div([html.H2('Login successful.')
                    , html.Br()
                    , html.P('Select a Dataset')
                    , dcc.Link('Data', href = '/data')
                ]) #end div
            , html.Div([html.Br()
                    , html.Button(id='back-button', children='Go back', n_clicks=0)
                ]) #end div
        ]) #end div

### 3.1.4) Login failed ----------------------------------------------------------------------------------------------------------------------------------------------------

failed = html.Div([ dcc.Location(id='url_login_df', refresh=True)
            , html.Div([html.H2('Log in Failed. Please try again.')
                    , html.Br()
                    , html.Div([login])
                    , html.Br()
                    , html.Button(id='back-button', children='Go back', n_clicks=0)
                ]) #end div
        ]) #end div

### 3.1.5) Login logout ----------------------------------------------------------------------------------------------------------------------------------------------------

logout = html.Div([dcc.Location(id='logout', refresh=True)
        , html.Br()
        , html.Div(html.H2('You have been logged out - Please login'))
        , html.Br()
        , html.Div([login])
        , html.Button(id='back-button', children='Go back', n_clicks=0)
    ])#end div

## 3.2) Set nav bar -----------------------------------------------------------------------------------------------------------------------------------------------------

### 3.2.1) Content used to display all content. Callbacks fills this.
content = html.Div(id="page-content")

### 3.2.2) Navbar which is updated by User log condition
navbar = html.Div(id="navbar-content")

#### 3.2.2.a) Navbar for unlogged session

navbar_unlogged = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink(html.Img(src="/assets/images/derivation-logo-2.png"), href='/')),
        dbc.NavItem(dbc.NavLink("Home", active=True, href="/",style={"color":"white"})),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Global", href="/dls/global", disabled=True),
                dbc.DropdownMenuItem("Language Comparison", href="/dls/languages", disabled=True),
                dbc.DropdownMenuItem("Digital Language Divide", href="/dls/lang_divide", disabled=True),
            ],
            nav=True,
            in_navbar=True,
            label='Language Support',
        ),        
        dbc.NavItem(dbc.NavLink("Request Access", href="https://forms.gle/ZTNgKdoKnMYumY6y6",style={"color":"white"})),
        # dbc.NavItem(dbc.NavLink("Subscribe", href="/subscribe",style={"color":"white"})),
        dbc.NavItem(dbc.NavLink("Login", href="/login",style={"color":"white"})),
    ],
    brand=html.Img(src="/assets/images/derivation-logo-2.png"),
    brand_href='/',
    # color='rgb(111 97 203)',
    color='transparent',
    dark=True,
)

#### 3.2.2.b) Navbar for logged session
navbar_logged = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink(html.Img(src="/assets/images/derivation-logo-2.png"), href='/')),
        dbc.NavItem(dbc.NavLink("Home", active=True, href="/",style={"color":"white"})),
        dbc.DropdownMenu(
            children=[                
                dbc.DropdownMenuItem("Global", href="/dls/global"),
                dbc.DropdownMenuItem("Language Comparison", href="/dls/languages"),
                dbc.DropdownMenuItem("Digital Language Divide", href="/dls/lang_divide"),
            ],
            nav=True,
            in_navbar=True,
            label='Language Support',
        ),                
        dbc.NavItem(dbc.NavLink("Logout", href="/logout",style={"color":"white"})),
        # dbc.DropdownMenu(
        #     children=[                
        #         dbc.DropdownMenuItem("Manage Account", href=""),
        #         dbc.DropdownMenuItem("Logout", href="/logout"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label='Hello, [User]',
        #     id='user-dropdown',
        #     # label=html.Div([dbc.Row(['Hello,']),
        #     #                 dbc.Row(['[User]'])
        #     #                 ]),
        # ),
    ],
    brand=html.Img(src="/assets/images/derivation-logo-2.png"),
    brand_href='/',
    # color='rgb(111 97 203)',
    color='transparent',
    dark=True,
)


#### 3.2.3) Page footer
page_footer = None
# page_footer = dbc.Nav(
#                 [
#                     dbc.NavLink("About Us", href="https://derivation.co/about-us/"),
#                     dbc.NavLink("Contact", href="https://derivation.co/contact/"),
#                 ], id="page_footer"
#                 )

## 3.3) Navbar + content + page footer Layout ---------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([dcc.Location(id="url"), # returns url of the app
                       navbar,
                       content,
                       page_footer,
                       dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Header")),
                                dbc.ModalBody("Login or Password is incorrect"),
                                # dbc.ModalFooter(
                                #     dbc.Button(
                                #         "Close", id="close_modal_incorrect_login", className="ms-auto", n_clicks=0
                                #     )
                                # ),
                            ],
                            id="modal_incorrect_login",
                            is_open=False,
                        )
                       ])

# 4) Callbacks ----------------------------------------------------------------------------------------------------------------------------------------------------------

## 4.1) Login callbacks ---------------------------------------------------------------------------------------------------------------------------------------------------

### 4.1.1) Insert Users ---------------------------------------------------------------------------------------------------------------------------------------------------

@app.callback(
    [Output('container-button-basic', "children")],
    [Input('submit-val', 'n_clicks')],
    [State('username', 'value'), 
     State('password', 'value'), 
     State('email', 'value'), 
     State('account_type', 'value')
     ])
def insert_users(n_clicks, un, pw, em,tp):
    """
    insert_users(n_clicks, un, pw, em,tp)
    ------------

    This functions create new users for the website. It sends the input to the database.
    The passwords are stored after being hashed, this process is for security reasons.

    Parameters
    ----------
    n_clicks: int
        used to trigger the callback when clicked.
    un: str
        Username with max length of 15. Should be unique.
    pw: str
        password with max length of 120.
    em: str
        email with max of 355 chars. Should be unique.
    tp: str
        specifies the user type max of 20 chars.

    Returns
    -------
    dash.html.*

    """
    if un is not None and pw is not None and em is not None and tp is not None:

        # For local test this check if database exists and create it if not        
        if __name__ == '__main__' and \
            not os.path.isfile('instance/data.sqlite'):
            Users.metadata.create_all(engine)

        # Check if un is already in the database
        # If un exists, return error message

        user = Users.query.filter_by(username=un).first()

        if user is not None:

            return [html.Div([html.H2('Username already exists'), dcc.Link('Click here to Log In', href='/login')])]
                

        # Check if user already exists
        # If user exists, return error message
        # customers = stripe.Customer.search(
        #     query=f"email:'{em}'",
        # )

        # if customers.data:
        #     # return dbc.Alert("User already exists", color="danger")
        #     return [html.Div([html.H2('E-mail already used'), dcc.Link('Click here to Log In', href='/login')])]
        
        # Create stripe user and get stripe id
        # Do I need to check if user already exists?
        # stripe_id = stripe.Customer.create(
        #     email=em,
        # )
        # stripe_id = stripe_id.id    

        
        # # Define user stripe default plan
        # stripe.Subscription.create(
        #     customer=stripe_id,
        #     items=[{"price": "price_1NC1syLFZmZcPB0MGjGz9az5"}] # Default plan
        #     # items=[{"price": "price_1NCAENLFZmZcPB0MwqhhAnod"}] # Default plan
        # )

        hashed_password = generate_password_hash(pw, method='sha256')
        # If local. Tries to insert value on users table in database
        # print([un, hashed_password, em,tp,stripe_id])
        if __name__ == '__main__':
            # Try to insert values in user table if fail, creates user table
            if os.path.isfile('instance/data.sqlite'):
                # print(1)
                ins = Users_tbl.insert().values(username=un,  password=hashed_password,
                                                # email=em, account_type=tp, stripe_id=stripe_id,
                                                email=em, account_type=tp)#,
                                                # account_interval='deactivated')

            else:
                # print(2)
                Users.metadata.create_all(engine)
                # Users_tbl.metadata.create_all(engine)
                # ins = Users_tbl.insert().values(username=un,  password=hashed_password, email=em,account_type=tp,stripe_id=stripe_id)
                ins = Users_tbl.insert().values(username=un,  password=hashed_password, email=em,account_type=tp)

        else:
            # ins = Users_tbl.insert().values(username=un, password=hashed_password, email=em,account_type=tp,stripe_id=stripe_id)
            ins = Users_tbl.insert().values(username=un, password=hashed_password, email=em,account_type=tp)
        
        # print(ins)
        conn = engine.connect()
        conn.execute(ins)
        conn.commit()
        conn.close()

        # print(request.host_url)

        # session = stripe.billing_portal.Session.create(
        #     customer=stripe_id,
        #     return_url=request.host_url,
        # )


        # return [login]
        # return [html.A('Go to Billing Portal', id='billing-portal-link', href=session.url)]
        return [
            html.Div([
                dbc.Row([
                    html.H2('Thank you for signing up!'),
                ]),
                # dbc.Row([
                #     html.A('Go to Billing Portal to finish subscription',
                #            id='billing-portal-link', href=session.url)
                # ])
            ])
            
            ]
    else:
        return [html.Div([html.H2('Already have a user account?'), dcc.Link('Click here to Log In', href='/login')])]

### 4.1.2) Success login --------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output('url_login', 'pathname'),
    Output('modal_incorrect_login', 'is_open')],
    [Input('login-button', 'n_clicks')],
    [State('uname-box', 'value'), State('pwd-box', 'value')],
    prevent_initial_call = True)
def successful(n_clicks, input1, input2):
    """
    successful(n_clicks, input1, input2)
    ------------------------------------

    Callback function to check username and password entered by the user.
    If both are correct, log in the user and redirect to the DLS page.
    If either the username or password is incorrect, show a modal with an error message.

    Parameters
    ----------
    n_clicks : int
        The number of times the login button has been clicked.
    input1 : str
        The username entered by the user.
    input2 : str
        The password entered by the user.

    Returns
    -------
    Tuple
        A tuple containing two elements:
        - A string that represents the URL of the DLS page if the username and password are correct,
          otherwise None.
        - A boolean that represents whether the modal with the error message should be open or not.
    """
    if n_clicks == None:
        return None, False

    # response = app.response_class()
    
    user = Users.query.filter_by(username=input1).first()
    #user = session.query(Users).filter_by(username=input1).first()
    # print(user.account_interval)
    # print(user.account_interval in ['month','year'])

    # if user and (user.account_interval in ['month','year']):
    if user :
        if check_password_hash(user.password, input2):
            
            flask.session["login_attempts"] = 0
            login_user(user)
            #logger.info(flask.session["login_attempts"])
            return '/dls/global', False
        else:

            flask.session['login_attempts'] = flask.session.get('login_attempts', 0) + 1
            # logger.info(flask.session["login_attempts"])
            return None, True
    else:
        flask.session['login_attempts'] = flask.session.get('login_attempts', 0) + 1
        # logger.info(dir(flask.session))
        # logger.info(flask.session.keys())
        # logger.info(flask.session["login_attempts"])
        return None, True

### 4.1.3) Update output --------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output('output-state', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('uname-box', 'value'), State('pwd-box', 'value')],
    prevent_initial_call = True)
def update_output(n_clicks, input1, input2):
    """
    update_output(n_clicks, input1, input2)
    ---------------------------------------

    Checks username and password on the database.
    If not pass 'Incorrect username or password' message
    
    Parameters
    ----------
    n_clicks: int
        used to trigger the callback when clicked.        
    input1: str
        Username to be checked
    input2:
        Password to be checked

    Returns
    -------
    string
        path for the url
    """
    if n_clicks > 0:
        user = Users.query.filter_by(username=input1).first()
        #user = session.query(Users).filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''

### 4.1.4) callback to reload the user object -------------------------------------------------------------------------------------------------------------------------------

# A callback to the login_manager is needed to complete the \
# login processes. This callback will go with the rest of the Dash Callbacks.
@login_manager.user_loader
def load_user(user_id):
    #return Users.query.get(int(user_id))
    return Users.query.get(int(user_id))


# @app.callback(dash.dependencies.Output('label1', 'children'),
#     [dash.dependencies.Input('interval1', 'n_intervals')])
# def update_interval(n):
#     logger.info(request.headers)
#     return 'Intervals Passed: ' + str(n)


## 4.2) redering pages content ---------------------------------------------------------------------------------------------------------------------------------------------

@app.callback(Output("page-content", "children"),
              Output("navbar-content", "children"),
             [Input("url", "pathname")])
def render_page_content(pathname):
    """
    render_page_content(pathname)
    -----------------------------

    Callback function to render page content and navbar based on the URL pathname.
    
    Parameters
    ----------
    pathname : str
        The URL pathname.

    Returns
    -------
    tuple
        A tuple containing two Dash HTML objects: the first is the content displayed in the main container,
        and the second is the navbar. This callback also checks whether the user is logged in, and displays
        the appropriate navbar based on their authentication status.

    Notes
    -----
    This callback function currently supports the following URL paths:
    
    - `/` or `/home`: Home page. Displays different content and navbar depending on whether the user is logged in.
    - `/subscribe`: Subscription page. Only accessible to Admin users.
    - `/login`: Login page.
    - `/success`: Login success page. Displays different content and navbar depending on whether the user is logged in.
    - `/dls/global`: Digital Language Support (DLS) global page. Displays different content and navbar depending on the user's account type.
    - `/dls/languages`: DLS languages page. Only accessible to Commercial and Admin users.
    - `/dls/matrix`: DLS matrix page. Only accessible to Commercial and Admin users.
    - `/logout`: Logout page.
    
    If the URL pathname does not match any of the above paths, a 404 page is displayed.
    """
    
    #logger.info(current_user.account_type)
    # logger.info(request.headers)
    ## Home page template -----------------------------------------------------------------------------------------------------------------------------------------------
    if pathname == "/": #or pathname =='/home':
        if current_user.is_authenticated:
            return Home.layout, \
                        html.Div([navbar_logged,Home.first_row],className="hero-sec")
            # return Digital_Language_Support_global.layout, navbar_logged
        else:
            return Home.layout, \
                        html.Div([navbar_unlogged,Home.first_row],className="hero-sec")
            # return login, None 

    ## Subscription page ------------------------------------------------------------------------------------------------------------------------------------------------
    elif pathname == '/subscribe':
        #  if current_user.is_authenticated:
        #     if current_user.account_type == "Admin":
                return create, None 
        #return create, navbar_unlogged

    ## Login page -------------------------------------------------------------------------------------------------------------------------------------------------------
    elif pathname == '/login':
        return login, None 

    ## Login Success page -----------------------------------------------------------------------------------------------------------------------------------------------
    elif pathname == '/success':
        if current_user.is_authenticated:
            return success, navbar_logged
        else:
            return failed, navbar_unlogged

    ## DLS global page -----------------------------------------------------------------------------------------------------------------------------------------------
    elif pathname =='/dls/global':
        if current_user.is_authenticated:
            # if (current_user.account_type == "commercial" or current_user.account_type == "Admin") and \
            #     (current_user.account_interval in ["month","year"]):
            if (current_user.account_type == "commercial" or current_user.account_type == "Admin"):
                return Digital_Language_Support_global.layout, \
                        html.Div([navbar_logged,Digital_Language_Support_global.first_row],className="hero-sec-inner")
            # elif current_user.account_type == "Academic" and \
            #     (current_user.account_interval in ["month","year"]):
            elif current_user.account_type == "Academic":
                return Digital_Language_Support_Academic.layout, navbar_logged
        else:
            return unauthorized_access_ac_co.layout, navbar_unlogged
    ## DLS Language page -----------------------------------------------------------------------------------------------------------------------------------------------
    elif pathname =='/dls/languages':
        if current_user.is_authenticated :
            # if current_user.account_type == "commercial" or current_user.account_type == "Admin" and \
            #     (current_user.account_interval in ["month","year"]):
            if current_user.account_type == "commercial" or current_user.account_type == "Admin":
                return Digital_Language_Support_languages.layout, \
                        html.Div([navbar_logged,Digital_Language_Support_languages.dls_CountryRank],className="hero-sec-inner")
            else:
                return unauthorized_access.layout, navbar_logged
        else:
            return unauthorized_access.layout, navbar_unlogged    
    ## DLS matrix page -----------------------------------------------------------------------------------------------------------------------------------------------
    elif pathname =='/dls/lang_divide':
        if current_user.is_authenticated:
            # if current_user.account_type == "commercial" or current_user.account_type == "Admin" and \
            #     (current_user.account_interval in ["month","year"]):
            if current_user.account_type == "commercial" or current_user.account_type == "Admin":
                # return lang_divide.layout, navbar_logged
                return lang_divide.footer, html.Div([navbar_logged,lang_divide.matrix_layout],className="hero-sec-inner")
            else:
                return unauthorized_access.layout, navbar_logged
        else:
            return unauthorized_access.layout, navbar_unlogged    

    ## Logout page -----------------------------------------------------------------------------------------------------------------------------------------------------
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return Home.layout, \
                        html.Div([navbar_unlogged,Home.first_row],className="hero-sec")
        else:
            return Home.layout, \
                        html.Div([navbar_unlogged,Home.first_row],className="hero-sec")

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# 5) Set debug mode -----------------------------------------------------------------------------------------------------------------------------------------------------
#logger.info("This is the __name__" + __name__)
if __name__ == '__main__':
    app.run_server(debug=True)
