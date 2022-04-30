from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask_login import logout_user, current_user


#main app
from app import app
from views import success, login, login_fd, logout
### connect to pages
from views.viz import live_temp, orbit

use_port = 8080

content_div = dbc.Container(children=[
    dbc.Row(
        html.Div(id='page-content', children=[])
            , justify='center' # Horizontal:start,center,end,between,around
        )],
fluid=True
)

# make a navitem 
nav_item = dbc.Container(children=[
    dbc.NavItem(dbc.NavLink("Home", href="http://10.1.5.93:{port}/".format(port=use_port), class_name="text-white", external_link=True)),
    # dbc.NavItem(dbc.NavLink(id='logout', className='ms-2', children=[]))
         ])   
# make a dropdown
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Live Feed", href='/views/viz/live_temp', external_link=False),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Orbit", href="/views/viz/orbit", external_link=False),
        # dbc.DropdownMenuItem(divider=True),
        # dbc.DropdownMenuItem("Sales Overview", href="/views/viz/sales_overview", external_link=False),
        # dbc.DropdownMenuItem(divider=True),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
    toggle_class_name="text-white"
)



logo_navbar = dbc.Navbar(
    dbc.Container(
        [# external Links
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(children=[   
                        dbc.Col(html.Img(src='/assets/Lipseys_[L]_RGB_Dark.png', height="55px")),
                        ],
                    align="center",
                    class_name="g-0",
                ),
                href="https://www.lipseys.com/",
                style={"textDecoration": "none"},
            ),
         dbc.Col(children=[dbc.NavbarBrand("Year Review", class_name="ms-2"),
                 # html.Div(id='user-name', className='ms-2', children=[]),
                 # html.Div(id='logout', className='ms-2', children=[])
                 ], 
                 class_name="text-white"),
        dbc.Nav(nav_item),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
                    dbc.Nav(
                            [dropdown],
                            class_name="text-white ms-auto",
                            navbar=True,
                            ),
                    id="navbar-collapse",
                    navbar=True,
                    class_name="text-white"
                    ),
        ],
    ),
    color="dark",
    dark=True,
    class_name="mb-5",
)

app.layout = html.Div(children=[dcc.Location(id='url', refresh=False), logo_navbar, content_div])


# Optional new in dash 1.12 to avoid call back exceptions associated with multipage apps dash.plotly.com/urls
# "complete" layout
app.validation_layout = html.Div([
    logo_navbar,
    content_div,
    login.layout,
    success.layout,
    login_fd.layout,
    logout.layout,
    live_temp.layout,
    orbit.layout,
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    ### Check user roles; place users roles into list
    if current_user.is_authenticated:
        user_roles = [role.name for role in current_user.roles]
    ### Roles Required to see Restricted Admin Pages
    dash_roles = ['Admin']
    #### Utiltiy Pages
    if pathname == '/':
        ##TODO: return login prompt only for anon users
        ##TODO: return a 'home page' for logged in users insead of login
        return login.layout
    elif pathname == '/views/login':
        return login.layout
    ####### testing only #######
    # elif pathname == '/views/login_fd':
    #     return login_fd.layout
    ##################################
    elif pathname == '/views/success':
        if current_user.is_authenticated:
            return success.layout
        else:
            return login_fd.layout
    elif pathname == '/views/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout  
        
    #### User Acccess Pages
    elif pathname == '/views/viz/live_temp':
        if current_user.is_authenticated:
            # if any(x in dash_roles for x in user_roles):
                return live_temp.layout
            # else:
                # return 'Access Denied'
        else:
            return login_fd.layout
    elif pathname == '/views/viz/orbit':
        if current_user.is_authenticated:
            # if any(x in dash_roles for x in user_roles):
                return orbit.layout
            # else:
                # return 'Access Denied'
        else:
            return login_fd.layout
    else:
        return "404 Page Error! Please choose a link"

@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.Div('Current user: ' + current_user.username)
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/views/logout', className="text-white")
    else:
        return ''
    
#callback to toggle the collapse on small screens
@app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

server = app.server
    
# if __name__ == '__main__':
#     app.run_server(debug=True, host='0.0.0.0', port=use_port, dev_tools_hot_reload=False)