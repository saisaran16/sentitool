import plotly.express as px
import pandas as pd
from pymongo import MongoClient
from pages.MongoDB_Keys import MONGO_HOST

###########################################################################################################################################################################################

# MongoDB connection
client = MongoClient(MONGO_HOST)
db = client["sentiment_analysis_result_db"]
collection = db["chevron_oil_collection"]

def query_twitter_mongo_db():
    pd.set_option('display.max_columns', None)
    result = collection.find({'social_media_platform': "b'Twitter'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_confidence_score_positive": 1, "MTA_document_confidence_score_neutral": 1, "MTA_document_confidence_score_negative": 1, '_id': 0}, limit=10)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_confidence_score_positive": "MTA Document Confidence Score Positive", "MTA_document_confidence_score_neutral": "MTA Document Confidence Score Neutral", "MTA_document_confidence_score_negative": "MTA Document Confidence Score Negative"}, inplace=True)
    indexNotApplicable = df_local[ (df_local['IWNLU Sentiment Document Score'] == 'N/A') | (df_local['GCNLA Sentiment Document Score'] == 'N/A') | (df_local['MTA Document Confidence Score Positive'] == 'N/A') | (df_local['MTA Document Confidence Score Neutral'] == 'N/A') | (df_local['MTA Document Confidence Score Negative'] == 'N/A') ].index
    df_local.drop(indexNotApplicable , inplace=True)
    df_local = df_local.astype(float)
    print(df_local)
    for val in df_local['IWNLU Sentiment Document Score']:
        print(type(val))
    return df_local

# Build a plot line using Twitter posts
def build_twitter_graph(df_local):
    fig_line = px.line(df_local, x='Post ID', y=df_local.columns[1:6], title="Twitter")
    fig_line.show()
    
###########################################################################################################################################################################################

def query_tumblr_mongo_db():
    pd.set_option('display.max_columns', None)
    result = collection.find({'social_media_platform': "b'Tumblr'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_confidence_score_positive": 1, "MTA_document_confidence_score_neutral": 1, "MTA_document_confidence_score_negative": 1, '_id': 0}, limit=10)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_confidence_score_positive": "MTA Document Confidence Score Positive", "MTA_document_confidence_score_neutral": "MTA Document Confidence Score Neutral", "MTA_document_confidence_score_negative": "MTA Document Confidence Score Negative"}, inplace=True)
    indexNotApplicable = df_local[ (df_local['IWNLU Sentiment Document Score'] == 'N/A') | (df_local['GCNLA Sentiment Document Score'] == 'N/A') | (df_local['MTA Document Confidence Score Positive'] == 'N/A') | (df_local['MTA Document Confidence Score Neutral'] == 'N/A') | (df_local['MTA Document Confidence Score Negative'] == 'N/A') ].index
    df_local.drop(indexNotApplicable , inplace=True)
    print(df_local)
    # for col in df_local.columns:
    #     print(type(col))
    return df_local

# Build a plot line using Tumblr posts
def build_tumblr_graph(df_local):
    fig_line = px.line(df_local, x='Post ID', y=df_local.columns[1:6], title="Tumblr") 
    fig_line.show()

###########################################################################################################################################################################################

def query_reddit_mongo_db():
    result = collection.find({'social_media_platform': "b'Reddit'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_confidence_score_positive": 1, "MTA_document_confidence_score_neutral": 1, "MTA_document_confidence_score_negative": 1, '_id': 0}, limit=10)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_confidence_score_positive": "MTA Document Confidence Score Positive", "MTA_document_confidence_score_neutral": "MTA Document Confidence Score Neutral", "MTA_document_confidence_score_negative": "MTA Document Confidence Score Negative"}, inplace=True)
    indexNotApplicable = df_local[ (df_local['IWNLU Sentiment Document Score'] == 'N/A') | (df_local['GCNLA Sentiment Document Score'] == 'N/A') | (df_local['MTA Document Confidence Score Positive'] == 'N/A') | (df_local['MTA Document Confidence Score Neutral'] == 'N/A') | (df_local['MTA Document Confidence Score Negative'] == 'N/A') ].index
    df_local.drop(indexNotApplicable , inplace=True)   
    for col in df_local.columns:
        print(type(col)) 
    return df_local

###########################################################################################################################################################################################

df_col = pd.DataFrame(columns = ['id', 'IWNLU_sentiment_document_score'])

def query_mongo_db():
    result = collection.find({}, {'id': 1, 'IWNLU_sentiment_document_score': 1, '_id': 0}, limit=10)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    print(df_local)
    build_graph(df_local)

def build_graph(df):
    fig = px.line(df, x='id', y='IWNLU_sentiment_document_score')
    fig.show()
    
###########################################################################################################################################################################################

if __name__=='__main__':
    df_twitter = query_twitter_mongo_db()
    build_twitter_graph(df_twitter)



##### Another implementation to append dictionaries to dataframes #####
# def query_mongo_db():
#     df_local = df
#     result = collection.find({}, {'id': 1, 'IWNLU_sentiment_document_score': 1, '_id': 0}, limit=10)

#     for document in result:
#         df_local = df_local.append(document, ignore_index=True)
#     print(df_local)

################## PROPER CALLBACK FUNCTION #############################
# def on_button_click(n_clicks, value):
#     if n_clicks > 0:
#         url = 'http://localhost:7071/api/HttpTrigger'
#         body = {
#                     "Company Name": value,
#                     "Twitter": "Yes",
#                     "Reddit": "Yes",
#                     "Tumblr": "No"
#                 }
#         resp = requests.post(url, json=body)
#         print(resp)
#         result = collection.find({}, {'id': 1, 'IWNLU_sentiment_document_score': 1, '_id': 0}, limit=10)
#         list_result = list(result)
#         df = pd.DataFrame(list_result)
#         print(df)
#         fig_line = px.line(df, x='id', y='IWNLU_sentiment_document_score')
#         return fig_line
#     else:
#         fig = {} 
#         return fig

############################### Sample Code that did not work!!! ########################################
# import dash
# from dash import dcc, html
# from dash.dependencies import Output, Input, State
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import pandas as pd
# import requests
# from pymongo import MongoClient
# from MongoDB_Keys import MONGO_HOST

# # https://www.bootstrapcdn.com/bootswatch/
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
#                 meta_tags=[{'name': 'viewport',
#                             'content': 'width=device-width, initial-scale=1.0'}])

# # MongoDB connection
# client = MongoClient(MONGO_HOST)
# db = client["sentiment_analysis_result_db"]
# collection = db["chevron_oil_collection"]

# # Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# # ************************************************************************
# app.layout = dbc.Container([

#     dbc.Row(
#         dbc.Col(
#             [html.H1("Sentiment Analysis of Social Media",
#                     className='text-center text-dark')],
#             width=6
#         ), justify='center', className='mt-5'
#     ),

#     dbc.Row(
#         [dbc.Col(
#             [dbc.Input(id="input-on-submit", 
#                         placeholder="Input your keyword", 
#                         type="text")],
#             width={'size': 6, 'offset': 2}
#         ), 

#         dbc.Col(
#             [dbc.Button("Submit", 
#                             id="submit-button",
#                             color="dark",
#                             n_clicks=0)],
#             width={'size': 2}
#         )], justify='center', className="mt-3"
#     ),

#     dbc.Row(
#         dbc.Col(
#             [#html.P(id="output"),
#             dcc.Graph(id='twitter-graph', figure={})] # ERROR: list and figure component. The list and figure should be removed
#         )
#     ),

#     # dbc.Row(
#     #     dbc.Col(
#     #         dbc.Checklist(options=[{"label": "Twitter", "value": "b'Twitter'"},
#     #                                 {"label": "Reddit", "value": "b'Reddit'"},
#     #                                 {"label": "Tumblr", "value": "b'Tumblr'"}],
#     #                         value=["b'Twitter'", "b'Reddit'", "b'Tumblr'"],
#     #                         id="social-media-input",
#     #                         inline=True),
#     #         width={'size': 6, 'offset': 3}
#     #     ), justify='center'
#     #)

# ], fluid=True)

# # Callback section: connecting the components
# # ************************************************************************

# @app.callback(
#     Output('twitter-graph', 'figure'),
#     #Output('output', 'children'),
#     Input('submit-button', 'n_clicks'),
#     State('input-on-submit', 'value')
# )

# def on_button_click(n_clicks, value):
#     if n_clicks > 0:
#         url = 'http://localhost:7071/api/HttpTrigger'
#         body = {
#                     "Company Name": value,
#                     "Twitter": "Yes",
#                     "Reddit": "Yes",
#                     "Tumblr": "No"
#                 }
#         resp = requests.post(url, json=body)
#         print(resp)
#         df = query_mongo_db()
#         print(df)
#         return build_twitter_graph(df)
#         #return f"{resp}" # ERROR: missing else statement. return {}

# def query_mongo_db():
#     result = collection.find({}, {'id': 1, 'IWNLU_sentiment_document_score': 1, '_id': 0}, limit=10)
#     list_result = list(result)
#     df_local = pd.DataFrame(list_result)
#     return df_local


# def build_twitter_graph(df_local):
#     return px.line(df_local, x='id', y='IWNLU_sentiment_document_score') # ERROR: not assigning the figure returned from line to a variable


# if __name__=='__main__':
#     app.run_server(debug=True, port=8000)