def id_factory(page: str):
    def func(_id: str):
        """
        Dash pages require each component in the app to have a totally
        unique id for callbacks. This is easy for small apps, but harder for larger 
        apps where there is overlapping functionality on each page. 
        For example, each page might have a div that acts as a trigger for reloading;
        instead of typing "page1-trigger" every time, this function allows you to 
        just use id('trigger') on every page.
        https://community.plotly.com/t/how-do-we-repeat-element-id-in-multi-page-apps/41339
        How:
            prepends the page to every id passed to it
        Why:
            saves some typing and lowers mental effort
        **Example**
        # SETUP
        from system.utils.utils import id_factory
        id = id_factory('page1') # create the id function for that page
        
        # LAYOUT
        layout = html.Div(
            id=id('main-div')
        )
        # CALLBACKS
        @app.callback(
            Output(id('main-div'),'children'),
            Input(id('main-div'),'style')
        )
        def funct(this):
            ...
        """
        return f"{page}-{_id}"
    return func


def remove_figure_background(fig):
    fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
    return fig


def colorscale_generator(n, starting_col = {'r' : 186, 'g' : 218, 'b' : 212}, finish_col = {'r' : 57, 'g' : 81, 'b' : 85}):
    """This function generate a colorscale between two given rgb extremes, for an amount of data points
    The rgb should be specified as dictionaries"""
    r = starting_col['r']
    g = starting_col['g']
    b = starting_col['b']
    rf = finish_col['r']
    gf = finish_col['g']
    bf = finish_col['b']
    ri = (rf - r) / n
    gi = (gf - g) / n
    bi = (bf - b) / n
    color_i = 'rgb(' + str(r) +','+ str(g) +',' + str(b) + ')'
    my_colorscale = []
    my_colorscale.append(color_i)
    for i in range(n):
        r = r + ri
        g = g + gi
        b = b + bi
        color = 'rgb(' + str(round(r)) +','+ str(round(g)) +',' + str(round(b)) + ')'
        my_colorscale.append(color)

    return my_colorscale

### Calc Gross Margin %
def calc_percent(x,z):
    if z != 0:
        y = round(((x / z) * 100) , 4)
    else:
        y = 0
    return y

# Define Formatters
def formatter_currency(x):
	return "${:,.0f}".format(x) if x >= 0 else "(${:,.0f})".format(abs(x))

def formatter_currency_with_cents(x):
	return "${:,.2f}".format(x) if x >= 0 else "(${:,.2f})".format(abs(x))

def formatter_percent(x):
	return "{:,.1f}%".format(x) if x >= 0 else "({:,.1f}%)".format(abs(x))

def formatter_percent_2_digits(x):
	return "{:,.2f}%".format(x) if x >= 0 else "({:,.2f}%)".format(abs(x))

def formatter_number(x):
	return "{:,.0f}".format(x) if x >= 0 else "({:,.0f})".format(abs(x))

### Create customer regions
def create_region_groups(x):
    if x in ['LA', 'AL', 'MS', 'FL', 'GA']:
        y = 'SouthEast'
    elif x in ['TN','KY']:
        y = 'TN, KY'
    elif x in ['NC','SC']:
        y = 'Carolinas'
    elif x in ['OH','IN',]:
        y = 'EastMidWest'
    elif x in ['AR','MO',]:
        y = 'Ozarks'
    elif x in ['ME', 'NH', 'NJ', 'NY', 'VT', 'MA','RI', 'CT',]:
        y = 'NewEngland'
    elif x in ['PA', 'VA', 'WV', 'DE', 'MD', 'DC']:
        y = 'Appalachia'
    elif x in ['TX', 'NM']:
        y = 'TX, NM'
    elif x in ['OK', 'KS', 'NE', 'CO', 'WY']:
        y = 'GreatPlains'
    elif x in ['ND', 'SD',]:
        y = 'Dakotas '
    elif x in ['NV', 'UT', 'AZ']:
        y = 'Desert'
    elif x in ['OR', 'WA']:
        y = 'Cascades'
    elif x in ['IA', 'MN', 'WI', 'IL']:
        y = 'WestMidWest'
    elif x in ['MT', 'ID']:
        y = 'MT, ID'
    elif x in ['AK', 'HI', 'PR', 'VI']:
        y = 'NonContiguous'
    else:
        # ['MI','CA',]
        y = x
    return y
