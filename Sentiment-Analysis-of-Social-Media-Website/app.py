import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State, ALL

# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}], use_pages=True)

# TODO Home is active when Results is selected 
navbar = dbc.Navbar(
    color="dark",
    dark=True,
    children=[
        html.Div(
            className="container-fluid",
            children=[
                html.A("SASM", href="/", className="navbar-brand", style={"font-size": "x-large"}),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    style={"font-size": "large"},
                    id="navbar-collapse",
                    navbar=True,
                    children=[
                        dbc.Nav(
                            className="ms-auto",
                            children=[
                                dbc.NavItem(
                                    dbc.NavLink("Home", href="/", id={"type":"link-navbar", "index": "/"})
                                ),
                                dbc.NavItem(
                                    dbc.NavLink("Results", href="/results", id={"type":"link-navbar", "index": "/results"})
                                ),
                                dbc.NavItem(
                                    dbc.NavLink("About", href="/about", id={"type":"link-navbar", "index": "/about"})
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ],
)

app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    dash.page_container
])

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    Output({"type":"link-navbar", "index":ALL}, "class_name"), 
    Input("url", "pathname"),
    Input({"type":"link-navbar", "index":ALL}, "id"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open")
)
def callback_func(pathname, link_elements, n, is_open):
    if n:
        val = not is_open
    else:
        val = is_open
    class_name = ["active" if val["index"] == pathname else "not-active" for val in link_elements]
    return val, class_name

################################################################

# # add callback for toggling the collapse on small screens
# @app.callback(
#     Output("navbar-collapse", "is_open"),
#     [Input("navbar-toggler", "n_clicks")],
#     [State("navbar-collapse", "is_open")],
# )
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

################################################################

# # add callback for toggling the collapse on small screens
# @app.callback(
#     Output("home-link", "class_name"),
#     Output("results-link", "class_name"),
#     Output("about-link", "class_name"),
#     Output("navbar-collapse", "is_open"),

#     Input("home-link", "n_clicks"),
#     Input("results-link", "n_clicks"),
#     Input("about-link", "n_clicks"),
#     Input("navbar-toggler", "n_clicks"),
#     State("navbar-collapse", "is_open"),    
# )

# def toggle_navbar_collapse(home_link_n_clicks, results_link_n_clicks, 
#                            about_link_n_clicks, navbar_toggler_n_clicks, navbar_collapse_state):
    
#     home_link_className = "active"
#     results_link_className = ""
#     about_link_className = ""

#     if home_link_n_clicks:
#         home_link_className = "active"
#         results_link_className = ""
#         about_link_className = ""
#     elif results_link_n_clicks:
#         home_link_className = ""
#         results_link_className = "active"
#         about_link_className = ""
#     elif about_link_n_clicks:
#         home_link_className = ""
#         results_link_className = ""
#         about_link_className = "active"
    
#     if navbar_toggler_n_clicks:
#         navbar_collapse_state = not navbar_collapse_state
    
#     return home_link_className, results_link_className, about_link_className, navbar_collapse_state

################################################################

# app.layout = html.Div([
# 	#html.H1('Multi-page app with Dash Pages'),

#     html.Div(
#         [
#             html.Div(
#                 dcc.Link(
#                     f"{page['name']} - {page['path']}", href=page["relative_path"]
#                 )
#             )
#             for page in dash.page_registry.values()
#         ]
#     ),

# 	dash.page_container
# ])

################################################################

# navbar = html.Div(
#     className="navbar",
#     children=[
#         html.A("Home", href="/", className="navbar-item"),
#         html.A("Results", href="/results", className="navbar-item"),
#         html.A("About", href="/about", className="navbar-item"),
#     ],
#     style={
#         "display": "flex",
#         "justify-content": "start",
#         "align-items": "center",
#         "height": "60px",
#         "background-color": "black",
#         "color": "white",
#         "padding": "0 1rem",
#     },
# )

################################################################
       
# # TODO Home is active when Results is selected 
# navbar = dbc.Navbar(
#     className="navbar-dark bg-dark",
#     children=[
#         html.Div(
#             className="container-fluid",
#             children=[
#                 html.A("SASM", href="/", className="navbar-brand", style={"font-size": "x-large"}),
#                 dbc.NavbarToggler(id="navbar-toggler"),
#                 dbc.Collapse(
#                     style={"font-size": "large"},
#                     id="navbar-collapse",
#                     navbar=True,
#                     children=[
#                         dbc.Nav(
#                             className="ms-auto",
#                             children=[
#                                 dbc.NavItem(
#                                     dbc.NavLink("Home", href="/", className="active", id="home-link")
#                                 ),
#                                 dbc.NavItem(
#                                     dbc.NavLink("Results", href="/results")
#                                 ),
#                                 dbc.NavItem(
#                                     dbc.NavLink("About", href="/about")
#                                 ),
#                             ],
#                         ),
#                     ],
#                 ),
#             ],
#         )
#     ],
# )

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80)