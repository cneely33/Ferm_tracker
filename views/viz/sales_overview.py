################################################################################################
################################################################################################
################################################################################################
#
# Visual and Layout Example
# pulled from year in review
#
################################################################################################
################################################################################################
################################################################################################

from dash import dcc, html
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly import colors
import pandas as pd
from datetime import datetime as dt

from app import app, no_data_fig, high_card_color_template
from data.dash_data import df_2
import functions
########## Load Data ###########

## create callback id prefex generator
id_gen = functions.id_factory('sales')

### Load color scale for heat map
scale = colors.sequential.Reds

### Dates ###
current_year = df_2['inv_posted_date_actual'].max().year
max_dt = df_2['inv_posted_date_actual'].max()
# min_dt = datetime.datetime.now().date()
min_dt = df_2['inv_posted_date_actual'].min()

max_dt_start = max_dt
## manually set min date #temp
# import datetime
# min_dt_start = (max_dt - datetime.timedelta(14))
min_dt_start = min_dt

initial_visible_month = dt(current_year,min_dt_start.month, 1)

## Graph properties
margins=dict(t=20, l=0, r=0, b=10)
allocation_types = ['PER REP', 'PER DEALER', 'ALLOCATED', 'UN-ALLOCATED']

##### static values for callbacks and labels ######
## for manufacturer sales proportion by state
manufacturer_series = sorted(df_2['manufacturer_name'].unique())
product_cat_series = sorted(df_2['product_category_name'].unique())
regions_series = sorted(df_2['region'].unique())
## for sales and freight by region labels
list_states_east = ['AL', 'AR', 'CT', 'DE', 'FL', 'GA', 'IA', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MO', 'MS', 'NC', 'NH', 'NJ', 'NY', 'OH', 'OK', 'PA', 'RI', 'SC', 'TN', 'TX', 'VA', 'VT', 'WI', 'WV']
list_states_west = ['AZ', 'CA', 'CO', 'DC', 'ID', 'MN', 'MT', 'ND', 'NE', 'NM', 'NV', 'OR', 'SD', 'UT', 'VI', 'WA', 'WY']

######################## Create Filter Controls ########################
######################## Global Controls
controls = dbc.Row([
    dbc.Col([
            html.Div([
                    html.H5(
                        children='Select Date Range:',
                        style = {'text-align' : 'left',
                                  }
                        ),
                    # Date Picker
                    dbc.Row([
                            dcc.DatePickerRange(
                                    id=id_gen('date_picker'),
                                  # with_portal=True,
                                  min_date_allowed=min_dt,
                                  max_date_allowed=max_dt,
                                  initial_visible_month=initial_visible_month,
                                  start_date=min_dt_start,
                                  end_date=max_dt_start,
                                  className='center'),
                             
                            ], style={'marginTop': 30, 'marginBottom': 15}),
                    dbc.Label("Allocation Type", html_for="allocation_type"),
                             html.Br(),
                             dcc.Checklist(
                                    id=id_gen('allocation_type'),
                                    options=[{'label': 'All', 'value': 'All'}] + 
                                     [{'label': k, 'value': k} for k in sorted(allocation_types)],
                                    value=['All'],
                                    labelStyle={'display': 'inline-block'},
                                    inputStyle={"margin-left": "10px", "margin-right": "5px"},
                                                ),
                             html.Br(),
                    dbc.Button(id=id_gen('submit_button_sales_1'), n_clicks=0, color="warning", children='Submit'),
                    ],style = {'margin-top' : '30',
                            'margin-bottom' : '15',
                            'text-align' : 'left',
                            'paddingLeft': 5})
          
        ],width = 3, align='center'),

                               
########################
    dbc.Col(
        [
            ## control for warehouse
            dbc.Label("Warehouse", html_for="wh_radio", width='auto'),
            html.Br(), 
            dcc.RadioItems(
            id=id_gen('wh_radio'),
            options=[{'label': 'All', 'value': 'All'}] + 
                [{'label': "BR Only", "value": 'BR'},
                {'label': "RP Only", "value": 'RP'}],
            value='All',
            style={'display': 'inline-block'},
            inputStyle={"margin-left": "10px", "margin-right": "5px"}
                        ),
            html.Br(),            
            
            dbc.Label("Product Categories", html_for="product_cat_groups_dd", width='auto'),
            dcc.Dropdown(id = id_gen('product_cat_groups_dd'),
                value = [''],
                multi = True,
                placeholder = "Select Product Category (leave blank to include all)",
                style = {'font-size': '13px', 
                         # 'color' : corporate_colors['medium-blue-grey'],
                         'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                ),

            # html.Br(),
            dbc.Label("Manufacturer", html_for="manufacturer_groups_dd", width='auto'),
            dcc.Dropdown(id = id_gen('manufacturer_groups_dd'),
                value = [''],
                multi = True,
                placeholder = "Select Manufacturer" + " (leave blank to include all)",
                style = {'font-size': '13px', 
                         # 'color' : corporate_colors['medium-blue-grey'], 
                         'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                )
  
        
        
        ], width=4, align='center', style = {'fontSize': 'large'}
        ),
########################
    dbc.Col([
        dbc.Label("OnlineOrders", html_for="onlineOrder_radio", width=2),
        html.Br(), 
        dcc.RadioItems(
        id=id_gen('onlineOrder_radio'),
        options=[{'label': 'All', 'value': 'All'}] + 
            [{'label': "OnlyOnlineOrders", "value": 1},
              {'label': "OnlyManualOrders", "value": 0}],
        value='All',
        style={'display': 'inline-block'},
        inputStyle={"margin-left": "10px", "margin-right": "5px"}
                    ),
        
        html.Br(),
        dbc.Label("SLM Teams", html_for="slm_team_lead_dropdown", width='auto'),
        dcc.Dropdown(
        id=id_gen('slm_team_lead_dropdown'),
        value = ['073', '152', '166'],
        multi = True,
        placeholder="Select Sales Team Lead(s)",
         style = {'font-size': '13px', 
                      'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                ),
          
        dbc.Label("SLM", html_for="slm_dropdown", width='auto'),
        dcc.Dropdown(id=id_gen('slm_dropdown'),
            value = [''],
            multi = True,
            placeholder = "Select Sales Exec(s)",
            style = {'font-size': '13px', 
                      'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                ),
            
        ], width=3, align='center', style = {'fontSize': 'large'}
        )
],justify='center', align='center',)



######################## End Controls ########################


layout = html.Div([
    dbc.Row([
            dbc.Col(html.H1("Sales Overview",
                            className='text-center text-primary mb-4'),
                    width=12)
                ],),
            dbc.Row(children=[controls], align='center', justify='center'),
            html.Br(),
############################################################################            
    dbc.Row([
        ### Placeholder for global summary stats
            dbc.Card([], color="dark", outline=True),
            ], align='center', justify='center'),
            html.Br(),
            html.Br(),
############################################################################              
    
    dbc.Container([
        dbc.Row([
        dbc.Col(html.H1("2021 Sales by SLM",
                        className='text-center text-primary mb-4'),
                width=12)
            ]),
        dbc.Row([
            dbc.Col([
                 dcc.Graph(id=id_gen('sales_allocations_%_bar_graph'), figure={},
                            style={"height": "95%"},
                           config = {'displayModeBar': False})
                ## Placeholder for summary stats
                ], width=3, class_name='h-100'), 
            dbc.Col([
                dcc.Graph(id=id_gen('sales_bar_graph'), figure={},
                           style={"height": "95%"}
                          )
                    ], width=5, class_name='h-100'),
            dbc.Col([
                dbc.Card([
                    html.Br(),
                    html.H3("Sales by Allocation Type Overview:", style={"text-align": "center"}),
                    html.P('New EDW feature in 2021: tracking Allocations based on Per Dealer and Per Rep.', style={"text-align": "center"}),
                    html.P('Prior to implementation, Allocation history was simply tracked as Allocated and Unallocated.', style={"text-align": "center"}),
                    html.Br(),
                    html.P('Left side splits each Sales Executive’s Total Sales into proportions based on Allocation Type.'
                           , style={"text-align": "center"}),
                    html.Br(),
                    html.P('Right side groups sales executives based on their teams and orders them in ascending order based on Total \
                           Sales Dollars. Bar color represent the Total Sales in Dollars for each Allocation Type.', style={"text-align": "center"}),
                    html.Br(),
                    ], color="dark", outline=True),
                ], width=4, align='center'),
            ], align='center', class_name='h-100'),
    ], fluid=True, style={"height": "100vh"}),
############################################################################     
     
    dbc.Container([
        dbc.Row([
        dbc.Col(html.H1("2021 Sales Trend",
                        className='text-center text-primary mb-4'), width=12)
            ]),
        dbc.Row([
            dbc.Col([
                    dbc.Card([ html.Br(), html.Br(),
                            html.H3("Sales Trend Overview:", style={"text-align": "center"}),
                            html.P('The two columns on the left show the sales trend within the months of 2021. The left column \
                                   contains Total Sales for each Day of the Month. The right column adjusts Total Sales for the \
                                       frequency that each day occurred in 2021.', style={"text-align": "center"}),
                            html.Br(),
                            html.P('Sales were strongest at the start and end of each month. This trend is more  \
                                   apparent after adjusting for the frequency of days', style={"text-align": "center"}),
                            html.P('-------------', style={"text-align": "center"}),
                            html.P('The heat map in the middle shows the overall sales trend for 2021 by Day of the Week \
                                   and Week of the Year. The line graph to the right shows 2021 cumulative sales by Product \
                                       Category Groups. ', style={"text-align": "center"}),
                            html.Br(),
                            html.P('Handgun sales picked back up after the ice storm between weeks 9 and 14 (MarchMadness)\
                                   Then exploded again between weeks 25 and 28 (6/21 - 7/15)', style={"text-align": "center"}),
                            html.Br(),
                            ], color="dark", outline=True),
                ], width=3, align='center'),
            dbc.Col([
                html.H5("Sales by Day of Month", style={"text-align": "center"}),
                dbc.Row([
                        dcc.Graph(id=id_gen('sales_heatmap_graph_month_day'), figure={}, config = {'displayModeBar': False},
                           style={"height": "98%",
                                   "width": "50%"
                                  }),
                         dcc.Graph(id=id_gen('sales_heatmap_graph_month_day_adjusted'), figure={}, config = {'displayModeBar': False},
                           style={"height": "98%",
                                   "width": "50%"
                                  })
                         ], align='top',
                    class_name='h-100'
                    )
                    ], width=2, class_name='h-100'),
            dbc.Col([
                html.H5("Sales by Week of Year", style={"text-align": "center"}),
                dcc.Graph(id=id_gen('sales_weekly_heatmap'), figure={}, style={"height": "98%"}, config = {'displayModeBar': False})
                    ], width=2, class_name='h-100'),
            dbc.Col([
                    html.H5("Cumlative Sales by Product Category Groups", style={"text-align": "center"}),
                    dcc.Graph(id=id_gen('sales_cumlative_sum_high'), figure={},
                                style={"height": "92%"}),
                    ], width=5, class_name='h-100'),
            
            ], align='top', class_name='h-100')
        ], fluid=True, style={"height": "100vh"}),
    html.Br(),html.Br(),

############################################################################
    html.Br(),      
    dbc.Row([
        ### Placeholder for global summary stats
            dbc.Card([], color="dark", outline=True),
            ], align='center', justify='center'),
            html.Br(),
##############################################################################################################################################    
    dbc.Container([
        dbc.Row([
                 dbc.Card([
                        html.Br(),
                        html.H3("Manufacturer Sales Percent By Sales Executive:", className="card-title", style={"text-align": "center"}),
                        html.P('Click the Submit Button to load graph', style={"text-align": "center"}),
                        html.Br(),
                        dcc.Checklist(id=id_gen('remove_top_man_slm'),
                               options=[{'label': 'Remove Manufacturers in Top 8 Total Sales', 'value': 'Y'}],
                               labelClassName="mr-2",
                               value=['Y'],
                               style={'display': 'inline-block', "text-align": 'center'},
                               inputStyle={"margin-left": "10px", "margin-right": "5px"}
                           ),
                        html.Div(id=id_gen("removed_top_manufacturers_slm"), style={"text-align": "center"}),
                        html.Br(),
                        dcc.Checklist(id=id_gen('remove_bottom_man_slm'),
                               options=[{'label': 'Remove Manufacturers in Bottom 15 Total Sales', 'value': 'Y'}],
                               labelClassName="mr-2",
                               value=['Y'],
                               style={'display': 'inline-block', "text-align": 'center'},
                               inputStyle={"margin-left": "10px", "margin-right": "5px"}
                           ),
                        html.Div(id=id_gen("removed_bottom_manufacturers_slm"), style={"text-align": "center"}),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                             dcc.Dropdown(id = id_gen('product_cat_groups_dd_propor_slm'),
                                value = [''],
                                options = [{'label': 'All', 'value': 'All'}] + \
                                            [{'label': k, 'value': k} for k in product_cat_series],
                                multi = True,
                                placeholder = "Select Product Category (leave blank to include all)",
                                style = {'font-size': '13px', 
                                         # 'color' : corporate_colors['medium-blue-grey'],
                                         'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                ),
                            html.Br(),
                            dcc.Dropdown(id = id_gen('manufacturer_groups_dd_propor_slm'),
                                value = [''],
                                options = [{'label': 'All', 'value': 'All'}] + \
                                            [{'label': k, 'value': k} for k in manufacturer_series],
                                multi = True,
                                placeholder = "Select Manufacturer" + " (leave blank to include all)",
                                style = {'font-size': '13px', 
                                         # 'color' : corporate_colors['medium-blue-grey'], 
                                         'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                ),
                                ], width=6),
                            dbc.Col([
                            dbc.Label("Select Region(s):", style={"text-align": 'center'}),
                            dcc.Checklist(id=id_gen('region_checklist_slm'),
                                   options=[{'label': 'All', 'value': 'All'}] + \
                                            [{'label': k, 'value': k} for k in regions_series],
                                   labelClassName="mr-2",
                                   value=['All'],
                                   style={'display': 'inline-block', "text-align": 'center'},
                                   inputStyle={"margin-left": "10px", "margin-right": "5px"}
                               ),
                            html.Br(),
                            dbc.Button(id=id_gen('submit_button_sales_2'), n_clicks=0, color="warning", children='Submit'),
                            ], width=6),
                            ]),
                        html.Br(),
                        ], color="dark", outline=True),
                     
                         dbc.Row([html.Br(),]),
                    ], align='center', class_name='h-100'),
            ], fluid=True, style={"height": "40vh"}),
    dbc.Container([
        dbc.Row([
                 dbc.Col([
                      dcc.Graph(id=id_gen('manufacturer_sales_percent_by_slm_bar'), figure=no_data_fig,
                                style={"height": "100%"}, config = {'displayModeBar': False}),
                    ],align='center', width=12, class_name='center h-100'),
                ], align='center', class_name='h-100'),
        ], fluid=True, style={"height": "100vh"}),
           
##############################################################################################################################################    
    dbc.Container([
        dbc.Row([
                 dbc.Card([
                        html.Br(),
                        html.H3("Manufacturer Sales Percent By State:", className="card-title", style={"text-align": "center"}),
                        html.P('Click the Submit Button to load graph', style={"text-align": "center"}),
                        html.Br(),
                        dcc.Checklist(id=id_gen('remove_top_man_state'),
                               options=[{'label': 'Remove Manufacturers in Top 8 Total Sales', 'value': 'Y'}],
                               labelClassName="mr-2",
                               value=['Y'],
                               style={'display': 'inline-block', "text-align": 'center'},
                               inputStyle={"margin-left": "10px", "margin-right": "5px"}
                           ),
                        html.Div(id=id_gen("removed_top_manufacturers_state"), style={"text-align": "center"}),
                        html.Br(),
                        dcc.Checklist(id=id_gen('remove_bottom_man_state'),
                               options=[{'label': 'Remove Manufacturers in Bottom 15 Total Sales', 'value': 'Y'}],
                               labelClassName="mr-2",
                               value=['Y'],
                               style={'display': 'inline-block', "text-align": 'center'},
                               inputStyle={"margin-left": "10px", "margin-right": "5px"}
                           ),
                        html.Div(id=id_gen("removed_bottom_manufacturers_state"), style={"text-align": "center"}),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                             dcc.Dropdown(id = id_gen('product_cat_groups_dd_propor_state'),
                                value = [''],
                                options = [{'label': 'All', 'value': 'All'}] + \
                                            [{'label': k, 'value': k} for k in product_cat_series],
                                multi = True,
                                placeholder = "Select Product Category (leave blank to include all)",
                                style = {'font-size': '13px', 
                                         # 'color' : corporate_colors['medium-blue-grey'],
                                         'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                ),
                            html.Br(),
                            dcc.Dropdown(id = id_gen('manufacturer_groups_dd_propor_state'),
                                value = [''],
                                options = [{'label': 'All', 'value': 'All'}] + \
                                            [{'label': k, 'value': k} for k in manufacturer_series],
                                multi = True,
                                placeholder = "Select Manufacturer" + " (leave blank to include all)",
                                style = {'font-size': '13px', 
                                         # 'color' : corporate_colors['medium-blue-grey'], 
                                         'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                ),
                                ], width=6),
                            dbc.Col([
                            dbc.Label("Select Region(s):", style={"text-align": 'center'}),
                            dcc.Checklist(id=id_gen('region_checklist_state'),
                                   options=[{'label': 'All', 'value': 'All'}] + \
                                            [{'label': k, 'value': k} for k in regions_series],
                                   labelClassName="mr-2",
                                   value=['All'],
                                   style={'display': 'inline-block', "text-align": 'center'},
                                   inputStyle={"margin-left": "10px", "margin-right": "5px"}
                               ),
                            html.Br(),
                            dbc.Button(id=id_gen('submit_button_sales_3'), n_clicks=0, color="warning", children='Submit'),
                            ], width=6),
                            ]),
                        html.Br(),
                        ], color="dark", outline=True),
                     
                         dbc.Row([html.Br(),]),
                    ], align='center', class_name='h-100'),
            ], fluid=True, style={"height": "40vh"}),
    dbc.Container([
        dbc.Row([
                 dbc.Col([
                      dcc.Graph(id=id_gen('manufacturer_sales_percent_by_state_bar'), figure=no_data_fig,
                                style={"height": "100%"}, config = {'displayModeBar': False}),
                    ],align='center', width=12, class_name='center h-100'),
                ], align='center', class_name='h-100'),
        ], fluid=True, style={"height": "100vh"}),
############################################################################     
    ])



######################## Callbacks ######################## 
    
##### create chained callback for slm number ######
#### Nested Drop Down Callback
@app.callback(
    Output(id_gen('slm_team_lead_dropdown'), 'options'),
    Output(id_gen('slm_dropdown'), 'options'),
    [Input(id_gen('slm_team_lead_dropdown'), 'value'),
     Input(id_gen('slm_dropdown'), 'value')])
def update_dropdown_options_slm(l1_dropdown_value, l2_dropdown_value):
    ## inital callback value [''] ; after removal of elements from dropdown, value becomes []
    
    # option to pull string representation of which dcc was triggered
    # ctx = callback_context
    # input_id = ctx.triggered[0]["prop_id"].split(".")[0]
   
    ### enter column names that contain filter categories ###
    column_name_1 = 'slm_team_lead'
    column_name_2 = 'slm_no'
    df = df_2
    #determine if 'All' items have been selected
    if l1_dropdown_value == []:
        isselect_all_l1 = 'Y'
    else:
        for i in l1_dropdown_value:
            if i == 'All' or i == '':
                isselect_all_l1 = 'Y'
                break
            else:
                isselect_all_l1 = 'N'
            
    ## Same for L2 selection
    if l2_dropdown_value == []:
        isselect_all_l2 = 'Y'
    else:
        for i in l2_dropdown_value:
            if i == 'All' or i == '':
                isselect_all_l2 = 'Y'
                break
            else:
                isselect_all_l2 = 'N'   
                
    ## create default unique list of values for callback options
    input_1_list = df[column_name_1].unique()
    input_2_list = df[column_name_2].unique()
    
    # If not all items are desired...
    if isselect_all_l1 == 'N':
        ## pull series of values for rows that match fitler criteria
        bool_filter_series = df[column_name_1].isin(l1_dropdown_value)
        ## use bool series to pull filtered list of unique values for call back 2
        input_2_list = df[column_name_2][bool_filter_series].unique()
        
    # If not all items are desired...
    if isselect_all_l2 == 'N':
        ## pull series of values for rows that match fitler criteria
        bool_filter_series = df[column_name_2].isin(l2_dropdown_value)
        ## use bool series to pull filtered list of unique values for call back 1
        input_1_list = df[column_name_1][bool_filter_series].unique()
    
    
    ### Set Callback options ###
    ### Options for Dropdown 1
    drop_down_1_options = [{'label': 'All', 'value': 'All'}] + \
                                    [{'label': str(k), 'value': str(k)} for k in sorted(input_1_list)]
    
    ### Options for Dropdown 2
    drop_down_2_options = [{'label': 'All', 'value': 'All'}] + \
                                    [{'label': str(k), 'value': str(k)} for k in sorted(input_2_list)]
        
    return drop_down_1_options, drop_down_2_options
  
##### create chained callback for Manufacturer and Product Cats ######
#### Nested Drop Down Callback
@app.callback(
    Output(id_gen('product_cat_groups_dd'), 'options'),
    Output(id_gen('manufacturer_groups_dd'), 'options'),
    [Input(id_gen('product_cat_groups_dd'), 'value'),
     Input(id_gen('manufacturer_groups_dd'), 'value')])
def update_dropdown_options_manufacturer(l1_dropdown_value, l2_dropdown_value):
    ## inital callback value [''] ; after removal of elements from dropdown, value becomes []
    
    # option to pull string representation of which dcc was triggered
    # ctx = callback_context
    # input_id = ctx.triggered[0]["prop_id"].split(".")[0]
   
    ### enter column names that contain filter categories ###
    column_name_1 = 'product_category_name'
    column_name_2 = 'manufacturer_name'
    df = df_2
    #determine if 'All' items have been selected
    if l1_dropdown_value == []:
        isselect_all_l1 = 'Y'
    else:
        for i in l1_dropdown_value:
            if i == 'All' or i == '':
                isselect_all_l1 = 'Y'
                break
            else:
                isselect_all_l1 = 'N'
            
    ## Same for L2 selection
    if l2_dropdown_value == []:
        isselect_all_l2 = 'Y'
    else:
        for i in l2_dropdown_value:
            if i == 'All' or i == '':
                isselect_all_l2 = 'Y'
                break
            else:
                isselect_all_l2 = 'N'   
                
    ## create default unique list of values for callback options
    input_1_list = df[column_name_1].unique()
    input_2_list = df[column_name_2].unique()
    
    # If not all items are desired...
    if isselect_all_l1 == 'N':
        ## pull series of values for rows that match fitler criteria
        bool_filter_series = df[column_name_1].isin(l1_dropdown_value)
        ## use bool series to pull filtered list of unique values for call back 2
        input_2_list = df[column_name_2][bool_filter_series].unique()
        
    # If not all items are desired...
    if isselect_all_l2 == 'N':
        ## pull series of values for rows that match fitler criteria
        bool_filter_series = df[column_name_2].isin(l2_dropdown_value)
        ## use bool series to pull filtered list of unique values for call back 1
        input_1_list = df[column_name_1][bool_filter_series].unique()
    
    
    ### Set Callback options ###
    ### Options for Dropdown 1
    drop_down_1_options = [{'label': 'All', 'value': 'All'}] + \
                                    [{'label': str(k), 'value': str(k)} for k in sorted(input_1_list)]
    
    ### Options for Dropdown 2
    drop_down_2_options = [{'label': 'All', 'value': 'All'}] + \
                                    [{'label': str(k), 'value': str(k)} for k in sorted(input_2_list)]
        
    return drop_down_1_options, drop_down_2_options


@app.callback(
        Output(id_gen('sales_bar_graph'), "figure"),
        Output(id_gen('sales_allocations_%_bar_graph'), "figure"),
        [Input(id_gen('submit_button_sales_1'), 'n_clicks'),
        State(id_gen('date_picker'), 'start_date'),
        State(id_gen('date_picker'), 'end_date'),
        State(id_gen('slm_team_lead_dropdown'), 'value'),
        State(id_gen('slm_dropdown'), "value"),
        State(id_gen('product_cat_groups_dd'), 'value'),
        State(id_gen('manufacturer_groups_dd'), 'value'),
        State(id_gen('wh_radio'), "value"),
        State(id_gen('onlineOrder_radio'), "value"),
        State(id_gen('allocation_type'), "value"),
        
        ],
    )
def sales_history_bar_charts(n_clicks, start, end, team, slm_no, product_cats, manufacturers, warehouse, online_order_ind
                             ,allocation_type):
    try:
        start = dt.strptime(start, '%Y-%m-%d').date()
        end = dt.strptime(end, '%Y-%m-%d').date()
        
        ## subset by dates
        dataset =  df_2.copy()
        dataset = dataset[(dataset['inv_posted_date_actual']>=start) & (dataset['inv_posted_date_actual']<=end)]
        
        if ('All' not in team) and ('' not in team) and (len(team) != 0):
            dataset = dataset[dataset['slm_team_lead'].isin(team)]
            
        if ('All' not in slm_no) and ('' not in slm_no) and (len(slm_no) != 0):
            dataset = dataset[dataset['slm_no'].isin(slm_no)]
            
        if not warehouse == 'All':
            dataset = dataset[dataset['hist_trx_location'] == warehouse]
            
        if ('All' not in product_cats) and ('' not in product_cats) and (len(product_cats) != 0):
            dataset = dataset[dataset['product_category_name'].isin(product_cats)]
            
        if ('All' not in manufacturers) and ('' not in manufacturers) and (len(manufacturers) != 0):
            dataset = dataset[dataset['manufacturer_name'].isin(manufacturers)]
            
        if not online_order_ind == 'All':
            dataset = dataset[dataset['online_order_ind'] == online_order_ind]        
        
        ## get total sales before filtering allocations
        total_sales_slm = dataset.groupby(['slm_name'], as_index=False)['hist_trx_sale_amt'].sum()
        
        if ('All' not in allocation_type) and ('' not in allocation_type) and (len(allocation_type) != 0):
             dataset = dataset[dataset['hst_trx_item_allocation_type'].isin(allocation_type)] 
             
        ### Get total Sales by slm and team lead
        grouped = dataset.groupby(['slm_name', 'slm_team_lead', 'hst_trx_item_allocation_type'], 
                                  as_index=False)['hist_trx_sale_amt'].sum()
               
        
        ## Get sort order for stacked H bar chart 
        grouped_sort_order = grouped.groupby(['slm_team_lead','slm_name'], as_index=False)['hist_trx_sale_amt'].sum()
        grouped_sort_order = grouped_sort_order.sort_values(['slm_team_lead', 'hist_trx_sale_amt'], ascending=False)
        
        fig_1 = px.bar(grouped, x='hist_trx_sale_amt', y='slm_name', color='hst_trx_item_allocation_type',
                     orientation='h', labels=({'hist_trx_sale_amt': "Sales", 'slm_name': "Sales Executive",
                                               'hst_trx_item_allocation_type': "Allocation Type"})
                     )
        fig_1.update_layout(
            margin=dict(t=0, r=0, l=0),
            # yaxis_visible=False,
            legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
            ),
            #sort
            yaxis={'categoryorder':'array', 'title': None, 'categoryarray':grouped_sort_order['slm_name']})

        
        
        ### Create sales proportions based on allocations chart
        df_1 = grouped.merge(total_sales_slm, how='inner', on=['slm_name'])
        df_1['percent_sales'] = df_1['hist_trx_sale_amt_x'] / df_1['hist_trx_sale_amt_y']
        
        fig_2 = px.bar(df_1, x='percent_sales', y='slm_name', color='hst_trx_item_allocation_type',
                     orientation='h', labels=({'hist_trx_sale_amt': "Sales", 
                                               'slm_name': "Sales Executive",
                                               'percent_sales': "% of Sales",
                                               'hst_trx_item_allocation_type': "Allocation Type"})
                     )
        fig_2.update_traces(texttemplate='%{x:,.2f}%', textposition='inside')
        fig_2.update_layout(
            uniformtext_minsize=7, uniformtext_mode='hide',
            yaxis_visible=False,
            margin=dict(t=0, r=0, l=0),
             legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=-0.52
            ),
            showlegend=False,
            #sort
            yaxis={'categoryorder':'array', 'categoryarray':grouped_sort_order['slm_name']})
        
        #TODO: if only one SLM selected, reformat chart to be smaller; display more info
        ## remove grid lines
        fig_1 = functions.remove_figure_background(fig_1)
        fig_2 = functions.remove_figure_background(fig_2)
        
    except Exception as e:
        print(e)
        fig_1 = fig_2 = no_data_fig
    return fig_1, fig_2


        
### Sales Heat Map Callback: Filter data for heat map
@app.callback(
    Output(id_gen('sales_weekly_heatmap'), 'figure'),
    Output(id_gen('sales_heatmap_graph_month_day'), 'figure'),
    Output(id_gen('sales_heatmap_graph_month_day_adjusted'), 'figure'),
 	[Input(id_gen('submit_button_sales_1'), 'n_clicks'),
     State(id_gen('date_picker'), 'start_date'),
	 State(id_gen('date_picker'), 'end_date'),
     State(id_gen('product_cat_groups_dd'), 'value'),
     State(id_gen('manufacturer_groups_dd'), 'value'),
     State(id_gen('wh_radio'), 'value'),
     State(id_gen('onlineOrder_radio'), 'value'),
     State(id_gen('slm_team_lead_dropdown'), 'value'),
     State(id_gen('slm_dropdown'), 'value')
     ])
def sales_heat_maps(n_clicks, start, end, product_cats, manufacturers, warehouse, online_order_ind, team, slm_no):
    try:
        start = dt.strptime(start, '%Y-%m-%d').date()
        end = dt.strptime(end, '%Y-%m-%d').date()
        
        ## subset by dates
        dataset =  df_2.copy()
        dataset = dataset[(dataset['inv_posted_date_actual']>=start) & (dataset['inv_posted_date_actual']<=end)]
     
        if ('All' not in team) and ('' not in team) and (len(team) != 0):
            dataset = dataset[dataset['slm_team_lead'].isin(team)]
    
        if ('All' not in slm_no) and ('' not in slm_no) and (len(slm_no) != 0):
            dataset = dataset[dataset['slm_no'].isin(slm_no)]
            
        if not warehouse == 'All':
            dataset = dataset[dataset['hist_trx_location']==warehouse]
     
        if ('All' not in product_cats) and ('' not in product_cats) and (len(product_cats) != 0):
            dataset = dataset[dataset['product_category_name'].isin(product_cats)]
            
        if ('All' not in manufacturers) and ('' not in manufacturers) and (len(manufacturers) != 0):
            dataset = dataset[dataset['manufacturer_name'].isin(manufacturers)]
        
        if not online_order_ind == 'All':
            dataset = dataset[dataset['online_order_ind'] == online_order_ind]  
            
            
        # dataset['month'] = pd.to_datetime(dataset['inv_posted_date_actual']).dt.strftime("%b")
        
        ####### Sales By Day of the Week and Week of the Year Heat map #######
        df = dataset.groupby(['inv_posted_week_of_year','inv_posted_day_of_week', 'inv_posted_date_actual'], as_index=False)['hist_trx_sale_amt'].agg('sum')
        
        hovertemplate_here = (
        "<i>Week</i>: %{y}<br>"+
        "<i>Weekday</i>: %{x}<br>"+
        "<i>Sales</i>: %{z}"+
        "<i>Date</i>: %{customdata}"+
        "<extra></extra>") # Remove trace info
        
        data = go.Heatmap(
            x = df['inv_posted_day_of_week'],
            y = df['inv_posted_week_of_year'],
            z = df['hist_trx_sale_amt'],
            customdata = df['inv_posted_date_actual'],
            hovertemplate = hovertemplate_here,
            hoverongaps = False,
            colorscale = scale,
            showscale = False,
            xgap = 1,
            ygap = 1)
        fig_1 = go.Figure(data=data, 
                        )
        fig_1.update_layout(
            margin=dict(t=0, r=0, l=0),
            # title={'text' : "Heatmap: Sales by week and weekday"},
            xaxis = {
                'title' : None,
                'tickvals' : [1,2,3,4,5,6,7], #Display x values with different labels
                'ticktext' : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
                },
            yaxis = {
                'title' : "Calendar Week",
                'showgrid' : False}
            )

        ####### Sales By Day of the Week and Day of the Month Heat map #######
       
        
         #Aggregate df plot 2
         ### set day of week to a constant to create dummy x_axis; comment out to revert back to day of week x axis
        dataset['inv_posted_day_of_week'] = 1
        
        df_day_count = dataset.groupby(['inv_posted_day_of_month','inv_posted_day_of_week'], 
                             as_index=False)[['inv_posted_date_actual']].nunique()
        
        df = dataset.groupby(['inv_posted_day_of_month','inv_posted_day_of_week'], 
                             as_index=False)[['hist_trx_sale_amt']].sum()
        
        df = df.merge(df_day_count, how='inner', on=['inv_posted_day_of_month','inv_posted_day_of_week'])
        
        ## adjust for number of days
        df_adjusted = df.copy()
        df_adjusted['hist_trx_sale_amt'] = round(df_adjusted['hist_trx_sale_amt'] / df_adjusted['inv_posted_date_actual'])
        
        
        ##### Day of Month and day of Week heat map
        hovertemplate_here = (
        "<i>Day</i>: %{y}<br>"+
        # "<i>Weekday</i>: %{x}<br>"+
        "%{z}<br>"+
        "<i>#Days</i>: %{customdata}"+
        "<extra></extra>") # Remove trace info
        ############### actual
        data = go.Heatmap(
            x = df['inv_posted_day_of_week'],
            y = df['inv_posted_day_of_month'],
            z = df['hist_trx_sale_amt'],
            customdata = df['inv_posted_date_actual'],
            hovertemplate = hovertemplate_here,
            hoverongaps = False,
            colorscale = scale,
            showscale = False,
            xgap = 1,
            ygap = 1)
        
        fig_2 = go.Figure(data=data)
        
         ## add formatting for fig2
        fig_2.update_layout(
        margin=dict(l=0, r=0, t=0),
        xaxis = {
            # 'tickvals' : [1,2,3,4,5,6,7], 
            'tickvals' : [1],
            #Display x values with different labels
            # 'ticktext' : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
            'ticktext' : ['ActualSales']
            },
        yaxis = {
            'title' : "Day of Month",
            'showgrid' : False}
        )
        ################ adjusted
        hovertemplate_here = (
        "<i>Day</i>: %{y}<br>"+
        # "<i>Weekday</i>: %{x}<br>"+
        "%{z}<br>"+
        "<i>#Days</i>: %{customdata}"+
        "<extra></extra>") # Remove trace info
        data = go.Heatmap(
            x = df_adjusted['inv_posted_day_of_week'],
            y = df_adjusted['inv_posted_day_of_month'],
            z = df_adjusted['hist_trx_sale_amt'],
            customdata = df_adjusted['inv_posted_date_actual'],
            hovertemplate = hovertemplate_here,
            hoverongaps = False,
            colorscale = scale,
            showscale = False,
            xgap = 1,
            ygap = 1)
        
        fig_3 = go.Figure(data=data)
        
         ## add formatting for fig2
        fig_3.update_layout(
        margin=dict(l=0, r=40, t=0),
        # width = 90,
        xaxis = {
            # 'tickvals' : [1,2,3,4,5,6,7], 
            'tickvals' : [1],
            #Display x values with different labels
            # 'ticktext' : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
            'ticktext' : ['AdjustSales']
            },
        yaxis_visible=False,
        yaxis = {
            'title' : "Day of Month",
            'showgrid' : False}
        )
      
        
        fig_1 = functions.remove_figure_background(fig_1)
        fig_2 = functions.remove_figure_background(fig_2)
        fig_3 = functions.remove_figure_background(fig_3)
    except Exception as e:
       print(e)
       fig_1 = fig_2, fig_3 = no_data_fig
       
    return fig_1, fig_2, fig_3

### Cumlative Sales
@app.callback(
    Output(id_gen('sales_cumlative_sum_high'), 'figure'),
    # Output(id_gen('sales_by_weekday_line'), 'figure'),
 	[Input(id_gen('submit_button_sales_1'), 'n_clicks'),
     State(id_gen('date_picker'), 'start_date'),
	 State(id_gen('date_picker'), 'end_date'),
     State(id_gen('product_cat_groups_dd'), 'value'),
     State(id_gen('manufacturer_groups_dd'), 'value'),
     State(id_gen('wh_radio'), 'value'),
     State(id_gen('onlineOrder_radio'), 'value'),
     State(id_gen('slm_team_lead_dropdown'), 'value'),
     State(id_gen('slm_dropdown'), 'value')
     ])
def cumlative_sales(n_clicks, start, end, product_cats, manufacturers, warehouse, online_order_ind, team, slm_no):
    try:
        start = dt.strptime(start, '%Y-%m-%d').date()
        end = dt.strptime(end, '%Y-%m-%d').date()
        
        ## subset by dates
        dataset =  df_2.copy()
        dataset = dataset[(dataset['inv_posted_date_actual']>=start) & (dataset['inv_posted_date_actual']<=end)]
     
        if ('All' not in team) and ('' not in team) and (len(team) != 0):
            dataset = dataset[dataset['slm_team_lead'].isin(team)]
    
        if ('All' not in slm_no) and ('' not in slm_no) and (len(slm_no) != 0):
            dataset = dataset[dataset['slm_no'].isin(slm_no)]
            
        if not warehouse == 'All':
            dataset = dataset[dataset['hist_trx_location']==warehouse]
     
        if ('All' not in product_cats) and ('' not in product_cats) and (len(product_cats) != 0):
            dataset = dataset[dataset['product_category_name'].isin(product_cats)]
            
        if ('All' not in manufacturers) and ('' not in manufacturers) and (len(manufacturers) != 0):
            dataset = dataset[dataset['manufacturer_name'].isin(manufacturers)]
        
        if not online_order_ind == 'All':
            dataset = dataset[dataset['online_order_ind'] == online_order_ind]  
    
        dataset['ProductCategoryGroups'] = dataset['product_category_name'].apply(lambda x: functions.create_groups(x))
        df = dataset.groupby(['inv_posted_date_actual', 'ProductCategoryGroups'], as_index=False)['hist_trx_sale_amt'].agg('sum')
        
        ####### Cumulative Sales
        
        
        ### create CDF plot for high volume categories
        fig_1 = px.ecdf(df, 
                        x="inv_posted_date_actual",
                        y='hist_trx_sale_amt', 
                        color='ProductCategoryGroups', 
                        # marginal='rug',
                        ecdfnorm=None
                        )
        
        fig_1 = functions.remove_figure_background(fig_1)
        
        fig_1.update_layout(
        modebar_add=['drawline', 'eraseshape'],
        margin=dict(t=0, r=0, l=0),    
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
        ),
        yaxis = {
        'showspikes': True,
        # 'title' : "Sales",
        'showgrid' : False},
        yaxis_visible=False,
        xaxis = {
        'showspikes': True,
        'title' : "Invoice Posted Date",
        'showgrid' : False})

          

         ####### Sales By Day of the Week Bar
        # fig_3 = px.bar(df,
        #               x='inv_posted_day_of_week',
        #               y='hist_trx_sale_amt',
        #               labels={'inv_posted_day_of_week': 'Day of Week', 'hist_trx_sale_amt': 'Sales'})
        
        # fig_3.update_layout(
        # xaxis = {
        #     'tickvals' : [1,2,3,4,5,6,7], 
        #     #Display x values with different labels
        #     'ticktext' : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        #     },
        # yaxis = {
        #     'title' : "Day of Week",
        #     'showgrid' : False}
        # )
        
    except Exception as e:
       print(e)
       fig_1 = no_data_fig
       
    return fig_1



@app.callback(
        Output(id_gen('manufacturer_sales_percent_by_slm_bar'), "figure"),
        Output(id_gen('removed_top_manufacturers_slm'), "children"),
        Output(id_gen('removed_bottom_manufacturers_slm'), "children"),
        [Input(id_gen('submit_button_sales_2'), 'n_clicks'),
         State(id_gen('remove_top_man_slm'), 'value'),
        State(id_gen('remove_bottom_man_slm'), 'value'),
        State(id_gen('slm_team_lead_dropdown'), 'value'),
        State(id_gen('slm_dropdown'), "value"),
        State(id_gen('product_cat_groups_dd_propor_slm'), 'value'),
        State(id_gen('manufacturer_groups_dd_propor_slm'), 'value'),
        State(id_gen('wh_radio'), "value"),
        State(id_gen('onlineOrder_radio'), "value"),
        State(id_gen('allocation_type'), "value"),
        State(id_gen('region_checklist_slm'), "value"),
        ],prevent_initial_call=True
    )
def create_manufactuere_by_slm_bar(n_clicks, remove_top, remove_bottom, team, slm_no, product_cats, manufacturers, warehouse,
                                online_order_ind, allocation_type, regions):
    try:        
        ## subset by dates
        dataset =  df_2.copy()
        
        
        
        if ('All' not in remove_top) and ('' not in remove_top) and (len(remove_top) != 0):
            top_manufacturers = dataset.groupby(['manufacturer_name'], as_index=False)['hist_trx_sale_amt'].sum()
            top_manufacturers['ranking']= top_manufacturers['hist_trx_sale_amt'].rank(ascending=False)
            top_manufacturers = top_manufacturers[top_manufacturers['ranking'] <= 8]
            top_manufacturers = top_manufacturers['manufacturer_name']
            dataset = dataset[~dataset['manufacturer_name'].isin(top_manufacturers)]
            top_manufacturers = ", ".join(sorted(top_manufacturers))
        else:
            top_manufacturers = ''
              
        if ('All' not in remove_bottom) and ('' not in remove_bottom) and (len(remove_bottom) != 0):
            bottom_manufacturers = dataset.groupby(['manufacturer_name'], as_index=False)['hist_trx_sale_amt'].sum()
            bottom_manufacturers['ranking']= bottom_manufacturers['hist_trx_sale_amt'].rank()
            bottom_manufacturers = bottom_manufacturers[bottom_manufacturers['ranking'] <= 10]
            bottom_manufacturers = bottom_manufacturers['manufacturer_name']
            dataset = dataset[~dataset['manufacturer_name'].isin(bottom_manufacturers)]
            bottom_manufacturers = ", ".join(sorted(bottom_manufacturers))
        else:
            bottom_manufacturers = ''
        
        if ('All' not in team) and ('' not in team) and (len(team) != 0):
            dataset = dataset[dataset['slm_team_lead'].isin(team)]
            
        if ('All' not in slm_no) and ('' not in slm_no) and (len(slm_no) != 0):
            dataset = dataset[dataset['slm_no'].isin(slm_no)]
            
        if not warehouse == 'All':
            dataset = dataset[dataset['hist_trx_location'] == warehouse]
            
        if not online_order_ind == 'All':
            dataset = dataset[dataset['online_order_ind'] == online_order_ind]        
        
        if ('All' not in allocation_type) and ('' not in allocation_type) and (len(allocation_type) != 0):
            dataset = dataset[dataset['hst_trx_item_allocation_type'].isin(allocation_type)] 
        
        if ('All' not in regions) and ('' not in regions) and (len(regions) != 0):
            dataset = dataset[dataset['region'].isin(regions)] 
            
                ### filter invalid States
        invalid_states = ['DC', 'KA', 'VI', 'PR', '**']
        dataset = dataset[~dataset['ship_to_state'].isin(invalid_states)]
        
        ### Get total Sales by state and manufacturer BEFORE SUBSETTING MANUFACTURER AND PRODUCT CAT
        df_total_sales = dataset.groupby(['slm_no'], as_index=False)['hist_trx_sale_amt'].sum()
            
        
        if ('All' not in product_cats) and ('' not in product_cats) and (len(product_cats) != 0):
            dataset = dataset[dataset['product_category_name'].isin(product_cats)]
            
        if ('All' not in manufacturers) and ('' not in manufacturers) and (len(manufacturers) != 0):
            dataset = dataset[dataset['manufacturer_name'].isin(manufacturers)]
            
                       
        ### Get total Sales by state and manufacturer
        df_total_sales_by_group = dataset.groupby(['slm_no', 'manufacturer_name'], 
                                  as_index=False)['hist_trx_sale_amt'].sum()
               
        ### Create sales proportions based on allocations chart;  grouped sales / total sales
        df_1 = df_total_sales_by_group.merge(df_total_sales, how='inner', on=['slm_no'])
        df_1['percent_sales'] = (df_1['hist_trx_sale_amt_x'] / df_1['hist_trx_sale_amt_y']) * 100
        
        ### reformat Sales as currency
        df_1['hist_trx_sale_amt_x'] = df_1['hist_trx_sale_amt_x'].apply(lambda x: functions.formatter_currency(x))
        
        ### set sort order 
        grouped_sort_order = df_1.sort_values(['slm_no', 'manufacturer_name'], ascending=False)
        
        fig_1 = px.bar(df_1, x='percent_sales', y='slm_no', color='manufacturer_name',
                       color_discrete_sequence=high_card_color_template,
                        hover_data=["hist_trx_sale_amt_x"],
                       labels=({'slm_no': "SLM Number", 
                                'manufacturer_name': "Manufacturer",
                                'percent_sales': "% of Sales",
                                'hist_trx_sale_amt_x': "Sales"
                                })
                     )
        fig_1.update_traces(texttemplate='%{x:,.1f}%', textposition='inside')
        fig_1.update_layout(
            # uniformtext_minsize=7, uniformtext_mode='hide',
            margin=dict(t=0, r=0, l=0, b=0),
            showlegend=False,
            yaxis={'categoryorder':'array', 'title': None, 'categoryarray':grouped_sort_order['slm_no']}
            )
        # fig_1.update_yaxes(ticklabelposition='outside right')
        
        ## remove grid lines
        fig_1 = functions.remove_figure_background(fig_1)
        
    except Exception as e:
       print(e)
       fig_1 =  no_data_fig
       top_manufacturers = bottom_manufacturers = ''
       
    return fig_1, top_manufacturers, bottom_manufacturers


@app.callback(
        Output(id_gen('manufacturer_sales_percent_by_state_bar'), "figure"),
        Output(id_gen('removed_top_manufacturers_state'), "children"),
        Output(id_gen('removed_bottom_manufacturers_state'), "children"),
        [Input(id_gen('submit_button_sales_3'), 'n_clicks'),
        State(id_gen('remove_top_man_state'), 'value'),
        State(id_gen('remove_bottom_man_state'), 'value'),
        State(id_gen('slm_team_lead_dropdown'), 'value'),
        State(id_gen('slm_dropdown'), "value"),
        State(id_gen('product_cat_groups_dd_propor_state'), 'value'),
        State(id_gen('manufacturer_groups_dd_propor_state'), 'value'),
        State(id_gen('wh_radio'), "value"),
        State(id_gen('onlineOrder_radio'), "value"),
        State(id_gen('allocation_type'), "value"),
        State(id_gen('region_checklist_state'), "value"),
        ],prevent_initial_call=True
    )
def create_manufactuere_by_state_bar(n_clicks, remove_top, remove_bottom, team, slm_no, product_cats, manufacturers, warehouse,
                                online_order_ind, allocation_type, regions):
    try:        
        ## subset by dates
        dataset =  df_2.copy()
        
        if ('All' not in remove_top) and ('' not in remove_top) and (len(remove_top) != 0):
            top_manufacturers = dataset.groupby(['manufacturer_name'], as_index=False)['hist_trx_sale_amt'].sum()
            top_manufacturers['ranking']= top_manufacturers['hist_trx_sale_amt'].rank(ascending=False)
            top_manufacturers = top_manufacturers[top_manufacturers['ranking'] <= 8]
            top_manufacturers = top_manufacturers['manufacturer_name']
            dataset = dataset[~dataset['manufacturer_name'].isin(top_manufacturers)]
            top_manufacturers = ", ".join(sorted(top_manufacturers))
        else:
            top_manufacturers = ''
              
        if ('All' not in remove_bottom) and ('' not in remove_bottom) and (len(remove_bottom) != 0):
            bottom_manufacturers = dataset.groupby(['manufacturer_name'], as_index=False)['hist_trx_sale_amt'].sum()
            bottom_manufacturers['ranking']= bottom_manufacturers['hist_trx_sale_amt'].rank()
            bottom_manufacturers = bottom_manufacturers[bottom_manufacturers['ranking'] <= 10]
            bottom_manufacturers = bottom_manufacturers['manufacturer_name']
            dataset = dataset[~dataset['manufacturer_name'].isin(bottom_manufacturers)]
            bottom_manufacturers = ", ".join(sorted(bottom_manufacturers))
        else:
            bottom_manufacturers = ''
        
        if ('All' not in team) and ('' not in team) and (len(team) != 0):
            dataset = dataset[dataset['slm_team_lead'].isin(team)]
            
        if ('All' not in slm_no) and ('' not in slm_no) and (len(slm_no) != 0):
            dataset = dataset[dataset['slm_no'].isin(slm_no)]
            
        if not warehouse == 'All':
            dataset = dataset[dataset['hist_trx_location'] == warehouse]
            
        if not online_order_ind == 'All':
            dataset = dataset[dataset['online_order_ind'] == online_order_ind]        
        
        if ('All' not in allocation_type) and ('' not in allocation_type) and (len(allocation_type) != 0):
            dataset = dataset[dataset['hst_trx_item_allocation_type'].isin(allocation_type)] 
        
        if ('All' not in regions) and ('' not in regions) and (len(regions) != 0):
            dataset = dataset[dataset['region'].isin(regions)] 
            
        ### Get total Sales by state and manufacturer BEFORE SUBSETTING MANUFACTURER AND PRODUCT CAT
        df_total_sales = dataset.groupby(['ship_to_state'], as_index=False)['hist_trx_sale_amt'].sum()
            
        
        if ('All' not in product_cats) and ('' not in product_cats) and (len(product_cats) != 0):
            dataset = dataset[dataset['product_category_name'].isin(product_cats)]
            
        if ('All' not in manufacturers) and ('' not in manufacturers) and (len(manufacturers) != 0):
            dataset = dataset[dataset['manufacturer_name'].isin(manufacturers)]
            
            
        ### filter invalid States
        invalid_states = ['DC', 'KA', 'VI', 'PR', '**']
        dataset = dataset[~dataset['ship_to_state'].isin(invalid_states)]
                       
        ### Get total Sales by state and manufacturer
        df_total_sales_by_group = dataset.groupby(['ship_to_state', 'manufacturer_name'], 
                                  as_index=False)['hist_trx_sale_amt'].sum()
               
        ### Create sales proportions based on allocations chart;  grouped sales / total sales
        df_1 = df_total_sales_by_group.merge(df_total_sales, how='inner', on=['ship_to_state'])
        df_1['percent_sales'] = (df_1['hist_trx_sale_amt_x'] / df_1['hist_trx_sale_amt_y']) * 100
        
        ### reformat Sales as currency
        df_1['hist_trx_sale_amt_x'] = df_1['hist_trx_sale_amt_x'].apply(lambda x: functions.formatter_currency(x))
        
        ### set sort order 
        grouped_sort_order = df_1.sort_values(['ship_to_state', 'manufacturer_name'], ascending=False)
        
        fig_1 = px.bar(df_1, x='percent_sales', y='ship_to_state', color='manufacturer_name',
                       color_discrete_sequence=high_card_color_template,
                        hover_data=["hist_trx_sale_amt_x"],
                       labels=({'ship_to_state': "State", 
                                'manufacturer_name': "Manufacturer",
                                'percent_sales': "% of Sales",
                                'hist_trx_sale_amt_x': "Sales"
                                })
                     )
        fig_1.update_traces(texttemplate='%{x:,.1f}%', textposition='inside')
        fig_1.update_layout(
            # uniformtext_minsize=7, uniformtext_mode='hide',
            margin=dict(t=0, r=0, l=0, b=0),
            showlegend=False,
            yaxis={'categoryorder':'array', 'title': None, 'categoryarray':grouped_sort_order['ship_to_state']}
            )
        # fig_1.update_yaxes(ticklabelposition='outside right')
        
        ## remove grid lines
        fig_1 = functions.remove_figure_background(fig_1)
        
    except Exception as e:
       print(e)
       fig_1 =  no_data_fig
       top_manufacturers = bottom_manufacturers = ''
       
    return fig_1, top_manufacturers, bottom_manufacturers



##TODO: Data table. Top SLM w/ biggest customer listed
##TODO: Online Orders vs Manual

##TODO: SLM Focus; Manufacturer/Product Focus; Customer Focus

### TODO: Customer Focus
## New customers sold to

## Unique number of customers sold to by SLM
## Top Customers by type
## Top Customers within reporting period (show new entrys)
## Customers with high velocity

#TODO: Manufacturer
### Ranked Sales, gross margin
### 

#marks request
#top 100 customers by sales, gross margin, net margin, slm, rolling 12, ytd, last year, qtr
## all sales execs
## all manufacturers
## items top 100

