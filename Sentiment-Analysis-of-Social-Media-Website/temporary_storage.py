import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from pymongo import MongoClient
from pages.MongoDB_Keys import MONGO_HOST

# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}], use_pages=True)

# MongoDB connection
client = MongoClient(MONGO_HOST)
db = client["sentiment_analysis_result_db"]

# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(
            [html.H1("Sentiment Analysis of Social Media",
                    className='text-center')],
            width=6
        ), justify='center', className='mt-5'
    ),

    dbc.Row(
        [dbc.Col(
            [dbc.Input(id="input-on-submit", 
                        placeholder="Input your keyword", 
                        type="text")],
            width={'size': 6, 'offset': 2}
        ), 

        dbc.Col(
            [dbc.Button("Submit", 
                            id="submit-button",
                            className="btn-secondary",
                            n_clicks=0)],
            width={'size': 2}
        )], justify='center', className="mt-3"
    ),

    # Table of Contents
    dbc.Row(
        dbc.Col(
            dash.page_container
        ), justify='center', className="mt-5"
    ),

    # Twitter Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='twitter-graph')
        ), className="mt-5"
    ),

    # Reddit Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='reddit-graph')
        ), className="mt-5"
    ),

    # Tumblr Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='tumblr-graph')
        ), className="mt-5"
    ),

    # IWNLU Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='IWNLU-graph')
        ), className="mt-5"
    ),

    # MTA Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='MTA-graph')
        ), className="mt-5"
    ),

    # GCNLA Graph
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='GCNLA-graph')
        ), className="mt-5"
    ),

    # Dropdown Row
    dbc.Row(
        [dbc.Col(
            [html.H3("Sentiment Analysis Table")],
            width={'size': 6, 'offset': 1}
        ),
        dbc.Col(
            dcc.Dropdown(
                id="social-media-platform"
            ),
            width={'size': 4}
        )], className="mt-5"

        # dbc.Col(
        #     id="sentiment-engine", 
        #     width={'size': 4, 'offset': 2}
        # )], className="mt-5"
    ),

    # Sentiment Table
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='sentiment-table',
                figure=go.Figure(data=[go.Table(
                                    header=dict(values=['Post ID', 'Post', 'Social Media Platform', 'IWNLU Sentiment Score', 'GCNLA Sentiment Score', 'MTA Sentiment Score'],
                                                align='center'),
                                    cells=dict(values=[["", "", "", "", "", ""],["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""]]))
                                ])
            )
        ), className="mt-5"
    ),
    # dbc.Row(
    #     dbc.Col(
    #         dcc.Graph(id='sentiment-table')
    #     ), className="mt-5"
    # ),

], fluid=True, className="mb-5")

# Callback section: connecting the components
# ************************************************************************

@app.callback(
    #Output('social-media-checklist', 'children'),
    Output('twitter-graph', 'figure'),
    Output('reddit-graph', 'figure'),
    Output('tumblr-graph', 'figure'),
    Output('IWNLU-graph', 'figure'),
    Output('MTA-graph', 'figure'),
    Output('GCNLA-graph', 'figure'),
    Output('social-media-platform', 'options'),
    Output('social-media-platform', 'value'),
    #Output('sentiment-engine', 'children'),
    #Output('sentiment-table', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('input-on-submit', 'value'),
)

def on_button_click(n_clicks, value):
    if n_clicks > 0:
        url = 'http://localhost:7071/api/HttpTrigger'
        body = {
                    "Company Name": value,
                    "Twitter": "Yes",
                    "Reddit": "Yes",
                    "Tumblr": "Yes"
                }
        resp = requests.post(url, json=body)
        print(resp)

        global collection
        collection = db[value]

        # children = dbc.Checklist(options=[{"label": "Twitter", "value": "b'Twitter'"},
        #                             {"label": "Reddit", "value": "b'Reddit'"},
        #                             {"label": "Tumblr", "value": "b'Tumblr'"}],
        #                     value=["b'Twitter'", "b'Reddit'", "b'Tumblr'"],
        #                     id="social-media-checklist-input",
        #                     inline=True)

        df_twitter = query_twitter_mongo_db()
        fig_twitter = build_twitter_graph(df_twitter)

        df_reddit = query_reddit_mongo_db()
        fig_reddit = build_reddit_graph(df_reddit)

        df_tumblr = query_tumblr_mongo_db()
        fig_tumblr = build_tumblr_graph(df_tumblr)

        df_IWNLU = query_IWNLU_mongo_db()
        fig_IWNLU = build_IWNLU_graph(df_IWNLU)

        df_MTA = query_MTA_mongo_db()
        fig_MTA = build_MTA_graph(df_MTA)

        df_GCNLA = query_GCNLA_mongo_db()
        fig_GCNLA = build_GCNLA_graph(df_GCNLA)

        social_media_platform_dropdown = [
                                            {
                                            'label':'All',
                                            'value':'All_Platforms',
                                            },
                                            {
                                            'label':'Twitter',
                                            'value':"b'Twitter'",
                                            },
                                            {
                                            'label':'Reddit',
                                            'value':"b'Reddit'",
                                            },
                                            {
                                            'label':'Tumblr',
                                            'value':"b'Tumblr'"
                                            }
                                        ]

        # sentiment_engine_dropdown = dcc.Dropdown(
        #                                 options={
        #                                         "All_Engines": "All",
        #                                         "IWNLU": "IBM Watson Natural Language Understanding (IWNLU)",
        #                                         "MTA": "Microsoft Text Analytics (MTA)",
        #                                         "GCNLA": "Google Cloud Natural Language API (GCNLA)"
        #                                 },
        #                                 value='All_Engines'
        #                             )

        # df_sentiment = query_sentiment_mongo_db("All_Platforms")
        # sentiment_table = build_sentiment_table(df_sentiment)

        #return children, fig_twitter, fig_reddit, fig_tumblr, fig_IWNLU, fig_MTA, fig_GCNLA
        return fig_twitter, fig_reddit, fig_tumblr, fig_IWNLU, fig_MTA, fig_GCNLA, social_media_platform_dropdown, "All_Platforms" #sentiment_engine_dropdown, #sentiment_table
    else:
        #return None, {}, {}, {}, {}, {}, {} 
        fig_twitter = px.scatter(title="Twitter")
        fig_reddit = px.scatter(title="Reddit")
        fig_tumblr = px.scatter(title="Tumblr")
        fig_IWNLU = px.scatter(title="IBM Watson Natural Language Understanding (IWNLU)")
        fig_MTA = px.scatter(title="Microsoft Text Analytics (MTA)")
        fig_GCNLA = px.scatter(title="Google Cloud Natural Language API (GCNLA)")
        return fig_twitter, fig_reddit, fig_tumblr, fig_IWNLU, fig_MTA, fig_GCNLA, [], None

##################################################################################
# Query Twitter posts in MongoDB
def query_twitter_mongo_db():
    #result = collection.find({'social_media_platform': "b'Twitter'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_confidence_score_positive": 1, "MTA_document_confidence_score_neutral": 1, "MTA_document_confidence_score_negative": 1, '_id': 0}, limit=10)
    result = collection.find({'social_media_platform': "b'Twitter'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0}, limit=10)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    #df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_confidence_score_positive": "MTA Document Confidence Score Positive", "MTA_document_confidence_score_neutral": "MTA Document Confidence Score Neutral", "MTA_document_confidence_score_negative": "MTA Document Confidence Score Negative"}, inplace=True)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    # indexNotApplicable = df_local[ (df_local['IWNLU Sentiment Document Score'] == 'N/A') | (df_local['GCNLA Sentiment Document Score'] == 'N/A') | (df_local['MTA Document Confidence Score Positive'] == 'N/A') | (df_local['MTA Document Confidence Score Neutral'] == 'N/A') | (df_local['MTA Document Confidence Score Negative'] == 'N/A') ].index
    # df_local.drop(indexNotApplicable , inplace=True)
    df_local.dropna(inplace=True)
    df_local = df_local.astype(float)
    return df_local

# Build a scatter plot using Twitter posts
def build_twitter_graph(df_local):
    fig_line = px.scatter(df_local, x='Post ID', y=df_local.columns[1:6], title="Twitter")
    return fig_line

##################################################################################
# Query Reddit posts in MongoDB
def query_reddit_mongo_db():
    #result = collection.find({'social_media_platform': "b'Reddit'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_confidence_score_positive": 1, "MTA_document_confidence_score_neutral": 1, "MTA_document_confidence_score_negative": 1, '_id': 0}, limit=10)
    result = collection.find({'social_media_platform': "b'Reddit'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0}, limit=10)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    #df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_confidence_score_positive": "MTA Document Confidence Score Positive", "MTA_document_confidence_score_neutral": "MTA Document Confidence Score Neutral", "MTA_document_confidence_score_negative": "MTA Document Confidence Score Negative"}, inplace=True)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    # indexNotApplicable = df_local[ (df_local['IWNLU Sentiment Document Score'] == 'N/A') | (df_local['GCNLA Sentiment Document Score'] == 'N/A') | (df_local['MTA Document Confidence Score Positive'] == 'N/A') | (df_local['MTA Document Confidence Score Neutral'] == 'N/A') | (df_local['MTA Document Confidence Score Negative'] == 'N/A') ].index
    # df_local.drop(indexNotApplicable , inplace=True)   
    df_local.dropna(inplace=True) 
    df_local = df_local.astype(float)
    return df_local

# Build a scatter plot using Reddit posts
def build_reddit_graph(df_local):
    fig_line = px.scatter(df_local, x='Post ID', y=df_local.columns[1:6], title="Reddit")
    return fig_line

##################################################################################
# Query Tumblr posts in MongoDB
def query_tumblr_mongo_db():
    #result = collection.find({'social_media_platform': "b'Tumblr'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_confidence_score_positive": 1, "MTA_document_confidence_score_neutral": 1, "MTA_document_confidence_score_negative": 1, '_id': 0}, limit=10)
    result = collection.find({'social_media_platform': "b'Tumblr'"}, {'id': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0}, limit=10)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    #df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_confidence_score_positive": "MTA Document Confidence Score Positive", "MTA_document_confidence_score_neutral": "MTA Document Confidence Score Neutral", "MTA_document_confidence_score_negative": "MTA Document Confidence Score Negative"}, inplace=True)
    df_local.rename(columns={'id': 'Post ID', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    # indexNotApplicable = df_local[ (df_local['IWNLU Sentiment Document Score'] == 'N/A') | (df_local['GCNLA Sentiment Document Score'] == 'N/A') | (df_local['MTA Document Confidence Score Positive'] == 'N/A') | (df_local['MTA Document Confidence Score Neutral'] == 'N/A') | (df_local['MTA Document Confidence Score Negative'] == 'N/A') ].index
    # df_local.drop(indexNotApplicable , inplace=True)
    df_local.dropna(inplace=True)
    df_local = df_local.astype(float)
    return df_local

# Build a scatter plot using Tumblr posts
def build_tumblr_graph(df_local):
    fig_line = px.scatter(df_local, x='Post ID', y=df_local.columns[1:6], title="Tumblr")
    return fig_line

##################################################################################
# Query MTA for Frequency Distribution
def query_MTA_mongo_db():
    result = collection.find({}, {"MTA_document_sentiment_score": 1, '_id': 0}, limit=30)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={"MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    df_local.dropna(inplace=True)
    df_local = df_local.astype(float)
    return df_local

def build_MTA_graph(df_MTA):
    fig = px.histogram(df_MTA, x="MTA Sentiment Document Score", nbins=30, title="Microsoft Text Analytics (MTA)")
    return fig

##################################################################################
# Query GCNLA for Frequency Distribution
def query_GCNLA_mongo_db():
    result = collection.find({}, {"GCNLA_document_sentiment_score": 1, '_id': 0}, limit=30)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={"GCNLA_document_sentiment_score": "GCNLA Sentiment Document Score"}, inplace=True)
    df_local.dropna(inplace=True)
    df_local = df_local.astype(float)
    return df_local

def build_GCNLA_graph(df_GCNLA):
    fig = px.histogram(df_GCNLA, x="GCNLA Sentiment Document Score", nbins=30, title="Google Cloud Natural Language API (GCNLA)")
    return fig

##################################################################################
# Query IWNLU for Frequency Distribution
def query_IWNLU_mongo_db():
    result = collection.find({}, {"IWNLU_sentiment_document_score": 1, '_id': 0}, limit=30)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={"IWNLU_sentiment_document_score": "IWNLU Sentiment Document Score"}, inplace=True)
    df_local.dropna(inplace=True)
    df_local = df_local.astype(float)
    return df_local

def build_IWNLU_graph(df_IWNLU):
    fig = px.histogram(df_IWNLU, x="IWNLU Sentiment Document Score", nbins=30, title="IBM Watson Natural Language Understanding (IWNLU)")
    return fig

##################################################################################
# Query MongoDB for Sentiment Table
def query_sentiment_mongo_db(smp):
    # if se == "All_Engines":
    #     IWNLU = 1
    #     GCNLA = 1
    #     MTA = 1
    # elif se == "IWNLU":
    #     IWNLU = 1
    #     GCNLA = 0
    #     MTA = 0
    # elif se == "GCNLA":
    #     IWNLU = 0
    #     GCNLA = 1
    #     MTA = 0
    # elif se == "MTA":
    #     IWNLU = 0
    #     GCNLA = 0
    #     MTA = 1

    if smp == "All_Platforms":
        result = collection.find({}, {'id': 1, 'full_text': 1, 'social_media_platform': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0}, limit=10)
    elif smp != "All_Platforms":
        result = collection.find({'social_media_platform': smp}, {'id': 1, 'full_text': 1, 'social_media_platform': 1, 'IWNLU_sentiment_document_score': 1, 'GCNLA_document_sentiment_score': 1, "MTA_document_sentiment_score": 1, '_id': 0}, limit=10)
    list_result = list(result)
    df_local = pd.DataFrame(list_result)
    df_local.rename(columns={'id': 'Post ID', 'full_text': 'Post', 'social_media_platform': 'Social Media Platform', 'IWNLU_sentiment_document_score': 'IWNLU Sentiment Document Score', 'GCNLA_document_sentiment_score': 'GCNLA Sentiment Document Score', "MTA_document_sentiment_score": "MTA Sentiment Document Score"}, inplace=True)
    df_local.dropna(inplace=True)
    return df_local

def build_sentiment_table(df_sentiment):
    fig = go.Figure(data=[go.Table(
    header=dict(values=['Post ID', 'Post', 'Social Media Platform', 'IWNLU Sentiment Score', 'GCNLA Sentiment Score', 'MTA Sentiment Score'],
                #fill_color='paleturquoise',
                align='center'),
    cells=dict(values=[df_sentiment['Post ID'], df_sentiment['Post'], df_sentiment['Social Media Platform'], df_sentiment['IWNLU Sentiment Document Score'], df_sentiment['GCNLA Sentiment Document Score'], df_sentiment['MTA Sentiment Document Score']],
               #fill_color='lavender',
               align='left'))
    ])
    return fig

###########################################################################
# Callback Function for Sentiment Table

@app.callback(
    Output('sentiment-table', 'figure'),
    Input('social-media-platform', 'value'),
)

def update_graph(smp):
    print(smp)
    if smp is not None:
        df_sentiment = query_sentiment_mongo_db(smp)
        fig = build_sentiment_table(df_sentiment)
        return fig
    else:
        raise PreventUpdate
       

if __name__=='__main__':
    app.run_server(debug=True, port=8000)