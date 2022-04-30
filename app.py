import dash
# import dash_auth
import dash_bootstrap_components as dbc
import pathlib
import plotly.express as px
# User management initialization
import os
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash


## local imports
from users_mgt import db, User as base
from users_mgt import Role
from config import config

# from data.dash_data import load_rolling_two_year_sales, load_yearly_sales_and_call_stats_by_slm
from exceptions import no_data_graphs
no_data_fig = no_data_graphs.figure_none_line()

### Set color template for high cardinality cats
high_card_color_template = px.colors.qualitative.Dark24 + px.colors.qualitative.Light24 + px.colors.qualitative.Prism
remove_colors = ['#FB00D1', '#FF0092', '#00FE35', '#22FFA7', '#0DF9FF']
for i in remove_colors:
    high_card_color_template.remove(i)

# df_1 = load_yearly_sales_and_call_stats_by_slm('parquet')
# df_2 = load_rolling_two_year_sales('parquet')

### gun metal grey
# external_stylesheets=['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/slate/bootstrap.min.css']
### black and white
# external_stylesheets=['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css']


# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, 
                # external_stylesheets=external_stylesheets,
                external_stylesheets=[dbc.themes.LUX],
                suppress_callback_exceptions=True,
                # meta_tags=[{'name': 'viewport',
                #             'content': 'width=device-width, initial-scale=1.0'}]
                )

### Temp password auth; replace with db maintained list of authorized users
# VALID_USERNAME_PASSWORD_PAIRS = {
#     'admin': 'pass'
# }
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# config
server.config.update(
    # SECRET_KEY=os.urandom(12),
    SECRET_KEY='f43d2c8ff34574075bfcd7861bd6566ca57de6413166089a',
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/views/login'


# Create User class with UserMixin
class User(UserMixin, base):
    pass

#https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
with server.app_context():
    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@example.com').first():
        user = User(username='admin',
            email='admin@example.com',
            password=generate_password_hash('P4ssw0rd#1', method='sha256'),
        )
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Agent'))
        db.session.add(user)
        db.session.commit()
        
    # Create 'member@example.com' user with no roles
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(username='member',
            email='member@example.com',
            password=generate_password_hash('Friday4', method='sha256'),
        )
        db.session.add(user)
        db.session.commit()

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




